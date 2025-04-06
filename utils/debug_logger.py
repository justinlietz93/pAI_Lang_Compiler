"""
Debug Logger utility for pAI_Lang tooling.

This module provides a centralized logging facility for all components
of the pAI_Lang tooling system, with configurable log levels and output destinations.
"""

import logging
import os
import sys
from pathlib import Path

class DebugLogger:
    """
    Debug logger for pAI_Lang tooling with configurable log levels and output destinations.
    
    Provides a singleton logger instance that can be used across all components
    of the pAI_Lang tooling system.
    """
    
    _instance = None
    
    def __new__(cls, log_level=logging.INFO, log_file=None):
        """
        Create a new DebugLogger instance or return the existing one (singleton pattern).
        
        Args:
            log_level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
            log_file (str, optional): Path to log file. If None, logs to console only.
            
        Returns:
            DebugLogger: Singleton logger instance.
        """
        if cls._instance is None:
            cls._instance = super(DebugLogger, cls).__new__(cls)
            cls._instance._initialize(log_level, log_file)
        return cls._instance
    
    def _initialize(self, log_level, log_file):
        """
        Initialize the logger with the specified log level and output destinations.
        
        Args:
            log_level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
            log_file (str, optional): Path to log file. If None, logs to console only.
        """
        # Create logger
        self.logger = logging.getLogger('pailang_tooling')
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add console handler to logger
        self.logger.addHandler(console_handler)
        
        # Add file handler if log file is specified
        if log_file:
            # Create directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            
            # Add file handler to logger
            self.logger.addHandler(file_handler)
        
        # Store configuration
        self.log_level = log_level
        self.log_file = log_file
    
    def set_level(self, log_level):
        """
        Set the logging level.
        
        Args:
            log_level (int): New logging level (e.g., logging.DEBUG, logging.INFO).
        """
        self.logger.setLevel(log_level)
        for handler in self.logger.handlers:
            handler.setLevel(log_level)
        self.log_level = log_level
    
    def debug(self, message):
        """
        Log a debug message.
        
        Args:
            message (str): Debug message to log.
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        Log an info message.
        
        Args:
            message (str): Info message to log.
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        Log a warning message.
        
        Args:
            message (str): Warning message to log.
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        Log an error message.
        
        Args:
            message (str): Error message to log.
        """
        self.logger.error(message)
    
    def critical(self, message):
        """
        Log a critical message.
        
        Args:
            message (str): Critical message to log.
        """
        self.logger.critical(message)

# Create default logger instance
logger = DebugLogger(
    log_level=logging.DEBUG if os.environ.get('PAILANG_DEBUG') else logging.INFO,
    log_file=os.environ.get('PAILANG_LOG_FILE')
).logger
