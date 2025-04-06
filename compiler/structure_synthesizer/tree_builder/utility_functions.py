"""
Utility Functions module for the TreeBuilder.

This module provides utility methods for tree operations.
"""

class UtilityFunctions:
    """
    Utility methods for tree operations.
    """
    
    def _copy_tree(self, tree):
        """
        Create a deep copy of the tree.
        
        Args:
            tree (dict): Expression tree.
            
        Returns:
            dict: Copy of the tree.
        """
        if tree is None:
            return None
        
        # Create new node
        new_node = {
            "type": tree.get("type")
        }
        
        # Copy properties
        for key, value in tree.items():
            if key == "type":
                continue
            
            if isinstance(value, dict):
                new_node[key] = self._copy_tree(value)
            else:
                new_node[key] = value
        
        return new_node
