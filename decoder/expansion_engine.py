"""
Expansion Engine for pAI_Lang

This module provides functionality for expanding pAI_Lang tokens and structures
into their corresponding Command Language (CL) representations.
"""

class ExpansionEngine:
    """
    Handles the expansion of pAI_Lang expressions into Command Language.
    """
    
    def __init__(self, context_manager, token_dictionary=None):
        """
        Initialize the expansion engine.
        
        Args:
            context_manager: The context manager to use for context-aware expansion.
            token_dictionary (dict, optional): Dictionary of token definitions.
        """
        self.context_manager = context_manager
        self.token_dictionary = token_dictionary or {}
        self.operator_definitions = self._initialize_operator_definitions()
    
    def expand_to_cl(self, parsed_pailang):
        """
        Expand a parsed pAI_Lang AST to Command Language.
        
        Args:
            parsed_pailang (dict): The parsed pAI_Lang AST.
            
        Returns:
            str: The expanded Command Language representation.
        """
        # Check if we have a valid pAI_Lang AST
        if not parsed_pailang or not isinstance(parsed_pailang, dict):
            return ""
        
        # Extract the main expression
        main_expression = None
        if parsed_pailang.get('type') == 'PAILang':
            main_expression = parsed_pailang.get('expression')
        else:
            main_expression = parsed_pailang  # Assume it's already the expression
        
        # If no expression, return empty string
        if not main_expression:
            return ""
        
        # Expand the main expression
        expanded_cl = self.expand_expression(main_expression)
        
        # Add header comment
        header = "# Generated Command Language from pAI_Lang\n"
        
        return header + expanded_cl
    
    def expand_to_nl(self, parsed_pailang):
        """
        Expand a parsed pAI_Lang AST to Natural Language.
        
        Args:
            parsed_pailang (dict): The parsed pAI_Lang AST.
            
        Returns:
            str: The expanded Natural Language representation.
        """
        # For now, we'll expand to CL first and then convert that to NL
        # In a real implementation, this would have direct pAI_Lang to NL mapping
        cl_output = self.expand_to_cl(parsed_pailang)
        
        # Convert CL to NL (simplified for this implementation)
        nl_output = self._convert_cl_to_nl(cl_output)
        
        return nl_output
    
    def _convert_cl_to_nl(self, cl_text):
        """
        Convert Command Language to Natural Language.
        
        Args:
            cl_text (str): Command Language text.
            
        Returns:
            str: Natural Language representation.
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NL generation
        
        # Replace command markers with natural language phrases
        nl_text = cl_text.replace(">>>", "Please")
        nl_text = nl_text.replace("END_BATCH", "complete the batch operation")
        nl_text = nl_text.replace("END_REPEAT", "complete the repetition")
        nl_text = nl_text.replace("END_CONDITIONAL", "complete the conditional operation")
        nl_text = nl_text.replace("END_PARALLEL", "complete the parallel execution")
        
        # Replace brackets with more natural language
        import re
        nl_text = re.sub(r'\[([^\]]+)\]', r'with \1', nl_text)
        
        # Add periods at the end of sentences
        lines = nl_text.split('\n')
        for i in range(len(lines)):
            line = lines[i].strip()
            if line and not line.endswith('.') and not line.endswith(':'):
                lines[i] = line + '.'
        
        nl_text = '\n'.join(lines)
        
        return nl_text
    
    def _initialize_operator_definitions(self):
        """
        Initialize definitions for pAI_Lang operators.
        
        Returns:
            dict: Operator definitions with expansion templates.
        """
        return {
            ">": {
                "name": "sequence",
                "expansionTemplate": "{operands[0]}\n{operands[1]}",
                "properties": {"type": "sequential"}
            },
            "&": {
                "name": "parallel",
                "expansionTemplate": ">>> PARALLEL\n    {operands[0]}\n    {operands[1]}\n>>> END_PARALLEL",
                "properties": {"type": "concurrent"}
            },
            "?:": {
                "name": "conditional",
                "expansionTemplate": ">>> CONDITIONAL [{condition}]\n    {true_branch}\n>>> ELSE\n    {false_branch}\n>>> END_CONDITIONAL",
                "properties": {"type": "branching"}
            },
            "|": {
                "name": "piping",
                "expansionTemplate": ">>> PIPE\n    >>> SOURCE\n        {operands[0]}\n    >>> TARGET\n        {operands[1]}\n>>> END_PIPE",
                "properties": {"type": "dataflow"}
            },
            "=": {
                "name": "assignment",
                "expansionTemplate": ">>> ASSIGN [{operands[0]}] = [{operands[1]}]",
                "properties": {"type": "assignment"}
            },
            "#": {
                "name": "aggregation",
                "expansionTemplate": ">>> AGGREGATE\n    {operands[0]}\n>>> END_AGGREGATE",
                "properties": {"type": "collection"}
            },
            "!": {
                "name": "context_activation",
                "expansionTemplate": ">>> ACTIVATE_CONTEXT [{operands[0]}]",
                "properties": {"type": "context"}
            },
            "**": {
                "name": "repetition",
                "expansionTemplate": ">>> REPEAT [{count}]\n    {operands[0]}\n>>> END_REPEAT",
                "properties": {"type": "iteration"}
            }
        }
    
    def expand_token(self, token):
        """
        Expand an individual token to its intermediate form.
        
        Args:
            token (dict): The token to expand.
            
        Returns:
            str: The expanded Command Language representation.
        """
        # Resolve token in current context
        resolved_token = self.context_manager.resolve_in_context(token, self.token_dictionary)
        
        # Get expansion template
        template = resolved_token.get('expansionTemplate')
        
        # If no template available, use default expansion
        if not template:
            return self._generate_default_expansion(token)
        
        # Apply template with token properties
        expansion = self._apply_template(template, {
            'token': token.get('value'),
            'category': token.get('categoryCode'),
            'identifier': token.get('identifier'),
            'properties': resolved_token.get('properties', {})
        })
        
        return expansion
    
    def _generate_default_expansion(self, token):
        """
        Generate a default expansion for a token when no template is available.
        
        Args:
            token (dict): The token to expand.
            
        Returns:
            str: The default expansion.
        """
        category_code = token.get('categoryCode')
        identifier = token.get('identifier', token.get('value', 'unknown'))
        
        # Map category codes to command names
        category_map = {
            'C': 'SET_CONTEXT',
            'L': 'APPLY_LOGIC',
            'M': 'ALLOCATE_MEMORY',
            'D': 'EXECUTE_DIRECTIVE',
            'N': 'NETWORK_OPERATION',
            'T': 'EXECUTE_TASK',
            'P': 'RUN_PROCESS',
            'R': 'ALLOCATE_RESOURCE',
            'S': 'APPLY_SECURITY',
            'H': 'REGISTER_HANDLER',
            'Q': 'EXECUTE_QUERY',
            'B': 'BATCH_OPERATION'
        }
        
        command = category_map.get(category_code, 'EXECUTE')
        
        # For complex tokens, include the type prefix
        if token.get('type') == 'ComplexToken':
            type_prefix = token.get('typePrefix')
            return f">>> {command} [TYPE={type_prefix}, ID={identifier}]"
        else:
            return f">>> {command} [ID={identifier}]"
    
    def expand_operator(self, operator, operands):
        """
        Apply operator semantics during expansion.
        
        Args:
            operator (str): The operator to expand.
            operands (list): The operands for the operator.
            
        Returns:
            str: The expanded Command Language representation.
        """
        # Get operator definition
        operator_def = self.operator_definitions.get(operator)
        
        if not operator_def:
            return f">>> UNKNOWN_OPERATOR [{operator}]"
        
        # Get expansion template
        template = operator_def.get('expansionTemplate')
        
        # Expand each operand
        expanded_operands = []
        for operand in operands:
            expanded_operands.append(self.expand_expression(operand))
        
        # Apply template with expanded operands
        expansion = self._apply_template(template, {
            'operator': operator,
            'operands': expanded_operands,
            'properties': operator_def.get('properties', {})
        })
        
        return expansion
    
    def expand_structure(self, structure):
        """
        Expand complex structures while preserving relationships.
        
        Args:
            structure (dict): The structure to expand.
            
        Returns:
            str: The expanded Command Language representation.
        """
        structure_type = structure.get('type')
        
        if structure_type == 'BatchOperation':
            # Expand batch header
            header = ">>> BATCH_OPERATION"
            
            # Expand each expression in the batch
            expanded_expressions = []
            for expr in structure.get('expressions', []):
                expanded_expressions.append(self.expand_expression(expr))
            
            # Combine with proper indentation and structure
            return self._format_batch_structure(header, expanded_expressions)
        
        elif structure_type == 'ContextActivation':
            # Process context activation in context manager
            expression = structure.get('expression')
            
            # Expand context activation header
            header = ">>> ACTIVATE_CONTEXT"
            
            # Expand the context expression
            expanded_context = self.expand_expression(expression)
            
            # Combine with proper structure
            return f"{header}\n    {expanded_context}"
        
        elif structure_type == 'TokenSequence':
            # Expand each expression in the sequence
            expanded_expressions = []
            for expr in structure.get('expressions', []):
                expanded_expressions.append(self.expand_expression(expr))
            
            # Join with commas
            return ", ".join(expanded_expressions)
        
        elif structure_type == 'Repetition':
            # Get count and expression
            count = structure.get('count', 1)
            expression = structure.get('expression')
            
            # Expand the expression
            expanded_expression = self.expand_expression(expression)
            
            # Format as repeat structure
            return f">>> REPEAT [{count}]\n    {expanded_expression}\n>>> END_REPEAT"
        
        # Handle other structure types or return error for unknown types
        return f">>> UNKNOWN_STRUCTURE [{structure_type}]"
    
    def _format_batch_structure(self, header, expanded_expressions):
        """
        Format a batch structure with proper indentation.
        
        Args:
            header (str): The batch header.
            expanded_expressions (list): List of expanded expressions.
            
        Returns:
            str: The formatted batch structure.
        """
        # Start with the header
        result = header
        
        # Add each expression with indentation
        for expr in expanded_expressions:
            # Split by lines and indent each line
            lines = expr.split('\n')
            indented_lines = [f"    {line}" for line in lines]
            indented_expr = '\n'.join(indented_lines)
            
            # Add to result
            result += f"\n{indented_expr}"
        
        # Add end marker
        result += "\n>>> END_BATCH"
        
        return result
    
    def expand_expression(self, expression):
        """
        Recursively expand nested expressions.
        
        Args:
            expression (dict): The expression to expand.
            
        Returns:
            str: The expanded Command Language representation.
        """
        if not expression or not isinstance(expression, dict):
            return ""
            
        expr_type = expression.get('type')
        
        # Base case: token
        if expr_type in ['StandardToken', 'ComplexToken']:
            return self.expand_token(expression)
        
        # Operator expressions
        elif expr_type == 'SequenceExpression':
            return self.expand_operator('>', [
                expression.get('leftExpression'),
                expression.get('rightExpression')
            ])
        
        elif expr_type == 'ParallelExpression':
            return self.expand_operator('&', [
                expression.get('leftExpression'),
                expression.get('rightExpression')
            ])
        
        elif expr_type == 'ConditionalExpression':
            condition = self.expand_expression(expression.get('condition'))
            true_branch = self.expand_expression(expression.get('trueBranch'))
            false_branch = self.expand_expression(expression.get('falseBranch'))
            
            template = self.operator_definitions.get('?:').get('expansionTemplate')
            return self._apply_template(template, {
                'condition': condition,
                'true_branch': true_branch,
                'false_branch': false_branch
            })
        
        elif expr_type == 'PipingExpression':
            return self.expand_operator('|', [
                expression.get('leftExpression'),
                expression.get('rightExpression')
            ])
        
        elif expr_type == 'AssignmentExpression':
            return self.expand_operator('=', [
                expression.get('leftExpression'),
                expression.get('rightExpression')
            ])
        
        elif expr_type == 'AggregationExpression':
            return self.expand_operator('#', [expression.get('expression')])
        
        # Complex structures
        elif expr_type in ['BatchOperation', 'ContextActivation', 'TokenSequence', 'Repetition']:
            return self.expand_structure(expression)
        
        # System identifier
        elif expr_type == 'SystemIdentifier':
            return f">>> SYSTEM [{expression.get('value')}]"
            
        # Unknown expression type
        else:
            return f">>> UNKNOWN_EXPRESSION [{expr_type}]"
    
    def _apply_template(self, template, data):
        """
        Apply a template with the provided data.
        
        Args:
            template (str): The template string with placeholders.
            data (dict): The data to fill in the placeholders.
            
        Returns:
            str: The filled template.
        """
        result = template
        
        # Replace simple placeholders
        for key, value in data.items():
            if isinstance(value, str):
                placeholder = f"{{{key}}}"
                if placeholder in result:
                    result = result.replace(placeholder, value)
        
        # Handle list placeholders (e.g., {operands[0]})
        import re
        list_placeholders = re.findall(r'\{(\w+)\[(\d+)\]\}', result)
        for list_name, index in list_placeholders:
            if list_name in data and isinstance(data[list_name], list):
                try:
                    index = int(index)
                    if 0 <= index < len(data[list_name]):
                        placeholder = f"{{{list_name}[{index}]}}"
                        result = result.replace(placeholder, data[list_name][index])
                except (ValueError, IndexError):
                    pass
        
        # Handle nested dictionary placeholders (e.g., {properties.name})
        dict_placeholders = re.findall(r'\{(\w+)\.(\w+)\}', result)
        for dict_name, key in dict_placeholders:
            if dict_name in data and isinstance(data[dict_name], dict):
                if key in data[dict_name]:
                    placeholder = f"{{{dict_name}.{key}}}"
                    result = result.replace(placeholder, str(data[dict_name][key]))
        
        return result
