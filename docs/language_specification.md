# pAI_Lang Language Specification

## Introduction

pAI_Lang is a token compression language designed for efficient representation of natural language instructions in a compact form. This document provides the formal specification for pAI_Lang syntax, semantics, and usage.

## Token Structure

### Standard Tokens

Standard tokens in pAI_Lang follow this format:
```
[CategoryCode][NumericIdentifier]
```

Where:
- `CategoryCode`: A single uppercase letter representing the token category
- `NumericIdentifier`: A numeric value uniquely identifying the token within its category

Example: `T12` (Task token with identifier 12)

### Complex Tokens

Complex tokens include additional type information:
```
[CategoryCode][TypePrefix]:[NumericIdentifier]
```

Where:
- `CategoryCode`: A single uppercase letter representing the token category
- `TypePrefix`: Additional type information for specialized tokens
- `NumericIdentifier`: A numeric value uniquely identifying the token within its category and type

Example: `D:SQL:45` (Data token with SQL type and identifier 45)

## Operators

pAI_Lang supports the following operators:

| Operator | Name | Description | Example |
|----------|------|-------------|---------|
| `>` | Sequence | Execute operations in sequence | `T12>D45` |
| `&` | Parallel | Execute operations in parallel | `T12&D45` |
| `?:` | Conditional | Conditional execution | `C1?T12:T13` |
| `\|` | Piping | Pipe output from one operation to another | `D45\|T12` |
| `=` | Assignment | Assign value to variable | `V1=D45` |
| `#` | Aggregation | Aggregate multiple operations | `#(T12,T13)` |
| `!` | Context Activation | Activate specific context | `!C5>T12` |
| `**` | Repetition | Repeat operation multiple times | `**3T12` |

## Operator Precedence

Operators are evaluated in the following order (highest to lowest precedence):

1. `!` (Context Activation)
2. `**` (Repetition)
3. `\|` (Piping)
4. `#` (Aggregation)
5. `=` (Assignment)
6. `&` (Parallel)
7. `>` (Sequence)
8. `?:` (Conditional)

## Expressions

### Basic Expressions

A basic expression consists of a token or a combination of tokens and operators:

```
T12>D45
```

### Compound Expressions

Compound expressions combine multiple basic expressions:

```
(T12>D45)&(T13>D46)
```

### Conditional Expressions

Conditional expressions use the `?:` operator:

```
C1?T12:T13
```

### Batch Operations

Batch operations group multiple expressions:

```
{T12>D45, T13>D46}
```

## System Identifiers

System identifiers specify the system version and capabilities:

```
@SYS:V1.0
```

## Context Activation

Context activation uses the `!` operator:

```
!C5>T12
```

## Examples

### Simple Task Sequence

```
T12>D45>T13
```

### Conditional Execution

```
C1?T12:T13
```

### Parallel Operations with Context

```
!C5>(T12&T13)>D45
```

### Complex Expression with Multiple Operators

```
!C5>(C1?T12:T13)>(D45|T14)
```
