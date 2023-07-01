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
                return 'assign', var_name, expr_value
            elif tokens[0][0] == 'WRITE':
                consume('WRITE')
                try:
                    var_name = consume('VAR')[1]
                    consume('SEMICOLON')
                    return ('write', ("var", var_name))  # Change 'write' to 'print' here
                except:
                    content = consume(["STRING", "INTEGER"])
                    consume("SEMICOLON")
                    return ("write", (content[0], content[1]))
            elif tokens[0][0] == "FOR":
                return expression()
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
                return 'integer', int(consume('INTEGER')[1])
            elif tokens[0][0] == "STRING":
                return "string", str(consume("STRING")[1])
            elif tokens[0][0] == 'VAR':
                return 'variable', consume('VAR')[1]
            elif tokens[0][0] == "FOR":
                consume("FOR")
                iteration = consume(["INTEGER", "VAR"])
                consume("WITH")
                var_to_iterate = consume("VAR")
                consume("LBRACE")
                loop_statements = []
                while tokens[0][0] != "RBRACE":
                    loop_statements.append(statement())
                consume("RBRACE")
                consume("SEMICOLON")
                return ("for_loop", iteration, var_to_iterate, loop_statements)
            else:
                raise SyntaxError(f"Unexpected token: {tokens[0][0]}")

        # Start parsing
        ast = []
        while tokens:
            ast.append(statement())
        return ast