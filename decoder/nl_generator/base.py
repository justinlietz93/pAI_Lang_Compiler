"""
Base module for the NL Generator.

This module provides the base functionality for template initialization.
"""

class BaseGenerator:
    """
    Base class for the NL Generator with template initialization functionality.
    """
    
    def __init__(self):
        """
        Initialize the base generator.
        """
        self.templates = self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """
        Initialize default templates for NL generation.
        
        Returns:
            dict: Default templates for different command types.
        """
        return {
            "INITIALIZE": "Initialize the {system} system",
            "SET_CONTEXT": "Set the context to {context}",
            "EXECUTE": "Execute {task}",
            "EXECUTE_TASK": "Execute task {id}",
            "CONDITIONAL": "If {condition}, then {true_action}; otherwise, {false_action}",
            "PARALLEL": "Simultaneously perform: {actions}",
            "REPEAT": "Repeat the following {count} times: {action}",
            "BATCH_OPERATION": "Execute the following operations as a batch: {operations}",
            "ACTIVATE_CONTEXT": "Activate the {context} context",
            "ALLOCATE_RESOURCE": "Allocate resource {id}",
            "APPLY_SECURITY": "Apply security protocol {id}",
            "EXECUTE_QUERY": "Execute query {id}",
            "PIPE": "Pipe the output of {source} to {target}",
            "ASSIGN": "Assign {target} the value of {value}",
            "AGGREGATE": "Aggregate the following: {items}"
        }
    
    def _combine_with_connectors(self, descriptions):
        """
        Combine descriptions with appropriate connectors.
        
        Args:
            descriptions (list): List of descriptions to combine.
            
        Returns:
            str: Combined description.
        """
        if not descriptions:
            return ""
        
        if len(descriptions) == 1:
            return descriptions[0]
        
        # For two descriptions, use 'and'
        if len(descriptions) == 2:
            return f"{descriptions[0]} and {descriptions[1]}"
        
        # For more than two, use commas and 'and'
        result = ", ".join(descriptions[:-1])
        result += f", and {descriptions[-1]}"
        
        return result
    
    def post_process(self, text):
        """
        Post-process generated Natural Language text.
        
        Args:
            text (str): Raw generated text.
            
        Returns:
            str: Post-processed text.
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Ensure proper capitalization
        text = text[0].upper() + text[1:]
        
        # Ensure proper ending punctuation
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
