"""
Base module for the Structure Synthesizer component.

This module provides the main StructureSynthesizer class that coordinates
the synthesis of pAI_Lang strings from token mappings and relationship mappings.
"""

from .tree_builder import TreeBuilder
from .expression_synthesizer import ExpressionSynthesizer

class StructureSynthesizer:
    """
    Synthesizes the final pAI_Lang string from token and relationship mappings.
    """
    
    def __init__(self):
        """
        Initialize the structure synthesizer.
        """
        self.operator_precedence = self._initialize_operator_precedence()
        self.tree_builder = TreeBuilder(self.operator_precedence)
        self.expression_synthesizer = ExpressionSynthesizer()
    
    def synthesize(self, token_mapping):
        """
        Synthesize pAI_Lang string from token mapping.
        
        Args:
            token_mapping (dict): Token mapping from the token mapper.
            
        Returns:
            str: Synthesized pAI_Lang string.
        """
        # Extract tokens and relationships
        tokens = token_mapping.get("tokens", {})
        relationships = token_mapping.get("relationships", [])
        
        # If no relationships, just return the first token
        if not relationships and tokens:
            first_token = next(iter(tokens.values()))
            return first_token.get("pailang_token", "")
        
        # Build expression tree
        expression_tree = self.tree_builder.build_expression_tree(relationships)
        
        # Synthesize pAI_Lang string from tree
        pailang_string = self.expression_synthesizer.synthesize_from_tree(expression_tree)
        
        return pailang_string
    
    def _initialize_operator_precedence(self):
        """
        Initialize operator precedence map.
        
        Returns:
            dict: Operator precedence (higher value means higher precedence).
        """
        return {
            "?:": 1,  # Conditional (lowest precedence)
            ">": 2,   # Sequence
            "&": 3,   # Parallel
            "|": 4,   # Piping
            "=": 5,   # Assignment
            "**": 6,  # Repetition
            "!": 7,   # Context activation
            "#": 8    # Aggregation (highest precedence)
        }
