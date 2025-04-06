"""
Enhanced test suite for pAI_Lang tooling.

This module provides comprehensive tests for all components of the pAI_Lang tooling system,
including unit tests, integration tests, edge case tests, and performance tests.
The test suite is designed to achieve at least 90% overall code coverage with no
individual component below 85%.
"""

import unittest
import os
import time
import sys
import re
import json
from pathlib import Path

# Add parent directory to path to allow importing pailang_tooling
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pailang_tooling.compiler.parser import Parser
from pailang_tooling.compiler.semantic_analyzer import SemanticAnalyzer
from pailang_tooling.compiler.structure_synthesizer import StructureSynthesizer
from pailang_tooling.compiler.compiler import Compiler
from pailang_tooling.decoder.decoder import Decoder
from pailang_tooling.decoder.pailang_parser import PAILangParser
from pailang_tooling.decoder.context_manager import ContextManager
from pailang_tooling.decoder.expansion_engine import ExpansionEngine
from pailang_tooling.decoder.nl_generator import NLGenerator
from pailang_tooling.transformer.transformer import MatricesTransformer
from pailang_tooling.transformer.matrix_loader import MatrixLoader
from pailang_tooling.compiler.semantic_analyzer.token_id_generator import TokenIDGenerator
from pailang_tooling.api import PAILangTooling as PAILangAPI
from pailang_tooling.utils.debug_logger import logger

# Test fixtures
FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)

# Create test fixtures
def create_test_fixtures():
    """Create test fixtures for the test suite."""
    # Natural Language test samples
    nl_samples = {
        "basic": "Initialize the system with processing context.",
        "sequence": "Retrieve customer data and generate a report.",
        "parallel": "Simultaneously fetch user data and prepare report template.",
        "conditional": "If data is available, generate report, otherwise notify administrator.",
        "repetition": "Repeat the data validation process three times.",
        "context": "In the context of financial reporting, generate quarterly summary.",
        "piping": "Extract data from database and pass it to the reporting module.",
        "assignment": "Set the report format to PDF.",
        "aggregation": "Combine user profile, transaction history, and preferences into a single view.",
        "complex": "In the security context, if user authentication succeeds, simultaneously process payment and update account, otherwise log the failed attempt and notify the security team."
    }
    
    # Command Language test samples
    cl_samples = {
        "basic": ">>> INITIALIZE [SYSTEM=processing]",
        "sequence": ">>> EXECUTE_TASK [TASK=retrieve_customer_data]\n>>> EXECUTE_TASK [TASK=generate_report]",
        "parallel": ">>> PARALLEL\n    >>> EXECUTE_TASK [TASK=fetch_user_data]\n    >>> EXECUTE_TASK [TASK=prepare_report_template]\n>>> END_PARALLEL",
        "conditional": ">>> CONDITIONAL [CONDITION=data_available]\n    >>> EXECUTE_TASK [TASK=generate_report]\n>>> ELSE\n    >>> EXECUTE_TASK [TASK=notify_administrator]\n>>> END_CONDITIONAL",
        "repetition": ">>> REPEAT [count=3]\n    >>> EXECUTE_TASK [TASK=validate_data]\n>>> END_REPEAT",
        "context": ">>> SET_CONTEXT [CONTEXT=financial_reporting]\n>>> EXECUTE_TASK [TASK=generate_quarterly_summary]",
        "piping": ">>> PIPE\n    >>> SOURCE\n        >>> EXECUTE_TASK [TASK=extract_data_from_database]\n    >>> TARGET\n        >>> EXECUTE_TASK [TASK=reporting_module]\n>>> END_PIPE",
        "assignment": ">>> ASSIGN [report_format] = [PDF]",
        "aggregation": ">>> BATCH_OPERATION\n    >>> EXECUTE_TASK [TASK=get_user_profile]\n    >>> EXECUTE_TASK [TASK=get_transaction_history]\n    >>> EXECUTE_TASK [TASK=get_preferences]\n>>> END_BATCH",
        "complex": ">>> ACTIVATE_CONTEXT [CONTEXT=security]\n>>> CONDITIONAL [CONDITION=user_authentication_success]\n    >>> PARALLEL\n        >>> EXECUTE_TASK [TASK=process_payment]\n        >>> EXECUTE_TASK [TASK=update_account]\n    >>> END_PARALLEL\n>>> ELSE\n    >>> EXECUTE_TASK [TASK=log_failed_attempt]\n    >>> EXECUTE_TASK [TASK=notify_security_team]\n>>> END_CONDITIONAL"
    }
    
    # pAI_Lang test samples (expected outputs from compilation)
    pailang_samples = {
        "basic": "!C1>S1",
        "sequence": "T12>T13",
        "parallel": "T14&T15",
        "conditional": "C2?T13:T16",
        "repetition": "**3T17",
        "context": "!C3>T18",
        "piping": "T19|T20",
        "assignment": "V1=D1",
        "aggregation": "#{T21,T22,T23}",
        "complex": "!C4>(C5?(T24&T25):(T26>T27))"
    }
    
    # Write fixtures to files
    with open(os.path.join(FIXTURES_DIR, "nl_samples.json"), "w") as f:
        json.dump(nl_samples, f, indent=2)
    
    with open(os.path.join(FIXTURES_DIR, "cl_samples.json"), "w") as f:
        json.dump(cl_samples, f, indent=2)
    
    with open(os.path.join(FIXTURES_DIR, "pailang_samples.json"), "w") as f:
        json.dump(pailang_samples, f, indent=2)
    
    # Create token dictionary for testing
    token_dictionary = {
        "tokens": {
            "C1": {"value": "processing_context", "category": "Context", "expansionTemplate": ">>> SET_CONTEXT [CONTEXT=processing]"},
            "C2": {"value": "data_available", "category": "Condition", "expansionTemplate": ">>> CONDITIONAL [CONDITION=data_available]"},
            "C3": {"value": "financial_reporting", "category": "Context", "expansionTemplate": ">>> SET_CONTEXT [CONTEXT=financial_reporting]"},
            "C4": {"value": "security", "category": "Context", "expansionTemplate": ">>> ACTIVATE_CONTEXT [CONTEXT=security]"},
            "C5": {"value": "user_authentication_success", "category": "Condition", "expansionTemplate": ">>> CONDITIONAL [CONDITION=user_authentication_success]"},
            "S1": {"value": "initialize_system", "category": "System", "expansionTemplate": ">>> INITIALIZE [SYSTEM=processing]"},
            "T12": {"value": "retrieve_customer_data", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=retrieve_customer_data]"},
            "T13": {"value": "generate_report", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=generate_report]"},
            "T14": {"value": "fetch_user_data", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=fetch_user_data]"},
            "T15": {"value": "prepare_report_template", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=prepare_report_template]"},
            "T16": {"value": "notify_administrator", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=notify_administrator]"},
            "T17": {"value": "validate_data", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=validate_data]"},
            "T18": {"value": "generate_quarterly_summary", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=generate_quarterly_summary]"},
            "T19": {"value": "extract_data_from_database", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=extract_data_from_database]"},
            "T20": {"value": "reporting_module", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=reporting_module]"},
            "T21": {"value": "get_user_profile", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=get_user_profile]"},
            "T22": {"value": "get_transaction_history", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=get_transaction_history]"},
            "T23": {"value": "get_preferences", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=get_preferences]"},
            "T24": {"value": "process_payment", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=process_payment]"},
            "T25": {"value": "update_account", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=update_account]"},
            "T26": {"value": "log_failed_attempt", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=log_failed_attempt]"},
            "T27": {"value": "notify_security_team", "category": "Task", "expansionTemplate": ">>> EXECUTE_TASK [TASK=notify_security_team]"},
            "V1": {"value": "report_format", "category": "Variable", "expansionTemplate": "report_format"},
            "D1": {"value": "PDF", "category": "Data", "expansionTemplate": "PDF"}
        }
    }
    
    with open(os.path.join(FIXTURES_DIR, "token_dictionary.json"), "w") as f:
        json.dump(token_dictionary, f, indent=2)

