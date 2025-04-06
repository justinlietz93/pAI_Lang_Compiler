"""
Updated Mapping Utilities module for the Semantic Analyzer component.

This module provides utility functions for mapping operations between
different language representations and pAI_Lang concepts.
"""

from pailang_tooling.compiler.semantic_analyzer.token_id_generator import TokenIDGenerator

class MappingUtils:
    """
    Utility functions for mapping operations.
    """
    
    def __init__(self, token_dictionary=None, token_registry_path=None):
        """
        Initialize the mapping utilities.
        
        Args:
            token_dictionary (dict, optional): Dictionary of token definitions.
            token_registry_path (str, optional): Path to token registry file.
        """
        self.token_dictionary = token_dictionary or {}
        self.category_mappings = self._initialize_category_mappings()
        self.token_id_generator = TokenIDGenerator(token_registry_path)
    
    def _initialize_category_mappings(self):
        """
        Initialize mappings from intent categories to pAI_Lang categories.
        
        Returns:
            dict: Category mappings.
        """
        return {
            "system_initialization": "system",
            "context_configuration": "context",
            "task_execution": "task",
            "conditional_logic": "condition",
            "parallel_execution": "action",
            "sequential_execution": "action",
            "repetition": "action",
            "resource_allocation": "resource",
            "security_operations": "system",
            "query_execution": "query",
            "batch_operations": "batch"
        }
    
    def map_intents_to_categories(self, intents):
        """
        Map intents to pAI_Lang categories.
        
        Args:
            intents (list): Recognized intents.
            
        Returns:
            dict: Mappings from intents to categories.
        """
        category_mappings = {}
        
        for intent in intents:
            category = intent.get("category")
            if category in self.category_mappings:
                pailang_category = self.category_mappings[category]
                
                # Store mapping
                category_mappings[intent["match"]] = {
                    "category": pailang_category,
                    "original_intent": intent
                }
        
        return category_mappings
    
    def map_entities_to_tokens(self, entities, category_mappings):
        """
        Map entities to pAI_Lang tokens.
        
        Args:
            entities (dict): Extracted entities.
            category_mappings (dict): Mappings from intents to categories.
            
        Returns:
            dict: Mappings from entities to tokens.
        """
        token_mappings = {}
        
        # Process each entity type
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                # Determine category based on entity type
                category = self._get_category_for_entity_type(entity_type)
                
                # Generate token ID using the token ID generator
                token = self.token_id_generator.generate_token_id(entity.get("value", ""), category)
                
                # Extract category prefix and ID
                category_prefix = token[0]
                token_id = token[1:]
                
                # Create token mapping
                token_mappings[entity["match"]] = {
                    "token": token,
                    "category": category,
                    "id": token_id,
                    "original_entity": entity,
                    "pailang_token": token  # For compatibility with existing code
                }
        
        return token_mappings
    
    def _get_category_for_entity_type(self, entity_type):
        """
        Get pAI_Lang category for entity type.
        
        Args:
            entity_type (str): Entity type.
            
        Returns:
            str: pAI_Lang category.
        """
        # Map entity types to categories
        entity_type_map = {
            "system_type": "system",
            "context_parameter": "context",
            "task_name": "task",
            "resource_identifier": "resource",
            "condition": "condition",
            "action": "action",
            "quantifier": "action"
        }
        
        return entity_type_map.get(entity_type, "directive")
    
    def map_relationships_to_operators(self, relationships):
        """
        Map relationships to pAI_Lang operators.
        
        Args:
            relationships (list): Extracted relationships.
            
        Returns:
            dict: Mappings from relationships to operators.
        """
        operator_mappings = {}
        
        for relationship in relationships:
            rel_type = relationship.get("type")
            
            # Map relationship types to operators
            if rel_type == "sequence":
                operator = ">"
            elif rel_type == "parallel":
                operator = "&"
            elif rel_type == "conditional":
                operator = "?:"
            elif rel_type == "repetition":
                operator = "**"
            else:
                operator = ">"  # Default to sequence
            
            # Store mapping
            operator_mappings[relationship["type"]] = {
                "operator": operator,
                "original_relationship": relationship
            }
        
        return operator_mappings
    
    def map_commands_to_tokens(self, commands):
        """
        Map Command Language commands to pAI_Lang tokens.
        
        Args:
            commands (list): Parsed commands.
            
        Returns:
            dict: Mappings from commands to tokens.
        """
        token_mappings = {}
        
        for command in commands:
            command_name = command.get("name", "")
            
            # Determine category based on command name
            category = self._get_category_for_command(command_name)
            
            # Extract key parameter value
            param_key = self._get_key_param_for_category(category)
            param_value = command.get("parameters", {}).get(param_key, "")
            
            # Generate token using the token ID generator
            token = self.token_id_generator.generate_token_id(param_value, category)
            
            # Extract category prefix and ID
            category_prefix = token[0]
            token_id = token[1:]
            
            # Create token mapping
            token_mappings[command["line"]] = {
                "token": token,
                "category": category,
                "id": token_id,
                "original_command": command,
                "pailang_token": token  # For compatibility with existing code
            }
        
        return token_mappings
    
    def _get_category_for_command(self, command_name):
        """
        Get pAI_Lang category for command name.
        
        Args:
            command_name (str): Command name.
            
        Returns:
            str: pAI_Lang category.
        """
        # Map command names to categories
        command_map = {
            "INITIALIZE": "system",
            "SET_CONTEXT": "context",
            "EXECUTE": "task",
            "EXECUTE_TASK": "task",
            "CONDITIONAL": "condition",
            "PARALLEL": "action",
            "REPEAT": "action",
            "BATCH_OPERATION": "batch",
            "ACTIVATE_CONTEXT": "context",
            "ALLOCATE_RESOURCE": "resource",
            "APPLY_SECURITY": "system",
            "EXECUTE_QUERY": "query"
        }
        
        return command_map.get(command_name, "directive")
    
    def _get_key_param_for_category(self, category):
        """
        Get key parameter name for category.
        
        Args:
            category (str): pAI_Lang category.
            
        Returns:
            str: Key parameter name.
        """
        # Map categories to key parameter names
        category_param_map = {
            "system": "SYSTEM",
            "context": "CONTEXT",
            "task": "TASK",
            "condition": "CONDITION",
            "action": "PROCESS",
            "resource": "RESOURCE",
            "query": "QUERY",
            "batch": "BATCH"
        }
        
        return category_param_map.get(category, "ID")
    
    def map_hierarchy_to_operators(self, hierarchy):
        """
        Map command hierarchy to pAI_Lang operators.
        
        Args:
            hierarchy (list): Command hierarchy.
            
        Returns:
            dict: Mappings from hierarchy to operators.
        """
        operator_mappings = {}
        
        # Process each command in hierarchy
        for command_node in hierarchy:
            self._process_command_node(command_node, operator_mappings)
        
        return operator_mappings
    
    def _process_command_node(self, command_node, operator_mappings, parent=None):
        """
        Process a command node in the hierarchy.
        
        Args:
            command_node (dict): Command node.
            operator_mappings (dict): Operator mappings to update.
            parent (dict, optional): Parent command node.
        """
        command_name = command_node.get("name", "")
        children = command_node.get("children", [])
        
        # Map command type to operator
        if command_name == "CONDITIONAL":
            # Conditional operator
            operator_mappings[command_node["line"]] = {
                "operator": "?:",
                "type": "conditional",
                "original_command": command_node
            }
        elif command_name == "PARALLEL":
            # Parallel operator
            operator_mappings[command_node["line"]] = {
                "operator": "&",
                "type": "parallel",
                "original_command": command_node
            }
        elif command_name == "REPEAT":
            # Repetition operator
            count = command_node.get("parameters", {}).get("count", "1")
            operator_mappings[command_node["line"]] = {
                "operator": "**",
                "type": "repetition",
                "count": count,
                "original_command": command_node
            }
        elif parent and children:
            # Sequence operator (parent with children)
            operator_mappings[command_node["line"]] = {
                "operator": ">",
                "type": "sequence",
                "original_command": command_node
            }
        
        # Process children recursively
        for child in children:
            self._process_command_node(child, operator_mappings, command_node)
