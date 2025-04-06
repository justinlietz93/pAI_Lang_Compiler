"""
Template Engine module for the NL Generator.

This module provides functionality for applying templates to generate Natural Language.
"""

class TemplateEngine:
    """
    Engine for applying templates to generate Natural Language.
    """
    
    def __init__(self):
        """
        Initialize the template engine.
        """
        self.templates = self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """
        Initialize default templates for different command types.
        
        Returns:
            dict: Default templates.
        """
        return {
            "INITIALIZE": "Initialize the {system} system",
            "SET_CONTEXT": "Set the context to {context}",
            "EXECUTE": "Execute {task}",
            "EXECUTE_TASK": "Execute task {task}",
            "CONDITIONAL": "If {condition}, then {true_action}; otherwise, {false_action}",
            "PARALLEL": "Simultaneously perform: {actions}",
            "REPEAT": "Repeat the following {count} times: {action}",
            "BATCH_OPERATION": "Execute the following operations as a batch: {operations}",
            "ACTIVATE_CONTEXT": "Activate the {context} context",
            "ALLOCATE_RESOURCE": "Allocate resource {resource}",
            "APPLY_SECURITY": "Apply security protocol {protocol}",
            "EXECUTE_QUERY": "Execute query {query}"
        }
    
    def apply_templates(self, command_descriptions):
        """
        Apply templates to generate Natural Language from command descriptions.
        
        Args:
            command_descriptions (list): List of command descriptions.
            
        Returns:
            str: Generated Natural Language text.
        """
        if not command_descriptions:
            return ""
        
        # Combine descriptions into a coherent narrative
        nl_text = self._combine_descriptions(command_descriptions)
        
        return nl_text
    
    def _combine_descriptions(self, descriptions):
        """
        Combine descriptions into a coherent narrative.
        
        Args:
            descriptions (list): List of descriptions to combine.
            
        Returns:
            str: Combined narrative.
        """
        # For a single description, return as is
        if len(descriptions) == 1:
            return descriptions[0]
        
        # For multiple descriptions, combine with appropriate connectors
        result = ""
        
        for i, desc in enumerate(descriptions):
            # First description
            if i == 0:
                result += desc
            # Last description
            elif i == len(descriptions) - 1:
                result += f", and then {desc}"
            # Middle descriptions
            else:
                result += f", then {desc}"
        
        return result
    
    def apply_template(self, command_type, parameters):
        """
        Apply a template for a specific command type with parameters.
        
        Args:
            command_type (str): Type of command.
            parameters (dict): Command parameters.
            
        Returns:
            str: Generated description.
        """
        # Get template for command type
        template = self.templates.get(command_type)
        
        if not template:
            # Default template for unknown command types
            return f"Execute {command_type.lower()} command with parameters: {parameters}"
        
        # Apply template with parameters
        try:
            return template.format(**parameters)
        except KeyError:
            # Fallback if parameters don't match template
            param_str = ", ".join(f"{k}={v}" for k, v in parameters.items())
            return f"{command_type.capitalize()} with {param_str}"
