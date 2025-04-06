"""
pAI_Lang Tooling Examples

This module contains example usage of the pAI_Lang tooling system,
demonstrating all pAI_Lang operators and features.
"""

import os
import sys

# Add parent directory to path to import pailang_tooling
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pailang_tooling.api import PAILangTooling

def run_examples():
    """
    Run examples demonstrating the pAI_Lang tooling system.
    """
    # Initialize the tooling system
    tooling = PAILangTooling()
    
    print("=== pAI_Lang Tooling Examples ===\n")
    
    # Example 1: Natural Language to pAI_Lang
    print("Example 1: Natural Language to pAI_Lang")
    nl_input = "initialize AI system"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    print()
    
    # Example 2: Command Language to pAI_Lang
    print("Example 2: Command Language to pAI_Lang")
    cl_input = ">>> INITIALIZE [SYSTEM=AI]"
    pailang = tooling.compile(cl_input, "CL")
    print(f"Input (CL): {cl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    print()
    
    # Example 3: pAI_Lang to Command Language
    print("Example 3: pAI_Lang to Command Language")
    pailang_input = "S1"
    cl_output = tooling.decode(pailang_input, "CL")
    print(f"Input (pAI_Lang): {pailang_input}")
    print(f"Output (CL): {cl_output}")
    print()
    
    # Example 4: pAI_Lang to Natural Language
    print("Example 4: pAI_Lang to Natural Language")
    pailang_input = "S1"
    nl_output = tooling.decode(pailang_input, "NL")
    print(f"Input (pAI_Lang): {pailang_input}")
    print(f"Output (NL): {nl_output}")
    print()
    
    # Example 5: Sequence Operator (>)
    print("Example 5: Sequence Operator (>)")
    nl_input = "Retrieve customer data and generate a report"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 6: Parallel Operator (&)
    print("Example 6: Parallel Operator (&)")
    nl_input = "Simultaneously fetch user data and prepare report template"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 7: Conditional Operator (?:)
    print("Example 7: Conditional Operator (?:)")
    nl_input = "If data is available, generate report, otherwise notify administrator"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 8: Repetition Operator (**)
    print("Example 8: Repetition Operator (**)")
    nl_input = "Repeat the data validation process three times"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 9: Context Activation Operator (!)
    print("Example 9: Context Activation Operator (!)")
    nl_input = "In the context of financial reporting, generate quarterly summary"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 10: Piping Operator (|)
    print("Example 10: Piping Operator (|)")
    nl_input = "Extract data from database and pass it to the reporting module"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 11: Assignment Operator (=)
    print("Example 11: Assignment Operator (=)")
    nl_input = "Set the report format to PDF"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 12: Aggregation Operator (#)
    print("Example 12: Aggregation Operator (#)")
    nl_input = "Combine user profile, transaction history, and preferences into a single view"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 13: Complex Nested Expression
    print("Example 13: Complex Nested Expression")
    nl_input = "In the security context, if user authentication succeeds, simultaneously process payment and update account, otherwise log the failed attempt and notify the security team"
    pailang = tooling.compile(nl_input, "NL")
    print(f"Input (NL): {nl_input}")
    print(f"Output (pAI_Lang): {pailang}")
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    print()
    
    # Example 14: Bidirectional Translation (Round-trip)
    print("Example 14: Bidirectional Translation (Round-trip)")
    nl_input = "Initialize AI system with processing context"
    print(f"Original (NL): {nl_input}")
    
    # NL -> pAI_Lang
    pailang = tooling.compile(nl_input, "NL")
    print(f"Compiled (pAI_Lang): {pailang}")
    
    # pAI_Lang -> CL
    cl_output = tooling.decode(pailang, "CL")
    print(f"Decoded (CL): {cl_output}")
    
    # CL -> NL
    nl_output = tooling.cl_to_nl(cl_output)
    print(f"Transformed (NL): {nl_output}")
    print()
    
    # Example 15: Direct Transformation
    print("Example 15: Direct Transformation")
    nl_input = "Execute analysis task on customer data"
    print(f"Original (NL): {nl_input}")
    
    # NL -> CL
    cl_output = tooling.nl_to_cl(nl_input)
    print(f"NL to CL: {cl_output}")
    
    # CL -> pAI_Lang
    pailang_output = tooling.cl_to_pailang(cl_output)
    print(f"CL to pAI_Lang: {pailang_output}")
    print()
    
    # Example 16: File Processing
    print("Example 16: File Processing")
    
    # Create example input files
    examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    os.makedirs(examples_dir, exist_ok=True)
    
    with open(os.path.join(examples_dir, "nl_input.txt"), "w") as f:
        f.write("Initialize AI system\nSet processing context\nExecute analysis task")
    
    with open(os.path.join(examples_dir, "cl_input.txt"), "w") as f:
        f.write(">>> INITIALIZE [SYSTEM=AI]\n>>> SET_CONTEXT [CONTEXT=processing]\n>>> EXECUTE [TASK=analysis]")
    
    with open(os.path.join(examples_dir, "pailang_input.txt"), "w") as f:
        f.write("S1>!C1>T1")
    
    # Process files
    tooling.process_file(
        os.path.join(examples_dir, "nl_input.txt"),
        os.path.join(examples_dir, "nl_to_pailang.txt"),
        "NL",
        "pAI_Lang"
    )
    
    tooling.process_file(
        os.path.join(examples_dir, "cl_input.txt"),
        os.path.join(examples_dir, "cl_to_pailang.txt"),
        "CL",
        "pAI_Lang"
    )
    
    tooling.process_file(
        os.path.join(examples_dir, "pailang_input.txt"),
        os.path.join(examples_dir, "pailang_to_cl.txt"),
        "pAI_Lang",
        "CL"
    )
    
    tooling.process_file(
        os.path.join(examples_dir, "pailang_input.txt"),
        os.path.join(examples_dir, "pailang_to_nl.txt"),
        "pAI_Lang",
        "NL"
    )
    
    print(f"Example files created in '{examples_dir}' directory:")
    print("- nl_input.txt: Natural Language input")
    print("- cl_input.txt: Command Language input")
    print("- pailang_input.txt: pAI_Lang input")
    print("- nl_to_pailang.txt: Natural Language compiled to pAI_Lang")
    print("- cl_to_pailang.txt: Command Language compiled to pAI_Lang")
    print("- pailang_to_cl.txt: pAI_Lang decoded to Command Language")
    print("- pailang_to_nl.txt: pAI_Lang decoded to Natural Language")
    print()
    
    # Example 17: Token Management
    print("Example 17: Token Management")
    
    # Get token ID for a value
    value = "initialize_system"
    category = "System"
    token_id = tooling.get_token_id(value, category)
    print(f"Token ID for '{value}' in category '{category}': {token_id}")
    
    # Register a new token
    new_value = "custom_operation"
    new_category = "Operation"
    new_token_id = "O1"
    success = tooling.register_token(new_value, new_category, new_token_id)
    print(f"Registered token '{new_token_id}' for '{new_value}' in category '{new_category}': {success}")
    
    # Get value from token
    retrieved_value, retrieved_category = tooling.get_value_from_token(token_id)
    print(f"Value and category for token '{token_id}': {retrieved_value}, {retrieved_category}")
    print()

if __name__ == "__main__":
    run_examples()
