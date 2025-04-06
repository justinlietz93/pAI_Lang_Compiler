"""
Command Language to Natural Language Transformer module.

This module provides functionality for transforming Command Language (CL)
to Natural Language (NL) using command matching and templates.
"""

import re
from .base import BaseTransformer
from ...utils.debug_logger import logger

class CLToNLTransformer(BaseTransformer):
    """
    Specialized transformer for Command Language to Natural Language transformation.
    
    Uses command matching and templates to generate Natural Language output.
    """
    
    def __init__(self, matrix_data):
        """
        Initialize the CL to NL transformer with matrix data.
        
        Args:
            matrix_data (dict): Matrix data for CL to NL transformation.
        """
        super().__init__(matrix_data)
        logger.debug("CLToNLTransformer initialized")
    
    def transform(self, input_text):
        """
        Transform Command Language input to Natural Language.
        
        Args:
            input_text (str): Command Language input text.
            
        Returns:
            str: Natural Language output text.
        """
        # Validate input
        if not self._validate_input(input_text):
            return self._handle_error("Invalid or empty input", input_text)
        
        logger.debug(f"Transforming CL to NL: {input_text}")
        
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
                    if "subcommands" in command_parts:
                        # Process subcommands recursively
                        subcommand_results = []
                        for subcommand in command_parts["subcommands"]:
                            subcommand_nl = self.transform(subcommand)
                            if subcommand_nl and not subcommand_nl.startswith("ERROR:"):
                                subcommand_results.append(subcommand_nl)
                        
                        # Add subcommand results to parameter values
                        if len(subcommand_results) > 0:
                            param_values["true_action"] = subcommand_results[0]
                        if len(subcommand_results) > 1:
                            param_values["false_action"] = subcommand_results[1]
                    
                    # Apply the template
                    template = command_entry.get("nl_template", "")
                    for param, value in param_values.items():
                        template = template.replace(f"{{{param}}}", value)
                    
                    logger.debug(f"CL to NL transformation successful: {template}")
                    return template
            
            # If no command matched, return error message
            logger.warning(f"No matching command found for CL input: {input_text}")
            return self._handle_error("No matching command found", input_text)
            
        except Exception as e:
            logger.error(f"Error during CL to NL transformation: {e}")
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
    
    def _format_nl_output(self, output):
        """
        Format Natural Language output for better readability.
        
        Args:
            output (str): Raw Natural Language output.
            
        Returns:
            str: Formatted Natural Language output.
        """
        try:
            # Capitalize first letter
            if output and len(output) > 0:
                output = output[0].upper() + output[1:]
            
            # Ensure output ends with a period if it doesn't already end with punctuation
            if output and not output[-1] in ['.', '!', '?']:
                output += '.'
            
            return output
            
        except Exception as e:
            logger.error(f"Error formatting NL output: {e}")
            return output
