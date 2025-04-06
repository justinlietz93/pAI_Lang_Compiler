# pAI_Lang Tooling

A comprehensive tooling system for the Promethean AI Language (pAI_Lang), a novel token compression language designed to significantly compress verbose natural language instructions or technical specifications into a highly compact, symbolic representation.

## Overview

The pAI_Lang tooling system provides:

1. **Compiler**: Converts Natural Language (NL) or Command Language (CL) to pAI_Lang
2. **Decoder**: Converts pAI_Lang back to Natural Language or Command Language
3. **Transformer**: Provides bidirectional mapping between different language forms
4. **API**: Unified interface for all pAI_Lang operations

## Installation

```bash
pip install pailang_tooling
```

Or install from source:

```bash
git clone https://github.com/example/pailang_tooling.git
cd pailang_tooling
pip install -e .
```

## Usage

### Basic Usage

```python
from pailang_tooling.api import PAILangAPI

# Initialize the API
api = PAILangAPI()

# Compile Natural Language to pAI_Lang
nl_input = "initialize AI system with processing context"
pailang = api.compile_nl(nl_input)
print(f"pAI_Lang: {pailang}")

# Decode pAI_Lang back to Natural Language
nl_output = api.decode_to_nl(pailang)
print(f"Natural Language: {nl_output}")

# Transform between different formats
cl = api.transform(nl_input, "nl", "cl")
print(f"Command Language: {cl}")
```

### Advanced Usage

```python
from pailang_tooling.compiler.compiler import Compiler
from pailang_tooling.decoder.decoder import Decoder
from pailang_tooling.transformer.transformer import MatricesTransformer

# Initialize components
compiler = Compiler()
decoder = Decoder()
transformer = MatricesTransformer()

# Compile Natural Language to pAI_Lang with custom options
pailang = compiler.compile_nl(nl_input, optimize=True)

# Decode pAI_Lang to Command Language with custom options
cl_output = decoder.decode_to_cl(pailang, verbose=True)

# Add custom matrix entries
transformer.add_matrix_entry("nl_to_cl", {
    "pattern": "perform {task} on {resource}",
    "template": ">>> EXECUTE [TASK={task}, RESOURCE={resource}]"
})
```

## Components

### Compiler

The compiler converts Natural Language or Command Language to pAI_Lang through:

1. **Parser**: Parses input text into structured representations
2. **Semantic Analyzer**: Analyzes parsed content and generates token mappings
3. **Structure Synthesizer**: Synthesizes pAI_Lang from semantic analysis

### Decoder

The decoder converts pAI_Lang back to Natural Language or Command Language through:

1. **pAI_Lang Parser**: Parses pAI_Lang into structured representations
2. **Context Manager**: Manages context activation and token resolution
3. **Expansion Engine**: Expands pAI_Lang tokens into intermediate forms
4. **NL Generator**: Generates Natural Language from intermediate forms

### Transformer

The transformer provides bidirectional mapping between different language forms:

1. **NL to CL**: Transforms Natural Language to Command Language
2. **CL to pAI_Lang**: Transforms Command Language to pAI_Lang
3. **pAI_Lang to CL**: Transforms pAI_Lang to Command Language
4. **CL to NL**: Transforms Command Language to Natural Language

## License

MIT License
