"""
Semantic Analyzer module for the pAI_Lang compiler with debug logging.

This module provides functionality for analyzing parsed input and mapping
it to pAI_Lang tokens and relationships.
"""

import os
import json
import re
from .semantic_analyzer.token_id_generator import TokenIDGenerator
from ..utils.debug_logger import logger

class SemanticAnalyzer:
    """
    Analyzes parsed input and maps it to pAI_Lang tokens and relationships.
    """
    
    def __init__(self, token_registry_path=None):
        """
        Initialize the semantic analyzer.
        
        Args:
            token_registry_path (str, optional): Path to token registry file.
        """
        logger.debug("Initializing SemanticAnalyzer")
        self.token_id_generator = TokenIDGenerator()
        
        # Initialize token registry
        self.token_registry = {}
        
        # Load token registry if provided
        if token_registry_path and os.path.exists(token_registry_path):
            self._load_token_registry(token_registry_path)
        else:
            # Initialize with default tokens
            self._initialize_default_tokens()
        
        logger.debug(f"Token registry initialized with {len(self.token_registry)} tokens")
    
    def analyze(self, parsed_input):
        """
        Analyze parsed input and map to pAI_Lang tokens and relationships.
        
        Args:
            parsed_input (dict): Parsed input from parser.
            
        Returns:
            dict: Semantic analysis with token mappings and relationships.
        """
        logger.debug(f"Analyzing parsed input: {parsed_input}")
        
        input_type = parsed_input.get("type", "NL")
        content = parsed_input.get("content", {})
        
        if input_type == "NL":
            return self._analyze_nl(content)
        elif input_type == "CL":
            return self._analyze_cl(content)
        else:
            logger.warning(f"Unknown input type: {input_type}")
            return {"token_mappings": {}, "operator_mappings": {}, "semantic_structure": {}}
    
    def _analyze_nl(self, nl_content):
        """
        Analyze Natural Language content.
        
        Args:
            nl_content (dict): Parsed NL content.
            
        Returns:
            dict: Semantic analysis.
        """
        logger.debug("Analyzing NL content")
        
        # Extract intents, entities, and relationships
        intents = nl_content.get("intents", [])
        entities = nl_content.get("entities", {})
        relationships = nl_content.get("relationships", [])
        
        logger.debug(f"Intents: {intents}")
        logger.debug(f"Entities: {entities}")
        logger.debug(f"Relationships: {relationships}")
        
        # Map intents and entities to tokens
        token_mappings = {}
        
        # Process system initialization intents
        for intent in intents:
            if intent.get("category") == "system_initialization":
                system_type = "main"  # Default
                
                # Extract system type from groups if available
                groups = intent.get("groups", [])
                if groups and len(groups) > 0:
                    system_type = groups[0]
                
                # Generate token ID for system initialization
                token_id = self.get_token_id("initialize_system", "system")
                
                # Add to token mappings
                token_mappings[f"intent_{len(token_mappings)}"] = {
                    "id": f"intent_{len(token_mappings)}",
                    "source": intent.get("match"),
                    "token": token_id,
                    "category": "system",
                    "value": "initialize_system",
                    "type": "token"  # Add type for structure synthesizer
                }
                
                # If system type is specified, add it as a parameter
                if system_type:
                    # Generate token ID for system type
                    system_token_id = self.get_token_id(system_type, "system_type")
                    
                    # Add to token mappings
                    token_mappings[f"param_{len(token_mappings)}"] = {
                        "id": f"param_{len(token_mappings)}",
                        "source": system_type,
                        "token": system_token_id,
                        "category": "system_type",
                        "value": system_type,
                        "type": "token"  # Add type for structure synthesizer
                    }
        
        # Process context configuration intents
        for intent in intents:
            if intent.get("category") == "context_configuration":
                context_type = "default"  # Default
                
                # Extract context type from groups if available
                groups = intent.get("groups", [])
                if groups and len(groups) > 0:
                    context_type = groups[0]
                
                # Generate token ID for context configuration
                token_id = self.get_token_id("set_context", "context")
                
                # Add to token mappings
                token_mappings[f"intent_{len(token_mappings)}"] = {
                    "id": f"intent_{len(token_mappings)}",
                    "source": intent.get("match"),
                    "token": token_id,
                    "category": "context",
                    "value": "set_context",
                    "type": "token"  # Add type for structure synthesizer
                }
                
                # If context type is specified, add it as a parameter
                if context_type:
                    # Generate token ID for context type
                    context_token_id = self.get_token_id(context_type, "context_parameter")
                    
                    # Add to token mappings
                    token_mappings[f"param_{len(token_mappings)}"] = {
                        "id": f"param_{len(token_mappings)}",
                        "source": context_type,
                        "token": context_token_id,
                        "category": "context_parameter",
                        "value": context_type,
                        "type": "token"  # Add type for structure synthesizer
                    }
        
        # Process entities
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                entity_value = entity.get("value", "")
                
                if entity_value:
                    # Generate token ID for entity
                    token_id = self.get_token_id(entity_value, entity_type)
                    
                    # Add to token mappings
                    token_mappings[f"entity_{len(token_mappings)}"] = {
                        "id": f"entity_{len(token_mappings)}",
                        "source": entity.get("match"),
                        "token": token_id,
                        "category": entity_type,
                        "value": entity_value,
                        "type": "token"  # Add type for structure synthesizer
                    }
        
        # Map relationships to operators
        operator_mappings = {}
        
        # Process relationships
        for relationship in relationships:
            rel_type = relationship.get("type")
            
            if rel_type == "sequence":
                operator_mappings[f"rel_{len(operator_mappings)}"] = {
                    "id": f"rel_{len(operator_mappings)}",
                    "type": "binary",
                    "operator": ">",
                    "source": relationship.get("source"),
                    "target": relationship.get("target")
                }
            
            elif rel_type == "parallel":
                operator_mappings[f"rel_{len(operator_mappings)}"] = {
                    "id": f"rel_{len(operator_mappings)}",
                    "type": "binary",
                    "operator": "&",
                    "expressions": relationship.get("expressions", [])
                }
            
            elif rel_type == "conditional":
                operator_mappings[f"rel_{len(operator_mappings)}"] = {
                    "id": f"rel_{len(operator_mappings)}",
                    "type": "conditional",
                    "operator": "?:",
                    "condition": relationship.get("condition"),
                    "trueBranch": relationship.get("trueBranch"),
                    "falseBranch": relationship.get("falseBranch", None)
                }
            
            elif rel_type == "repetition":
                operator_mappings[f"rel_{len(operator_mappings)}"] = {
                    "id": f"rel_{len(operator_mappings)}",
                    "type": "repetition",
                    "operator": "**",
                    "expression": relationship.get("expression"),
                    "count": relationship.get("count", 1)
                }
        
        # If no relationships were found but we have tokens, create a default sequence
        if not operator_mappings and len(token_mappings) >= 2:
            # Find tokens for system initialization and context setting
            system_tokens = [t for t in token_mappings.values() if t.get("value") == "initialize_system"]
            context_tokens = [t for t in token_mappings.values() if t.get("value") == "set_context"]
            
            if system_tokens and context_tokens:
                operator_mappings["rel_default"] = {
                    "id": "rel_default",
                    "type": "binary",
                    "operator": ">",
                    "source": system_tokens[0].get("source"),
                    "target": context_tokens[0].get("source")
                }
        
        # If we still don't have any relationships but have tokens, create a simple token list
        if not operator_mappings and token_mappings:
            # Create a simple list of tokens for the structure synthesizer
            elements = []
            for token in token_mappings.values():
                elements.append({"type": "token", "value": token.get("token", "")})
            
            # Create semantic structure with elements
            semantic_structure = {
                "tokens": list(token_mappings.values()),
                "operators": list(operator_mappings.values()),
                "relationships": list(operator_mappings.values()),
                "elements": elements  # Add elements for direct use by structure synthesizer
            }
        else:
            # Create semantic structure
            semantic_structure = {
                "tokens": list(token_mappings.values()),
                "operators": list(operator_mappings.values()),
                "relationships": list(operator_mappings.values())
            }
        
        # Create and return semantic analysis
        semantic_analysis = {
            "token_mappings": token_mappings,
            "operator_mappings": operator_mappings,
            "semantic_structure": semantic_structure
        }
        
        logger.debug(f"NL semantic analysis: {semantic_analysis}")
        return semantic_analysis
    
    def _analyze_cl(self, cl_content):
        """
        Analyze Command Language content.
        
        Args:
            cl_content (dict): Parsed CL content.
            
        Returns:
            dict: Semantic analysis.
        """
        logger.debug("Analyzing CL content")
        
        # Extract commands and parameters
        commands = cl_content.get("commands", [])
        
        logger.debug(f"Commands: {commands}")
        
        # Map commands to tokens
        token_mappings = {}
        
        # Process commands
        for i, command in enumerate(commands):
            command_name = command.get("command", "")
            parameters = command.get("parameters", {})
            
            # Generate token ID for command
            token_id = self.get_token_id(command_name.lower(), "command")
            
            # Add to token mappings
            token_mappings[f"cmd_{i}"] = {
                "id": f"cmd_{i}",
                "source": command.get("original", ""),
                "token": token_id,
                "category": "command",
                "value": command_name.lower(),
                "type": "token"  # Add type for structure synthesizer
            }
            
            # Process parameters
            for param_name, param_value in parameters.items():
                # Generate token ID for parameter
                param_token_id = self.get_token_id(param_value, param_name.lower())
                
                # Add to token mappings
                token_mappings[f"param_{len(token_mappings)}"] = {
                    "id": f"param_{len(token_mappings)}",
                    "source": f"{param_name}={param_value}",
                    "token": param_token_id,
                    "category": param_name.lower(),
                    "value": param_value,
                    "type": "token"  # Add type for structure synthesizer
                }
        
        # Map command sequence to operators
        operator_mappings = {}
        
        # Create sequence relationships between commands
        for i in range(len(commands) - 1):
            operator_mappings[f"seq_{i}"] = {
                "id": f"seq_{i}",
                "type": "binary",
                "operator": ">",
                "source": commands[i].get("original", ""),
                "target": commands[i + 1].get("original", "")
            }
        
        # If we don't have any relationships but have tokens, create a simple token list
        if not operator_mappings and token_mappings:
            # Create a simple list of tokens for the structure synthesizer
            elements = []
            for token in token_mappings.values():
                elements.append({"type": "token", "value": token.get("token", "")})
            
            # Create semantic structure with elements
            semantic_structure = {
                "tokens": list(token_mappings.values()),
                "operators": list(operator_mappings.values()),
                "relationships": list(operator_mappings.values()),
                "elements": elements  # Add elements for direct use by structure synthesizer
            }
        else:
            # Create semantic structure
            semantic_structure = {
                "tokens": list(token_mappings.values()),
                "operators": list(operator_mappings.values()),
                "relationships": list(operator_mappings.values())
            }
        
        # Create and return semantic analysis
        semantic_analysis = {
            "token_mappings": token_mappings,
            "operator_mappings": operator_mappings,
            "semantic_structure": semantic_structure
        }
        
        logger.debug(f"CL semantic analysis: {semantic_analysis}")
        return semantic_analysis
    
    def get_token_id(self, value, category):
        """
        Get a token ID for a value in a specific category.
        
        Args:
            value (str): The value to get a token ID for.
            category (str): The category of the token.
            
        Returns:
            str: The token ID.
        """
        # Check if token already exists in registry
        for token_id, token_info in self.token_registry.items():
            if token_info.get("value") == value and token_info.get("category") == category:
                return token_id
        
        # Generate new token ID
        token_id = self.token_id_generator.generate_token_id(value, category)
        
        # Register the new token
        self.register_token(value, category, token_id)
        
        return token_id
    
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
        # Check if token ID already exists
        if token_id in self.token_registry:
            return False
        
        # Register the token
        self.token_registry[token_id] = {
            "value": value,
            "category": category
        }
        
        return True
    
    def get_value_from_token(self, token):
        """
        Get the value associated with a token ID.
        
        Args:
            token (str): The token ID to look up.
            
        Returns:
            tuple: (value, category) if found, (None, None) otherwise.
        """
        if token in self.token_registry:
            token_info = self.token_registry[token]
            return token_info.get("value"), token_info.get("category")
        
        return None, None
    
    def _load_token_registry(self, token_registry_path):
        """
        Load token registry from file.
        
        Args:
            token_registry_path (str): Path to token registry file.
        """
        try:
            with open(token_registry_path, 'r') as f:
                self.token_registry = json.load(f)
        except Exception as e:
            logger.error(f"Error loading token registry: {e}")
            self._initialize_default_tokens()
    
    def _initialize_default_tokens(self):
        """
        Initialize default tokens.
        """
        # System tokens
        self.register_token("initialize_system", "system", "S001")
        self.register_token("shutdown_system", "system", "S002")
        self.register_token("restart_system", "system", "S003")
        
        # Context tokens
        self.register_token("set_context", "context", "C001")
        self.register_token("clear_context", "context", "C002")
        self.register_token("save_context", "context", "C003")
        
        # Task tokens
        self.register_token("execute_task", "task", "T001")
        self.register_token("cancel_task", "task", "T002")
        self.register_token("pause_task", "task", "T003")
        
        # Parameter tokens
        self.register_token("production", "context_parameter", "P001")
        self.register_token("development", "context_parameter", "P002")
        self.register_token("testing", "context_parameter", "P003")
        
        # System type tokens
        self.register_token("main", "system_type", "S101")
        self.register_token("backup", "system_type", "S102")
        self.register_token("auxiliary", "system_type", "S103")
        
        # Command tokens
        self.register_token("initialize", "command", "CMD001")
        self.register_token("set_context", "command", "CMD002")
        self.register_token("execute", "command", "CMD003")
