"""
Description Generator module for the NL Generator.

This module provides functionality for generating natural language descriptions
from Command Language commands.
"""

class DescriptionGenerator:
    """
    Generates natural language descriptions from Command Language commands.
    """
    
    def __init__(self):
        """
        Initialize the description generator.
        """
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self):
        """
        Initialize templates for different command types.
        
        Returns:
            dict: Templates for command types.
        """
        return {
            "INITIALIZE": "initialize the {SYSTEM} system",
            "SET_CONTEXT": "set the context to {CONTEXT}",
            "EXECUTE": "execute {TASK}",
            "EXECUTE_TASK": "execute task {TASK}",
            "CONDITIONAL": "if {CONDITION}, then {TRUE_ACTION}; otherwise, {FALSE_ACTION}",
            "PARALLEL": "simultaneously perform: {ACTIONS}",
            "REPEAT": "repeat the following {count} times: {ACTION}",
            "BATCH_OPERATION": "execute the following operations as a batch: {OPERATIONS}",
            "ACTIVATE_CONTEXT": "activate the {CONTEXT} context",
            "ALLOCATE_RESOURCE": "allocate resource {RESOURCE}",
            "APPLY_SECURITY": "apply security protocol {PROTOCOL}",
            "EXECUTE_QUERY": "execute query {QUERY}"
        }
    
    def generate_description(self, command):
        """
        Generate a natural language description for a command.
        
        Args:
            command (dict): Command to generate description for.
            
        Returns:
            str: Natural language description.
        """
        command_type = command.get('type', '')
        
        # Get template for command type
        template = self.templates.get(command_type)
        
        if not template:
            # Default description for unknown command types
            params_str = ', '.join(f"{k}={v}" for k, v in command.get('parameters', {}).items())
            return f"execute {command_type.lower()} command with parameters: {params_str}"
        
        # Apply template with parameters
        return self._apply_template(template, command)
    
    def _apply_template(self, template, command):
        """
        Apply a template with command parameters.
        
        Args:
            template (str): Template string.
            command (dict): Command with parameters.
            
        Returns:
            str: Filled template.
        """
        # Extract parameters
        params = command.get('parameters', {})
        
        # Create a copy of parameters for template formatting
        format_params = {}
        
        # Add all parameters to format_params
        for key, value in params.items():
            format_params[key] = value
        
        # Handle special cases based on command type
        command_type = command.get('type', '')
        
        if command_type == 'CONDITIONAL':
            # Handle conditional command
            true_branch = command.get('true_branch', [])
            false_branch = command.get('false_branch', [])
            
            # Generate descriptions for true and false branches
            true_desc = self._generate_branch_description(true_branch)
            false_desc = self._generate_branch_description(false_branch)
            
            # Add to format parameters
            format_params['TRUE_ACTION'] = true_desc
            format_params['FALSE_ACTION'] = false_desc
        
        elif command_type == 'PARALLEL':
            # Handle parallel command
            actions = command.get('actions', [])
            
            # Generate description for actions
            actions_desc = self._generate_branch_description(actions)
            
            # Add to format parameters
            format_params['ACTIONS'] = actions_desc
        
        elif command_type == 'REPEAT':
            # Handle repeat command
            action = command.get('action', [])
            
            # Generate description for action
            action_desc = self._generate_branch_description(action)
            
            # Add to format parameters
            format_params['ACTION'] = action_desc
            format_params['count'] = params.get('count', '1')
        
        elif command_type == 'BATCH_OPERATION':
            # Handle batch operation command
            operations = command.get('operations', [])
            
            # Generate description for operations
            operations_desc = self._generate_branch_description(operations)
            
            # Add to format parameters
            format_params['OPERATIONS'] = operations_desc
        
        # Apply template with format parameters
        try:
            return template.format(**format_params)
        except KeyError as e:
            # Fallback if parameters don't match template
            return f"execute {command_type.lower()} command"
    
    def _generate_branch_description(self, commands):
        """
        Generate a description for a branch of commands.
        
        Args:
            commands (list): List of commands in the branch.
            
        Returns:
            str: Description of the branch.
        """
        if not commands:
            return "do nothing"
        
        # Generate descriptions for each command
        descriptions = []
        for command in commands:
            desc = self.generate_description(command)
            descriptions.append(desc)
        
        # Combine descriptions
        if len(descriptions) == 1:
            return descriptions[0]
        
        # For multiple descriptions, use commas and 'and'
        result = ", ".join(descriptions[:-1])
        result += f", and {descriptions[-1]}"
        
        return result
