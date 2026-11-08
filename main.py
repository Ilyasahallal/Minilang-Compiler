from src.lexer import tokenize
from src.parser import Parser
from pprint import pprint

source = """
let x = 10;
let y = 5 * 2;
print(x + y);
"""

tokens = tokenize(source)
parser = Parser(tokens)

ast = parser.parse()

pprint(ast)