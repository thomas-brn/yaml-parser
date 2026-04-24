# YAML Parser (Pushdown Automaton Approach)

## Overview

This project implements a simplified YAML parser using a tokenizer + parser pipeline.
It reads a YAML file, tokenizes it, and validates whether the document matches the
supported grammar.

## Features

- Lexical analysis for comments, keys, scalar values, and sequence markers.
- Indentation-based parsing for nested mappings and sequences.
- Clear success/failure feedback from the command line.
- Example files for valid and invalid inputs.

## Project Structure

- `parser.py`: Main syntax parser.
- `tokenizer.py`: Lexer that converts input text into tokens.
- `examples/`: Example YAML files used for manual testing.

## Requirements

- Python 3.8+ (tested with Python 3.x)

## Installation

```bash
git clone https://github.com/thomas-brn/yaml_parser
cd yaml_parser
```

## Usage

Run the parser on a YAML file:

```bash
python3 parser.py <file.yaml>
```

Examples:

```bash
python3 parser.py examples/valid_example.yaml
python3 parser.py examples/invalid_example.yaml
```

## Supported Grammar (Simplified YAML)

The parser is based on a simplified YAML grammar expressed in EBNF:

```ebnf
<document> ::= (<element>)*

<element> ::= <comment>
            | <key_value>
            | <sequence>
            | <mapping>

<comment> ::= '#' <text> '\n'

<key_value> ::= <indentation> <key> ':' <space>? <value>? '\n'

<key> ::= <scalar>

<value> ::= <scalar>
          | <sequence>
          | <mapping>

<sequence> ::= (<indentation> '-' <space>? <value>? '\n')+

<mapping> ::= (<key_value>)+

<scalar> ::= <string>
           | <number>
           | <boolean>
           | <null>

<string> ::= '"' [^"\n]* '"'
           | "'" [^'\n]* "'"
           | [^\s:#\[\]\{\}][^\n#]*

<number> ::= '-'? [0-9]+ ('.' [0-9]+)?

<boolean> ::= 'true' | 'false'

<null> ::= 'null' | '~'

<space> ::= ' ' | '\t'

<indentation> ::= (<space>)*

<text> ::= [^\n]*
```

## Notes and Limitations

- This is an educational parser, not a full YAML 1.2 implementation.
- Indentation drives nesting, but advanced YAML features are not supported
  (anchors, aliases, tags, multiline block scalars, flow collections, etc.).
- Inline comments are removed by the tokenizer before parsing.

## Quick Test Cases

Simple key-value pair:

```yaml
name: "Alice"
```

Scalar sequence:

```yaml
- Apple
- Banana
- Cherry
```

Nested mapping:

```yaml
person:
  name: "John"
  age: 25
```

Sequence of mappings:

```yaml
- name: "Anna"
  age: 30
- name: "Bob"
  age: 40
```

## Contributing

Contributions are welcome. Please open an issue first if you want to discuss a
larger change.

## License

No license file is currently included. Add a `LICENSE` file before publishing if
you want to explicitly allow reuse.
