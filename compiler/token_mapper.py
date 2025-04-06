"""
Token Mapper for pAI_Lang

This module provides functionality for mapping semantic structures to pAI_Lang tokens
based on the semantic analysis of Natural Language (NL) and Command Language (CL) inputs.
"""

class TokenMapper:
    """
    Maps semantic structures to pAI_Lang tokens.
    """
    
    def __init__(self, token_dictionary=None):
        """
        Initialize the token mapper.
        
        Args:
            token_dictionary (dict, optional): Dictionary of token definitions.
        """
        self.token_dictionary = token_dictionary or {}
    
    def map_tokens(self, semantic_analysis):
        """
        Map semantic analysis to pAI_Lang tokens.
        
        Args:
            semantic_analysis (dict): Semantic analysis from the semantic analyzer.
            
        Returns:
            dict: Token mapping with pAI_Lang tokens.
        """
        # Extract semantic structure
        semantic_structure = semantic_analysis.get("semantic_structure", {})
        
        # Map tokens
        token_mapping = self._map_structure_tokens(semantic_structure)
        
        # Map relationships
        relationship_mapping = self._map_structure_relationships(semantic_structure)
        
        return {
            "tokens": token_mapping,
            "relationships": relationship_mapping,
            "original_structure": semantic_structure
        }
    
    def _map_structure_tokens(self, semantic_structure):
        """
        Map tokens from semantic structure.
        
        Args:
            semantic_structure (dict): Semantic structure.
            
        Returns:
            dict: Mapping of source to pAI_Lang tokens.
        """
        token_mapping = {}
        
        # Process each token in structure
        for token_info in semantic_structure.get("tokens", []):
            source = token_info.get("source", "")
            token = token_info.get("token", "")
            
            # Store mapping
            token_mapping[source] = {
                "pailang_token": token,
                "original_info": token_info
            }
            
            # Add to token dictionary if not present
            if token not in self.token_dictionary:
                self.token_dictionary[token] = {
                    "category": token_info.get("category", ""),
                    "id": token_info.get("id", ""),
                    "source": source
                }
        
        return token_mapping
    
    def _map_structure_relationships(self, semantic_structure):
        """
        Map relationships from semantic structure.
        
        Args:
            semantic_structure (dict): Semantic structure.
            
        Returns:
            list: Mapped relationships.
        """
        relationship_mapping = []
        
        # Process each relationship in structure
        for relationship in semantic_structure.get("relationships", []):
            rel_type = relationship.get("type", "")
            
            if rel_type == "binary":
                # Binary relationship (sequence, parallel)
                mapped_rel = self._map_binary_relationship(relationship)
                relationship_mapping.append(mapped_rel)
            
            elif rel_type == "conditional":
                # Conditional relationship
                mapped_rel = self._map_conditional_relationship(relationship)
                relationship_mapping.append(mapped_rel)
            
            elif rel_type == "repetition":
                # Repetition relationship
                mapped_rel = self._map_repetition_relationship(relationship)
                relationship_mapping.append(mapped_rel)
        
        return relationship_mapping
    
    def _map_binary_relationship(self, relationship):
        """
        Map binary relationship.
        
        Args:
            relationship (dict): Binary relationship.
            
        Returns:
            dict: Mapped relationship.
        """
        operator = relationship.get("operator", ">")
        
        # For sequence relationship
        if "source" in relationship and "target" in relationship:
            source = relationship.get("source", "")
            target = relationship.get("target", "")
            
            # Look up tokens
            source_token = self._find_token_for_source(source)
            target_token = self._find_token_for_source(target)
            
            return {
                "type": "sequence",
                "operator": operator,
                "source_token": source_token,
                "target_token": target_token,
                "pailang_expression": f"{source_token}{operator}{target_token}"
            }
        
        # For parallel relationship
        elif "expressions" in relationship:
            expressions = relationship.get("expressions", [])
            
            # Look up tokens
            tokens = [self._find_token_for_source(expr) for expr in expressions]
            
            # Join with operator
            pailang_expression = operator.join(tokens)
            
            return {
                "type": "parallel",
                "operator": operator,
                "tokens": tokens,
                "pailang_expression": pailang_expression
            }
        
        # Default case
        return {
            "type": "unknown",
            "operator": operator,
            "original_relationship": relationship
        }
    
    def _map_conditional_relationship(self, relationship):
        """
        Map conditional relationship.
        
        Args:
            relationship (dict): Conditional relationship.
            
        Returns:
            dict: Mapped relationship.
        """
        condition = relationship.get("condition", "")
        true_branch = relationship.get("trueBranch", "")
        false_branch = relationship.get("falseBranch", "")
        
        # Look up tokens
        condition_token = self._find_token_for_source(condition)
        true_token = self._find_token_for_source(true_branch)
        false_token = self._find_token_for_source(false_branch) if false_branch else ""
        
        # Build pAI_Lang expression
        if false_token:
            pailang_expression = f"{condition_token}?{true_token}:{false_token}"
        else:
            pailang_expression = f"{condition_token}?{true_token}"
        
        return {
            "type": "conditional",
            "operator": "?:",
            "condition_token": condition_token,
            "true_token": true_token,
            "false_token": false_token,
            "pailang_expression": pailang_expression
        }
    
    def _map_repetition_relationship(self, relationship):
        """
        Map repetition relationship.
        
        Args:
            relationship (dict): Repetition relationship.
            
        Returns:
            dict: Mapped relationship.
        """
        expression = relationship.get("expression", "")
        count = relationship.get("count", 1)
        
        # Look up token
        token = self._find_token_for_source(expression)
        
        # Build pAI_Lang expression
        pailang_expression = f"**{count}{token}"
        
        return {
            "type": "repetition",
            "operator": "**",
            "token": token,
            "count": count,
            "pailang_expression": pailang_expression
        }
    
    def _find_token_for_source(self, source):
        """
        Find pAI_Lang token for a source string.
        
        Args:
            source (str): Source string.
            
        Returns:
            str: pAI_Lang token, or empty string if not found.
        """
        # Search token dictionary
        for token, definition in self.token_dictionary.items():
            if definition.get("source") == source:
                return token
        
        # If not found, check if source is already a token
        if source in self.token_dictionary:
            return source
        
        # If still not found, return empty string
        return ""
