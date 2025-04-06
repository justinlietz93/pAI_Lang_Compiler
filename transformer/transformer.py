"""
Matrices Transformer for pAI_Lang

This module implements the component managing the bidirectional mapping matrices
between Natural Language (NL), Command Language (CL), and pAI_Lang.

The transformer provides methods for:
- nl_to_cl: Convert Natural Language to Command Language
- cl_to_pailang: Convert Command Language to pAI_Lang
- pailang_to_cl: Convert pAI_Lang to Command Language
- cl_to_nl: Convert Command Language to Natural Language
"""

import re
import os
import json
from pathlib import Path
from .matrix_loader import MatrixLoader
from .transformer_modules.nl_cl_transformer import NLToCLTransformer
from .transformer_modules.cl_pailang_transformer import CLToPAILangTransformer
from .transformer_modules.pailang_cl_transformer import PAILangToCLTransformer
from .transformer_modules.cl_nl_transformer import CLToNLTransformer
from ..utils.debug_logger import logger
from ..compiler.semantic_analyzer.token_id_generator import TokenIDGenerator

class MatricesTransformer:
    """
    Main class for managing bidirectional mapping matrices and performing transformations
    between different representations (NL, CL, pAI_Lang).
    """
    
    def __init__(self, matrix_data=None, matrix_dir=None, token_registry_path=None):
        """
        Initialize the MatricesTransformer with optional matrix data.
        
        Args:
            matrix_data (dict, optional): Pre-loaded matrix data. If None, matrices will be loaded.
            matrix_dir (str, optional): Directory containing matrix files. If None, default location will be used.
            token_registry_path (str, optional): Path to token registry file. If None, an in-memory registry will be used.
        """
        logger.debug("Initializing MatricesTransformer")
        
        # Initialize matrix loader and load matrices
        self.matrix_loader = MatrixLoader(matrix_dir)
        self.matrices = matrix_data if matrix_data is not None else self.matrix_loader.load_matrices()
        
        # Initialize token ID generator with registry path
        self.token_id_generator = TokenIDGenerator(token_registry_path)
        
        # Initialize specialized transformer modules
        self.nl_cl_transformer = NLToCLTransformer(self.matrices["nl_to_cl"])
        self.cl_pailang_transformer = CLToPAILangTransformer(self.matrices["cl_to_pailang"], self.token_id_generator)
        self.pailang_cl_transformer = PAILangToCLTransformer(self.matrices["pailang_to_cl"], self.token_id_generator)
        self.cl_nl_transformer = CLToNLTransformer(self.matrices["cl_to_nl"])
        
        # Initialize cache for performance
        self.cache = {
            "nl_to_cl": {},
            "cl_to_pailang": {},
            "pailang_to_cl": {},
            "cl_to_nl": {}
        }
        
        logger.debug("MatricesTransformer initialized successfully")
    
    def nl_to_cl(self, nl_input):
        """
        Convert Natural Language to Command Language.
        
        Args:
            nl_input (str): Natural Language input string.
            
        Returns:
            str: Command Language output string.
        """
        logger.debug(f"Converting NL to CL: {nl_input}")
        
        # Check cache first
        if nl_input in self.cache["nl_to_cl"]:
            logger.debug("Using cached NL to CL result")
            return self.cache["nl_to_cl"][nl_input]
        
        # Use specialized transformer
        cl_output = self.nl_cl_transformer.transform(nl_input)
        
        # Cache the result
        self.cache["nl_to_cl"][nl_input] = cl_output
        
        logger.debug(f"NL to CL result: {cl_output}")
        return cl_output
    
    def cl_to_pailang(self, cl_input):
        """
        Convert Command Language to pAI_Lang.
        
        Args:
            cl_input (str): Command Language input string.
            
        Returns:
            str: pAI_Lang output string.
        """
        logger.debug(f"Converting CL to pAI_Lang: {cl_input}")
        
        # Check cache first
        if cl_input in self.cache["cl_to_pailang"]:
            logger.debug("Using cached CL to pAI_Lang result")
            return self.cache["cl_to_pailang"][cl_input]
        
        # Use specialized transformer
        pailang_output = self.cl_pailang_transformer.transform(cl_input)
        
        # Cache the result
        self.cache["cl_to_pailang"][cl_input] = pailang_output
        
        logger.debug(f"CL to pAI_Lang result: {pailang_output}")
        return pailang_output
    
    def pailang_to_cl(self, pailang_input):
        """
        Convert pAI_Lang to Command Language.
        
        Args:
            pailang_input (str): pAI_Lang input string.
            
        Returns:
            str: Command Language output string.
        """
        logger.debug(f"Converting pAI_Lang to CL: {pailang_input}")
        
        # Check cache first
        if pailang_input in self.cache["pailang_to_cl"]:
            logger.debug("Using cached pAI_Lang to CL result")
            return self.cache["pailang_to_cl"][pailang_input]
        
        # Use specialized transformer
        cl_output = self.pailang_cl_transformer.transform(pailang_input)
        
        # Cache the result
        self.cache["pailang_to_cl"][pailang_input] = cl_output
        
        logger.debug(f"pAI_Lang to CL result: {cl_output}")
        return cl_output
    
    def cl_to_nl(self, cl_input):
        """
        Convert Command Language to Natural Language.
        
        Args:
            cl_input (str): Command Language input string.
            
        Returns:
            str: Natural Language output string.
        """
        logger.debug(f"Converting CL to NL: {cl_input}")
        
        # Check cache first
        if cl_input in self.cache["cl_to_nl"]:
            logger.debug("Using cached CL to NL result")
            return self.cache["cl_to_nl"][cl_input]
        
        # Use specialized transformer
        nl_output = self.cl_nl_transformer.transform(cl_input)
        
        # Cache the result
        self.cache["cl_to_nl"][cl_input] = nl_output
        
        logger.debug(f"CL to NL result: {nl_output}")
        return nl_output
    
    def transform(self, input_text, source_format, target_format):
        """
        Transform text from one format to another.
        
        Args:
            input_text (str): Input text to transform.
            source_format (str): Source format ('nl', 'cl', or 'pailang').
            target_format (str): Target format ('nl', 'cl', or 'pailang').
            
        Returns:
            str: Transformed text.
        """
        logger.debug(f"Transforming from {source_format} to {target_format}")
        
        # Validate formats
        valid_formats = ['nl', 'cl', 'pailang']
        if source_format not in valid_formats or target_format not in valid_formats:
            error_msg = f"Invalid format: {source_format} or {target_format}. Valid formats are {valid_formats}"
            logger.error(error_msg)
            return f"ERROR: {error_msg}"
        
        # Direct transformations
        if source_format == 'nl' and target_format == 'cl':
            return self.nl_to_cl(input_text)
        elif source_format == 'cl' and target_format == 'pailang':
            return self.cl_to_pailang(input_text)
        elif source_format == 'pailang' and target_format == 'cl':
            return self.pailang_to_cl(input_text)
        elif source_format == 'cl' and target_format == 'nl':
            return self.cl_to_nl(input_text)
        
        # Multi-step transformations
        if source_format == 'nl' and target_format == 'pailang':
            cl_text = self.nl_to_cl(input_text)
            return self.cl_to_pailang(cl_text)
        elif source_format == 'pailang' and target_format == 'nl':
            cl_text = self.pailang_to_cl(input_text)
            return self.cl_to_nl(cl_text)
        
        # Same format, return input
        if source_format == target_format:
            return input_text
        
        # Should never reach here
        return f"ERROR: Unsupported transformation from {source_format} to {target_format}"
    
    def add_matrix_entry(self, matrix_type, entry):
        """
        Add a new entry to a specific matrix.
        
        Args:
            matrix_type (str): Type of matrix ('nl_to_cl', 'cl_to_pailang', etc.)
            entry (dict): New entry to add.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        logger.debug(f"Adding entry to {matrix_type} matrix")
        
        # Validate matrix type
        if matrix_type not in self.matrices:
            logger.error(f"Invalid matrix type: {matrix_type}")
            return False
        
        # Add entry to appropriate section based on matrix type
        if matrix_type == "nl_to_cl" and "pattern" in entry and "template" in entry:
            self.matrices[matrix_type]["patterns"].append(entry)
            self.nl_cl_transformer.update_matrix(self.matrices[matrix_type])
        elif matrix_type == "cl_to_pailang" and "command" in entry and "pailang_template" in entry:
            self.matrices[matrix_type]["commands"].append(entry)
            self.cl_pailang_transformer.update_matrix(self.matrices[matrix_type])
        elif matrix_type == "pailang_to_cl" and "pattern" in entry and "template" in entry:
            self.matrices[matrix_type]["tokens"].append(entry)
            self.pailang_cl_transformer.update_matrix(self.matrices[matrix_type])
        elif matrix_type == "cl_to_nl" and "command" in entry and "nl_template" in entry:
            self.matrices[matrix_type]["commands"].append(entry)
            self.cl_nl_transformer.update_matrix(self.matrices[matrix_type])
        else:
            logger.error(f"Invalid entry format for matrix type: {matrix_type}")
            return False
        
        # Clear cache for this matrix type
        self.cache[matrix_type] = {}
        
        # Save updated matrix
        return self.matrix_loader.save_matrix(matrix_type, self.matrices[matrix_type])
    
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
    
    def get_value_from_token(self, token):
        """
        Get the value associated with a token ID.
        
        Args:
            token (str): The token ID to look up.
            
        Returns:
            tuple: (value, category) if found, (None, None) otherwise.
        """
        return self.token_id_generator.get_value_from_token(token)
    
    def save_matrices(self):
        """
        Save all matrices to their respective files.
        
        Returns:
            bool: True if all saves were successful, False otherwise.
        """
        logger.debug("Saving all matrices")
        success = True
        for matrix_type, matrix_data in self.matrices.items():
            if not self.matrix_loader.save_matrix(matrix_type, matrix_data):
                success = False
        return success
