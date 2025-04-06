"""
Natural Language Parser module for the Parser component.

This module provides functionality for parsing Natural Language inputs.
"""

import re

class NLParser:
    """
    Parser for Natural Language inputs.
    """
    
    def __init__(self):
        """
        Initialize the NL parser.
        """
        # Initialize patterns for intent recognition
        self.intent_patterns = self._initialize_intent_patterns()
        
        # Initialize patterns for entity extraction
        self.entity_patterns = self._initialize_entity_patterns()
    
    def parse(self, nl_text):
        """
        Parse Natural Language input (main interface method).
        
        Args:
            nl_text (str): Natural Language input text.
            
        Returns:
            dict: Parsed representation with intents, entities, and relationships.
        """
        return self.parse_nl(nl_text)
    
    def parse_nl(self, nl_text):
        """
        Parse Natural Language input.
        
        Args:
            nl_text (str): Natural Language input text.
            
        Returns:
            dict: Parsed representation with intents, entities, and relationships.
        """
        # Recognize intents
        intents = self._recognize_intents(nl_text)
        
        # Extract entities
        entities = self._extract_entities(nl_text, intents)
        
        # Extract relationships
        relationships = self._extract_relationships(nl_text, entities)
        
        return {
            "intents": intents,
            "entities": entities,
            "relationships": relationships,
            "original_text": nl_text
        }
    
    def _initialize_intent_patterns(self):
        """
        Initialize patterns for intent recognition.
        
        Returns:
            dict: Intent patterns organized by category.
        """
        return {
            "system_initialization": [
                r"initialize (\w+) system",
                r"start (\w+) system",
                r"boot (\w+) system",
                r"set up (\w+) system"
            ],
            "context_configuration": [
                r"set (\w+) context",
                r"configure (\w+) context",
                r"establish (\w+) context",
                r"define (\w+) context"
            ],
            "task_execution": [
                r"execute (\w+) task",
                r"run (\w+) task",
                r"perform (\w+) task",
                r"do (\w+) task"
            ],
            "conditional_logic": [
                r"if (.+?) then (.+)",
                r"when (.+?) do (.+)",
                r"on condition (.+?) execute (.+)"
            ],
            "parallel_execution": [
                r"simultaneously (.+) and (.+)",
                r"in parallel (.+) and (.+)",
                r"concurrently (.+) and (.+)"
            ],
            "sequential_execution": [
                r"first (.+) then (.+)",
                r"after (.+) do (.+)",
                r"(.+) followed by (.+)"
            ],
            "repetition": [
                r"repeat (.+) (\d+) times",
                r"do (.+) (\d+) times",
                r"execute (.+) (\d+) times"
            ],
            "resource_allocation": [
                r"allocate (\w+) resource",
                r"assign (\w+) resource",
                r"reserve (\w+) resource"
            ],
            "security_operations": [
                r"apply (\w+) security",
                r"enforce (\w+) security",
                r"implement (\w+) security"
            ],
            "query_execution": [
                r"query (\w+)",
                r"search (\w+)",
                r"find (\w+)"
            ],
            "batch_operations": [
                r"batch process (.+)",
                r"process batch of (.+)",
                r"execute batch (.+)"
            ]
        }
    
    def _initialize_entity_patterns(self):
        """
        Initialize patterns for entity extraction.
        
        Returns:
            dict: Entity patterns organized by type.
        """
        return {
            "system_type": [
                r"(AI|ML|NLP|DP|IOT|HPC) system",
                r"system (AI|ML|NLP|DP|IOT|HPC)"
            ],
            "context_parameter": [
                r"context (\w+)",
                r"(\w+) context",
                r"environment (\w+)",
                r"(\w+) environment"
            ],
            "task_name": [
                r"task (\w+)",
                r"(\w+) task",
                r"operation (\w+)",
                r"(\w+) operation"
            ],
            "resource_identifier": [
                r"resource (\w+)",
                r"(\w+) resource",
                r"(\w+) allocation"
            ],
            "condition": [
                r"if (.+?)(?: then| do| execute)",
                r"when (.+?)(?: then| do| execute)",
                r"condition (.+?)(?: is met| is true)"
            ],
            "action": [
                r"(execute|run|perform|do) (.+?)(?:$|\.)",
                r"(allocate|assign|reserve) (.+?)(?:$|\.)",
                r"(apply|enforce|implement) (.+?)(?:$|\.)"
            ],
            "quantifier": [
                r"(\d+) times",
                r"repeat (\d+)",
                r"(\d+) iterations"
            ]
        }
    
    def _recognize_intents(self, nl_text):
        """
        Recognize intents in Natural Language text.
        
        Args:
            nl_text (str): Natural Language input text.
            
        Returns:
            list: Recognized intents with categories and details.
        """
        recognized_intents = []
        
        # Check each intent category
        for category, patterns in self.intent_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, nl_text, re.IGNORECASE)
                for match in matches:
                    intent = {
                        "category": category,
                        "pattern": pattern,
                        "match": match.group(0)
                    }
                    
                    # Add captured groups
                    groups = match.groups()
                    if groups:
                        intent["groups"] = groups
                    
                    recognized_intents.append(intent)
        
        return recognized_intents
    
    def _extract_entities(self, nl_text, intents):
        """
        Extract entities from Natural Language text.
        
        Args:
            nl_text (str): Natural Language input text.
            intents (list): Recognized intents.
            
        Returns:
            dict: Extracted entities organized by type.
        """
        entities = {}
        
        # Check each entity type
        for entity_type, patterns in self.entity_patterns.items():
            entities[entity_type] = []
            
            for pattern in patterns:
                matches = re.finditer(pattern, nl_text, re.IGNORECASE)
                for match in matches:
                    entity = {
                        "type": entity_type,
                        "pattern": pattern,
                        "match": match.group(0)
                    }
                    
                    # Add captured groups
                    groups = match.groups()
                    if groups:
                        entity["value"] = groups[-1]  # Usually the last group contains the entity value
                    
                    entities[entity_type].append(entity)
        
        return entities
    
    def _extract_relationships(self, nl_text, entities):
        """
        Extract relationships between entities.
        
        Args:
            nl_text (str): Natural Language input text.
            entities (dict): Extracted entities.
            
        Returns:
            list: Extracted relationships.
        """
        relationships = []
        
        # Extract sequence relationships
        sequence_patterns = [
            r"(.+?) then (.+)",
            r"(.+?) followed by (.+)",
            r"after (.+?) do (.+)"
        ]
        
        for pattern in sequence_patterns:
            matches = re.finditer(pattern, nl_text, re.IGNORECASE)
            for match in matches:
                relationships.append({
                    "type": "sequence",
                    "operator": ">",
                    "source": match.group(1),
                    "target": match.group(2)
                })
        
        # Extract parallel relationships
        parallel_patterns = [
            r"(.+?) and (.+?) simultaneously",
            r"(.+?) in parallel with (.+?)",
            r"concurrently (.+?) and (.+?)"
        ]
        
        for pattern in parallel_patterns:
            matches = re.finditer(pattern, nl_text, re.IGNORECASE)
            for match in matches:
                relationships.append({
                    "type": "parallel",
                    "operator": "&",
                    "expressions": [match.group(1), match.group(2)]
                })
        
        # Extract conditional relationships
        conditional_patterns = [
            r"if (.+?) then (.+?)(?: else (.+))?",
            r"when (.+?) do (.+?)(?: otherwise (.+))?"
        ]
        
        for pattern in conditional_patterns:
            matches = re.finditer(pattern, nl_text, re.IGNORECASE)
            for match in matches:
                relationship = {
                    "type": "conditional",
                    "operator": "?:",
                    "condition": match.group(1),
                    "trueBranch": match.group(2)
                }
                
                # Add false branch if present
                if match.lastindex >= 3:
                    relationship["falseBranch"] = match.group(3)
                
                relationships.append(relationship)
        
        # Extract repetition relationships
        repetition_patterns = [
            r"repeat (.+?) (\d+) times",
            r"do (.+?) (\d+) times"
        ]
        
        for pattern in repetition_patterns:
            matches = re.finditer(pattern, nl_text, re.IGNORECASE)
            for match in matches:
                relationships.append({
                    "type": "repetition",
                    "operator": "**",
                    "expression": match.group(1),
                    "count": int(match.group(2))
                })
        
        return relationships
