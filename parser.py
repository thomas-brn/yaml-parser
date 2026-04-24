# This file contains the parser code. It analyzes the structure of a YAML
# document from the token list produced by the tokenizer.

from tokenizer import tokenize, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens to parse
        self.current = 0  # Current token index
        self.success = True  # Parsing success flag

    def parse(self):
        try:
            while self.current < len(self.tokens):
                self.element()  # Parse each top-level element
            return True  # Return True when parsing succeeds
        except Exception as e:
            print(f"Parsing error: {e}")  # Display parsing error
            return False  # Return False when an error is found

    def element(self):
        token = self.tokens[self.current]  # Get current token
        if token.type == 'COMMENT':
            self.current += 1  # Ignore comments
        elif token.type == 'KEY':
            self.mapping()  # Parse a key-value pair
        elif token.type == 'DASH':
            self.sequence()  # Parse a sequence item
        elif token.type == 'VALUE':
            self.current += 1  # Ignore standalone scalar values
        else:
            raise Exception(f"Unexpected token {token}")  # Raise on unknown token

    # Parse a key-value pair.
    # A pair is composed of a key (KEY) and an optional associated value (VALUE).
    # It may also contain nested mappings or sequences.
    def mapping(self):
        token = self.tokens[self.current]
        indent_level = token.indent_level  # Key indentation level
        self.current += 1  # Move to next token (after key)
        # Check whether there is an associated value
        if self.current < len(self.tokens) and self.tokens[self.current].type == 'VALUE':
            self.current += 1  # Move to next token (after value)
        # Parse nested mappings or sequences
        while self.current < len(self.tokens) and self.tokens[self.current].indent_level > indent_level:
            self.element()  # Parse nested elements

    # Parse a sequence item.
    # A sequence item starts with a dash (-) and may have an associated value (VALUE).
    # It may also contain nested mappings or sequences.
    def sequence(self):
        token = self.tokens[self.current]
        indent_level = token.indent_level  # Sequence item indentation level
        self.current += 1  # Move to next token (after dash)
        # Check whether there is an associated value
        if self.current < len(self.tokens) and self.tokens[self.current].type == 'VALUE':
            self.current += 1  # Move to next token (after value)
        # Parse nested elements
        while self.current < len(self.tokens) and self.tokens[self.current].indent_level > indent_level:
            self.element()  # Parse nested elements

# Parser entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py <yaml_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        input_text = f.read()

    tokens = tokenize(input_text)  # Tokenize input text
    parser = Parser(tokens)  # Create parser with tokens
    result = parser.parse()  # Parse token stream
    if result:
        print("The YAML document is valid.")  # Success message
    else:
        print("The YAML document is not valid.")  # Failure message