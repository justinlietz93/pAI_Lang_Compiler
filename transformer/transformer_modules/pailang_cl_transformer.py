"""
pAI_Lang to Command Language Transformer module.

This module provides functionality for transforming pAI_Lang
to Command Language (CL) using pattern matching and templates.
"""

import re
from .base import BaseTransformer
from ...utils.debug_logger import logger

class PAILangToCLTransformer(BaseTransformer):
    """
    Specialized transformer for pAI_Lang to Command Language transformation.
    
    Uses pattern matching with regular expressions to identify pAI_Lang tokens and expressions,
    and applies templates to generate Command Language output.
    """
    
    def __init__(self, matrix_data, token_id_generator):
        """
        Initialize the pAI_Lang to CL transformer with matrix data and token ID generator.
        
        Args:
            matrix_data (dict): Matrix data for pAI_Lang to CL transformation.
            token_id_generator: Token ID generator for resolving token references.
        """
        super().__init__(matrix_data)
        self.token_id_generator = token_id_generator
        self._compile_patterns()
        logger.debug("PAILangToCLTransformer initialized")
    
    def transform(self, input_text):
        """
        Transform pAI_Lang input to Command Language.
        
        Args:
            input_text (str): pAI_Lang input text.
            
        Returns:
            str: Command Language output text.
        """
        # Validate input
        if not self._validate_input(input_text):
            return self._handle_error("Invalid or empty input", input_text)
        
        logger.debug(f"Transforming pAI_Lang to CL: {input_text}")
        
        try:
            # Find matching patterns
            for token_entry in self.matrix.get("tokens", []):
                # Get the compiled regex pattern
                regex_pattern = token_entry.get("_compiled_pattern")
                if not regex_pattern:
                    # If pattern wasn't compiled during initialization, compile it now
                    pattern_str = token_entry.get("pattern", "")
                    regex_pattern = re.compile(pattern_str)
                
                # Try to match the pattern
                match = regex_pattern.search(input_text)
                if match:
                    # Extract captured groups
                    captured_values = match.groups()
                    
                    # Create a mapping of placeholders to captured values
                    template = token_entry.get("template", "")
                    placeholders = re.findall(r'\{(\w+)\}', template)
                    
                    placeholder_values = {}
                    for i, placeholder in enumerate(placeholders):
                        if i < len(captured_values):
                            # If this is a token ID, try to resolve it to a value
                            if "_id" in placeholder:
                                category = placeholder.replace("_id", "")
                                token_id = captured_values[i]
                                value, _ = self.token_id_generator.get_value_from_token(token_id)
                                if value:
                                    placeholder_values[placeholder] = value
                                else:
                                    placeholder_values[placeholder] = token_id
                            else:
                                placeholder_values[placeholder] = captured_values[i]
                    
                    # Apply the template
                    result = template
                    for placeholder, value in placeholder_values.items():
                        result = result.replace(f"{{{placeholder}}}", value)
                    
                    # Handle special cases for complex patterns
                    if "?" in input_text and ":" in input_text:
                        # This is a conditional expression
                        conditional_parts = self._parse_pailang_conditional(input_text)
                        if conditional_parts:
                            # Process condition, true branch, and false branch
                            condition_cl = self.transform(conditional_parts["condition"])
                            true_branch_cl = self.transform(conditional_parts["true_branch"])
                            false_branch_cl = self.transform(conditional_parts["false_branch"])
                            
                            # Extract just the relevant parts
                            condition_value = self._extract_cl_parameter_value(condition_cl)
                            true_action = true_branch_cl.strip()
                            false_action = false_branch_cl.strip()
                            
                            # Replace placeholders in template
                            result = result.replace("{condition_id}", condition_value)
                            result = result.replace("{true_action}", true_action)
                            result = result.replace("{false_action}", false_action)
                    
                    logger.debug(f"pAI_Lang to CL transformation successful: {result}")
                    return result
            
            # If no pattern matched, try to handle composite expressions
            if ">" in input_text:
                # Handle sequence operator
                parts = input_text.split(">")
                if len(parts) >= 2:
                    left_cl = self.transform(parts[0])
                    right_cl = self.transform(parts[1])
                    if not left_cl.startswith("ERROR:") and not right_cl.startswith("ERROR:"):
                        result = f"{left_cl}\n{right_cl}"
                        logger.debug(f"Handled sequence operator: {result}")
                        return result
            
            elif "&" in input_text:
                # Handle parallel operator
                parts = input_text.split("&")
                if len(parts) >= 2:
                    left_cl = self.transform(parts[0])
                    right_cl = self.transform(parts[1])
                    if not left_cl.startswith("ERROR:") and not right_cl.startswith("ERROR:"):
                        result = f"{left_cl} AND {right_cl}"
                        logger.debug(f"Handled parallel operator: {result}")
                        return result
            
            # If still no match, return error message
            logger.warning(f"No matching pattern found for pAI_Lang input: {input_text}")
            return self._handle_error("No matching pattern found", input_text)
            
        except Exception as e:
            logger.error(f"Error during pAI_Lang to CL transformation: {e}")
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
            for token_entry in self.matrix.get("tokens", []):
                pattern_str = token_entry.get("pattern", "")
                token_entry["_compiled_pattern"] = re.compile(pattern_str)
            logger.debug("Compiled pAI_Lang to CL patterns")
        except Exception as e:
            logger.error(f"Error compiling patterns: {e}")
    
    def _parse_pailang_conditional(self, pailang_input):
        """
        Parse a pAI_Lang conditional expression.
        
        Args:
            pailang_input (str): pAI_Lang conditional expression.
            
        Returns:
            dict: Parsed conditional components, or None if parsing failed.
        """
        try:
            # Pattern: condition?true_branch:false_branch
            match = re.search(r'(.*?)\?(.*?):(.*)', pailang_input)
            if not match:
                logger.warning(f"Failed to match conditional pattern in: {pailang_input}")
                return None
            
            return {
                "condition": match.group(1),
                "true_branch": match.group(2),
                "false_branch": match.group(3)
            }
            
        except Exception as e:
            logger.error(f"Error parsing pAI_Lang conditional: {e}")
            return None
    
    def _extract_cl_parameter_value(self, cl_command):
        """
        Extract parameter value from a Command Language command.
        
        Args:
            cl_command (str): Command Language command.
            
        Returns:
            str: Extracted parameter value, or empty string if extraction failed.
        """
        try:
            # Extract the parameter value from [PARAM=value]
            match = re.search(r'\[(.*?)=(.*?)\]', cl_command)
            if match:
                return match.group(2)
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting CL parameter value: {e}")
            return ""
