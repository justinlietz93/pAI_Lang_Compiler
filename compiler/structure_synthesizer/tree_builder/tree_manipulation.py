"""
Tree Manipulation module for the TreeBuilder.

This module provides methods for manipulating expression trees with different relationship types.
"""

class TreeManipulation:
    """
    Methods for tree manipulation in expression trees.
    """
    
    def _add_sequence_to_tree(self, relationship, tree):
        """
        Add sequence relationship to expression tree.
        
        Args:
            relationship (dict): Sequence relationship.
            tree (dict): Current expression tree.
            
        Returns:
            dict: Updated expression tree.
        """
        source_token = relationship.get("source_token", "")
        target_token = relationship.get("target_token", "")
        
        # If tree is None, create new tree
        if tree is None:
            return {
                "type": "sequence",
                "operator": ">",
                "left": {"type": "token", "value": source_token},
                "right": {"type": "token", "value": target_token}
            }
        
        # If tree already has this relationship, return unchanged
        if (tree.get("type") == "sequence" and
            tree.get("left", {}).get("value") == source_token and
            tree.get("right", {}).get("value") == target_token):
            return tree
        
        # Check if source token is in tree
        source_node = self._find_node_with_value(tree, source_token)
        if source_node:
            # Replace source node with sequence
            return self._replace_node_with_sequence(
                tree, source_node, source_token, target_token
            )
        
        # Check if target token is in tree
        target_node = self._find_node_with_value(tree, target_token)
        if target_node:
            # Replace target node with sequence
            return self._replace_node_with_sequence(
                tree, target_node, source_token, target_token
            )
        
        # If neither token is in tree, create new sequence and merge
        sequence = {
            "type": "sequence",
            "operator": ">",
            "left": {"type": "token", "value": source_token},
            "right": {"type": "token", "value": target_token}
        }
        
        return self._merge_trees(tree, sequence)
    
    def _add_parallel_to_tree(self, relationship, tree):
        """
        Add parallel relationship to expression tree.
        
        Args:
            relationship (dict): Parallel relationship.
            tree (dict): Current expression tree.
            
        Returns:
            dict: Updated expression tree.
        """
        tokens = relationship.get("tokens", [])
        
        # If no tokens, return unchanged
        if not tokens:
            return tree
        
        # If only one token, return as token node
        if len(tokens) == 1:
            return {"type": "token", "value": tokens[0]}
        
        # Build parallel node
        parallel_node = {
            "type": "parallel",
            "operator": "&",
            "left": {"type": "token", "value": tokens[0]},
            "right": {"type": "token", "value": tokens[1]}
        }
        
        # Add additional tokens if present
        for i in range(2, len(tokens)):
            parallel_node = {
                "type": "parallel",
                "operator": "&",
                "left": parallel_node,
                "right": {"type": "token", "value": tokens[i]}
            }
        
        # If tree is None, return parallel node
        if tree is None:
            return parallel_node
        
        # Otherwise, merge trees
        return self._merge_trees(tree, parallel_node)
    
    def _add_conditional_to_tree(self, relationship, tree):
        """
        Add conditional relationship to expression tree.
        
        Args:
            relationship (dict): Conditional relationship.
            tree (dict): Current expression tree.
            
        Returns:
            dict: Updated expression tree.
        """
        condition_token = relationship.get("condition_token", "")
        true_token = relationship.get("true_token", "")
        false_token = relationship.get("false_token", "")
        
        # Build conditional node
        conditional_node = {
            "type": "conditional",
            "operator": "?:",
            "condition": {"type": "token", "value": condition_token},
            "true_branch": {"type": "token", "value": true_token}
        }
        
        # Add false branch if present
        if false_token:
            conditional_node["false_branch"] = {"type": "token", "value": false_token}
        
        # If tree is None, return conditional node
        if tree is None:
            return conditional_node
        
        # Otherwise, merge trees
        return self._merge_trees(tree, conditional_node)
    
    def _add_repetition_to_tree(self, relationship, tree):
        """
        Add repetition relationship to expression tree.
        
        Args:
            relationship (dict): Repetition relationship.
            tree (dict): Current expression tree.
            
        Returns:
            dict: Updated expression tree.
        """
        token = relationship.get("token", "")
        count = relationship.get("count", 1)
        
        # Build repetition node
        repetition_node = {
            "type": "repetition",
            "operator": "**",
            "count": count,
            "expression": {"type": "token", "value": token}
        }
        
        # If tree is None, return repetition node
        if tree is None:
            return repetition_node
        
        # Check if token is in tree
        token_node = self._find_node_with_value(tree, token)
        if token_node:
            # Replace token node with repetition
            return self._replace_node_with_repetition(
                tree, token_node, token, count
            )
        
        # Otherwise, merge trees
        return self._merge_trees(tree, repetition_node)
    
    def _replace_node_with_sequence(self, tree, node, source_token, target_token):
        """
        Replace node with sequence in tree.
        
        Args:
            tree (dict): Expression tree.
            node (dict): Node to replace.
            source_token (str): Source token.
            target_token (str): Target token.
            
        Returns:
            dict: Updated tree.
        """
        # Create a copy of the tree
        new_tree = self._copy_tree(tree)
        
        # Replace node with sequence
        sequence = {
            "type": "sequence",
            "operator": ">",
            "left": {"type": "token", "value": source_token},
            "right": {"type": "token", "value": target_token}
        }
        
        # Perform replacement
        return self._replace_node(new_tree, node, sequence)
    
    def _replace_node_with_repetition(self, tree, node, token, count):
        """
        Replace node with repetition in tree.
        
        Args:
            tree (dict): Expression tree.
            node (dict): Node to replace.
            token (str): Token to repeat.
            count (int): Repetition count.
            
        Returns:
            dict: Updated tree.
        """
        # Create a copy of the tree
        new_tree = self._copy_tree(tree)
        
        # Replace node with repetition
        repetition = {
            "type": "repetition",
            "operator": "**",
            "count": count,
            "expression": {"type": "token", "value": token}
        }
        
        # Perform replacement
        return self._replace_node(new_tree, node, repetition)
    
    def _merge_trees(self, tree1, tree2):
        """
        Merge two expression trees.
        
        Args:
            tree1 (dict): First expression tree.
            tree2 (dict): Second expression tree.
            
        Returns:
            dict: Merged tree.
        """
        # If either tree is None, return the other
        if tree1 is None:
            return tree2
        if tree2 is None:
            return tree1
        
        # If both trees are tokens, create sequence
        if tree1.get("type") == "token" and tree2.get("type") == "token":
            return {
                "type": "sequence",
                "operator": ">",
                "left": tree1,
                "right": tree2
            }
        
        # If tree1 is token and tree2 is not, add tree1 as left child of tree2
        if tree1.get("type") == "token":
            # Find leftmost node in tree2
            leftmost = self._find_leftmost_node(tree2)
            # Replace leftmost with sequence of tree1 and leftmost
            return self._replace_node(
                tree2,
                leftmost,
                {
                    "type": "sequence",
                    "operator": ">",
                    "left": tree1,
                    "right": leftmost
                }
            )
        
        # If tree2 is token and tree1 is not, add tree2 as right child of tree1
        if tree2.get("type") == "token":
            # Find rightmost node in tree1
            rightmost = self._find_rightmost_node(tree1)
            # Replace rightmost with sequence of rightmost and tree2
            return self._replace_node(
                tree1,
                rightmost,
                {
                    "type": "sequence",
                    "operator": ">",
                    "left": rightmost,
                    "right": tree2
                }
            )
        
        # Otherwise, create sequence of both trees
        return {
            "type": "sequence",
            "operator": ">",
            "left": tree1,
            "right": tree2
        }
