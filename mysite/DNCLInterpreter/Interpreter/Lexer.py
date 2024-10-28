import re
from typing import List, Tuple

# トークンの種類
TOKEN_SPECIFICATION = [
    ('NUMBER', r'[\+|-]?\d+(\.\d*)?'),      # 整数または浮動小数点数
    ('STRING', r'"(.*)"'),                  # 文字列
    ('ID', r'[A-Za-z_]\w*'),                # 識別子
    ('OP', r'\*\*|([+\-*/%=,])'),           # 演算子
    ('PARENTHESES', r'[()]'),               # かっこ
    ('NEWLINE', r'\n'),                     # 改行
    ('SKIP', r'[ \t]+'),                    # スペースとタブ
    ('BLOCK', r'[┃┗]'),                     # 条件分岐とループの塊
    ('OTHERCHARS', r'[^ \t()]+'),             # 漢字やひらがななど
]

# エラー処理用の例外クラス
class LexerError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Lexer クラス
class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.line = 1  # 行数の追跡

    def tokenize(self) -> List[Tuple[str, str]]:
        tokens = []
        position = 0
        while position < len(self.code):
            match = None
            for regex_type, regex in TOKEN_SPECIFICATION:
                pattern = re.compile(regex)
                match = pattern.match(self.code, position)
                if match:
                    token_value = match.group(0)
                    if regex_type == 'NEWLINE':
                        self.line += 1  # 改行で行数をインクリメント
                    elif regex_type != 'SKIP':  # スキップ以外はトークンに追加
                        tokens.append((regex_type, token_value))
                    position = match.end(0)
                    break
            if not match:
                raise LexerError(f"不明なトークン '{self.code[position]}' at line {self.line}")
        return tokens
