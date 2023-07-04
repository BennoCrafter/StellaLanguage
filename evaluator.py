class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        variables = {}

        def visit(node):
            if node[0] == 'assign':
                var_name, expr = node[1], node[2]
                variables[var_name] = (evaluate_expression(expr), node[2][0])
            elif node[0] == 'write':
                if node[1][0] == "INTEGER" or node[1][0] == "STRING":
                    print(node[1][1].replace('"', ''))
                else:
                    var_name = node[1][1]
                    if var_name in variables:
                        print(variables[var_name][0])
                    else:
                        raise NameError(f"Variable '{var_name}' is not defined.")
            elif node[0] == "for_loop":
                variables[node[2][1]] = (1, "integer")
                commands = node[3]
                if node[1][0] == "INTEGER":
                    iteration = node[1][1]
                else:
                    iteration = variables[node[1][1]][0]
                for i in range(int(iteration)):
                    for element in commands:
                        visit(element)
                    variables[node[2][1]] = (variables[node[2][1]][0] + 1, variables[node[2][1]][1])
            elif node[0] == "if_statement":
                condition = node[1]
                commands = node[2]
                if evaluate_condition(condition):
                    for element in commands:
                        visit(element)
            else:
                raise ValueError(f"Unknown node type: {node[0]}")

        def evaluate_expression(expr):
            if expr[0] == 'INTEGER':
                return int(expr[1])
            if expr[0] == 'STRING':
                return expr[1]
            elif expr[0] == 'VAR':
                var_name = expr[1]
                if var_name in list(variables.keys()):
                    return variables[var_name][0]
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

        def evaluate_condition(condition):
            condition_type = condition[0]
            left_expr = condition[1][0]
            right_expr = condition[1][1]
            if condition_type == 'EQUAL':
                return evaluate_expression(left_expr) == evaluate_expression(right_expr)
            elif condition_type == "NOTEQUAL":
                return evaluate_expression(left_expr) != evaluate_expression(right_expr)
            elif condition_type == "GREATER_THAN":
                return evaluate_expression(left_expr) > evaluate_expression(right_expr)
            elif condition_type == "LESS_THAN":
                return evaluate_expression(left_expr) < evaluate_expression(right_expr)
            else:
                raise ValueError(f"Unknown condition type: {condition_type}")

        for statement in ast:
            visit(statement)