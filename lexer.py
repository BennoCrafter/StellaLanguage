import re


class Lexer:
    def __init__(self):
        # Define token types
        self.token_specification = [
            ('INTEGER', r'\d+'),
            ("STRING", r'"[^"]*"'),
            ('FLOAT', r'\d+\.\d+'),
            ('WRITE', r'write'),
            ('VAR', r'[a-zA-Z][a-zA-Z0-9]*'),
            ('ASSIGN', r'='),
            ('SEMICOLON', r';'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('TIMES', r'\*'),
            ('DIVIDE', r'/'),
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def tokenize(self, code):
        tokens = []
        for match in re.finditer(self.token_regex, code):
            for name, value in match.groupdict().items():
                if value:
                    tokens.append((name, value))
                    break
        return tokens
