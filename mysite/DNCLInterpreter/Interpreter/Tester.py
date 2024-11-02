from Lexer import *
from MyParser import *
from Expression import *

# testcode ゾーン
"""x = 4 \r
もし 1 + x == 3 ならば: \r
┃ 表示する("1 + xは3です")\r
そうでなくもし 1 + x == 2 ならば: \r
┃ 表示する("1 + xは2です")\r
そうでなくもし 1 + x == 4 ならば: \r
┃ 表示する("1 + xは4です")\r
そうでなければ: \r
┗ 表示する("1 + xは2でも3でも4でもありません")\r
"""
"""i を 3 から 0 まで 1 ずつ減らしながら繰り返す: \r
┗ 表示する(i)\r
"""
"""i = 0 \r
i < 3の間繰り返す:\r
┃ i = i + 1\r
┗ 表示する(i)\r
"""
# ---

code = """Tokuten = [10,20,30,40,50,60]\r
Tokuten のすべての値を 0 にする\r
表示する(Tokuten)\r
"""
lexer = Lexer(code)
try:
    tokens = lexer.tokenize()
    print(tokens)  # トークンのリストを表示
except LexerError as e:
    print(e)

parser = Parser(tokens)
try:
    i, program = parser.program(0)
    print(program.print())
    program.evaluate()
    print(IOProcess.get_output())
except ParserError as e:
    print(e)

