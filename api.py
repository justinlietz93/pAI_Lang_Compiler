"""
Updated API module for the pAI_Lang tooling system.

This module provides the main API for the pAI_Lang tooling system,
integrating the compiler, decoder, and transformer components.
"""

from .compiler.compiler import Compiler
from .decoder.decoder import Decoder
from .transformer.transformer import MatricesTransformer
import os

class PAILangTooling:
    """
    Main API for the pAI_Lang tooling system.
    
    This class provides a unified interface for all pAI_Lang operations:
    - Compiling NL/CL to pAI_Lang
    - Decoding pAI_Lang to CL/NL
    - Direct transformation between different language representations
    """
    
    def __init__(self, token_registry_path=None, matrix_dir=None):
        """
        Initialize the pAI_Lang tooling system.
        
        Args:
            token_registry_path (str, optional): Path to token registry file.
                If None, a default path will be used.
            matrix_dir (str, optional): Directory containing matrix files.
                If None, a default location will be used.
        """
        # Set default paths if not provided
        if token_registry_path is None:
            token_registry_path = os.path.join(os.path.dirname(__file__), 'data', 'token_registry.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(token_registry_path), exist_ok=True)
        
        # Initialize components
        self.compiler = Compiler(token_registry_path=token_registry_path)
        self.decoder = Decoder()
        self.transformer = MatricesTransformer(matrix_dir=matrix_dir)
    
    def compile(self, input_text, input_type="NL"):
        """
        Compile Natural Language or Command Language to pAI_Lang.
        
        Args:
            input_text (str): Input text to compile.
            input_type (str, optional): Type of input text ('NL' or 'CL'). Defaults to 'NL'.
            
        Returns:
            str: Compiled pAI_Lang string.
        """
        return self.compiler.compile(input_text, input_type)
    
    def decode(self, pailang_text, output_type="CL"):
        """
        Decode pAI_Lang to Command Language or Natural Language.
        
        Args:
            pailang_text (str): pAI_Lang text to decode.
            output_type (str, optional): Type of output text ('CL' or 'NL'). Defaults to 'CL'.
            
        Returns:
            str: Decoded output text.
        """
        return self.decoder.decode(pailang_text, output_type)
    
    def nl_to_cl(self, nl_text):
        """
        Transform Natural Language to Command Language.
        
        Args:
            nl_text (str): Natural Language text.
            
        Returns:
            str: Command Language text.
        """
        return self.transformer.nl_to_cl(nl_text)
    
    def cl_to_pailang(self, cl_text):
        """
        Transform Command Language to pAI_Lang.
        
        Args:
            cl_text (str): Command Language text.
            
        Returns:
            str: pAI_Lang text.
        """
        return self.transformer.cl_to_pailang(cl_text)
    
    def pailang_to_cl(self, pailang_text):
        """
        Transform pAI_Lang to Command Language.
        
        Args:
            pailang_text (str): pAI_Lang text.
            
        Returns:
            str: Command Language text.
        """
        return self.transformer.pailang_to_cl(pailang_text)
    
    def cl_to_nl(self, cl_text):
        """
        Transform Command Language to Natural Language.
        
        Args:
            cl_text (str): Command Language text.
            
        Returns:
            str: Natural Language text.
        """
        return self.transformer.cl_to_nl(cl_text)
    
    def get_token_id(self, value, category):
        """
        Get a token ID for a value in a specific category.
        
        Args:
            value (str): The value to get a token ID for.
            category (str): The category of the token.
            
        Returns:
            str: The token ID.
        """
        return self.compiler.get_token_id(value, category)
    
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
        return self.compiler.register_token(value, category, token_id)
    
    def get_value_from_token(self, token):
        """
        Get the value associated with a token ID.
        
        Args:
            token (str): The token ID to look up.
            
        Returns:
            tuple: (value, category) if found, (None, None) otherwise.
        """
        return self.compiler.get_value_from_token(token)
    
    def process_file(self, input_file, output_file, input_type="NL", output_type="pAI_Lang"):
        """
        Process a file, converting its content from one language representation to another.
        
        Args:
            input_file (str): Path to input file.
            output_file (str): Path to output file.
            input_type (str, optional): Type of input text ('NL', 'CL', or 'pAI_Lang'). Defaults to 'NL'.
            output_type (str, optional): Type of output text ('NL', 'CL', or 'pAI_Lang'). Defaults to 'pAI_Lang'.
            
        Returns:
            bool: True if processing was successful, False otherwise.
        """
        try:
            # Read input file
            with open(input_file, 'r') as f:
                input_text = f.read()
            
            # Process based on input and output types
            if input_type == "NL" and output_type == "pAI_Lang":
                output_text = self.compile(input_text, "NL")
            elif input_type == "CL" and output_type == "pAI_Lang":
                output_text = self.compile(input_text, "CL")
            elif input_type == "pAI_Lang" and output_type == "CL":
                output_text = self.decode(input_text, "CL")
            elif input_type == "pAI_Lang" and output_type == "NL":
                output_text = self.decode(input_text, "NL")
            elif input_type == "NL" and output_type == "CL":
                output_text = self.nl_to_cl(input_text)
            elif input_type == "CL" and output_type == "NL":
                output_text = self.cl_to_nl(input_text)
            else:
                raise ValueError(f"Unsupported conversion: {input_type} to {output_type}")
            
            # Write output file
            with open(output_file, 'w') as f:
                f.write(output_text)
            
            return True
        
        except Exception as e:
            print(f"Error processing file: {e}")
            return False
