"""
Token ID Generator module for the Semantic Analyzer component.

This module provides a robust implementation for generating and managing
token IDs across different categories in the pAI_Lang system.
"""

import hashlib
import re
import os
import json
from pathlib import Path
import uuid
from pailang_tooling.utils.debug_logger import logger

class TokenIDGenerator:
    """
    Generates and manages consistent token IDs for pAI_Lang tokens.
    """
    
    def __init__(self, token_registry_path=None):
        """
        Initialize the token ID generator.
        
        Args:
            token_registry_path (str, optional): Path to token registry file.
                If None, a default in-memory registry will be used.
        """
        logger.debug("Initializing TokenIDGenerator")
        self.token_registry_path = token_registry_path
        self.token_registry = self._load_token_registry()
        
        # Define category prefixes according to the formal specification
        self.category_prefixes = {
            "system": "S",
            "context": "C",
            "task": "T",
            "condition": "L",
            "action": "P",
            "resource": "R",
            "query": "Q",
            "batch": "B",
            "directive": "D",
            "memory": "M",
            "network": "N",
            "handler": "H",
            "security": "S"
        }
        
        # Initialize category counters for deterministic ID assignment
        self.category_counters = {category: 1 for category in self.category_prefixes.keys()}
        
        # Load existing counters from registry
        self._initialize_category_counters()
        
        logger.debug(f"TokenIDGenerator initialized with {len(self.token_registry)} registered tokens")
    
    def generate_token_id(self, value, category):
        """
        Generate a consistent token ID for a value in a specific category.
        
        Args:
            value (str): The value to generate a token ID for.
            category (str): The category of the token.
            
        Returns:
            str: The generated token ID.
        """
        logger.debug(f"Generating token ID for value '{value}' in category '{category}'")
        
        # Normalize value and category
        normalized_value = self._normalize_value(value)
        normalized_category = category.lower()
        
        # Get category prefix
        prefix = self.category_prefixes.get(normalized_category, "D")  # Default to Directive
        
        # Check if token already exists in registry
        if normalized_category in self.token_registry and normalized_value in self.token_registry[normalized_category]:
            token_id = self.token_registry[normalized_category][normalized_value]
            logger.debug(f"Found existing token ID: {prefix}{token_id}")
            return f"{prefix}{token_id}"
        
        # Generate new token ID
        token_id = self._generate_new_token_id(normalized_value, normalized_category)
        
        # Store in registry
        if normalized_category not in self.token_registry:
            self.token_registry[normalized_category] = {}
        
        self.token_registry[normalized_category][normalized_value] = token_id
        
        # Update category counter
        if normalized_category in self.category_counters:
            self.category_counters[normalized_category] = max(
                self.category_counters[normalized_category],
                int(token_id) + 1
            )
        
        # Save registry if path is provided
        if self.token_registry_path:
            self._save_token_registry()
        
        logger.debug(f"Generated new token ID: {prefix}{token_id}")
        return f"{prefix}{token_id}"
    
    def get_token_id(self, value, category):
        """
        Get an existing token ID or generate a new one if it doesn't exist.
        
        Args:
            value (str): The value to get a token ID for.
            category (str): The category of the token.
            
        Returns:
            str: The token ID.
        """
        return self.generate_token_id(value, category)
    
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
        logger.debug(f"Registering token ID '{token_id}' for value '{value}' in category '{category}'")
        
        # Normalize value and category
        normalized_value = self._normalize_value(value)
        normalized_category = category.lower()
        
        # Remove prefix if present
        if token_id and len(token_id) > 1 and token_id[0] in self.category_prefixes.values():
            token_id = token_id[1:]
        
        # Store in registry
        if normalized_category not in self.token_registry:
            self.token_registry[normalized_category] = {}
        
        self.token_registry[normalized_category][normalized_value] = token_id
        
        # Update category counter if needed
        if normalized_category in self.category_counters and token_id.isdigit():
            self.category_counters[normalized_category] = max(
                self.category_counters[normalized_category],
                int(token_id) + 1
            )
        
        # Save registry if path is provided
        if self.token_registry_path:
            self._save_token_registry()
        
        logger.debug(f"Token registered successfully")
        return True
    
    def get_value_from_token(self, token):
        """
        Get the value associated with a token ID.
        
        Args:
            token (str): The token ID to look up.
            
        Returns:
            tuple: (value, category) if found, (None, None) otherwise.
        """
        logger.debug(f"Looking up value for token '{token}'")
        
        # Extract prefix and ID
        if not token or len(token) < 2:
            logger.warning(f"Invalid token format: {token}")
            return None, None
        
        prefix = token[0]
        token_id = token[1:]
        
        # Find category from prefix
        category = None
        for cat, pre in self.category_prefixes.items():
            if pre == prefix:
                category = cat
                break
        
        if not category:
            logger.warning(f"Unknown category prefix: {prefix}")
            return None, None
        
        # Look up value in registry
        if category in self.token_registry:
            for value, tid in self.token_registry[category].items():
                if tid == token_id:
                    logger.debug(f"Found value '{value}' for token '{token}'")
                    return value, category
        
        logger.warning(f"No value found for token '{token}'")
        return None, None
    
    def _normalize_value(self, value):
        """
        Normalize a value for consistent token ID generation.
        
        Args:
            value (str): The value to normalize.
            
        Returns:
            str: The normalized value.
        """
        if not value:
            return ""
        
        # Convert to lowercase
        normalized = str(value).lower()
        
        # Remove special characters
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        # Replace whitespace with underscore
        normalized = re.sub(r'\s+', '_', normalized)
        
        return normalized
    
    def _generate_new_token_id(self, value, category):
        """
        Generate a new token ID for a value in a specific category.
        
        Args:
            value (str): The normalized value.
            category (str): The normalized category.
            
        Returns:
            str: The generated token ID.
        """
        # Use a combination of semantic hashing and category-specific counters
        # to ensure both determinism and uniqueness
        
        # Get next available ID in category
        next_id = self.category_counters.get(category, 1)
        
        # For deterministic generation based on value content
        if value:
            # Create a semantic hash of the value
            # Use SHA-256 for better distribution than MD5
            hash_obj = hashlib.sha256(value.encode())
            hash_hex = hash_obj.hexdigest()
            
            # Use first 8 digits of hash as a seed
            seed = int(hash_hex[:8], 16)
            
            # Combine with category-specific counter for uniqueness
            category_counter = self.category_counters.get(category, 1)
            
            # Generate ID between 1 and 99
            token_id = ((seed + category_counter) % 99) + 1
            
            # Check for collisions
            while category in self.token_registry and any(tid == str(token_id).zfill(2) for tid in self.token_registry[category].values()):
                token_id = (token_id % 99) + 1
                
                # If we've cycled through all possible IDs, use UUID fallback
                if token_id == ((seed + category_counter) % 99) + 1:
                    # Generate a UUID and use last 2 digits
                    uuid_str = str(uuid.uuid4()).replace('-', '')
                    token_id = int(uuid_str[-2:], 16) % 99 + 1
        else:
            token_id = next_id
        
        # Update category counter
        self.category_counters[category] = max(next_id, token_id) + 1
        
        # Format as 2-digit number
        return f"{token_id:02d}"
    
    def _load_token_registry(self):
        """
        Load token registry from file or initialize empty registry.
        
        Returns:
            dict: The loaded token registry.
        """
        if self.token_registry_path and os.path.exists(self.token_registry_path):
            try:
                with open(self.token_registry_path, 'r') as f:
                    logger.debug(f"Loading token registry from {self.token_registry_path}")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading token registry: {e}")
        
        # Initialize empty registry with all categories
        logger.debug("Initializing empty token registry")
        return {category: {} for category in self.category_prefixes.keys()}
    
    def _save_token_registry(self):
        """
        Save token registry to file.
        
        Returns:
            bool: True if save was successful, False otherwise.
        """
        if not self.token_registry_path:
            return False
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.token_registry_path), exist_ok=True)
            
            with open(self.token_registry_path, 'w') as f:
                logger.debug(f"Saving token registry to {self.token_registry_path}")
                json.dump(self.token_registry, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving token registry: {e}")
            return False
    
    def _initialize_category_counters(self):
        """
        Initialize category counters based on existing registry entries.
        """
        for category, tokens in self.token_registry.items():
            if category in self.category_counters:
                # Find the highest token ID in this category
                max_id = 0
                for token_id in tokens.values():
                    if isinstance(token_id, str) and token_id.isdigit():
                        max_id = max(max_id, int(token_id))
                
                # Set counter to one more than the highest ID
                self.category_counters[category] = max_id + 1
                logger.debug(f"Initialized counter for category '{category}' to {self.category_counters[category]}")
