"""
Natural Language Generator for pAI_Lang

This module provides functionality for translating Command Language (CL) output
to Natural Language (NL) using templates.
"""

from .nl_generator.base import NLGeneratorBase
from .nl_generator.parser import CLParser
from .nl_generator.template_engine import TemplateEngine
from .nl_generator.description_generator import DescriptionGenerator

class NLGenerator(NLGeneratorBase, CLParser, TemplateEngine, DescriptionGenerator):
    """
    Generates Natural Language descriptions from Command Language.
    """
    
    def __init__(self, templates=None):
        """
        Initialize the NL Generator with optional templates.
        
        Args:
            templates (dict, optional): Templates for NL generation.
        """
        self.templates = templates or self._initialize_default_templates()
    
    def generate_nl(self, cl_content):
        """
        Generate Natural Language from Command Language.
        
        Args:
            cl_content (str): Command Language content.
            
        Returns:
            str: Natural Language description.
        """
        # Parse the command language
        commands = self._parse_cl(cl_content)
        
        # Generate description for each command
        descriptions = []
        for command in commands:
            description = self._generate_command_description(command)
            descriptions.append(description)
        
        # Combine descriptions with appropriate connectors
        return self._combine_with_connectors(descriptions)
