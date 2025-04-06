# API Reference

## PAILangTooling

The main API class for interacting with the pAI_Lang tooling system.

### Methods

#### `compile(input_text, input_type="NL")`
Compiles input text from Natural Language (NL) or Command Language (CL) to pAI_Lang.

**Parameters:**
- `input_text` (str): The input text to compile
- `input_type` (str): The format of the input text ('NL' or 'CL')

**Returns:**
- `str`: The compiled pAI_Lang string

#### `decode(pailang_text, output_type="CL")`
Decodes pAI_Lang text to Natural Language (NL) or Command Language (CL).

**Parameters:**
- `pailang_text` (str): The pAI_Lang text to decode
- `output_type` (str): The target format ('CL' or 'NL')

**Returns:**
- `str`: The decoded text in the target format

#### `nl_to_cl(nl_text)`
Transform Natural Language to Command Language.

**Parameters:**
- `nl_text` (str): Natural Language text

**Returns:**
- `str`: Command Language text

#### `cl_to_pailang(cl_text)`
Transform Command Language to pAI_Lang.

**Parameters:**
- `cl_text` (str): Command Language text

**Returns:**
- `str`: pAI_Lang text

#### `pailang_to_cl(pailang_text)`
Transform pAI_Lang to Command Language.

**Parameters:**
- `pailang_text` (str): pAI_Lang text

**Returns:**
- `str`: Command Language text

#### `cl_to_nl(cl_text)`
Transform Command Language to Natural Language.

**Parameters:**
- `cl_text` (str): Command Language text

**Returns:**
- `str`: Natural Language text

#### `get_token_id(value, category)`
Get a token ID for a value in a specific category.

**Parameters:**
- `value` (str): The value to get a token ID for
- `category` (str): The category of the token

**Returns:**
- `str`: The token ID

#### `register_token(value, category, token_id)`
Register a token ID for a value in a specific category.

**Parameters:**
- `value` (str): The value to register
- `category` (str): The category of the token
- `token_id` (str): The token ID to register

**Returns:**
- `bool`: True if registration was successful, False otherwise

#### `get_value_from_token(token)`
Get the value associated with a token ID.

**Parameters:**
- `token` (str): The token ID to look up

**Returns:**
- `tuple`: (value, category) if found, (None, None) otherwise

#### `process_file(input_file, output_file, input_type="NL", output_type="pAI_Lang")`
Process a file, converting its content from one language representation to another.

**Parameters:**
- `input_file` (str): Path to input file
- `output_file` (str): Path to output file
- `input_type` (str): Type of input text ('NL', 'CL', or 'pAI_Lang')
- `output_type` (str): Type of output text ('NL', 'CL', or 'pAI_Lang')

**Returns:**
- `bool`: True if processing was successful, False otherwise

## Compiler

### Compiler

The class for the compiler component.

### Methods

#### `compile(input_text, input_type="NL")`
Compiles input text to pAI_Lang.

**Parameters:**
- `input_text` (str): The input text to compile
- `input_type` (str): The format of the input text ('NL' or 'CL')

**Returns:**
- `str`: The compiled pAI_Lang string

#### `compile_nl(nl_text)`
Compiles Natural Language text to pAI_Lang.

**Parameters:**
- `nl_text` (str): The Natural Language text to compile

**Returns:**
- `str`: The compiled pAI_Lang string

#### `compile_cl(cl_text)`
Compiles Command Language text to pAI_Lang.

**Parameters:**
- `cl_text` (str): The Command Language text to compile

**Returns:**
- `str`: The compiled pAI_Lang string

## Decoder

### Decoder

The class for the decoder component.

### Methods

#### `decode(pailang_text, output_type="CL")`
Decodes pAI_Lang text to the specified output format.

**Parameters:**
- `pailang_text` (str): The pAI_Lang text to decode
- `output_type` (str): The target format ('CL' or 'NL')

**Returns:**
- `str`: The decoded text in the target format

#### `decode_to_nl(pailang_text)`
Decodes pAI_Lang text to Natural Language.

**Parameters:**
- `pailang_text` (str): The pAI_Lang text to decode

**Returns:**
- `str`: The decoded Natural Language text

#### `decode_to_cl(pailang_text)`
Decodes pAI_Lang text to Command Language.

**Parameters:**
- `pailang_text` (str): The pAI_Lang text to decode

**Returns:**
- `str`: The decoded Command Language text

## Transformer

### MatricesTransformer

The class for the transformer component.

### Methods

#### `nl_to_cl(nl_text)`
Transform Natural Language to Command Language.

**Parameters:**
- `nl_text` (str): Natural Language text

**Returns:**
- `str`: Command Language text

#### `cl_to_pailang(cl_text)`
Transform Command Language to pAI_Lang.

**Parameters:**
- `cl_text` (str): Command Language text

**Returns:**
- `str`: pAI_Lang text

#### `pailang_to_cl(pailang_text)`
Transform pAI_Lang to Command Language.

**Parameters:**
- `pailang_text` (str): pAI_Lang text

**Returns:**
- `str`: Command Language text

#### `cl_to_nl(cl_text)`
Transform Command Language to Natural Language.

**Parameters:**
- `cl_text` (str): Command Language text

**Returns:**
- `str`: Natural Language text
