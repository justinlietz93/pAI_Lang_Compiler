"""
Base TreeBuilder module.

This module provides the main TreeBuilder class that coordinates
the building of expression trees from relationships.
"""

from .node_operations import NodeOperations
from .tree_manipulation import TreeManipulation
from .utility_functions import UtilityFunctions

class TreeBuilder(NodeOperations, TreeManipulation, UtilityFunctions):
    """
    Builds expression trees from relationships.
    """
    
    def __init__(self, operator_precedence):
        """
        Initialize the tree builder.
        
        Args:
            operator_precedence (dict): Operator precedence map.
        """
        self.operator_precedence = operator_precedence
    
    def build_expression_tree(self, relationships):
        """
        Build expression tree from relationships.
        
        Args:
            relationships (list): Relationship mappings.
            
        Returns:
            dict: Expression tree.
        """
        # Sort relationships by operator precedence
        sorted_relationships = sorted(
            relationships,
            key=lambda r: self.operator_precedence.get(r.get("operator"), 0),
            reverse=True  # Higher precedence first
        )
        
        # Start with empty tree
        tree = None
        
        # Process each relationship
        for relationship in sorted_relationships:
            rel_type = relationship.get("type")
            
            if rel_type == "sequence":
                tree = self._add_sequence_to_tree(relationship, tree)
            elif rel_type == "parallel":
                tree = self._add_parallel_to_tree(relationship, tree)
            elif rel_type == "conditional":
                tree = self._add_conditional_to_tree(relationship, tree)
            elif rel_type == "repetition":
                tree = self._add_repetition_to_tree(relationship, tree)
        
        return tree
