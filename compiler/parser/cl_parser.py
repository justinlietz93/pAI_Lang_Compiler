"""
Command Language Parser module for the Parser component.

This module provides functionality for parsing Command Language inputs.
"""

import re

class CLParser:
    """
    Parser for Command Language inputs.
    """
    
    def __init__(self):
        """
        Initialize the CL parser.
        
        Sets up the command patterns and syntax rules for parsing
        Command Language inputs according to the pAI_Lang specification.
        """
        # Define command patterns for recognition
        self.command_pattern = r'^\s*>>>\s*([A-Z_]+)(?:\[([^\]]*)\])?'
        
        # Define known command types and their required parameters
        self.command_types = {
            "INITIALIZE": ["SYSTEM"],
            "SET_CONTEXT": ["CONTEXT"],
            "EXECUTE": ["TASK"],
            "EXECUTE_TASK": ["TASK"],
            "CONDITIONAL": ["CONDITION"],
            "PARALLEL": [],
            "REPEAT": ["count"],
            "BATCH_OPERATION": ["BATCH"],
            "ACTIVATE_CONTEXT": ["CONTEXT"],
            "ALLOCATE_RESOURCE": ["RESOURCE"],
            "APPLY_SECURITY": ["SECURITY"],
            "EXECUTE_QUERY": ["QUERY"]
        }
        
        # Compile regex patterns for efficient parsing
        self.command_regex = re.compile(self.command_pattern)
    
    def parse(self, cl_text):
        """
        Parse Command Language input (main interface method).
        
        Args:
            cl_text (str): Command Language input text.
            
        Returns:
            dict: Parsed representation with commands and structure.
        """
        return self.parse_cl(cl_text)
    
    def parse_cl(self, cl_text):
        """
        Parse Command Language input.
        
        Args:
            cl_text (str): Command Language input text.
            
        Returns:
            dict: Parsed representation with commands and structure.
        """
        # Parse commands
        commands = self._parse_commands(cl_text)
        
        # Build command hierarchy
        command_hierarchy = self._build_command_hierarchy(commands)
        
        return {
            "commands": commands,
            "hierarchy": command_hierarchy,
            "original_text": cl_text
        }
    
    def _parse_commands(self, cl_text):
        """
        Parse commands from Command Language text.
        
        Args:
            cl_text (str): Command Language input text.
            
        Returns:
            list: Parsed commands.
        """
        commands = []
        lines = cl_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if line starts with >>>
            if line.startswith('>>>'):
                # Extract command and parameters
                command_parts = line[3:].strip().split('[', 1)
                command_name = command_parts[0].strip()
                
                command = {
                    "name": command_name,
                    "parameters": {},
                    "indentation": 0,
                    "line": line
                }
                
                # Count indentation (number of spaces before >>>)
                indentation_match = re.match(r'^(\s*)>>>', line)
                if indentation_match:
                    command["indentation"] = len(indentation_match.group(1))
                
                # Extract parameters if present
                if len(command_parts) > 1 and ']' in command_parts[1]:
                    params_str = command_parts[1].split(']', 1)[0].strip()
                    command["parameters"] = self._parse_parameters(params_str)
                
                commands.append(command)
        
        return commands
    
    def _parse_parameters(self, params_str):
        """
        Parse parameters string into a dictionary.
        
        Args:
            params_str (str): Parameters string.
            
        Returns:
            dict: Parsed parameters.
        """
        params = {}
        
        # Handle empty parameters
        if not params_str:
            return params
        
        # Split by commas, but respect nested structures
        param_parts = []
        current_part = ""
        bracket_depth = 0
        
        for char in params_str:
            if char == '[':
                bracket_depth += 1
                current_part += char
            elif char == ']':
                bracket_depth -= 1
                current_part += char
            elif char == ',' and bracket_depth == 0:
                param_parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char
        
        # Add the last part if not empty
        if current_part.strip():
            param_parts.append(current_part.strip())
        
        # Process each parameter part
        for part in param_parts:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key.strip()] = value.strip()
            else:
                # For parameters without explicit key
                params[part.strip()] = True
        
        return params
    
    def _build_command_hierarchy(self, commands):
        """
        Build command hierarchy based on indentation.
        
        Args:
            commands (list): List of parsed commands.
            
        Returns:
            list: Command hierarchy with parent-child relationships.
        """
        hierarchy = []
        stack = []
        
        for command in commands:
            indentation = command["indentation"]
            
            # Pop stack until we find a parent with less indentation
            while stack and stack[-1]["indentation"] >= indentation:
                stack.pop()
            
            # Create a copy of the command with children
            command_node = command.copy()
            command_node["children"] = []
            
            # Add as child to parent if stack is not empty
            if stack:
                stack[-1]["children"].append(command_node)
            else:
                # Add to root hierarchy
                hierarchy.append(command_node)
            
            # Push to stack
            stack.append(command_node)
        
        return hierarchy