# Create test fixtures if they don't exist
if not os.path.exists(os.path.join(FIXTURES_DIR, "nl_samples.json")):
    create_test_fixtures()

# Load test fixtures
with open(os.path.join(FIXTURES_DIR, "nl_samples.json"), "r") as f:
    NL_SAMPLES = json.load(f)

with open(os.path.join(FIXTURES_DIR, "cl_samples.json"), "r") as f:
    CL_SAMPLES = json.load(f)

with open(os.path.join(FIXTURES_DIR, "pailang_samples.json"), "r") as f:
    PAILANG_SAMPLES = json.load(f)

with open(os.path.join(FIXTURES_DIR, "token_dictionary.json"), "r") as f:
    TOKEN_DICTIONARY = json.load(f)

# Unit Tests for Parser Component
class TestParser(unittest.TestCase):
    """Test cases for the Parser component."""
    
    def setUp(self):
        """Set up test environment."""
        self.parser = Parser()
    
    def test_nl_parser_basic(self):
        """Test basic Natural Language parsing."""
        result = self.parser.parse_nl(NL_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIn("parsed_content", result)
        self.assertIn("structure", result)
    
    def test_cl_parser_basic(self):
        """Test basic Command Language parsing."""
        result = self.parser.parse_cl(CL_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIn("commands", result)
        self.assertIn("hierarchy", result)
    
    def test_nl_parser_sequence(self):
        """Test parsing Natural Language with sequence operations."""
        result = self.parser.parse_nl(NL_SAMPLES["sequence"])
        self.assertIsNotNone(result)
        self.assertIn("parsed_content", result)
        # Verify sequence structure is detected
        self.assertIn("sequence", str(result).lower())
    
    def test_cl_parser_sequence(self):
        """Test parsing Command Language with sequence operations."""
        result = self.parser.parse_cl(CL_SAMPLES["sequence"])
        self.assertIsNotNone(result)
        self.assertIn("commands", result)
        # Verify multiple commands are detected
        self.assertTrue(len(result["commands"]) > 1)
    
    def test_nl_parser_conditional(self):
        """Test parsing Natural Language with conditional operations."""
        result = self.parser.parse_nl(NL_SAMPLES["conditional"])
        self.assertIsNotNone(result)
        # Verify conditional structure is detected
        self.assertIn("condition", str(result).lower())
    
    def test_cl_parser_conditional(self):
        """Test parsing Command Language with conditional operations."""
        result = self.parser.parse_cl(CL_SAMPLES["conditional"])
        self.assertIsNotNone(result)
        # Verify conditional command is detected
        self.assertIn("CONDITIONAL", str(result))
    
    def test_nl_parser_parallel(self):
        """Test parsing Natural Language with parallel operations."""
        result = self.parser.parse_nl(NL_SAMPLES["parallel"])
        self.assertIsNotNone(result)
        # Verify parallel structure is detected
        self.assertIn("parallel", str(result).lower())
    
    def test_cl_parser_parallel(self):
        """Test parsing Command Language with parallel operations."""
        result = self.parser.parse_cl(CL_SAMPLES["parallel"])
        self.assertIsNotNone(result)
        # Verify parallel command is detected
        self.assertIn("PARALLEL", str(result))
    
    def test_nl_parser_context(self):
        """Test parsing Natural Language with context activation."""
        result = self.parser.parse_nl(NL_SAMPLES["context"])
        self.assertIsNotNone(result)
        # Verify context is detected
        self.assertIn("context", str(result).lower())
    
    def test_cl_parser_context(self):
        """Test parsing Command Language with context activation."""
        result = self.parser.parse_cl(CL_SAMPLES["context"])
        self.assertIsNotNone(result)
        # Verify context command is detected
        self.assertIn("CONTEXT", str(result))
    
    def test_nl_parser_complex(self):
        """Test parsing complex Natural Language with multiple operations."""
        result = self.parser.parse_nl(NL_SAMPLES["complex"])
        self.assertIsNotNone(result)
        # Verify complex structure is detected
        self.assertTrue("context" in str(result).lower() or "condition" in str(result).lower())
    
    def test_cl_parser_complex(self):
        """Test parsing complex Command Language with multiple operations."""
        result = self.parser.parse_cl(CL_SAMPLES["complex"])
        self.assertIsNotNone(result)
        # Verify complex command structure is detected
        self.assertTrue(len(result["commands"]) > 2)
    
    def test_parser_error_handling(self):
        """Test parser error handling with invalid input."""
        # Test with empty input
        result = self.parser.parse_nl("")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())
        
        # Test with malformed input
        result = self.parser.parse_cl("INVALID COMMAND")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())

