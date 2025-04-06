"""
pAI_Lang Parser

This module provides functionality for parsing pAI_Lang strings according to the formal EBNF grammar.
It uses the Lark parser library to implement the parsing logic.
"""

from lark import Lark, Transformer, v_args

class PAILangParser:
    """
    Parser for pAI_Lang strings based on the formal EBNF grammar.
    """
    
    def __init__(self):
        """
        Initialize the pAI_Lang parser with the grammar definition.
        """
        # Define the pAI_Lang grammar in EBNF notation based on the formal specification
        self.grammar = r"""
            // Top-level structure
            pailang: [system_with_version] expression

            // System identifier with optional version
            system_with_version: system_id [version_declaration]
            system_id: ALPHA_CHAR DIGIT [DIGIT]
            version_declaration: "[" version_component ("," version_component)* "]"
            version_component: VERSION_TYPE "-" version_number
            VERSION_TYPE: "G" | "TD" | "OP"
            version_number: DIGIT "." DIGIT ["." DIGIT]

            // Expressions with operator precedence (highest to lowest)
            expression: assignment_expression

            // Assignment expression (lowest precedence)
            assignment_expression: conditional_expression ("=" conditional_expression)*

            // Conditional expression
            conditional_expression: piping_expression ("?" piping_expression ":" piping_expression)*

            // Piping expression
            piping_expression: parallel_expression ("|" parallel_expression)*

            // Parallel expression
            parallel_expression: sequence_expression ("&" sequence_expression)*

            // Sequence expression
            sequence_expression: aggregation_expression (">" aggregation_expression)*

            // Aggregation expression
            aggregation_expression: repetition_expression | ("#" "[" expression ("," expression)* "]")

            // Repetition expression
            repetition_expression: atomic_expression ("**" DIGIT ["[" expression "]"])?

            // Atomic expressions
            atomic_expression: token
                             | bracketed_expression
                             | batch_operation
                             | context_activation
                             | token_sequence

            // Token sequence
            token_sequence: token token+

            // Bracketed expression (for grouping)
            bracketed_expression: "[" expression ("," expression)* "]"

            // Batch operation
            batch_operation: "B" "[" expression ("&" expression)* "]"

            // Context activation
            context_activation: expression "!" token_sequence

            // Token
            token: standard_token | complex_token

            // Standard token
            standard_token: CATEGORY_CODE IDENTIFIER
            CATEGORY_CODE: /[CLMDNTPRSHQB]/
            IDENTIFIER: DIGIT DIGIT

            // Complex token
            complex_token: TYPE_PREFIX CATEGORY_CODE COMPLEX_IDENTIFIER
            TYPE_PREFIX: ALPHA_CHAR ALPHA_CHAR [ALPHA_CHAR]
            COMPLEX_IDENTIFIER: DIGIT DIGIT DIGIT

            // Basic elements
            ALPHA_CHAR: /[A-Z]/
            DIGIT: /[0-9]/

            // Whitespace handling
            %import common.WS
            %ignore WS
        """
        
        # Initialize the Lark parser with the grammar
        self.parser = Lark(self.grammar, start='pailang', parser='lalr')
    
    def parse(self, pailang_string):
        """
        Parse a pAI_Lang string into an abstract syntax tree.
        
        Args:
            pailang_string (str): The pAI_Lang string to parse.
            
        Returns:
            dict: A dictionary representation of the parsed AST.
            
        Raises:
            Exception: If the parsing fails due to syntax errors.
        """
        try:
            # Parse the input string using Lark
            parse_tree = self.parser.parse(pailang_string)
            
            # Transform the parse tree into a more usable structure
            transformer = PAILangTransformer()
            ast = transformer.transform(parse_tree)
            
            return ast
        
        except Exception as e:
            # Handle parsing errors
            error_msg = f"Error parsing pAI_Lang string: {str(e)}"
            print(error_msg)  # Log the error for debugging
            raise Exception(error_msg)


