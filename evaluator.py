class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        variables = {}

        def visit(node):
            if node[0] == 'assign':
                var_name, expr = node[1], node[2]
                variables[var_name] = evaluate_expression(expr)
            elif node[0] == 'write':
                if node[1][0] == "INTEGER" or node[1][0] == "STRING":
                    print(node[1][1].replace('"', ''))
                else:
                    var_name = node[1][1]
                    if var_name in variables:
                        print(variables[var_name])
                    else:
                        raise NameError(f"Variable '{var_name}' is not defined.")
            else:
                raise ValueError(f"Unknown node type: {node[0]}")

        def evaluate_expression(expr):
            if expr[0] == 'integer':
                return expr[1]
            if expr[0] == 'string':
                return expr[1]
            elif expr[0] == 'variable':
                var_name = expr[1]
                if var_name in variables:
                    return variables[var_name]
                else:
                    raise NameError(f"Variable '{var_name}' is not defined.")
            elif expr[0] == 'binop':
                operator, left_expr, right_expr = expr[1], expr[2], expr[3]
                left_value = evaluate_expression(left_expr)
                right_value = evaluate_expression(right_expr)
                if operator == 'PLUS':
                    return left_value + right_value
                elif operator == 'MINUS':
                    return left_value - right_value
                elif operator == '*':
                    return left_value * right_value
                elif operator == '/':
                    return left_value / right_value
                else:
                    raise ValueError(f"Unknown operator: {operator}")
            else:
                raise ValueError(f"Unknown expression type: {expr[0]}")

        for statement in ast:
            visit(statement)