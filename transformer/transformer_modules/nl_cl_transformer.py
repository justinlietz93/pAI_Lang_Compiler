"""
Natural Language to Command Language Transformer module.

This module provides functionality for transforming Natural Language (NL)
to Command Language (CL) using pattern matching and templates.
"""

import re
from .base import BaseTransformer
from ...utils.debug_logger import logger

class NLToCLTransformer(BaseTransformer):
    """
    Specialized transformer for Natural Language to Command Language transformation.
    
    Uses pattern matching with regular expressions to identify commands and
    applies templates to generate Command Language output.
    """
    
    def __init__(self, matrix_data):
        """
        Initialize the NL to CL transformer with matrix data.
        
        Args:
            matrix_data (dict): Matrix data for NL to CL transformation.
        """
        super().__init__(matrix_data)
        self._compile_patterns()
        logger.debug("NLToCLTransformer initialized")
    
    def transform(self, input_text):
        """
        Transform Natural Language input to Command Language.
        
        Args:
            input_text (str): Natural Language input text.
            
        Returns:
            str: Command Language output text.
        """
        # Validate input
        if not self._validate_input(input_text):
            return self._handle_error("Invalid or empty input", input_text)
        
        logger.debug(f"Transforming NL to CL: {input_text}")
        
        try:
            # Find matching patterns
            for pattern_entry in self.matrix.get("patterns", []):
                # Get the compiled regex pattern
                regex_pattern = pattern_entry.get("_compiled_pattern")
                if not regex_pattern:
                    # If pattern wasn't compiled during initialization, compile it now
                    pattern_str = pattern_entry.get("pattern", "")
                    regex_pattern = self._convert_pattern_to_regex(pattern_str)
                
                # Extract placeholder names
                placeholders = re.findall(r'\{(\w+)\}', pattern_entry.get("pattern", ""))
                
                # Try to match the pattern
                match = regex_pattern.search(input_text)
                if match:
                    # Extract captured groups
                    captured_values = match.groups()
                    
                    # Create a mapping of placeholders to captured values
                    placeholder_values = {}
                    for i, placeholder in enumerate(placeholders):
                        if i < len(captured_values):
                            placeholder_values[placeholder] = captured_values[i]
                    
                    # Apply the template
                    template = pattern_entry.get("template", "")
                    for placeholder, value in placeholder_values.items():
                        template = template.replace(f"{{{placeholder}}}", value)
                    
                    logger.debug(f"NL to CL transformation successful: {template}")
                    return template
            
            # If no pattern matched, return error message
            logger.warning(f"No matching pattern found for NL input: {input_text}")
            return self._handle_error("No matching pattern found", input_text)
            
        except Exception as e:
            logger.error(f"Error during NL to CL transformation: {e}")
            return self._handle_error(f"Transformation error: {str(e)}", input_text)
    
    def update_matrix(self, new_matrix):
        """
        Update the transformation matrix and recompile patterns.
        
        Args:
            new_matrix (dict): New matrix data.
            
        Returns:
            bool: True if update was successful, False otherwise.
        """
        result = super().update_matrix(new_matrix)
        if result:
            self._compile_patterns()
        return result
    
    def _compile_patterns(self):
        """
        Precompile regex patterns for better performance.
        """
        try:
            for pattern_entry in self.matrix.get("patterns", []):
                pattern_str = pattern_entry.get("pattern", "")
                pattern_entry["_compiled_pattern"] = self._convert_pattern_to_regex(pattern_str)
            logger.debug("Compiled NL to CL patterns")
        except Exception as e:
            logger.error(f"Error compiling patterns: {e}")
    
    def _convert_pattern_to_regex(self, pattern):
        """
        Convert a pattern with {placeholders} to a compiled regex pattern.
        
        Args:
            pattern (str): Pattern with {placeholders}.
            
        Returns:
            re.Pattern: Compiled regex pattern.
        """
        # Replace placeholders with capture groups
        regex_pattern = pattern
        placeholders = re.findall(r'\{(\w+)\}', pattern)
        for placeholder in placeholders:
            regex_pattern = regex_pattern.replace(f"{{{placeholder}}}", r"(.*?)")
        
        # Escape special regex characters except for the capture groups
        regex_pattern = re.sub(r'(\(\.\*\?\))', r'___CAPTURE___', regex_pattern)
        regex_pattern = re.escape(regex_pattern)
        regex_pattern = regex_pattern.replace(r'___CAPTURE___', r'(.*?)')
        
        # Add start and end anchors for exact matching
        regex_pattern = f"^{regex_pattern}$"
        
        # Compile the pattern with case insensitivity
        return re.compile(regex_pattern, re.IGNORECASE)
