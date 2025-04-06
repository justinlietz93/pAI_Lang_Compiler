"""
Updated SemanticAnalyzer module for the pAI_Lang compiler.

This module provides the main SemanticAnalyzer class that coordinates
the analysis of parsed Natural Language (NL) and Command Language (CL) inputs.
"""

from pailang_tooling.compiler.semantic_analyzer.nl_analyzer import NLAnalyzer
from pailang_tooling.compiler.semantic_analyzer.cl_analyzer import CLAnalyzer
from pailang_tooling.compiler.semantic_analyzer.mapping_utils import MappingUtils
from pailang_tooling.compiler.semantic_analyzer.token_id_generator import TokenIDGenerator

class SemanticAnalyzer:
    """
    Analyzes the semantic meaning of parsed inputs and maps them to pAI_Lang concepts.
    """
    
    def __init__(self, token_dictionary=None, token_registry_path=None):
        """
        Initialize the semantic analyzer.
        
        Args:
            token_dictionary (dict, optional): Dictionary of token definitions.
            token_registry_path (str, optional): Path to token registry file.
        """
        self.token_dictionary = token_dictionary or {}
        self.token_registry_path = token_registry_path
        self.token_id_generator = TokenIDGenerator(token_registry_path)
        self.mapping_utils = MappingUtils(self.token_dictionary, token_registry_path)
        self.nl_analyzer = NLAnalyzer(self.mapping_utils)
        self.cl_analyzer = CLAnalyzer(self.mapping_utils)
    
    def analyze(self, parsed_input):
        """
        Analyze parsed input and map to pAI_Lang concepts.
        
        Args:
            parsed_input (dict): Parsed input from the parser.
            
        Returns:
            dict: Semantic analysis with pAI_Lang mappings.
        """
        input_type = parsed_input.get("type", "NL")
        
        if input_type == "CL":
            return self.cl_analyzer.analyze_cl(parsed_input.get("content", {}))
        else:  # Default to NL
            return self.nl_analyzer.analyze_nl(parsed_input.get("content", {}))
    
    def get_token_id(self, value, category):
        """
        Get a token ID for a value in a specific category.
        
        Args:
            value (str): The value to get a token ID for.
            category (str): The category of the token.
            
        Returns:
            str: The token ID.
        """
        return self.token_id_generator.get_token_id(value, category)
    
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
        return self.token_id_generator.register_token(value, category, token_id)
    
    def get_value_from_token(self, token):
        """
        Get the value associated with a token ID.
        
        Args:
            token (str): The token ID to look up.
            
        Returns:
            tuple: (value, category) if found, (None, None) otherwise.
        """
        return self.token_id_generator.get_value_from_token(token)
