from Lexer import *
from MyParser import *

code = """x > 1 の間繰り返す:
┃ x = 【外部からの入力】
┗ 2 + 3
"""
lexer = Lexer(code)
try:
    tokens = lexer.tokenize()
    print(tokens)  # トークンのリストを表示
except LexerError as e:
    print(e)

parser = Parser(tokens)
try:
    i, statement = parser.statement(0)
    print(statement.print())
except ParserError as e:
    print(e)

