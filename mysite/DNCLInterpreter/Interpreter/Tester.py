from .Lexer import *
from .MyParser import *

code = """もし 1 == 1 ならば:
┃ 表示する("aaa")
┃ 1 + 2
そうでなくもし 1 > 1 ならば:
┃ 1 + 3
┃ 1 + 4
そうでなければ:
┗ 1 + 5
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

