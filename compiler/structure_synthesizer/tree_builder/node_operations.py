"""
Node Operations module for the TreeBuilder.

This module provides methods for finding and replacing nodes in expression trees.
"""

class NodeOperations:
    """
    Methods for node operations in expression trees.
    """
    
    def _find_node_with_value(self, tree, value):
        """
        Find node with specific value in tree.
        
        Args:
            tree (dict): Expression tree.
            value (str): Value to find.
            
        Returns:
            dict: Node with value, or None if not found.
        """
        if tree is None:
            return None
        
        # Check if this node has the value
        if tree.get("type") == "token" and tree.get("value") == value:
            return tree
        
        # Check left branch
        if "left" in tree:
            left_result = self._find_node_with_value(tree["left"], value)
            if left_result:
                return left_result
        
        # Check right branch
        if "right" in tree:
            right_result = self._find_node_with_value(tree["right"], value)
            if right_result:
                return right_result
        
        # Check condition
        if "condition" in tree:
            condition_result = self._find_node_with_value(tree["condition"], value)
            if condition_result:
                return condition_result
        
        # Check true branch
        if "true_branch" in tree:
            true_result = self._find_node_with_value(tree["true_branch"], value)
            if true_result:
                return true_result
        
        # Check false branch
        if "false_branch" in tree:
            false_result = self._find_node_with_value(tree["false_branch"], value)
            if false_result:
                return false_result
        
        # Check expression
        if "expression" in tree:
            expr_result = self._find_node_with_value(tree["expression"], value)
            if expr_result:
                return expr_result
        
        # Not found
        return None
    
    def _replace_node(self, tree, node, replacement):
        """
        Replace node in tree with replacement.
        
        Args:
            tree (dict): Expression tree.
            node (dict): Node to replace.
            replacement (dict): Replacement node.
            
        Returns:
            dict: Updated tree.
        """
        if tree is None:
            return replacement
        
        # Check if this is the node to replace
        if tree is node:
            return replacement
        
        # Check and replace in left branch
        if "left" in tree:
            tree["left"] = self._replace_node(tree["left"], node, replacement)
        
        # Check and replace in right branch
        if "right" in tree:
            tree["right"] = self._replace_node(tree["right"], node, replacement)
        
        # Check and replace in condition
        if "condition" in tree:
            tree["condition"] = self._replace_node(tree["condition"], node, replacement)
        
        # Check and replace in true branch
        if "true_branch" in tree:
            tree["true_branch"] = self._replace_node(tree["true_branch"], node, replacement)
        
        # Check and replace in false branch
        if "false_branch" in tree:
            tree["false_branch"] = self._replace_node(tree["false_branch"], node, replacement)
        
        # Check and replace in expression
        if "expression" in tree:
            tree["expression"] = self._replace_node(tree["expression"], node, replacement)
        
        return tree
    
    def _find_leftmost_node(self, tree):
        """
        Find leftmost node in tree.
        
        Args:
            tree (dict): Expression tree.
            
        Returns:
            dict: Leftmost node.
        """
        if tree.get("type") == "token":
            return tree
        
        if "left" in tree:
            return self._find_leftmost_node(tree["left"])
        
        if "condition" in tree:
            return self._find_leftmost_node(tree["condition"])
        
        if "expression" in tree:
            return self._find_leftmost_node(tree["expression"])
        
        return tree
    
    def _find_rightmost_node(self, tree):
        """
        Find rightmost node in tree.
        
        Args:
            tree (dict): Expression tree.
            
        Returns:
            dict: Rightmost node.
        """
        if tree.get("type") == "token":
            return tree
        
        if "right" in tree:
            return self._find_rightmost_node(tree["right"])
        
        if "false_branch" in tree:
            return self._find_rightmost_node(tree["false_branch"])
        
        if "true_branch" in tree:
            return self._find_rightmost_node(tree["true_branch"])
        
        if "expression" in tree:
            return self._find_rightmost_node(tree["expression"])
        
        return tree
