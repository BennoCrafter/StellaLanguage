from lexer import Lexer
from parser import Parser
from evaluator import Evaluator


def main(filename):
    with open(path  +filename, "r") as file_code:
        code = file_code.read()
        file_code.close()
    lexer = Lexer()
    tokens = lexer.tokenize(code)

    parser = Parser()
    ast = parser.parse(tokens)
    print(ast)

    evaluator = Evaluator()
    evaluator.evaluate(ast)


if __name__ == "__main__":
    path = "ExampleCodes/"
    main("if_in_for_loop.st")
