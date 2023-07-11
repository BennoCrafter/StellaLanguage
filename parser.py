class Parser:
    def __init__(self):
        pass

    def parse(self, tokens):
        # Helper function to consume a token
        def consume(token_types):
            if isinstance(token_types, list):
                if tokens and tokens[0][0] in token_types:
                    return tokens.pop(0)
            elif isinstance(token_types, str):
                if tokens and tokens[0][0] == token_types:
                    return tokens.pop(0)
            raise SyntaxError(f"Expected {token_types}, but found {tokens[0][0]}")

        # Grammar rules
        def statement():
            if tokens[0][0] == 'VAR':
                var_name = consume('VAR')[1]
                consume('ASSIGN')
                expr_value = expression()
                consume('SEMICOLON')
                return ('assign', var_name, expr_value)
            elif tokens[0][0] == 'WRITE':
                content = []
                consume('WRITE')
                while tokens[0][0] != "SEMICOLON":
                    if tokens[0][0] != "ADD_STRING":
                        content.append(tokens[0])
                    consume(["STRING", "INTEGER", "ADD_STRING", "VAR"])
                consume("SEMICOLON")
                return ('write', content)
            elif tokens[0][0] == "FOR":
                consume("FOR")
                iteration = consume(["INTEGER", "VAR"])
                consume("WITH")
                var_to_iterate = consume("VAR")[1]
                consume("LBRACE")
                loop_statements = []
                while tokens[0][0] != "RBRACE":
                    loop_statements.append(statement())
                consume("RBRACE")
                return ('for_loop', iteration, var_to_iterate, loop_statements)
            elif tokens[0][0] == "IF":
                consume("IF")
                first_param = consume(["INTEGER", "STRING", "VAR"])
                operator = consume(["EQUAL", "NOTEQUAL", "LESS_THAN", "GREATER_THAN"])[0]
                second_param = consume(["INTEGER", "STRING", "VAR"])
                consume("LBRACE")
                if_statements = []
                while tokens[0][0] != "RBRACE":
                    if_statements.append(statement())
                consume("RBRACE")
                return ('if_statement', (operator, (first_param, second_param)), if_statements)
            elif tokens[0][0] == "INPUT":
                consume("INPUT")
                s = consume("STRING")[1]
                return ("input", s)
            else:
                raise SyntaxError(f"Unexpected token: {tokens[0][0]}")

        def expression():
            term_value = term()
            while tokens and tokens[0][0] in {'PLUS', 'MINUS'}:
                operator = tokens[0][0]
                consume(operator)
                term_value2 = term()
                term_value = ('binop', operator, term_value, term_value2)
            return term_value

        def term():
            factor_value = factor()
            while tokens and tokens[0][0] in {'TIMES', 'DIVIDE'}:
                operator = tokens[0][0]
                consume(operator)
                factor_value2 = factor()
                factor_value = ('binop', operator, factor_value, factor_value2)
            return factor_value

        def factor():
            if tokens[0][0] == 'INTEGER':
                return ('INTEGER', int(consume('INTEGER')[1]))
            elif tokens[0][0] == "STRING":
                return ("STRING", str(consume("STRING")[1]))
            elif tokens[0][0] == 'VAR':
                return ('VAR', consume('VAR')[1])
            elif tokens[0][0] == "INPUT":
                consume("INPUT")
                s = consume("STRING")[1]
                return ("input", s)
            else:
                raise SyntaxError(f"Unexpected token: {tokens[0][0]}")

        # Start parsing
        ast = []
        while tokens:
            ast.append(statement())
        return ast
