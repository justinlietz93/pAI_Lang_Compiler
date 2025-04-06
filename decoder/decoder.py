"""
Updated Decoder module for the pAI_Lang decoder.

This module provides the main Decoder class that coordinates
the decoding process from pAI_Lang to Command Language or Natural Language.
"""

from .pailang_parser import PAILangParser
from .context_manager import ContextManager
from .expansion_engine import ExpansionEngine
from .nl_generator import NLGenerator

class Decoder:
    """
    Decodes pAI_Lang to Command Language or Natural Language.
    """
    
    def __init__(self):
        """
        Initialize the decoder.
        """
        self.pailang_parser = PAILangParser()
        self.context_manager = ContextManager()
        self.expansion_engine = ExpansionEngine(self.context_manager)
        self.nl_generator = NLGenerator()
    
    def decode(self, pailang_text, output_type="CL"):
        """
        Decode pAI_Lang to Command Language or Natural Language.
        
        Args:
            pailang_text (str): pAI_Lang text to decode.
            output_type (str, optional): Type of output text ('CL' or 'NL'). Defaults to 'CL'.
            
        Returns:
            str: Decoded output text.
        """
        # Parse pAI_Lang
        parsed_pailang = self.pailang_parser.parse(pailang_text)
        
        # Apply context
        contextualized_pailang = self.context_manager.apply_context(parsed_pailang)
        
        # Expand to Command Language
        cl_output = self.expansion_engine.expand_to_cl(contextualized_pailang)
        
        # If output type is NL, convert CL to NL
        if output_type.upper() == "NL":
            return self.nl_generator.generate_nl(cl_output)
        
        # Otherwise, return CL
        return cl_output
    
    def pailang_to_cl(self, pailang_text):
        """
        Convert pAI_Lang to Command Language.
        
        Args:
            pailang_text (str): pAI_Lang text.
            
        Returns:
            str: Command Language text.
        """
        return self.decode(pailang_text, "CL")
    
    def pailang_to_nl(self, pailang_text):
        """
        Convert pAI_Lang to Natural Language.
        
        Args:
            pailang_text (str): pAI_Lang text.
            
        Returns:
            str: Natural Language text.
        """
        return self.decode(pailang_text, "NL")
