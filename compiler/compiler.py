"""
Updated Compiler module for the pAI_Lang compiler with debug logging.

This module provides the main Compiler class that coordinates
the compilation process from Natural Language or Command Language to pAI_Lang.
"""

from .parser.nl_parser import NLParser
from .parser.cl_parser import CLParser
from .semantic_analyzer import SemanticAnalyzer
from .structure_synthesizer import StructureSynthesizer
from ..utils.debug_logger import logger

class Compiler:
    """
    Compiles Natural Language or Command Language to pAI_Lang.
    """
    
    def __init__(self, token_registry_path=None):
        """
        Initialize the compiler.
        
        Args:
            token_registry_path (str, optional): Path to token registry file.
        """
        logger.debug("Initializing Compiler")
        self.nl_parser = NLParser()
        self.cl_parser = CLParser()
        self.semantic_analyzer = SemanticAnalyzer(token_registry_path=token_registry_path)
        self.structure_synthesizer = StructureSynthesizer()
    
    def compile(self, input_text, input_type="NL"):
        """
        Compile input text to pAI_Lang.
        
        Args:
            input_text (str): Input text to compile.
            input_type (str, optional): Type of input text ('NL' or 'CL'). Defaults to 'NL'.
            
        Returns:
            str: Compiled pAI_Lang string.
        """
        logger.debug(f"Compiling {input_type} input: {input_text}")
        
        # Parse input
        parsed_input = self._parse_input(input_text, input_type)
        logger.debug(f"Parsed input: {parsed_input}")
        
        # Analyze semantics
        semantic_analysis = self.semantic_analyzer.analyze(parsed_input)
        logger.debug(f"Semantic analysis: {semantic_analysis}")
        
        # Synthesize pAI_Lang
        pailang_string = self.structure_synthesizer.synthesize(semantic_analysis)
        logger.debug(f"Synthesized pAI_Lang: {pailang_string}")
        
        return pailang_string
    
    def _parse_input(self, input_text, input_type):
        """
        Parse input text based on input type.
        
        Args:
            input_text (str): Input text to parse.
            input_type (str): Type of input text ('NL' or 'CL').
            
        Returns:
            dict: Parsed input.
        """
        logger.debug(f"Parsing {input_type} input")
        if input_type.upper() == "CL":
            return {
                "type": "CL",
                "content": self.cl_parser.parse(input_text)
            }
        else:  # Default to NL
            return {
                "type": "NL",
                "content": self.nl_parser.parse(input_text)
            }
    
    def get_token_id(self, value, category):
        """
        Get a token ID for a value in a specific category.
        
        Args:
            value (str): The value to get a token ID for.
            category (str): The category of the token.
            
        Returns:
            str: The token ID.
        """
        return self.semantic_analyzer.get_token_id(value, category)
    
    def register_token(self, value, category, token_id):
        """
        Register a token ID for a value in a specific category.
        
        Args:
            value (str): The value to register.
            category (str): The category of the token.
            token_id (str): The token ID to register.
            
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        return self.semantic_analyzer.register_token(value, category, token_id)
    
    def get_value_from_token(self, token):
        """
        Get the value associated with a token ID.
        
        Args:
            token (str): The token ID to look up.
            
        Returns:
            tuple: (value, category) if found, (None, None) otherwise.
        """
        return self.semantic_analyzer.get_value_from_token(token)
