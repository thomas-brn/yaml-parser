# This file contains the tokenizer code, which converts an input string into a
# list of tokens.
# Tokens represent YAML building blocks such as keys, values, and sequence
# items.
# The tokenizer uses regular expressions to identify token types in the input.
# Each token stores its type, value, indentation level, and line number.
# The resulting token list is then consumed by the parser.

import re

class Token:
    def __init__(self, type_, value, indent_level=0, line_number=0):
        self.type = type_ # Token type (KEY, VALUE, DASH, COMMENT)
        self.value = value # Token value
        self.indent_level = indent_level # Token indentation level
        self.line_number = line_number # Token line number

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value}, indent_level={self.indent_level}, line={self.line_number})"


def tokenize(input_text):
    tokens = []
    lines = input_text.split('\n')  # Split input text into individual lines
    
    ## For example, if the input text is:
    ## key1: value1
    ## key2: value2
    ## - item1
    ## - item2
    ## - item3
    
    ## The text is split into the following list of lines:
    ## ['key1: value1', 'key2: value2', '- item1', '- item2', '- item3']
    
    # Iterate over input lines
    for line_number, line in enumerate(lines, start=1):
        original_line = line  # Keep original line for error messages
        
        # Ignore empty lines
        if not line.strip():
            continue

        # Comment handling
        if re.match(r'^\s*#', line):  # Line starts with a comment
            tokens.append(Token('COMMENT', line.strip(), line_number=line_number))  # Add COMMENT token
            continue

        # Remove inline comments, for example:
        # "key: value # Comment" becomes "key: value"
        line = re.sub(r'#.*$', '', line).rstrip()  # Remove everything after '#' and trailing spaces
        if not line.strip():  # Skip if line is empty after comment removal
            continue

        # Compute indentation level, for example:
        # "  key: value" has indentation level 2
        indent_level = len(line) - len(line.lstrip(' '))  # Count leading spaces

        # Check for key-value pairs
        key_value_match = re.match(r'^\s*(\S.*?)\s*:\s*(.*)', line)  # Check key-value structure
        if key_value_match:
            key = key_value_match.group(1)  # Extract key
            value = key_value_match.group(2)  # Extract value
            tokens.append(Token('KEY', key.strip(), indent_level, line_number))  # Add KEY token
            if value:
                tokens.append(Token('VALUE', value.strip(), indent_level, line_number))  # Add VALUE token if present
            continue

        # Check for sequence items
        seq_match = re.match(r'^\s*-\s*(.*)', line)  # Check sequence structure
        if seq_match:
            value = seq_match.group(1)  # Extract value after dash
            tokens.append(Token('DASH', '-', indent_level, line_number))  # Add DASH token
            if value:
                tokens.append(Token('VALUE', value.strip(), indent_level, line_number))  # Add VALUE token if present
            continue

        # Raise when line does not match any known structure
        raise Exception(f"Lexical error on line {line_number}: '{original_line.strip()}'")  # Unknown line pattern

    return tokens  # Return generated token list