@v_args(inline=True)
class PAILangTransformer(Transformer):
    """
    Transformer to convert the Lark parse tree into a more usable dictionary structure.
    """
    
    def pailang(self, *args):
        """Transform the top-level pAI_Lang structure."""
        result = {
            "type": "PAILang"
        }
        
        # Handle optional system with version
        if len(args) > 1:
            result["system"] = args[0]
            result["expression"] = args[1]
        else:
            result["expression"] = args[0]
        
        return result
    
    def system_with_version(self, system_id, *args):
        """Transform system identifier with optional version."""
        result = {
            "type": "SystemIdentifier",
            "id": system_id
        }
        
        # Add version if present
        if args and args[0] is not None:
            result["version"] = args[0]
        
        return result
    
    def system_id(self, alpha_char, digit1, *args):
        """Transform system identifier."""
        if args:
            return f"{alpha_char}{digit1}{args[0]}"
        return f"{alpha_char}{digit1}"
    
    def version_declaration(self, *args):
        """Transform version declaration."""
        return {
            "type": "VersionDeclaration",
            "components": list(args)
        }
    
    def version_component(self, version_type, version_number):
        """Transform version component."""
        return {
            "type": version_type,
            "number": version_number
        }
    
    def version_number(self, digit1, digit2, *args):
        """Transform version number."""
        if args:
            return f"{digit1}.{digit2}.{args[0]}"
        return f"{digit1}.{digit2}"
    
    def expression(self, expr):
        """Transform expression."""
        return expr
    
    def assignment_expression(self, *args):
        """Transform assignment expression."""
        if len(args) == 1:
            return args[0]
        
        result = args[0]
        for i in range(1, len(args)):
            result = {
                "type": "AssignmentExpression",
                "operator": "=",
                "leftExpression": result,
                "rightExpression": args[i]
            }
        return result
    
    def conditional_expression(self, *args):
        """Transform conditional expression."""
        if len(args) == 1:
            return args[0]
        
        # For conditional expressions, we need to group them in threes
        # (condition, true branch, false branch)
        result = args[0]
        i = 1
        while i < len(args) - 1:
            result = {
                "type": "ConditionalExpression",
                "operator": "?:",
                "condition": result,
                "trueBranch": args[i],
                "falseBranch": args[i+1]
            }
            i += 2
        
        return result
    
    def piping_expression(self, *args):
        """Transform piping expression."""
        if len(args) == 1:
            return args[0]
        
        result = args[0]
        for i in range(1, len(args)):
            result = {
                "type": "PipingExpression",
                "operator": "|",
                "leftExpression": result,
                "rightExpression": args[i]
            }
        return result
    
    def parallel_expression(self, *args):
        """Transform parallel expression."""
        if len(args) == 1:
            return args[0]
        
        result = args[0]
        for i in range(1, len(args)):
            result = {
                "type": "ParallelExpression",
                "operator": "&",
                "leftExpression": result,
                "rightExpression": args[i]
            }
        return result
    
    def sequence_expression(self, *args):
        """Transform sequence expression."""
        if len(args) == 1:
            return args[0]
        
        result = args[0]
        for i in range(1, len(args)):
            result = {
                "type": "SequenceExpression",
                "operator": ">",
                "leftExpression": result,
                "rightExpression": args[i]
            }
        return result
    
    def aggregation_expression(self, *args):
        """Transform aggregation expression."""
        if len(args) == 1:
            return args[0]
        
        # For aggregation with # operator
        return {
            "type": "AggregationExpression",
            "operator": "#",
            "expressions": list(args[1:])  # Skip the # symbol
        }
    
    def repetition_expression(self, expr, *args):
        """Transform repetition expression."""
        if not args:
            return expr
        
        # For repetition with ** operator
        if len(args) == 1:
            return {
                "type": "RepetitionExpression",
                "operator": "**",
                "count": int(args[0]),
                "expression": expr
            }
        else:
            return {
                "type": "RepetitionExpression",
                "operator": "**",
                "count": int(args[0]),
                "expression": args[1]
            }
    
    def atomic_expression(self, expr):
        """Transform atomic expression."""
        return expr
    
    def token_sequence(self, *args):
        """Transform token sequence."""
        return {
            "type": "TokenSequence",
            "tokens": list(args)
        }
    
    def bracketed_expression(self, *args):
        """Transform bracketed expression."""
        return {
            "type": "BracketedExpression",
            "expressions": list(args)
        }
    
    def batch_operation(self, *args):
        """Transform batch operation."""
        return {
            "type": "BatchOperation",
            "expressions": list(args[1:])  # Skip the B symbol
        }
    
    def context_activation(self, expr, token_sequence):
        """Transform context activation."""
        return {
            "type": "ContextActivation",
            "expression": expr,
            "context": token_sequence
        }
    
    def token(self, token):
        """Transform token."""
        return token
    
    def standard_token(self, category_code, identifier):
        """Transform standard token."""
        return {
            "type": "StandardToken",
            "categoryCode": str(category_code),
            "identifier": str(identifier),
            "value": f"{category_code}{identifier}"
        }
    
    def complex_token(self, type_prefix, category_code, complex_id):
        """Transform complex token."""
        return {
            "type": "ComplexToken",
            "typePrefix": str(type_prefix),
            "categoryCode": str(category_code),
            "identifier": str(complex_id),
            "value": f"{type_prefix}{category_code}{complex_id}"
        }
