"""
Command Language to pAI_Lang Transformer module.

This module provides functionality for transforming Command Language (CL)
to pAI_Lang using command matching and templates with token ID generation.
"""

import re
from .base import BaseTransformer
from ...utils.debug_logger import logger

class CLToPAILangTransformer(BaseTransformer):
    """
    Specialized transformer for Command Language to pAI_Lang transformation.
    
    Uses command matching and templates to generate pAI_Lang output,
    with token ID generation for consistent token references.
    """
    
    def __init__(self, matrix_data, token_id_generator):
        """
        Initialize the CL to pAI_Lang transformer with matrix data and token ID generator.
        
        Args:
            matrix_data (dict): Matrix data for CL to pAI_Lang transformation.
            token_id_generator: Token ID generator for consistent token references.
        """
        super().__init__(matrix_data)
        self.token_id_generator = token_id_generator
        logger.debug("CLToPAILangTransformer initialized")
    
    def transform(self, input_text):
        """
        Transform Command Language input to pAI_Lang.
        
        Args:
            input_text (str): Command Language input text.
            
        Returns:
            str: pAI_Lang output text.
        """
        # Validate input
        if not self._validate_input(input_text):
            return self._handle_error("Invalid or empty input", input_text)
        
        logger.debug(f"Transforming CL to pAI_Lang: {input_text}")
        
        try:
            # Parse the command structure
            command_parts = self._parse_cl_command(input_text)
            if not command_parts:
                return self._handle_error("Failed to parse command", input_text)
            
            # Find matching command
            for command_entry in self.matrix.get("commands", []):
                if command_entry.get("command") == command_parts.get("command"):
                    # Extract parameter values
                    param_values = {}
                    for param in command_entry.get("parameters", []):
                        if param in command_parts.get("parameters", {}):
                            param_values[param.lower()] = command_parts["parameters"][param]
                    
                    # Handle subcommands if needed
                    if command_entry.get("subcommands", False) and "subcommands" in command_parts:
                        # Process subcommands recursively
                        subcommand_results = []
                        for subcommand in command_parts["subcommands"]:
                            subcommand_pailang = self.transform(subcommand)
                            if subcommand_pailang and not subcommand_pailang.startswith("ERROR:"):
                                subcommand_results.append(subcommand_pailang)
                        
                        # Add subcommand results to parameter values
                        if len(subcommand_results) > 0:
                            param_values["true_action"] = subcommand_results[0]
                        if len(subcommand_results) > 1:
                            param_values["false_action"] = subcommand_results[1]
                    
                    # Generate token IDs for parameters
                    for param, value in list(param_values.items()):
                        # Convert parameter name to token category
                        category = self._param_to_category(param)
                        if category:
                            # Generate or retrieve token ID
                            token_id = self.token_id_generator.get_token_id(value, category)
                            param_values[f"{param}_id"] = token_id
                    
                    # Apply the template
                    template = command_entry.get("pailang_template", "")
                    for param, value in param_values.items():
                        template = template.replace(f"{{{param}}}", value)
                    
                    logger.debug(f"CL to pAI_Lang transformation successful: {template}")
                    return template
            
            # If no command matched, return error message
            logger.warning(f"No matching command found for CL input: {input_text}")
            return self._handle_error("No matching command found", input_text)
            
        except Exception as e:
            logger.error(f"Error during CL to pAI_Lang transformation: {e}")
            return self._handle_error(f"Transformation error: {str(e)}", input_text)
    
    def _parse_cl_command(self, cl_input):
        """
        Parse a Command Language command into its components.
        
        Args:
            cl_input (str): Command Language input string.
            
        Returns:
            dict: Parsed command components, or None if parsing failed.
        """
        try:
            # Basic command pattern: >>> COMMAND [PARAM1=value1, PARAM2=value2]
            command_match = re.search(r'>>>\s+(\w+)\s+\[(.*?)\]', cl_input)
            if not command_match:
                logger.warning(f"Failed to match command pattern in: {cl_input}")
                return None
            
            command = command_match.group(1)
            params_str = command_match.group(2)
            
            # Parse parameters
            parameters = {}
            param_matches = re.findall(r'(\w+)=(.*?)(?:,|$)', params_str)
            for param_name, param_value in param_matches:
                parameters[param_name] = param_value.strip()
            
            # Check for subcommands (indented lines)
            subcommands = []
            lines = cl_input.split('\n')
            for i, line in enumerate(lines):
                if i > 0 and line.strip().startswith('>>>') and line.startswith('    '):
                    subcommands.append(line.strip())
            
            result = {
                "command": command,
                "parameters": parameters
            }
            
            if subcommands:
                result["subcommands"] = subcommands
            
            logger.debug(f"Parsed CL command: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing CL command: {e}")
            return None
    
    def _param_to_category(self, param_name):
        """
        Convert parameter name to token category.
        
        Args:
            param_name (str): Parameter name.
            
        Returns:
            str: Token category, or None if no mapping exists.
        """
        param_to_category = {
            "system": "system",
            "context": "context",
            "task": "task",
            "condition": "condition",
            "true_action": "action",
            "false_action": "action",
            "resource": "resource",
            "query": "query",
            "batch": "batch",
            "directive": "directive"
        }
        
        category = param_to_category.get(param_name.lower())
        if not category:
            logger.warning(f"No category mapping for parameter: {param_name}")
        
        return category