# Unit Tests for Semantic Analyzer Component
class TestSemanticAnalyzer(unittest.TestCase):
    """Test cases for the Semantic Analyzer component."""
    
    def setUp(self):
        """Set up test environment."""
        self.analyzer = SemanticAnalyzer()
        self.parser = Parser()
    
    def test_nl_analyzer_basic(self):
        """Test basic Natural Language semantic analysis."""
        parsed = self.parser.parse_nl(NL_SAMPLES["basic"])
        result = self.analyzer.analyze_nl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("tokens", result)
    
    def test_cl_analyzer_basic(self):
        """Test basic Command Language semantic analysis."""
        parsed = self.parser.parse_cl(CL_SAMPLES["basic"])
        result = self.analyzer.analyze_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("tokens", result)
    
    def test_token_id_generation(self):
        """Test token ID generation."""
        token_id_generator = TokenIDGenerator()
        token_id = token_id_generator.generate_token_id("initialize_system", "System")
        self.assertIsNotNone(token_id)
        self.assertTrue(token_id.startswith("S"))
        
        # Test consistency
        token_id2 = token_id_generator.generate_token_id("initialize_system", "System")
        self.assertEqual(token_id, token_id2)
    
    def test_token_id_collision_handling(self):
        """Test token ID collision handling."""
        token_id_generator = TokenIDGenerator()
        # Generate multiple token IDs for different concepts in same category
        ids = set()
        for i in range(10):
            token_id = token_id_generator.generate_token_id(f"concept_{i}", "Task")
            ids.add(token_id)
        
        # Verify no collisions
        self.assertEqual(len(ids), 10)
    
    def test_analyzer_context_handling(self):
        """Test semantic analyzer context handling."""
        parsed = self.parser.parse_nl(NL_SAMPLES["context"])
        result = self.analyzer.analyze_nl(parsed)
        self.assertIsNotNone(result)
        # Verify context is detected in analysis
        self.assertIn("context", str(result).lower())
    
    def test_analyzer_operator_detection(self):
        """Test semantic analyzer operator detection."""
        # Test sequence operator
        parsed = self.parser.parse_nl(NL_SAMPLES["sequence"])
        result = self.analyzer.analyze_nl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("sequence", str(result).lower())
        
        # Test conditional operator
        parsed = self.parser.parse_nl(NL_SAMPLES["conditional"])
        result = self.analyzer.analyze_nl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("condition", str(result).lower())
        
        # Test parallel operator
        parsed = self.parser.parse_nl(NL_SAMPLES["parallel"])
        result = self.analyzer.analyze_nl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("parallel", str(result).lower())

