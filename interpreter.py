from lexer import Lexer
from parser import Parser
from evaluator import Evaluator


def main():
    #code = 'a = 4; b = 10; result = a + b; write 55;'
    code = 'x = 4; for x with i { write "Result:"; write i; }; write "end";'
    lexer = Lexer()
    tokens = lexer.tokenize(code)

    parser = Parser()
    ast = parser.parse(tokens)
    print(ast)

    evaluator = Evaluator()
    evaluator.evaluate(ast)


if __name__ == "__main__":
    main()
