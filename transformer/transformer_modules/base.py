"""
Base Transformer module for the pAI_Lang transformer component.

This module provides the base class for all specialized transformer modules.
"""

from ...utils.debug_logger import logger

class BaseTransformer:
    """
    Base class for all transformer modules.
    
    Provides common functionality and interface for specialized transformers.
    """
    
    def __init__(self, matrix_data):
        """
        Initialize the base transformer with matrix data.
        
        Args:
            matrix_data (dict): Matrix data for the specific transformation direction.
        """
        self.matrix = matrix_data
        logger.debug(f"Initialized {self.__class__.__name__} with matrix data")
    
    def transform(self, input_text):
        """
        Transform input text according to the transformation rules.
        
        Args:
            input_text (str): Input text to transform.
            
        Returns:
            str: Transformed text.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement transform() method")
    
    def update_matrix(self, new_matrix):
        """
        Update the transformation matrix.
        
        Args:
            new_matrix (dict): New matrix data.
            
        Returns:
            bool: True if update was successful, False otherwise.
        """
        try:
            self.matrix = new_matrix
            logger.debug(f"Updated matrix for {self.__class__.__name__}")
            return True
        except Exception as e:
            logger.error(f"Error updating matrix for {self.__class__.__name__}: {e}")
            return False
    
    def _validate_input(self, input_text):
        """
        Validate input text before transformation.
        
        Args:
            input_text (str): Input text to validate.
            
        Returns:
            bool: True if input is valid, False otherwise.
        """
        if not isinstance(input_text, str):
            logger.error(f"Invalid input type: {type(input_text)}. Expected str.")
            return False
        
        if not input_text.strip():
            logger.warning("Empty input text")
            return False
        
        return True
    
    def _handle_error(self, error_message, input_text=None):
        """
        Handle transformation errors.
        
        Args:
            error_message (str): Error message.
            input_text (str, optional): Input text that caused the error.
            
        Returns:
            str: Error message formatted for output.
        """
        if input_text:
            logger.error(f"{error_message} for input: {input_text}")
        else:
            logger.error(error_message)
        
        return f"ERROR: {error_message}"
