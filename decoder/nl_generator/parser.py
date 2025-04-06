"""
Parser module for the NL Generator.

This module provides functionality for parsing Command Language and templates.
"""

class NLTemplateParser:
    """
    Parser for NL templates and Command Language.
    """
    
    def __init__(self):
        """
        Initialize the NL template parser.
        """
        self.cl_parser = CLParser()
    
    def parse_cl(self, cl_content):
        """
        Parse Command Language content into a structured representation.
        
        Args:
            cl_content (str): Command Language content.
            
        Returns:
            list: List of parsed commands.
        """
        return self.cl_parser._parse_cl(cl_content)
    
    def parse_template(self, template_content):
        """
        Parse template content into a structured representation.
        
        Args:
            template_content (str): Template content.
            
        Returns:
            dict: Parsed template structure.
        """
        templates = {}
        
        # Parse template content
        lines = template_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse template definition
            if ':' in line:
                key, value = line.split(':', 1)
                templates[key.strip()] = value.strip()
        
        return templates


class CLParser:
    """
    Parser for Command Language.
    """
    
    def _parse_cl(self, cl_content):
        """
        Parse Command Language content into a structured representation.
        
        Args:
            cl_content (str): Command Language content.
            
        Returns:
            list: List of parsed commands.
        """
        commands = []
        lines = cl_content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Check if line starts with >>>
            if line.startswith('>>>'):
                # Extract command and parameters
                command_parts = line[3:].strip().split('[', 1)
                command_type = command_parts[0].strip()
                
                # Initialize command object
                command = {
                    'type': command_type,
                    'parameters': {},
                    'subcommands': []
                }
                
                # Extract parameters if present
                if len(command_parts) > 1 and ']' in command_parts[1]:
                    params_str = command_parts[1].split(']', 1)[0].strip()
                    command['parameters'] = self._parse_parameters(params_str)
                
                # Check for subcommands or block structure
                if command_type in ['CONDITIONAL', 'PARALLEL', 'REPEAT', 'BATCH_OPERATION', 'PIPE']:
                    # Find the end of the block
                    end_marker = f">>> END_{command_type}"
                    block_content = []
                    j = i + 1
                    
                    # Collect all lines until end marker
                    while j < len(lines) and not lines[j].strip().startswith(end_marker):
                        block_content.append(lines[j])
                        j += 1
                    
                    # Process block content based on command type
                    if command_type == 'CONDITIONAL':
                        # Split into true and false branches
                        true_branch, false_branch = self._split_conditional_block(block_content)
                        command['true_branch'] = self._parse_cl('\n'.join(true_branch))
                        command['false_branch'] = self._parse_cl('\n'.join(false_branch))
                    
                    elif command_type == 'PARALLEL':
                        # Parse parallel actions
                        command['actions'] = self._parse_cl('\n'.join(block_content))
                    
                    elif command_type == 'REPEAT':
                        # Parse repeated action
                        command['action'] = self._parse_cl('\n'.join(block_content))
                        command['count'] = command['parameters'].get('count', '1')
                    
                    elif command_type == 'BATCH_OPERATION':
                        # Parse batch operations
                        command['operations'] = self._parse_cl('\n'.join(block_content))
                    
                    elif command_type == 'PIPE':
                        # Split into source and target
                        source, target = self._split_pipe_block(block_content)
                        command['source'] = self._parse_cl('\n'.join(source))
                        command['target'] = self._parse_cl('\n'.join(target))
                    
                    # Update index to skip processed block
                    i = j + 1
                else:
                    # Simple command without block structure
                    i += 1
                
                commands.append(command)
            else:
                # Line doesn't start with >>>, skip it
                i += 1
        
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
    
    def _split_conditional_block(self, block_content):
        """
        Split conditional block into true and false branches.
        
        Args:
            block_content (list): Lines in the conditional block.
            
        Returns:
            tuple: (true_branch_lines, false_branch_lines)
        """
        true_branch = []
        false_branch = []
        
        # Find the ELSE marker
        in_true_branch = True
        for line in block_content:
            if line.strip().startswith('>>> ELSE'):
                in_true_branch = False
                continue
            
            if in_true_branch:
                true_branch.append(line)
            else:
                false_branch.append(line)
        
        return true_branch, false_branch
    
    def _split_pipe_block(self, block_content):
        """
        Split pipe block into source and target.
        
        Args:
            block_content (list): Lines in the pipe block.
            
        Returns:
            tuple: (source_lines, target_lines)
        """
        source = []
        target = []
        
        # Find SOURCE and TARGET markers
        current_section = None
        for line in block_content:
            if line.strip().startswith('>>> SOURCE'):
                current_section = 'source'
                continue
            elif line.strip().startswith('>>> TARGET'):
                current_section = 'target'
                continue
            
            if current_section == 'source':
                source.append(line)
            elif current_section == 'target':
                target.append(line)
        
        return source, target
