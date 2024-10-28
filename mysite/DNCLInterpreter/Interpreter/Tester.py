from Lexer import *
from MyParser import *

code = 'x = 表示する(1 * 2, 2)'
lexer = Lexer(code)
try:
    tokens = lexer.tokenize()
    print(tokens)  # トークンのリストを表示
except LexerError as e:
    print(e)

parser = Parser(tokens)
try:
    expressions = parser.assign(0)
    print(expressions[1].print())
except ParserError as e:
    print(e)

