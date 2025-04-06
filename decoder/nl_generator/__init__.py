"""
Natural Language Generator module for the pAI_Lang decoder.

This module provides the NLGenerator class for converting
Command Language to Natural Language.
"""

from .base import BaseGenerator
from .parser import NLTemplateParser
from .template_engine import TemplateEngine
from .description_generator import DescriptionGenerator

class NLGenerator:
    """
    Generates Natural Language from Command Language.
    """
    
    def __init__(self):
        """
        Initialize the Natural Language generator.
        """
        self.template_parser = NLTemplateParser()
        self.template_engine = TemplateEngine()
        self.description_generator = DescriptionGenerator()
        self.base_generator = BaseGenerator()
    
    def generate_nl(self, cl_text):
        """
        Generate Natural Language from Command Language.
        
        Args:
            cl_text (str): Command Language text.
            
        Returns:
            str: Natural Language text.
        """
        # Parse Command Language
        parsed_cl = self.template_parser.parse_cl(cl_text)
        
        # Generate descriptions for each command
        command_descriptions = []
        for command in parsed_cl:
            description = self.description_generator.generate_description(command)
            command_descriptions.append(description)
        
        # Apply templates to generate Natural Language
        nl_text = self.template_engine.apply_templates(command_descriptions)
        
        # Post-process Natural Language
        nl_text = self.base_generator.post_process(nl_text)
        
        return nl_text