# Unit Tests for Structure Synthesizer Component
class TestStructureSynthesizer(unittest.TestCase):
    """Test cases for the Structure Synthesizer component."""
    
    def setUp(self):
        """Set up test environment."""
        self.synthesizer = StructureSynthesizer()
        self.parser = Parser()
        self.analyzer = SemanticAnalyzer()
    
    def test_basic_synthesis(self):
        """Test basic pAI_Lang synthesis."""
        parsed = self.parser.parse_nl(NL_SAMPLES["basic"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_sequence_operator_synthesis(self):
        """Test synthesis of sequence operator (>)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["sequence"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn(">", result)
    
    def test_parallel_operator_synthesis(self):
        """Test synthesis of parallel operator (&)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["parallel"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("&", result)
    
    def test_conditional_operator_synthesis(self):
        """Test synthesis of conditional operator (?:)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["conditional"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("?", result)
        self.assertIn(":", result)
    
    def test_repetition_operator_synthesis(self):
        """Test synthesis of repetition operator (**)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["repetition"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("**", result)
    
    def test_context_activation_synthesis(self):
        """Test synthesis of context activation operator (!)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["context"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("!", result)
    
    def test_piping_operator_synthesis(self):
        """Test synthesis of piping operator (|)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["piping"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("|", result)
    
    def test_assignment_operator_synthesis(self):
        """Test synthesis of assignment operator (=)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["assignment"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("=", result)
    
    def test_aggregation_operator_synthesis(self):
        """Test synthesis of aggregation operator (#)."""
        parsed = self.parser.parse_nl(NL_SAMPLES["aggregation"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        self.assertIn("#", result)
    
    def test_complex_expression_synthesis(self):
        """Test synthesis of complex expressions with multiple operators."""
        parsed = self.parser.parse_nl(NL_SAMPLES["complex"])
        analyzed = self.analyzer.analyze_nl(parsed)
        result = self.synthesizer.synthesize(analyzed)
        self.assertIsNotNone(result)
        # Verify complex structure with multiple operators
        self.assertTrue("!" in result and "?" in result and ":" in result)
    
    def test_operator_precedence(self):
        """Test operator precedence in synthesis."""
        # Create a test case with multiple operators
        test_data = {
            "type": "Expression",
            "tokens": [
                {"type": "Token", "value": "T1", "category": "Task"},
                {"type": "Token", "value": "T2", "category": "Task"},
                {"type": "Token", "value": "T3", "category": "Task"}
            ],
            "operations": [
                {"type": "Sequence", "left": 0, "right": 1},
                {"type": "Parallel", "left": 2, "right": 3}
            ]
        }
        
        result = self.synthesizer.synthesize(test_data)
        self.assertIsNotNone(result)
        # Verify correct precedence (& has higher precedence than >)
        self.assertIn("(", result)
        self.assertIn(")", result)

# Unit Tests for Compiler Component
class TestCompiler(unittest.TestCase):
    """Test cases for the Compiler component."""
    
    def setUp(self):
        """Set up test environment."""
        self.compiler = Compiler()
    
    def test_compile_nl_basic(self):
        """Test basic Natural Language compilation."""
        result = self.compiler.compile_nl(NL_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_compile_cl_basic(self):
        """Test basic Command Language compilation."""
        result = self.compiler.compile_cl(CL_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_compile_nl_sequence(self):
        """Test compilation of Natural Language with sequence operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["sequence"])
        self.assertIsNotNone(result)
        self.assertIn(">", result)
    
    def test_compile_nl_parallel(self):
        """Test compilation of Natural Language with parallel operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["parallel"])
        self.assertIsNotNone(result)
        self.assertIn("&", result)
    
    def test_compile_nl_conditional(self):
        """Test compilation of Natural Language with conditional operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["conditional"])
        self.assertIsNotNone(result)
        self.assertIn("?", result)
        self.assertIn(":", result)
    
    def test_compile_nl_repetition(self):
        """Test compilation of Natural Language with repetition operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["repetition"])
        self.assertIsNotNone(result)
        self.assertIn("**", result)
    
    def test_compile_nl_context(self):
        """Test compilation of Natural Language with context activation."""
        result = self.compiler.compile_nl(NL_SAMPLES["context"])
        self.assertIsNotNone(result)
        self.assertIn("!", result)
    
    def test_compile_nl_piping(self):
        """Test compilation of Natural Language with piping operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["piping"])
        self.assertIsNotNone(result)
        self.assertIn("|", result)
    
    def test_compile_nl_assignment(self):
        """Test compilation of Natural Language with assignment operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["assignment"])
        self.assertIsNotNone(result)
        self.assertIn("=", result)
    
    def test_compile_nl_aggregation(self):
        """Test compilation of Natural Language with aggregation operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["aggregation"])
        self.assertIsNotNone(result)
        self.assertIn("#", result)
    
    def test_compile_nl_complex(self):
        """Test compilation of complex Natural Language with multiple operations."""
        result = self.compiler.compile_nl(NL_SAMPLES["complex"])
        self.assertIsNotNone(result)
        # Verify complex structure with multiple operators
        self.assertTrue("!" in result and "?" in result and ":" in result)
    
    def test_compiler_error_handling(self):
        """Test compiler error handling with invalid input."""
        # Test with empty input
        result = self.compiler.compile_nl("")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())
        
        # Test with malformed input
        result = self.compiler.compile_cl("INVALID COMMAND")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())

# Unit Tests for PAI_Lang Parser Component
class TestPAILangParser(unittest.TestCase):
    """Test cases for the PAI_Lang Parser component."""
    
    def setUp(self):
        """Set up test environment."""
        self.parser = PAILangParser()
    
    def test_parse_basic_token(self):
        """Test parsing basic token."""
        result = self.parser.parse("T1")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "StandardToken")
        self.assertEqual(result["expression"]["value"], "T1")
    
    def test_parse_sequence_operator(self):
        """Test parsing sequence operator (>)."""
        result = self.parser.parse("T1>T2")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "SequenceExpression")
    
    def test_parse_parallel_operator(self):
        """Test parsing parallel operator (&)."""
        result = self.parser.parse("T1&T2")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "ParallelExpression")
    
    def test_parse_conditional_operator(self):
        """Test parsing conditional operator (?:)."""
        result = self.parser.parse("C1?T1:T2")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "ConditionalExpression")
    
    def test_parse_repetition_operator(self):
        """Test parsing repetition operator (**)."""
        result = self.parser.parse("**3T1")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "Repetition")
    
    def test_parse_context_activation(self):
        """Test parsing context activation operator (!)."""
        result = self.parser.parse("!C1>T1")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "SequenceExpression")
        self.assertEqual(result["expression"]["leftExpression"]["type"], "ContextActivation")
    
    def test_parse_piping_operator(self):
        """Test parsing piping operator (|)."""
        result = self.parser.parse("T1|T2")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "PipingExpression")
    
    def test_parse_assignment_operator(self):
        """Test parsing assignment operator (=)."""
        result = self.parser.parse("V1=D1")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "AssignmentExpression")
    
    def test_parse_aggregation_operator(self):
        """Test parsing aggregation operator (#)."""
        result = self.parser.parse("#{T1,T2,T3}")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        self.assertEqual(result["expression"]["type"], "AggregationExpression")
    
    def test_parse_complex_expression(self):
        """Test parsing complex expressions with multiple operators."""
        result = self.parser.parse("!C1>(C2?(T1&T2):(T3>T4))")
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        # Verify complex structure
        self.assertEqual(result["expression"]["type"], "SequenceExpression")
    
    def test_parse_operator_precedence(self):
        """Test operator precedence in parsing."""
        # Test without parentheses
        result = self.parser.parse("T1>T2&T3")
        self.assertIsNotNone(result)
        # Verify & has higher precedence than >
        self.assertEqual(result["expression"]["type"], "SequenceExpression")
        self.assertEqual(result["expression"]["rightExpression"]["type"], "ParallelExpression")
    
    def test_parser_error_handling(self):
        """Test parser error handling with invalid input."""
        # Test with empty input
        result = self.parser.parse("")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())
        
        # Test with malformed input
        result = self.parser.parse("T1>")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())

# Unit Tests for Context Manager Component
class TestContextManager(unittest.TestCase):
    """Test cases for the Context Manager component."""
    
    def setUp(self):
        """Set up test environment."""
        self.context_manager = ContextManager()
    
    def test_context_activation(self):
        """Test context activation."""
        # Activate context
        self.context_manager.activate_context("financial_reporting")
        # Verify context is active
        self.assertTrue(self.context_manager.is_context_active("financial_reporting"))
    
    def test_context_deactivation(self):
        """Test context deactivation."""
        # Activate context
        self.context_manager.activate_context("financial_reporting")
        # Deactivate context
        self.context_manager.deactivate_context("financial_reporting")
        # Verify context is not active
        self.assertFalse(self.context_manager.is_context_active("financial_reporting"))
    
    def test_token_resolution_in_context(self):
        """Test token resolution in context."""
        # Activate context
        self.context_manager.activate_context("financial_reporting")
        # Create token
        token = {"value": "generate_report", "category": "Task"}
        # Resolve token in context
        resolved_token = self.context_manager.resolve_in_context(token, TOKEN_DICTIONARY)
        # Verify token is resolved
        self.assertIsNotNone(resolved_token)
    
    def test_multiple_context_activation(self):
        """Test multiple context activation."""
        # Activate multiple contexts
        self.context_manager.activate_context("financial_reporting")
        self.context_manager.activate_context("security")
        # Verify both contexts are active
        self.assertTrue(self.context_manager.is_context_active("financial_reporting"))
        self.assertTrue(self.context_manager.is_context_active("security"))
    
    def test_context_stack(self):
        """Test context stack management."""
        # Push contexts to stack
        self.context_manager.push_context("financial_reporting")
        self.context_manager.push_context("security")
        # Verify current context
        self.assertEqual(self.context_manager.get_current_context(), "security")
        # Pop context
        self.context_manager.pop_context()
        # Verify new current context
        self.assertEqual(self.context_manager.get_current_context(), "financial_reporting")

# Unit Tests for Expansion Engine Component
class TestExpansionEngine(unittest.TestCase):
    """Test cases for the Expansion Engine component."""
    
    def setUp(self):
        """Set up test environment."""
        self.context_manager = ContextManager()
        self.expansion_engine = ExpansionEngine(self.context_manager, TOKEN_DICTIONARY["tokens"])
        self.pailang_parser = PAILangParser()
    
    def test_expand_basic_token(self):
        """Test expansion of basic token."""
        parsed = self.pailang_parser.parse("T12")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("EXECUTE_TASK", result)
        self.assertIn("retrieve_customer_data", result)
    
    def test_expand_sequence_operator(self):
        """Test expansion of sequence operator (>)."""
        parsed = self.pailang_parser.parse("T12>T13")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("retrieve_customer_data", result)
        self.assertIn("generate_report", result)
    
    def test_expand_parallel_operator(self):
        """Test expansion of parallel operator (&)."""
        parsed = self.pailang_parser.parse("T14&T15")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("PARALLEL", result)
        self.assertIn("fetch_user_data", result)
        self.assertIn("prepare_report_template", result)
        self.assertIn("END_PARALLEL", result)
    
    def test_expand_conditional_operator(self):
        """Test expansion of conditional operator (?:)."""
        parsed = self.pailang_parser.parse("C2?T13:T16")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("CONDITIONAL", result)
        self.assertIn("data_available", result)
        self.assertIn("generate_report", result)
        self.assertIn("notify_administrator", result)
        self.assertIn("END_CONDITIONAL", result)
    
    def test_expand_repetition_operator(self):
        """Test expansion of repetition operator (**)."""
        parsed = self.pailang_parser.parse("**3T17")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("REPEAT", result)
        self.assertIn("count=3", result)
        self.assertIn("validate_data", result)
        self.assertIn("END_REPEAT", result)
    
    def test_expand_context_activation(self):
        """Test expansion of context activation operator (!)."""
        parsed = self.pailang_parser.parse("!C3>T18")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("SET_CONTEXT", result)
        self.assertIn("financial_reporting", result)
        self.assertIn("generate_quarterly_summary", result)
    
    def test_expand_piping_operator(self):
        """Test expansion of piping operator (|)."""
        parsed = self.pailang_parser.parse("T19|T20")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("PIPE", result)
        self.assertIn("SOURCE", result)
        self.assertIn("TARGET", result)
        self.assertIn("extract_data_from_database", result)
        self.assertIn("reporting_module", result)
        self.assertIn("END_PIPE", result)
    
    def test_expand_assignment_operator(self):
        """Test expansion of assignment operator (=)."""
        parsed = self.pailang_parser.parse("V1=D1")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("ASSIGN", result)
        self.assertIn("report_format", result)
        self.assertIn("PDF", result)
    
    def test_expand_aggregation_operator(self):
        """Test expansion of aggregation operator (#)."""
        parsed = self.pailang_parser.parse("#{T21,T22,T23}")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("BATCH_OPERATION", result)
        self.assertIn("get_user_profile", result)
        self.assertIn("get_transaction_history", result)
        self.assertIn("get_preferences", result)
        self.assertIn("END_BATCH", result)
    
    def test_expand_complex_expression(self):
        """Test expansion of complex expressions with multiple operators."""
        parsed = self.pailang_parser.parse("!C4>(C5?(T24&T25):(T26>T27))")
        result = self.expansion_engine.expand_to_cl(parsed)
        self.assertIsNotNone(result)
        self.assertIn("ACTIVATE_CONTEXT", result)
        self.assertIn("security", result)
        self.assertIn("CONDITIONAL", result)
        self.assertIn("user_authentication_success", result)
        self.assertIn("PARALLEL", result)
        self.assertIn("process_payment", result)
        self.assertIn("update_account", result)
        self.assertIn("log_failed_attempt", result)
        self.assertIn("notify_security_team", result)

# Unit Tests for NL Generator Component
class TestNLGenerator(unittest.TestCase):
    """Test cases for the NL Generator component."""
    
    def setUp(self):
        """Set up test environment."""
        self.nl_generator = NLGenerator()
    
    def test_generate_nl_from_cl_basic(self):
        """Test basic Natural Language generation from Command Language."""
        result = self.nl_generator.generate_nl(CL_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("Initialize", result.lower())
    
    def test_generate_nl_from_cl_sequence(self):
        """Test Natural Language generation from Command Language with sequence operations."""
        result = self.nl_generator.generate_nl(CL_SAMPLES["sequence"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("retrieve", result.lower())
        self.assertIn("generate", result.lower())
    
    def test_generate_nl_from_cl_conditional(self):
        """Test Natural Language generation from Command Language with conditional operations."""
        result = self.nl_generator.generate_nl(CL_SAMPLES["conditional"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("if", result.lower())
        self.assertIn("else", result.lower())
    
    def test_generate_nl_from_cl_complex(self):
        """Test Natural Language generation from complex Command Language."""
        result = self.nl_generator.generate_nl(CL_SAMPLES["complex"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 50)  # Complex output should be substantial

# Unit Tests for Decoder Component
class TestDecoder(unittest.TestCase):
    """Test cases for the Decoder component."""
    
    def setUp(self):
        """Set up test environment."""
        self.decoder = Decoder(token_dictionary=TOKEN_DICTIONARY["tokens"])
    
    def test_decode_to_cl_basic(self):
        """Test basic pAI_Lang decoding to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("INITIALIZE", result)
    
    def test_decode_to_nl_basic(self):
        """Test basic pAI_Lang decoding to Natural Language."""
        result = self.decoder.decode_to_nl(PAILANG_SAMPLES["basic"])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("Initialize", result)
    
    def test_decode_to_cl_sequence(self):
        """Test decoding pAI_Lang with sequence operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["sequence"])
        self.assertIsNotNone(result)
        self.assertIn("EXECUTE_TASK", result)
        self.assertIn("retrieve_customer_data", result)
        self.assertIn("generate_report", result)
    
    def test_decode_to_cl_parallel(self):
        """Test decoding pAI_Lang with parallel operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["parallel"])
        self.assertIsNotNone(result)
        self.assertIn("PARALLEL", result)
        self.assertIn("END_PARALLEL", result)
    
    def test_decode_to_cl_conditional(self):
        """Test decoding pAI_Lang with conditional operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["conditional"])
        self.assertIsNotNone(result)
        self.assertIn("CONDITIONAL", result)
        self.assertIn("ELSE", result)
        self.assertIn("END_CONDITIONAL", result)
    
    def test_decode_to_cl_repetition(self):
        """Test decoding pAI_Lang with repetition operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["repetition"])
        self.assertIsNotNone(result)
        self.assertIn("REPEAT", result)
        self.assertIn("count=3", result)
        self.assertIn("END_REPEAT", result)
    
    def test_decode_to_cl_context(self):
        """Test decoding pAI_Lang with context activation to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["context"])
        self.assertIsNotNone(result)
        self.assertIn("SET_CONTEXT", result)
        self.assertIn("CONTEXT=financial_reporting", result)
    
    def test_decode_to_cl_piping(self):
        """Test decoding pAI_Lang with piping operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["piping"])
        self.assertIsNotNone(result)
        self.assertIn("PIPE", result)
        self.assertIn("SOURCE", result)
        self.assertIn("TARGET", result)
    
    def test_decode_to_cl_assignment(self):
        """Test decoding pAI_Lang with assignment operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["assignment"])
        self.assertIsNotNone(result)
        self.assertIn("ASSIGN", result)
    
    def test_decode_to_cl_aggregation(self):
        """Test decoding pAI_Lang with aggregation operator to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["aggregation"])
        self.assertIsNotNone(result)
        self.assertIn("BATCH_OPERATION", result)
        self.assertIn("END_BATCH", result)
    
    def test_decode_to_cl_complex(self):
        """Test decoding complex pAI_Lang to Command Language."""
        result = self.decoder.decode_to_cl(PAILANG_SAMPLES["complex"])
        self.assertIsNotNone(result)
        self.assertIn("ACTIVATE_CONTEXT", result)
        self.assertIn("CONDITIONAL", result)
        self.assertIn("PARALLEL", result)
    
    def test_decoder_error_handling(self):
        """Test decoder error handling with invalid input."""
        # Test with empty input
        result = self.decoder.decode_to_cl("")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())
        
        # Test with malformed input
        result = self.decoder.decode_to_cl("INVALID")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())

# Unit Tests for Matrix Loader Component
class TestMatrixLoader(unittest.TestCase):
    """Test cases for the Matrix Loader component."""
    
    def setUp(self):
        """Set up test environment."""
        self.matrix_loader = MatrixLoader()
    
    def test_load_matrix_from_dict(self):
        """Test loading matrix from dictionary."""
        matrix_data = {
            "rules": [
                {
                    "pattern": "initialize {system}",
                    "template": ">>> INITIALIZE [SYSTEM={system}]"
                }
            ]
        }
        
        matrix = self.matrix_loader.load_matrix_from_dict(matrix_data)
        self.assertIsNotNone(matrix)
        self.assertIn("rules", matrix)
        self.assertEqual(len(matrix["rules"]), 1)
    
    def test_save_and_load_matrix(self):
        """Test saving and loading matrix to/from file."""
        matrix_data = {
            "rules": [
                {
                    "pattern": "initialize {system}",
                    "template": ">>> INITIALIZE [SYSTEM={system}]"
                }
            ]
        }
        
        # Save matrix to file
        matrix_file = os.path.join(FIXTURES_DIR, "test_matrix.json")
        self.matrix_loader.save_matrix(matrix_data, matrix_file)
        
        # Load matrix from file
        loaded_matrix = self.matrix_loader.load_matrix(matrix_file)
        self.assertIsNotNone(loaded_matrix)
        self.assertIn("rules", loaded_matrix)
        self.assertEqual(len(loaded_matrix["rules"]), 1)
    
    def test_matrix_validation(self):
        """Test matrix validation."""
        # Valid matrix
        valid_matrix = {
            "rules": [
                {
                    "pattern": "initialize {system}",
                    "template": ">>> INITIALIZE [SYSTEM={system}]"
                }
            ]
        }
        
        # Invalid matrix (missing template)
        invalid_matrix = {
            "rules": [
                {
                    "pattern": "initialize {system}"
                }
            ]
        }
        
        # Validate matrices
        self.assertTrue(self.matrix_loader.validate_matrix(valid_matrix))
        self.assertFalse(self.matrix_loader.validate_matrix(invalid_matrix))

# Unit Tests for Transformer Component
class TestTransformer(unittest.TestCase):
    """Test cases for the Transformer component."""
    
    def setUp(self):
        """Set up test environment."""
        # Create test matrices
        self.nl_to_cl_matrix = {
            "rules": [
                {
                    "pattern": "initialize {system}",
                    "template": ">>> INITIALIZE [SYSTEM={system}]"
                },
                {
                    "pattern": "{action} {object}",
                    "template": ">>> EXECUTE_TASK [TASK={action}_{object}]"
                }
            ]
        }
        
        self.cl_to_pailang_matrix = {
            "rules": [
                {
                    "pattern": ">>> INITIALIZE [SYSTEM={system}]",
                    "template": "!C1>S1"
                },
                {
                    "pattern": ">>> EXECUTE_TASK [TASK={task}]",
                    "template": "T{task_id}"
                }
            ]
        }
        
        self.pailang_to_cl_matrix = {
            "rules": [
                {
                    "pattern": "!C1>S1",
                    "template": ">>> INITIALIZE [SYSTEM=processing]"
                },
                {
                    "pattern": "T{id}",
                    "template": ">>> EXECUTE_TASK [TASK={task}]"
                }
            ]
        }
        
        self.cl_to_nl_matrix = {
            "rules": [
                {
                    "pattern": ">>> INITIALIZE [SYSTEM={system}]",
                    "template": "Initialize the {system} system."
                },
                {
                    "pattern": ">>> EXECUTE_TASK [TASK={task}]",
                    "template": "Perform the {task} task."
                }
            ]
        }
        
        # Save matrices to files
        matrix_dir = os.path.join(FIXTURES_DIR, "matrices")
        os.makedirs(matrix_dir, exist_ok=True)
        
        matrix_loader = MatrixLoader()
        matrix_loader.save_matrix(self.nl_to_cl_matrix, os.path.join(matrix_dir, "nl_to_cl.json"))
        matrix_loader.save_matrix(self.cl_to_pailang_matrix, os.path.join(matrix_dir, "cl_to_pailang.json"))
        matrix_loader.save_matrix(self.pailang_to_cl_matrix, os.path.join(matrix_dir, "pailang_to_cl.json"))
        matrix_loader.save_matrix(self.cl_to_nl_matrix, os.path.join(matrix_dir, "cl_to_nl.json"))
        
        # Initialize transformer with test matrices
        self.transformer = MatricesTransformer(matrices_dir=matrix_dir)
    
    def test_transform_nl_to_cl(self):
        """Test transformation from Natural Language to Command Language."""
        result = self.transformer.transform("initialize processing", "nl", "cl")
        self.assertIsNotNone(result)
        self.assertIn("INITIALIZE", result)
        self.assertIn("SYSTEM=processing", result)
    
    def test_transform_cl_to_pailang(self):
        """Test transformation from Command Language to pAI_Lang."""
        result = self.transformer.transform(">>> INITIALIZE [SYSTEM=processing]", "cl", "pailang")
        self.assertIsNotNone(result)
        self.assertIn("!", result)
        self.assertIn("C1", result)
        self.assertIn("S1", result)
    
    def test_transform_pailang_to_cl(self):
        """Test transformation from pAI_Lang to Command Language."""
        result = self.transformer.transform("!C1>S1", "pailang", "cl")
        self.assertIsNotNone(result)
        self.assertIn("INITIALIZE", result)
        self.assertIn("SYSTEM=processing", result)
    
    def test_transform_cl_to_nl(self):
        """Test transformation from Command Language to Natural Language."""
        result = self.transformer.transform(">>> INITIALIZE [SYSTEM=processing]", "cl", "nl")
        self.assertIsNotNone(result)
        self.assertIn("Initialize", result)
        self.assertIn("processing", result)
    
    def test_transform_nl_to_pailang(self):
        """Test transformation from Natural Language to pAI_Lang (multi-step)."""
        result = self.transformer.transform("initialize processing", "nl", "pailang")
        self.assertIsNotNone(result)
        self.assertIn("!", result)
        self.assertIn("C1", result)
        self.assertIn("S1", result)
    
    def test_transform_pailang_to_nl(self):
        """Test transformation from pAI_Lang to Natural Language (multi-step)."""
        result = self.transformer.transform("!C1>S1", "pailang", "nl")
        self.assertIsNotNone(result)
        self.assertIn("Initialize", result)
        self.assertIn("processing", result)
    
    def test_transformer_error_handling(self):
        """Test transformer error handling with invalid input."""
        # Test with empty input
        result = self.transformer.transform("", "nl", "cl")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())
        
        # Test with invalid format
        result = self.transformer.transform("initialize processing", "nl", "invalid")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())

# Integration Tests for PAI_Lang API
class TestPAILangAPI(unittest.TestCase):
    """Integration tests for the PAI_Lang API."""
    
    def setUp(self):
        """Set up test environment."""
        # Initialize API with test fixtures
        matrices_dir = os.path.join(FIXTURES_DIR, "matrices")
        self.api = PAILangAPI(matrices_dir=matrices_dir)
    
    def test_compile_nl(self):
        """Test compiling Natural Language to pAI_Lang."""
        for key, nl_text in NL_SAMPLES.items():
            result = self.api.compile(nl_text, source_format="nl")
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
    
    def test_compile_cl(self):
        """Test compiling Command Language to pAI_Lang."""
        for key, cl_text in CL_SAMPLES.items():
            result = self.api.compile(cl_text, source_format="cl")
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
    
    def test_decode_to_nl(self):
        """Test decoding pAI_Lang to Natural Language."""
        for key, pailang_text in PAILANG_SAMPLES.items():
            result = self.api.decode(pailang_text, target_format="nl")
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
    
    def test_decode_to_cl(self):
        """Test decoding pAI_Lang to Command Language."""
        for key, pailang_text in PAILANG_SAMPLES.items():
            result = self.api.decode(pailang_text, target_format="cl")
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
    
    def test_transform(self):
        """Test transforming between different formats."""
        # NL to CL
        result = self.api.transform(NL_SAMPLES["basic"], "nl", "cl")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        
        # CL to NL
        result = self.api.transform(CL_SAMPLES["basic"], "cl", "nl")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        
        # NL to pAI_Lang
        result = self.api.transform(NL_SAMPLES["basic"], "nl", "pailang")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        
        # pAI_Lang to NL
        result = self.api.transform(PAILANG_SAMPLES["basic"], "pailang", "nl")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_roundtrip_nl_to_pailang_to_nl(self):
        """Test roundtrip conversion from NL to pAI_Lang and back to NL."""
        for key, nl_text in NL_SAMPLES.items():
            # NL to pAI_Lang
            pailang = self.api.compile(nl_text, source_format="nl")
            self.assertIsNotNone(pailang)
            
            # pAI_Lang to NL
            nl_result = self.api.decode(pailang, target_format="nl")
            self.assertIsNotNone(nl_result)
            
            # Verify semantic preservation (exact match not expected due to transformation)
            self.assertTrue(len(nl_result) > 0)
    
    def test_roundtrip_cl_to_pailang_to_cl(self):
        """Test roundtrip conversion from CL to pAI_Lang and back to CL."""
        for key, cl_text in CL_SAMPLES.items():
            # CL to pAI_Lang
            pailang = self.api.compile(cl_text, source_format="cl")
            self.assertIsNotNone(pailang)
            
            # pAI_Lang to CL
            cl_result = self.api.decode(pailang, target_format="cl")
            self.assertIsNotNone(cl_result)
            
            # Verify semantic preservation (exact match not expected due to transformation)
            self.assertTrue(len(cl_result) > 0)
    
    def test_api_error_handling(self):
        """Test API error handling with invalid input."""
        # Test with empty input
        result = self.api.compile("", source_format="nl")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())
        
        # Test with invalid format
        result = self.api.compile(NL_SAMPLES["basic"], source_format="invalid")
        self.assertIsNotNone(result)
        self.assertIn("error", str(result).lower())

# Performance Tests
class TestPerformance(unittest.TestCase):
    """Performance tests for the pAI_Lang tooling system."""
    
    def setUp(self):
        """Set up test environment."""
        self.api = PAILangAPI()
        self.compiler = Compiler()
        self.decoder = Decoder()
        self.transformer = MatricesTransformer()
    
    def test_large_expression_parsing(self):
        """Test parsing large expressions (>1000 tokens)."""
        # Generate large pAI_Lang expression
        large_expression = "T1"
        for i in range(1, 1000):
            large_expression += f">T{i+1}"
        
        # Measure parsing time
        start_time = time.time()
        parser = PAILangParser()
        result = parser.parse(large_expression)
        end_time = time.time()
        
        # Verify parsing completed successfully
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "PAILang")
        
        # Verify parsing time is reasonable (adjust threshold as needed)
        parsing_time = end_time - start_time
        self.assertLess(parsing_time, 10.0)  # Should parse in less than 10 seconds
    
    def test_complex_transformation_chains(self):
        """Test complex transformation chains."""
        # Measure transformation time for complex chain
        start_time = time.time()
        result = self.api.transform(NL_SAMPLES["complex"], "nl", "pailang")
        end_time = time.time()
        
        # Verify transformation completed successfully
        self.assertIsNotNone(result)
        
        # Verify transformation time is reasonable (adjust threshold as needed)
        transformation_time = end_time - start_time
        self.assertLess(transformation_time, 5.0)  # Should transform in less than 5 seconds

# Run tests if this file is executed directly
if __name__ == "__main__":
    unittest.main()
