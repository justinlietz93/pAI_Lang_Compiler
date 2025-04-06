"""
Structure Synthesizer module for the pAI_Lang compiler.

This module provides a new implementation for synthesizing pAI_Lang strings
from token mappings, with proper handling of operator precedence and grouping.
"""

from ..utils.debug_logger import logger

class StructureSynthesizer:
    """
    Synthesizes the final pAI_Lang string from token and relationship mappings.
    Uses a shunting-yard based approach for handling operator precedence.
    """
    
    def __init__(self):
        """
        Initialize the structure synthesizer with operator precedence rules.
        """
        logger.debug("Initializing StructureSynthesizer")
        # Initialize operator precedence according to the formal specification
        # (from highest to lowest precedence)
        self.operator_precedence = {
            "[]": 9,   # Grouping operators (highest precedence)
            "!": 8,    # Context activation operator
            "**": 7,   # Repetition operator
            "?:": 6,   # Conditional operator
            "&": 5,    # Parallelism operator
            "|": 4,    # Piping operator
            ">": 3,    # Sequencing operator
            "=": 2,    # Assignment operator
            "#": 1     # Aggregation operator (lowest precedence)
        }
        
        # Define operator associativity (left or right)
        self.operator_associativity = {
            "[]": "none",  # Grouping has no associativity
            "!": "right",  # Context activation is right-associative
            "**": "right", # Repetition is right-associative
            "?:": "right", # Conditional is right-associative
            "&": "left",   # Parallelism is left-associative
            "|": "left",   # Piping is left-associative
            ">": "left",   # Sequencing is left-associative
            "=": "right",  # Assignment is right-associative
            "#": "right"   # Aggregation is right-associative
        }
    
    def synthesize(self, semantic_analysis):
        """
        Synthesize pAI_Lang string from semantic analysis.
        
        Args:
            semantic_analysis (dict): Semantic analysis from the semantic analyzer.
            
        Returns:
            str: Synthesized pAI_Lang string.
        """
        logger.debug(f"Synthesizing pAI_Lang from semantic analysis")
        
        # Extract tokens and relationships
        token_mappings = semantic_analysis.get("token_mappings", {})
        operator_mappings = semantic_analysis.get("operator_mappings", {})
        semantic_structure = semantic_analysis.get("semantic_structure", {})
        
        # If no semantic structure, return empty string
        if not semantic_structure:
            logger.warning("No semantic structure found in semantic analysis")
            # Fallback: If we have tokens but no structure, return the first token
            if token_mappings:
                first_token = next(iter(token_mappings.values()))
                token_value = first_token.get("token", "")
                logger.debug(f"Falling back to first token: {token_value}")
                return token_value
            return ""
        
        # Convert semantic structure to expression elements
        elements = self._convert_to_expression_elements(semantic_structure, token_mappings, operator_mappings)
        logger.debug(f"Expression elements: {elements}")
        
        # If no elements were created, return empty string
        if not elements:
            logger.warning("No expression elements created")
            return ""
        
        # Apply shunting-yard algorithm to handle operator precedence
        output_queue = self._apply_shunting_yard(elements)
        logger.debug(f"Output queue after shunting-yard: {output_queue}")
        
        # Build the final expression from the output queue
        pailang_string = self._build_expression(output_queue)
        logger.debug(f"Final pAI_Lang string: {pailang_string}")
        
        return pailang_string
    
    def _convert_to_expression_elements(self, semantic_structure, token_mappings, operator_mappings):
        """
        Convert semantic structure to expression elements.
        
        Args:
            semantic_structure (dict): Semantic structure from semantic analysis.
            token_mappings (dict): Token mappings from semantic analysis.
            operator_mappings (dict): Operator mappings from semantic analysis.
            
        Returns:
            list: Expression elements (tokens and operators).
        """
        logger.debug("Converting semantic structure to expression elements")
        
        # Check if semantic structure has direct elements list
        elements = semantic_structure.get("elements", [])
        if elements:
            logger.debug(f"Using direct elements from semantic structure: {elements}")
            return elements
        
        # Extract tokens and relationships from semantic structure
        tokens = semantic_structure.get("tokens", [])
        relationships = semantic_structure.get("relationships", [])
        
        logger.debug(f"Tokens: {tokens}")
        logger.debug(f"Relationships: {relationships}")
        
        # If no relationships, just return tokens as elements
        if not relationships and tokens:
            elements = []
            for token in tokens:
                elements.append({"type": "token", "value": token.get("token", "")})
            return elements
        
        # Convert relationships to expression elements
        elements = []
        
        # Process each relationship
        for relationship in relationships:
            rel_type = relationship.get("type")
            logger.debug(f"Processing relationship of type: {rel_type}")
            
            if rel_type == "binary":
                # Handle binary relationships (sequence, parallel, piping)
                operator = relationship.get("operator", ">")
                source = relationship.get("source")
                target = relationship.get("target")
                
                # Find tokens that match source and target
                source_token = None
                target_token = None
                
                for token_id, token in token_mappings.items():
                    if token.get("source") == source:
                        source_token = token
                    if token.get("source") == target:
                        target_token = token
                
                if source_token and target_token:
                    # Add source token
                    elements.append({"type": "token", "value": source_token.get("token", "")})
                    
                    # Add operator
                    elements.append(operator)
                    
                    # Add target token
                    elements.append({"type": "token", "value": target_token.get("token", "")})
            
            elif rel_type == "conditional":
                # Handle conditional relationships
                condition = relationship.get("condition")
                true_branch = relationship.get("trueBranch")
                false_branch = relationship.get("falseBranch")
                
                # Find tokens that match condition, true branch, and false branch
                condition_token = None
                true_token = None
                false_token = None
                
                for token_id, token in token_mappings.items():
                    if token.get("source") == condition:
                        condition_token = token
                    if token.get("source") == true_branch:
                        true_token = token
                    if token.get("source") == false_branch:
                        false_token = token
                
                if condition_token and true_token:
                    # Add condition token
                    elements.append({"type": "token", "value": condition_token.get("token", "")})
                    
                    # Add conditional operator start
                    elements.append("?")
                    
                    # Add true branch token
                    elements.append({"type": "token", "value": true_token.get("token", "")})
                    
                    if false_token:
                        # Add conditional operator middle
                        elements.append(":")
                        
                        # Add false branch token
                        elements.append({"type": "token", "value": false_token.get("token", "")})
            
            elif rel_type == "repetition":
                # Handle repetition relationships
                expression = relationship.get("expression")
                count = relationship.get("count", 1)
                
                # Find token that matches expression
                expr_token = None
                
                for token_id, token in token_mappings.items():
                    if token.get("source") == expression:
                        expr_token = token
                
                if expr_token:
                    # Add expression token
                    elements.append({"type": "token", "value": expr_token.get("token", "")})
                    
                    # Add repetition operator
                    elements.append("**")
                    
                    # Add count
                    elements.append({"type": "token", "value": str(count)})
            
            elif rel_type == "context_activation":
                # Handle context activation relationships
                expression = relationship.get("expression")
                context = relationship.get("context")
                
                # Find tokens that match expression and context
                expr_token = None
                context_token = None
                
                for token_id, token in token_mappings.items():
                    if token.get("source") == expression:
                        expr_token = token
                    if token.get("source") == context:
                        context_token = token
                
                if expr_token and context_token:
                    # Add expression token
                    elements.append({"type": "token", "value": expr_token.get("token", "")})
                    
                    # Add context activation operator
                    elements.append("!")
                    
                    # Add context token
                    elements.append({"type": "token", "value": context_token.get("token", "")})
            
            elif rel_type == "aggregation":
                # Handle aggregation relationships
                expressions = relationship.get("expressions", [])
                
                # Find tokens that match expressions
                expr_tokens = []
                
                for expr in expressions:
                    for token_id, token in token_mappings.items():
                        if token.get("source") == expr:
                            expr_tokens.append(token)
                
                if expr_tokens:
                    # Add aggregation operator
                    elements.append("#")
                    
                    # Add left bracket
                    elements.append("[")
                    
                    # Add first expression
                    elements.append({"type": "token", "value": expr_tokens[0].get("token", "")})
                    
                    # Add remaining expressions with commas
                    for i in range(1, len(expr_tokens)):
                        elements.append(",")
                        elements.append({"type": "token", "value": expr_tokens[i].get("token", "")})
                    
                    # Add right bracket
                    elements.append("]")
        
        # If no elements were created but we have tokens, create a simple token list
        if not elements and tokens:
            for token in tokens:
                elements.append({"type": "token", "value": token.get("token", "")})
        
        return elements
    
    def _apply_shunting_yard(self, elements):
        """
        Apply the shunting-yard algorithm to handle operator precedence.
        
        Args:
            elements (list): Expression elements (tokens and operators).
            
        Returns:
            list: Output queue in postfix notation.
        """
        logger.debug("Applying shunting-yard algorithm")
        output_queue = []
        operator_stack = []
        
        i = 0
        while i < len(elements):
            element = elements[i]
            
            # If token, add to output queue
            if isinstance(element, dict) and element.get("type") == "token":
                output_queue.append(element)
            
            # If left bracket, push to operator stack
            elif element == "[":
                operator_stack.append(element)
            
            # If right bracket, pop operators until left bracket
            elif element == "]":
                while operator_stack and operator_stack[-1] != "[":
                    output_queue.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1] == "[":
                    operator_stack.pop()  # Discard the left bracket
            
            # If comma, pop operators until left bracket
            elif element == ",":
                while operator_stack and operator_stack[-1] != "[":
                    output_queue.append(operator_stack.pop())
            
            # If operator, handle according to precedence
            elif isinstance(element, str):
                # Handle conditional operator as a special case
                if element == "?":
                    # Find the matching ":"
                    j = i + 1
                    nesting = 0
                    while j < len(elements):
                        if elements[j] == "?" and nesting == 0:
                            nesting += 1
                        elif elements[j] == ":" and nesting == 0:
                            break
                        elif elements[j] == ":" and nesting > 0:
                            nesting -= 1
                        j += 1
                    
                    if j < len(elements):
                        # Process the condition
                        condition = elements[i-1]
                        
                        # Process the true branch
                        true_branch_elements = elements[i+1:j]
                        true_branch = self._apply_shunting_yard(true_branch_elements)
                        
                        # Process the false branch
                        false_branch_elements = elements[j+1:]
                        false_branch = self._apply_shunting_yard(false_branch_elements)
                        
                        # Create conditional expression
                        conditional = {
                            "type": "conditional",
                            "condition": condition,
                            "true_branch": true_branch,
                            "false_branch": false_branch
                        }
                        
                        # Replace the last element in output_queue with the conditional
                        if output_queue:  # Check if output_queue is not empty
                            output_queue.pop()  # Remove the condition
                        output_queue.append(conditional)
                        
                        # Skip to the end
                        i = len(elements)
                        continue
                
                # Get operator precedence
                op_precedence = self._get_operator_precedence(element)
                
                # Handle other operators
                while (operator_stack and 
                       operator_stack[-1] != "[" and
                       ((self._get_operator_associativity(element) == "left" and
                         op_precedence <= self._get_operator_precedence(operator_stack[-1])) or
                        (self._get_operator_associativity(element) == "right" and
                         op_precedence < self._get_operator_precedence(operator_stack[-1])))):
                    output_queue.append(operator_stack.pop())
                
                operator_stack.append(element)
            
            i += 1
        
        # Pop any remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _build_expression(self, output_queue):
        """
        Build the final expression from the output queue.
        
        Args:
            output_queue (list): Output queue in postfix notation.
            
        Returns:
            str: Final pAI_Lang expression.
        """
        logger.debug("Building expression from output queue")
        if not output_queue:
            logger.warning("Empty output queue")
            return ""
        
        stack = []
        
        for element in output_queue:
            # If token, push to stack
            if isinstance(element, dict) and element.get("type") == "token":
                stack.append(element.get("value", ""))
            
            # If conditional, handle specially
            elif isinstance(element, dict) and element.get("type") == "conditional":
                condition = element.get("condition", {}).get("value", "")
                true_branch = self._build_expression(element.get("true_branch", []))
                false_branch = self._build_expression(element.get("false_branch", []))
                
                # Create conditional expression with proper bracketing
                expr = f"{condition}?{true_branch}:{false_branch}"
                stack.append(expr)
            
            # If operator, pop operands and apply
            elif isinstance(element, str):
                if element in [">", "&", "|", "="]:
                    # Binary operators
                    if len(stack) >= 2:
                        right = stack.pop()
                        left = stack.pop()
                        
                        # Check if operands need bracketing
                        left_needs_brackets = self._needs_brackets(left, element)
                        right_needs_brackets = self._needs_brackets(right, element)
                        
                        left_expr = f"[{left}]" if left_needs_brackets else left
                        right_expr = f"[{right}]" if right_needs_brackets else right
                        
                        stack.append(f"{left_expr}{element}{right_expr}")
                    else:
                        logger.warning(f"Not enough operands for binary operator {element}")
                        # Handle the case where we don't have enough operands
                        if stack:
                            # If we have at least one operand, use it
                            operand = stack.pop()
                            stack.append(operand)
                
                elif element == "#":
                    # Aggregation operator
                    if len(stack) >= 1:
                        operand = stack.pop()
                        stack.append(f"#{operand}")
                    else:
                        logger.warning("No operand for aggregation operator #")
                
                elif element == "!":
                    # Context activation operator
                    if len(stack) >= 2:
                        context = stack.pop()
                        expression = stack.pop()
                        stack.append(f"{expression}!{context}")
                    else:
                        logger.warning("Not enough operands for context activation operator !")
                        # Handle the case where we don't have enough operands
                        if stack:
                            # If we have at least one operand, use it
                            operand = stack.pop()
                            stack.append(operand)
                
                elif element == "**":
                    # Repetition operator
                    if len(stack) >= 2:
                        count = stack.pop()
                        expression = stack.pop()
                        
                        # Check if expression needs bracketing
                        expr_needs_brackets = self._needs_brackets(expression, "**")
                        expr_with_brackets = f"[{expression}]" if expr_needs_brackets else expression
                        
                        stack.append(f"**{count}{expr_with_brackets}")
                    else:
                        logger.warning("Not enough operands for repetition operator **")
                        # Handle the case where we don't have enough operands
                        if stack:
                            # If we have at least one operand, use it
                            operand = stack.pop()
                            stack.append(operand)
        
        # The final result should be the only item on the stack
        if not stack:
            logger.warning("Empty stack after building expression")
            return ""
        
        result = stack[0] if stack else ""
        logger.debug(f"Built expression: {result}")
        return result
    
    def _get_operator_precedence(self, operator):
        """
        Get precedence value for an operator.
        
        Args:
            operator (str): Operator symbol.
            
        Returns:
            int: Precedence value (higher means higher precedence).
        """
        # Handle special cases
        if operator == "?":
            return self.operator_precedence.get("?:", 0)
        elif operator == ":":
            return self.operator_precedence.get("?:", 0)
        
        return self.operator_precedence.get(operator, 0)
    
    def _get_operator_associativity(self, operator):
        """
        Get associativity for an operator.
        
        Args:
            operator (str): Operator symbol.
            
        Returns:
            str: Associativity ("left", "right", or "none").
        """
        # Handle special cases
        if operator == "?":
            return self.operator_associativity.get("?:", "right")
        elif operator == ":":
            return self.operator_associativity.get("?:", "right")
        
        return self.operator_associativity.get(operator, "left")
    
    def _needs_brackets(self, expr, parent_operator):
        """
        Determine if an expression needs brackets based on operator precedence.
        
        Args:
            expr (str): The expression to check.
            parent_operator (str): The parent operator.
            
        Returns:
            bool: True if brackets are needed, False otherwise.
        """
        # If expression is empty or a single token, no brackets needed
        if not expr or (len(expr) <= 3 and not any(op in expr for op in self.operator_precedence.keys())):
            return False
        
        # Check for operators in the expression
        for op in self.operator_precedence.keys():
            if op in expr and op != parent_operator:
                # If the expression contains an operator with lower precedence than the parent,
                # it needs brackets
                if self.operator_precedence.get(op, 0) < self.operator_precedence.get(parent_operator, 0):
                    return True
        
        return False
