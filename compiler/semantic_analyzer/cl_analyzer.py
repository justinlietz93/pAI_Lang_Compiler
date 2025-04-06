"""
Command Language Analyzer module for the Semantic Analyzer component.

This module provides functionality for analyzing the semantic meaning of parsed
Command Language (CL) inputs and mapping them to pAI_Lang concepts.
"""

class CLAnalyzer:
    """
    Analyzes the semantic meaning of parsed Command Language inputs.
    """
    
    def __init__(self, mapping_utils):
        """
        Initialize the CL analyzer.
        
        Args:
            mapping_utils (MappingUtils): Utility functions for mapping operations.
        """
        self.mapping_utils = mapping_utils
    
    def analyze_cl(self, cl_content):
        """
        Analyze Command Language content.
        
        Args:
            cl_content (dict): Parsed CL content.
            
        Returns:
            dict: Semantic analysis with pAI_Lang mappings.
        """
        # Extract commands and hierarchy
        commands = cl_content.get("commands", [])
        hierarchy = cl_content.get("hierarchy", [])
        
        # Map commands to pAI_Lang tokens
        token_mappings = self.mapping_utils.map_commands_to_tokens(commands)
        
        # Map command hierarchy to pAI_Lang operators
        operator_mappings = self.mapping_utils.map_hierarchy_to_operators(hierarchy)
        
        # Build semantic structure
        semantic_structure = self.build_cl_semantic_structure(
            token_mappings, operator_mappings, hierarchy
        )
        
        return {
            "token_mappings": token_mappings,
            "operator_mappings": operator_mappings,
            "semantic_structure": semantic_structure,
            "original_content": cl_content
        }
    
    def build_cl_semantic_structure(self, token_mappings, operator_mappings, hierarchy):
        """
        Build semantic structure from Command Language mappings.
        
        Args:
            token_mappings (dict): Mappings from commands to tokens.
            operator_mappings (dict): Mappings from hierarchy to operators.
            hierarchy (list): Command hierarchy.
            
        Returns:
            dict: Semantic structure.
        """
        # Start with empty structure
        structure = {
            "type": "Expression",
            "tokens": [],
            "operators": [],
            "relationships": []
        }
        
        # Add tokens
        for command_line, token_info in token_mappings.items():
            structure["tokens"].append({
                "token": token_info["token"],
                "category": token_info["category"],
                "id": token_info["id"],
                "source": command_line
            })
        
        # Add operators
        for command_line, operator_info in operator_mappings.items():
            structure["operators"].append({
                "operator": operator_info["operator"],
                "type": operator_info["type"],
                "source": command_line
            })
        
        # Build relationships from hierarchy
        structure["relationships"] = self.build_relationships_from_hierarchy(hierarchy, token_mappings)
        
        return structure
    
    def build_relationships_from_hierarchy(self, hierarchy, token_mappings):
        """
        Build relationships from command hierarchy.
        
        Args:
            hierarchy (list): Command hierarchy.
            token_mappings (dict): Mappings from commands to tokens.
            
        Returns:
            list: Relationships.
        """
        relationships = []
        
        # Process each command in hierarchy
        for command_node in hierarchy:
            self.process_relationships(command_node, relationships, token_mappings)
        
        return relationships
    
    def process_relationships(self, command_node, relationships, token_mappings):
        """
        Process relationships for a command node.
        
        Args:
            command_node (dict): Command node.
            relationships (list): Relationships to update.
            token_mappings (dict): Mappings from commands to tokens.
        """
        command_name = command_node.get("name", "")
        children = command_node.get("children", [])
        
        # Skip if no children
        if not children:
            return
        
        # Get token for this command
        command_token = token_mappings.get(command_node["line"], {}).get("token")
        
        # Get tokens for children
        child_tokens = []
        for child in children:
            child_token = token_mappings.get(child["line"], {}).get("token")
            if child_token:
                child_tokens.append({
                    "token": child_token,
                    "node": child
                })
        
        # Create relationship based on command type
        if command_name == "CONDITIONAL" and len(child_tokens) >= 1:
            # Conditional relationship
            relationship = {
                "type": "conditional",
                "operator": "?:",
                "condition": command_token,
                "trueBranch": child_tokens[0]["token"]
            }
            
            # Add false branch if present
            if len(child_tokens) >= 2:
                relationship["falseBranch"] = child_tokens[1]["token"]
            
            relationships.append(relationship)
        
        elif command_name == "PARALLEL" and child_tokens:
            # Parallel relationship
            relationship = {
                "type": "parallel",
                "operator": "&",
                "expressions": [token_info["token"] for token_info in child_tokens]
            }
            
            relationships.append(relationship)
        
        elif command_name == "REPEAT" and child_tokens:
            # Repetition relationship
            count = command_node.get("parameters", {}).get("count", "1")
            relationship = {
                "type": "repetition",
                "operator": "**",
                "expression": child_tokens[0]["token"],
                "count": count
            }
            
            relationships.append(relationship)
        
        elif len(child_tokens) >= 2:
            # Sequence relationship for adjacent children
            for i in range(len(child_tokens) - 1):
                relationship = {
                    "type": "sequence",
                    "operator": ">",
                    "source": child_tokens[i]["token"],
                    "target": child_tokens[i + 1]["token"]
                }
                
                relationships.append(relationship)
        
        # Process children recursively
        for child in children:
            self.process_relationships(child, relationships, token_mappings)
