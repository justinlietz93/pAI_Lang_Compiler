"""
Expression Synthesizer module for the Structure Synthesizer component.

This module provides functionality for synthesizing pAI_Lang strings from expression trees.
"""

class ExpressionSynthesizer:
    """
    Synthesizes pAI_Lang strings from expression trees.
    """
    
    def __init__(self):
        """
        Initialize the expression synthesizer.
        
        Sets up the operator precedence rules and bracketing requirements
        for different expression types in pAI_Lang.
        """
        # Define operator precedence (higher number = higher precedence)
        self.operator_precedence = {
            "?:": 1,  # Conditional (lowest precedence)
            ">": 2,   # Sequence
            "&": 3,   # Parallel
            "!": 4,   # Context activation
            "**": 5,  # Repetition
            "|": 6    # Piping (highest precedence)
        }
        
        # Define which operators require brackets in different contexts
        self.requires_brackets = {
            # When operator is used as left operand of parent operator
            "left": {
                ">": {"?:"},
                "&": {"?:", ">"},
                "!": {"?:", ">", "&"},
                "**": {"?:", ">", "&", "!"},
                "|": {"?:", ">", "&", "!", "**"}
            },
            # When operator is used as right operand of parent operator
            "right": {
                ">": {"?:"},
                "&": {"?:", ">"},
                "!": {"?:", ">", "&"},
                "**": {"?:", ">", "&", "!"},
                "|": {"?:", ">", "&", "!", "**"}
            }
        }
    
    def synthesize_from_tree(self, tree):
        """
        Synthesize pAI_Lang string from expression tree.
        
        Args:
            tree (dict): Expression tree.
            
        Returns:
            str: Synthesized pAI_Lang string.
        """
        if tree is None:
            return ""
        
        tree_type = tree.get("type")
        
        if tree_type == "token":
            return tree.get("value", "")
        
        elif tree_type == "sequence":
            left = self.synthesize_from_tree(tree.get("left"))
            right = self.synthesize_from_tree(tree.get("right"))
            return f"{left}{tree.get('operator', '>')}{right}"
        
        elif tree_type == "parallel":
            left = self.synthesize_from_tree(tree.get("left"))
            right = self.synthesize_from_tree(tree.get("right"))
            return f"{left}{tree.get('operator', '&')}{right}"
        
        elif tree_type == "conditional":
            condition = self.synthesize_from_tree(tree.get("condition"))
            true_branch = self.synthesize_from_tree(tree.get("true_branch"))
            
            # Check if false branch exists
            if "false_branch" in tree:
                false_branch = self.synthesize_from_tree(tree.get("false_branch"))
                return f"{condition}?{true_branch}:{false_branch}"
            else:
                return f"{condition}?{true_branch}"
        
        elif tree_type == "repetition":
            count = tree.get("count", 1)
            expression = self.synthesize_from_tree(tree.get("expression"))
            return f"**{count}{expression}"
        
        # Unknown node type
        return ""
