"""
Matrix Loader for pAI_Lang

This module handles loading matrix data for the Matrices Transformer component.
It provides functionality to load mapping matrices from various sources like
JSON files, CSV files, or hardcoded defaults.
"""

import json
import os
import csv
from pathlib import Path

class MatrixLoader:
    """
    Handles loading and parsing of mapping matrices for the pAI_Lang system.
    """
    
    def __init__(self, matrix_dir=None):
        """
        Initialize the MatrixLoader with an optional directory for matrix files.
        
        Args:
            matrix_dir (str, optional): Directory containing matrix files. If None,
                                       a default location will be used.
        """
        self.matrix_dir = matrix_dir or os.path.join(os.path.dirname(__file__), 'matrices')
    
    def load_matrices(self):
        """
        Load all mapping matrices.
        
        Returns:
            dict: All mapping matrices for the different transformation directions.
        """
        return {
            "nl_to_cl": self.load_matrix("nl_to_cl"),
            "cl_to_pailang": self.load_matrix("cl_to_pailang"),
            "pailang_to_cl": self.load_matrix("pailang_to_cl"),
            "cl_to_nl": self.load_matrix("cl_to_nl")
        }
    
    def load_matrix(self, matrix_type):
        """
        Load a specific mapping matrix.
        
        Args:
            matrix_type (str): Type of matrix to load ('nl_to_cl', 'cl_to_pailang', etc.)
            
        Returns:
            dict: The loaded matrix data.
        """
        # Try to load from JSON file
        json_path = os.path.join(self.matrix_dir, f"{matrix_type}.json")
        if os.path.exists(json_path):
            return self._load_from_json(json_path)
        
        # Try to load from CSV file
        csv_path = os.path.join(self.matrix_dir, f"{matrix_type}.csv")
        if os.path.exists(csv_path):
            return self._load_from_csv(csv_path, matrix_type)
        
        # Fall back to default hardcoded matrices
        return self._get_default_matrix(matrix_type)
    
    def _load_from_json(self, file_path):
        """
        Load matrix data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file.
            
        Returns:
            dict: Matrix data loaded from the JSON file.
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading matrix from JSON: {e}")
            return self._get_default_matrix(Path(file_path).stem)
    
    def _load_from_csv(self, file_path, matrix_type):
        """
        Load matrix data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
            matrix_type (str): Type of matrix to load.
            
        Returns:
            dict: Matrix data loaded from the CSV file.
        """
        try:
            matrix_data = {}
            
            if matrix_type == "nl_to_cl":
                matrix_data["patterns"] = []
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        matrix_data["patterns"].append({
                            "pattern": row.get("pattern", ""),
                            "template": row.get("template", ""),
                            "examples": []  # CSV doesn't easily support nested structures
                        })
            
            elif matrix_type == "cl_to_pailang":
                matrix_data["commands"] = []
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        matrix_data["commands"].append({
                            "command": row.get("command", ""),
                            "parameters": row.get("parameters", "").split(","),
                            "pailang_template": row.get("pailang_template", ""),
                            "subcommands": row.get("subcommands", "").lower() == "true",
                            "examples": []
                        })
            
            elif matrix_type == "pailang_to_cl":
                matrix_data["tokens"] = []
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        matrix_data["tokens"].append({
                            "pattern": row.get("pattern", ""),
                            "template": row.get("template", ""),
                            "examples": []
                        })
            
            elif matrix_type == "cl_to_nl":
                matrix_data["commands"] = []
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        matrix_data["commands"].append({
                            "command": row.get("command", ""),
                            "parameters": row.get("parameters", "").split(","),
                            "nl_template": row.get("nl_template", ""),
                            "examples": []
                        })
            
            return matrix_data
        
        except Exception as e:
            print(f"Error loading matrix from CSV: {e}")
            return self._get_default_matrix(matrix_type)
    
    def _get_default_matrix(self, matrix_type):
        """
        Get a default hardcoded matrix when file loading fails.
        
        Args:
            matrix_type (str): Type of matrix to get.
            
        Returns:
            dict: Default matrix data.
        """
        if matrix_type == "nl_to_cl":
            return self._get_default_nl_to_cl_matrix()
        elif matrix_type == "cl_to_pailang":
            return self._get_default_cl_to_pailang_matrix()
        elif matrix_type == "pailang_to_cl":
            return self._get_default_pailang_to_cl_matrix()
        elif matrix_type == "cl_to_nl":
            return self._get_default_cl_to_nl_matrix()
        else:
            return {}
    
    def _get_default_nl_to_cl_matrix(self):
        """
        Get the default Natural Language to Command Language mapping matrix.
        
        Returns:
            dict: Default NL to CL mapping rules.
        """
        return {
            "patterns": [
                {
                    "pattern": "initialize {system} system",
                    "template": ">>> INITIALIZE [SYSTEM={system}]",
                    "examples": [
                        {"nl": "initialize AI system", "cl": ">>> INITIALIZE [SYSTEM=AI]"}
                    ]
                },
                {
                    "pattern": "set {context} context",
                    "template": ">>> SET_CONTEXT [{context}]",
                    "examples": [
                        {"nl": "set processing context", "cl": ">>> SET_CONTEXT [processing]"}
                    ]
                },
                {
                    "pattern": "execute {task} task",
                    "template": ">>> EXECUTE [TASK={task}]",
                    "examples": [
                        {"nl": "execute analysis task", "cl": ">>> EXECUTE [TASK=analysis]"}
                    ]
                },
                {
                    "pattern": "if {condition} then {action}",
                    "template": ">>> CONDITIONAL [CONDITION={condition}]\n    >>> {action}",
                    "examples": [
                        {
                            "nl": "if temperature exceeds threshold then activate cooling",
                            "cl": ">>> CONDITIONAL [CONDITION=temperature exceeds threshold]\n    >>> ACTIVATE [SYSTEM=cooling]"
                        }
                    ]
                }
            ]
        }
    
    def _get_default_cl_to_pailang_matrix(self):
        """
        Get the default Command Language to pAI_Lang mapping matrix.
        
        Returns:
            dict: Default CL to pAI_Lang mapping rules.
        """
        return {
            "commands": [
                {
                    "command": "INITIALIZE",
                    "parameters": ["SYSTEM"],
                    "pailang_template": "AI{system_id}",
                    "examples": [
                        {"cl": ">>> INITIALIZE [SYSTEM=AI]", "pailang": "AI4"}
                    ]
                },
                {
                    "command": "SET_CONTEXT",
                    "parameters": ["context"],
                    "pailang_template": "!C{context_id}",
                    "examples": [
                        {"cl": ">>> SET_CONTEXT [processing]", "pailang": "!C01"}
                    ]
                },
                {
                    "command": "EXECUTE",
                    "parameters": ["TASK"],
                    "pailang_template": "T{task_id}",
                    "examples": [
                        {"cl": ">>> EXECUTE [TASK=analysis]", "pailang": "T01"}
                    ]
                },
                {
                    "command": "CONDITIONAL",
                    "parameters": ["CONDITION"],
                    "subcommands": True,
                    "pailang_template": "Q{condition_id}?{true_action}:{false_action}",
                    "examples": [
                        {
                            "cl": ">>> CONDITIONAL [CONDITION=temperature exceeds threshold]\n    >>> ACTIVATE [SYSTEM=cooling]",
                            "pailang": "Q01?T01:T02"
                        }
                    ]
                }
            ]
        }
    
    def _get_default_pailang_to_cl_matrix(self):
        """
        Get the default pAI_Lang to Command Language mapping matrix.
        
        Returns:
            dict: Default pAI_Lang to CL mapping rules.
        """
        return {
            "tokens": [
                {
                    "pattern": "AI(\\d+)",
                    "template": ">>> INITIALIZE [SYSTEM=AI{system_id}]",
                    "examples": [
                        {"pailang": "AI4", "cl": ">>> INITIALIZE [SYSTEM=AI4]"}
                    ]
                },
                {
                    "pattern": "!C(\\d+)",
                    "template": ">>> SET_CONTEXT [CONTEXT={context_id}]",
                    "examples": [
                        {"pailang": "!C01", "cl": ">>> SET_CONTEXT [CONTEXT=01]"}
                    ]
                },
                {
                    "pattern": "T(\\d+)",
                    "template": ">>> EXECUTE [TASK={task_id}]",
                    "examples": [
                        {"pailang": "T01", "cl": ">>> EXECUTE [TASK=01]"}
                    ]
                },
                {
                    "pattern": "Q(\\d+)\\?(.*?):(.*)",
                    "template": ">>> CONDITIONAL [CONDITION={condition_id}]\n    >>> {true_action}\n>>> ELSE\n    >>> {false_action}",
                    "examples": [
                        {
                            "pailang": "Q01?T01:T02",
                            "cl": ">>> CONDITIONAL [CONDITION=01]\n    >>> EXECUTE [TASK=01]\n>>> ELSE\n    >>> EXECUTE [TASK=02]"
                        }
                    ]
                }
            ]
        }
    
    def _get_default_cl_to_nl_matrix(self):
        """
        Get the default Command Language to Natural Language mapping matrix.
        
        Returns:
            dict: Default CL to NL mapping rules.
        """
        return {
            "commands": [
                {
                    "command": "INITIALIZE",
                    "parameters": ["SYSTEM"],
                    "nl_template": "Initialize the {system} system",
                    "examples": [
                        {"cl": ">>> INITIALIZE [SYSTEM=AI4]", "nl": "Initialize the AI4 system"}
                    ]
                },
                {
                    "command": "SET_CONTEXT",
                    "parameters": ["CONTEXT"],
                    "nl_template": "Set the context to {context}",
                    "examples": [
                        {"cl": ">>> SET_CONTEXT [CONTEXT=01]", "nl": "Set the context to 01"}
                    ]
                },
                {
                    "command": "EXECUTE",
                    "parameters": ["TASK"],
                    "nl_template": "Execute task {task}",
                    "examples": [
                        {"cl": ">>> EXECUTE [TASK=01]", "nl": "Execute task 01"}
                    ]
                },
                {
                    "command": "CONDITIONAL",
                    "parameters": ["CONDITION"],
                    "nl_template": "If condition {condition} is true, then {true_action}; otherwise, {false_action}",
                    "examples": [
                        {
                            "cl": ">>> CONDITIONAL [CONDITION=01]\n    >>> EXECUTE [TASK=01]\n>>> ELSE\n    >>> EXECUTE [TASK=02]",
                            "nl": "If condition 01 is true, then execute task 01; otherwise, execute task 02"
                        }
                    ]
                }
            ]
        }
    
    def save_matrix(self, matrix_type, matrix_data):
        """
        Save a matrix to a JSON file.
        
        Args:
            matrix_type (str): Type of matrix to save ('nl_to_cl', 'cl_to_pailang', etc.)
            matrix_data (dict): Matrix data to save.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure the matrix directory exists
            os.makedirs(self.matrix_dir, exist_ok=True)
            
            # Save to JSON file
            json_path = os.path.join(self.matrix_dir, f"{matrix_type}.json")
            with open(json_path, 'w') as f:
                json.dump(matrix_data, f, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Error saving matrix to JSON: {e}")
            return False
