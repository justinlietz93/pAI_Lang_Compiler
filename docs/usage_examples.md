# Usage Examples

This document provides examples of how to use the pAI_Lang tooling system.

## Basic Usage

### Compiling Natural Language to pAI_Lang

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Compile Natural Language to pAI_Lang
nl_text = "Retrieve customer data and generate a report"
pailang_text = api.compile(nl_text, input_type="NL")
print(pailang_text)
```

### Decoding pAI_Lang to Command Language

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Decode pAI_Lang to Command Language
pailang_text = "T12>D45"
cl_text = api.decode(pailang_text, output_type="CL")
print(cl_text)
```

### Direct Transformation Between Language Forms

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Transform Natural Language to Command Language
nl_text = "Retrieve customer data and generate a report"
cl_text = api.nl_to_cl(nl_text)
print(cl_text)

# Transform Command Language to pAI_Lang
pailang_text = api.cl_to_pailang(cl_text)
print(pailang_text)

# Transform pAI_Lang to Command Language
cl_text = api.pailang_to_cl(pailang_text)
print(cl_text)

# Transform Command Language to Natural Language
nl_text = api.cl_to_nl(cl_text)
print(nl_text)
```

## Advanced Usage

### Working with Context

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Set context and compile
nl_text = "In the context of financial reporting, generate quarterly summary"
pailang_text = api.compile(nl_text, input_type="NL")
print(pailang_text)
```

### Using Conditional Expressions

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Compile conditional expression
nl_text = "If data is available, generate report, otherwise notify administrator"
pailang_text = api.compile(nl_text, input_type="NL")
print(pailang_text)
```

### Parallel Execution

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Compile parallel execution
nl_text = "Simultaneously fetch user data and prepare report template"
pailang_text = api.compile(nl_text, input_type="NL")
print(pailang_text)
```

## Working with Components Directly

### Using the Compiler

```python
from pailang_tooling.compiler.compiler import Compiler

# Initialize the compiler
compiler = Compiler()

# Compile Natural Language to pAI_Lang
nl_text = "Retrieve customer data and generate a report"
pailang_text = compiler.compile_nl(nl_text)
print(pailang_text)
```

### Using the Decoder

```python
from pailang_tooling.decoder.decoder import Decoder

# Initialize the decoder
decoder = Decoder()

# Decode pAI_Lang to Natural Language
pailang_text = "T12>D45"
nl_text = decoder.decode_to_nl(pailang_text)
print(nl_text)
```

### Using the Transformer

```python
from pailang_tooling.transformer.transformer import MatricesTransformer

# Initialize the transformer
transformer = MatricesTransformer()

# Transform Natural Language to Command Language
nl_text = "Retrieve customer data and generate a report"
cl_text = transformer.nl_to_cl(nl_text)
print(cl_text)
```

## File Processing

```python
from pailang_tooling.api import PAILangTooling
import os

# Initialize the API
api = PAILangTooling()

# Create example directory
examples_dir = "examples"
os.makedirs(examples_dir, exist_ok=True)

# Create example input file
with open(os.path.join(examples_dir, "nl_input.txt"), "w") as f:
    f.write("Initialize AI system\nSet processing context\nExecute analysis task")

# Process file: NL to pAI_Lang
api.process_file(
    os.path.join(examples_dir, "nl_input.txt"),
    os.path.join(examples_dir, "nl_to_pailang.txt"),
    input_type="NL",
    output_type="pAI_Lang"
)

# Read and print the result
with open(os.path.join(examples_dir, "nl_to_pailang.txt"), "r") as f:
    print(f.read())
```

## Token Management

```python
from pailang_tooling.api import PAILangTooling

# Initialize the API
api = PAILangTooling()

# Get token ID for a value
value = "initialize_system"
category = "System"
token_id = api.get_token_id(value, category)
print(f"Token ID for '{value}' in category '{category}': {token_id}")

# Register a new token
new_value = "custom_operation"
new_category = "Operation"
new_token_id = "O1"
success = api.register_token(new_value, new_category, new_token_id)
print(f"Registered token '{new_token_id}' for '{new_value}' in category '{new_category}': {success}")

# Get value from token
retrieved_value, retrieved_category = api.get_value_from_token(token_id)
print(f"Value and category for token '{token_id}': {retrieved_value}, {retrieved_category}")
```
