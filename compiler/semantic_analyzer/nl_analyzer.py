"""
Natural Language Analyzer module for the Semantic Analyzer component.

This module provides functionality for analyzing the semantic meaning of parsed
Natural Language (NL) inputs and mapping them to pAI_Lang concepts.
"""

class NLAnalyzer:
    """
    Analyzes the semantic meaning of parsed Natural Language inputs.
    """
    
    def __init__(self, mapping_utils):
        """
        Initialize the NL analyzer.
        
        Args:
            mapping_utils (MappingUtils): Utility functions for mapping operations.
        """
        self.mapping_utils = mapping_utils
    
    def analyze_nl(self, nl_content):
        """
        Analyze Natural Language content.
        
        Args:
            nl_content (dict): Parsed NL content.
            
        Returns:
            dict: Semantic analysis with pAI_Lang mappings.
        """
        # Extract intents, entities, and relationships
        intents = nl_content.get("intents", [])
        entities = nl_content.get("entities", {})
        relationships = nl_content.get("relationships", [])
        
        # Map intents to pAI_Lang categories
        category_mappings = self.mapping_utils.map_intents_to_categories(intents)
        
        # Map entities to pAI_Lang tokens
        token_mappings = self.mapping_utils.map_entities_to_tokens(entities, category_mappings)
        
        # Map relationships to pAI_Lang operators
        operator_mappings = self.mapping_utils.map_relationships_to_operators(relationships)
        
        # Build semantic structure
        semantic_structure = self.build_semantic_structure(
            category_mappings, token_mappings, operator_mappings
        )
        
        return {
            "category_mappings": category_mappings,
            "token_mappings": token_mappings,
            "operator_mappings": operator_mappings,
            "semantic_structure": semantic_structure,
            "original_content": nl_content
        }
    
    def build_semantic_structure(self, category_mappings, token_mappings, operator_mappings):
        """
        Build semantic structure from mappings.
        
        Args:
            category_mappings (dict): Mappings from intents to categories.
            token_mappings (dict): Mappings from entities to tokens.
            operator_mappings (dict): Mappings from relationships to operators.
            
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
        for entity_match, token_info in token_mappings.items():
            structure["tokens"].append({
                "token": token_info["token"],
                "category": token_info["category"],
                "id": token_info["id"],
                "source": entity_match
            })
        
        # Add operators
        for rel_type, operator_info in operator_mappings.items():
            structure["operators"].append({
                "operator": operator_info["operator"],
                "type": rel_type,
                "source": operator_info["original_relationship"]
            })
        
        # Add relationships
        for relationship in operator_mappings.values():
            rel = relationship["original_relationship"]
            
            if "source" in rel and "target" in rel:
                # Sequence relationship
                structure["relationships"].append({
                    "type": "binary",
                    "operator": relationship["operator"],
                    "source": rel["source"],
                    "target": rel["target"]
                })
            elif "expressions" in rel:
                # Parallel relationship
                structure["relationships"].append({
                    "type": "binary",
                    "operator": relationship["operator"],
                    "expressions": rel["expressions"]
                })
            elif "condition" in rel:
                # Conditional relationship
                conditional = {
                    "type": "conditional",
                    "operator": relationship["operator"],
                    "condition": rel["condition"],
                    "trueBranch": rel["trueBranch"]
                }
                
                if "falseBranch" in rel:
                    conditional["falseBranch"] = rel["falseBranch"]
                
                structure["relationships"].append(conditional)
            elif "expression" in rel and "count" in rel:
                # Repetition relationship
                structure["relationships"].append({
                    "type": "repetition",
                    "operator": relationship["operator"],
                    "expression": rel["expression"],
                    "count": rel["count"]
                })
        
        return structure
