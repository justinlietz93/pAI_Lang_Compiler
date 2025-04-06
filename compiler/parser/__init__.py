"""
Base module for the Parser component.

This module provides the main Parser class that coordinates
the parsing of Natural Language and Command Language inputs.
"""

from .nl_parser import NLParser
from .cl_parser import CLParser

class Parser:
    """
    Parser for Natural Language and Command Language inputs.
    """
    
    def __init__(self):
        """
        Initialize the parser.
        """
        self.nl_parser = NLParser()
        self.cl_parser = CLParser()
    
    def parse(self, input_text):
        """
        Parse input text and determine whether it's NL or CL.
        
        Args:
            input_text (str): The input text to parse.
            
        Returns:
            dict: Parsed representation with input type and parsed content.
        """
        # Determine input type
        input_type = self._determine_input_type(input_text)
        
        # Parse based on input type
        if input_type == "CL":
            parsed_content = self.cl_parser.parse_cl(input_text)
        else:  # Default to NL
            parsed_content = self.nl_parser.parse_nl(input_text)
        
        return {
            "type": input_type,
            "content": parsed_content
        }
    
    def _determine_input_type(self, input_text):
        """
        Determine whether the input is Natural Language or Command Language.
        
        Args:
            input_text (str): The input text to analyze.
            
        Returns:
            str: "CL" for Command Language, "NL" for Natural Language.
        """
        # Check for Command Language pattern (>>> prefix)
        import re
        if re.search(r'^\s*>>>\s+\w+', input_text, re.MULTILINE):
            return "CL"
        else:
            return "NL"
