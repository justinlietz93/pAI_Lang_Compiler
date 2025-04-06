"""
Context Manager for pAI_Lang

This module provides functionality for tracking and managing the active context stack
during the expansion of pAI_Lang expressions.
"""

class ContextManager:
    """
    Manages the context stack during pAI_Lang expansion.
    """
    
    def __init__(self):
        """
        Initialize the context manager with an empty context stack.
        """
        self.context_stack = []
        self.system_context = None
    
    def activate_context(self, context):
        """
        Push a new context onto the stack.
        
        Args:
            context (dict): The context to activate, containing id, definition, and properties.
        """
        self.context_stack.append(context)
    
    def deactivate_context(self):
        """
        Remove the top context from the stack.
        
        Returns:
            dict: The deactivated context, or None if the stack is empty.
        """
        if self.context_stack:
            return self.context_stack.pop()
        return None
    
    def get_current_context(self):
        """
        Get the current active context.
        
        Returns:
            dict: The current context, or None if the stack is empty.
        """
        if self.context_stack:
            return self.context_stack[-1]
        return None
    
    def is_context_active(self, context_id):
        """
        Check if a specific context is active.
        
        Args:
            context_id (str): The ID of the context to check.
            
        Returns:
            bool: True if the context is active, False otherwise.
        """
        return any(ctx.get('id') == context_id for ctx in self.context_stack)
    
    def apply_context(self, parsed_pailang):
        """
        Apply context to the parsed pAI_Lang AST.
        
        Args:
            parsed_pailang (dict): The parsed pAI_Lang AST.
            
        Returns:
            dict: The contextualized pAI_Lang AST.
        """
        # Initialize system context if present
        if 'type' in parsed_pailang and parsed_pailang['type'] == 'PAILang':
            # Extract system identifier if present
            system_id = None
            if 'expression' in parsed_pailang and parsed_pailang['expression'].get('type') == 'SystemIdentifier':
                system_id = parsed_pailang['expression'].get('value')
                
                # Initialize system context
                token_dictionary = {}  # This would be populated in a real implementation
                self.initialize_system_context({'systemIdentifier': {'value': system_id}}, token_dictionary)
            
            # Process context activations in the AST
            self._process_context_activations(parsed_pailang)
        
        # Return the contextualized AST
        return parsed_pailang
    
    def _process_context_activations(self, ast_node):
        """
        Recursively process context activations in the AST.
        
        Args:
            ast_node (dict): The AST node to process.
        """
        if not isinstance(ast_node, dict):
            return
        
        # Process context activation nodes
        if ast_node.get('type') == 'ContextActivation':
            token_dictionary = {}  # This would be populated in a real implementation
            self.process_context_activation(ast_node, token_dictionary)
        
        # Recursively process child nodes
        for key, value in ast_node.items():
            if isinstance(value, dict):
                self._process_context_activations(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._process_context_activations(item)
    
    def process_context_activation(self, context_activation, token_dictionary):
        """
        Process a context activation expression.
        
        Args:
            context_activation (dict): The context activation expression.
            token_dictionary (dict): Dictionary of token definitions.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Extract the context expression
            context_expr = context_activation.get('expression')
            
            # If this is a token sequence, activate each token in sequence
            if context_expr.get('type') == 'TokenSequence':
                for expr in context_expr.get('expressions', []):
                    self._activate_single_context(expr, token_dictionary)
            else:
                # Otherwise, activate a single context
                self._activate_single_context(context_expr, token_dictionary)
            
            return True
        
        except Exception as e:
            print(f"Error processing context activation: {e}")
            return False
    
    def _activate_single_context(self, context_token, token_dictionary):
        """
        Activate a single context based on a token.
        
        Args:
            context_token (dict): The token representing the context.
            token_dictionary (dict): Dictionary of token definitions.
        """
        # Only process context category tokens
        if context_token.get('type') in ['StandardToken', 'ComplexToken'] and \
           context_token.get('categoryCode') == 'C':
            
            # Look up the token definition
            token_value = context_token.get('value')
            token_def = token_dictionary.get(token_value, {})
            
            # Create context object
            context = {
                'id': token_value,
                'definition': token_def,
                'properties': token_def.get('properties', {})
            }
            
            # Activate the context
            self.activate_context(context)
    
    def initialize_system_context(self, ast, token_dictionary):
        """
        Initialize the system context based on the AST.
        
        Args:
            ast (dict): The abstract syntax tree.
            token_dictionary (dict): Dictionary of token definitions.
            
        Returns:
            dict: The system context.
        """
        # Extract system identifier
        system_id = None
        if 'systemIdentifier' in ast:
            system_id = ast['systemIdentifier'].get('value')
        
        # Extract version information
        versions = {}
        if 'versionDeclaration' in ast:
            version_str = ast['versionDeclaration'].get('value', '')
            # Parse version string (e.g., [G-1.2,TD-2.3.1,OP-1.1])
            if version_str.startswith('[') and version_str.endswith(']'):
                version_parts = version_str[1:-1].split(',')
                for part in version_parts:
                    if '-' in part:
                        component, version = part.split('-', 1)
                        versions[component] = version
        
        # Look up system properties
        system_props = {}
        if system_id and system_id in token_dictionary:
            system_props = token_dictionary[system_id].get('properties', {})
        
        # Create system context
        self.system_context = {
            'id': 'SYSTEM',
            'systemId': system_id,
            'versions': versions,
            'properties': system_props
        }
        
        # Activate system context
        self.activate_context(self.system_context)
        
        return self.system_context
    
    def resolve_in_context(self, token, token_dictionary):
        """
        Resolve token semantics based on active context.
        
        Args:
            token (dict): The token to resolve.
            token_dictionary (dict): Dictionary of token definitions.
            
        Returns:
            dict: The resolved token definition.
        """
        # Get token value
        token_value = token.get('value')
        
        # Get base token definition
        token_def = token_dictionary.get(token_value, {})
        
        # If no active context, use default resolution
        active_context = self.get_current_context()
        if not active_context:
            return token_def
        
        # Check if token has context-specific behavior
        context_id = active_context.get('id')
        if 'contextBehaviors' in token_def and context_id in token_def['contextBehaviors']:
            return token_def['contextBehaviors'][context_id]
        
        # Check if token behavior is modified by any active context
        for ctx in self.context_stack:
            ctx_def = ctx.get('definition', {})
            if 'tokenModifiers' in ctx_def:
                category = token.get('categoryCode')
                if category in ctx_def['tokenModifiers']:
                    return self._apply_context_modifier(token_def, ctx_def['tokenModifiers'][category])
        
        # Default to standard definition
        return token_def
    
    def _apply_context_modifier(self, token_def, modifier):
        """
        Apply context modifier to token definition.
        
        Args:
            token_def (dict): The original token definition.
            modifier (dict): The modifier to apply.
            
        Returns:
            dict: The modified token definition.
        """
        # Create a copy of the original definition
        modified_def = token_def.copy()
        
        # Apply modifications
        for key, value in modifier.items():
            if key == 'override':
                # Complete override
                return value
            elif key == 'extend':
                # Extend properties
                for prop_key, prop_value in value.items():
                    if prop_key not in modified_def:
                        modified_def[prop_key] = prop_value
                    elif isinstance(modified_def[prop_key], dict) and isinstance(prop_value, dict):
                        modified_def[prop_key].update(prop_value)
                    elif isinstance(modified_def[prop_key], list) and isinstance(prop_value, list):
                        modified_def[prop_key].extend(prop_value)
                    else:
                        modified_def[prop_key] = prop_value
            elif key == 'modify':
                # Modify specific properties
                for prop_key, prop_value in value.items():
                    if prop_key in modified_def:
                        modified_def[prop_key] = prop_value
        
        return modified_def
