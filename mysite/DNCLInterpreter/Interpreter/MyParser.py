from .Expression import Expression

# エラー処理用の例外クラス
class ParserError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Parser クラス
class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens = tokens
    
    def factor(self, token_num: int) -> tuple[int, Expression]:
        type = self.tokens[token_num][0]
        content = self.tokens[token_num][1]

        if type == 'NUMBER':
            return (token_num + 1, Expression('NUMBER', [int(content)]))
        elif type == 'STRING':
            return (token_num + 1, Expression('STRING', [content]))
        elif type == 'ID':
            if self.check_operator(token_num + 1, ["["]):
                new_token_num, subscript = self.assign(token_num + 2)
                self.token(new_token_num, "]")
                return (new_token_num + 1, Expression('ELM', [Expression('VAR', [content]), subscript]))
            
            return (token_num + 1, Expression('VAR', [content]))
        elif type == 'OTHERCHARS':
            if content == "【外部からの入力】":
                return (token_num + 1, Expression('INPUT', []))

            if self.check_operator(token_num + 1, ["("]):
                params = []
                new_token_num = token_num + 2

                while not self.check_operator(new_token_num, [")"]):
                    new_token_num, expression = self.assign(new_token_num)
                    params.append(expression)

                    if self.check_operator(new_token_num, [")"]):
                        continue
                    if self.check_operator(new_token_num, [","]):
                        new_token_num += 1
                        continue
                    raise ParserError("不明なトークンです。1{0}".format(self.tokens[new_token_num]))
                
                return (new_token_num + 1, Expression('FUNC', [content] + params))
            return (token_num + 1, Expression('VAR', [content]))
        elif content == "[":
                params = []
                new_token_num = token_num + 1

                while not self.check_operator(new_token_num, ["]"]):
                    new_token_num, expression = self.assign(new_token_num)
                    params.append(expression)

                    if self.check_operator(new_token_num, ["]"]):
                        continue
                    if self.check_operator(new_token_num, [","]):
                        new_token_num += 1
                        continue
                    raise ParserError("不明なトークンです。2{0}".format(self.tokens[new_token_num]))
                
                return (new_token_num + 1, Expression('ARRAY', params))
        elif content == "(":
            new_token_num, expression = self.assign(token_num + 1)
            self.token(new_token_num, ")")
            return (new_token_num + 1, expression)
        else:
            raise ParserError("不明なトークンです。3{0}".format(content))
    
    def power(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.factor(token_num)

        if self.check_operator(new_token_num_left, ["**"]):
            new_token_num_right, right = self.power(new_token_num_left + 1)
            return (new_token_num_right, Expression('OP', ["**", left, right]))
        
        return (new_token_num_left, left)
    
    def mlt_or_div(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.power(token_num)

        while self.check_operator(new_token_num_left, ["*", "/", "%"]):
            new_token_num_right, right = self.power(new_token_num_left + 1)
            left = Expression('OP', [self.tokens[new_token_num_left][1], left, right])
            new_token_num_left = new_token_num_right
        
        return (new_token_num_left, left)
    
    def add_or_sub(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.mlt_or_div(token_num)

        while self.check_operator(new_token_num_left, ["+", "-"]):
            new_token_num_right, right = self.mlt_or_div(new_token_num_left + 1)
            left = Expression('OP', [self.tokens[new_token_num_left][1], left, right])
            new_token_num_left = new_token_num_right
        
        return (new_token_num_left, left)
    
    def compare(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.add_or_sub(token_num)

        while self.check_operator(new_token_num_left, ["==", "!=", "<", ">", "<=", ">="]):
            new_token_num_right, right = self.add_or_sub(new_token_num_left + 1)
            left = Expression('OP', [self.tokens[new_token_num_left][1], left, right])
            new_token_num_left = new_token_num_right
        
        return (new_token_num_left, left)
    
    def logicalnot(self, token_num: int) -> tuple[int, Expression]:
        if self.check_operator(token_num, ["not"]):
            new_token_num, child = self.logicalnot(token_num + 1)
            return (new_token_num, Expression('OP', ["not", child]))
        
        new_token_num, child = self.compare(token_num)
        return (new_token_num, child)
    
    def logicaland(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.logicalnot(token_num)

        while self.check_operator(new_token_num_left, ["and"]):
            new_token_num_right, right = self.logicalnot(new_token_num_left + 1)
            left = Expression('OP', ["and", left, right])
            new_token_num_left = new_token_num_right
        
        return (new_token_num_left, left)
    
    def logicalor(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.logicaland(token_num)

        while self.check_operator(new_token_num_left, ["or"]):
            new_token_num_right, right = self.logicaland(new_token_num_left + 1)
            left = Expression('OP', ["or", left, right])
            new_token_num_left = new_token_num_right
        
        return (new_token_num_left, left)
    
    def assign(self, token_num: int) -> tuple[int, Expression]:
        new_token_num_left, left = self.logicalor(token_num)

        if self.check_operator(new_token_num_left, ["="]):
            new_token_num_right, right = self.assign(new_token_num_left + 1)
            return (new_token_num_right, Expression('OP', ["=", left, right]))
        
        return (new_token_num_left, left)
    
    def statement(self, token_num: int) -> tuple[int, Expression]:
        if self.check_operator(token_num, ["もし"]):
            block_list = []
            condition_exps = []

            new_token_num, condition_exp = self.assign(token_num + 1)
            new_token_num = self.token(new_token_num, "ならば:")
            new_token_num = self.token(new_token_num, "\r\n")
            level = self.count_level(new_token_num)
            new_token_num, expressions = self.block(new_token_num, level, True)

            condition_exps.append(condition_exp)
            block_list.append(expressions)

            while self.check_operator(new_token_num, ["そうでなくもし"]):
                new_token_num, condition_exp = self.assign(new_token_num + 1)
                new_token_num = self.token(new_token_num, "ならば:")
                new_token_num = self.token(new_token_num, "\r\n")
                new_token_num, expressions = self.block(new_token_num, level, True)

                condition_exps.append(condition_exp)
                block_list.append(expressions)

            if self.check_operator(new_token_num, ["そうでなければ:"]):
                new_token_num = self.token(new_token_num + 1, "\r\n")
                new_token_num, expressions = self.block(new_token_num, level)

                condition_exps.append(None)
                block_list.append(expressions)

            return new_token_num, Expression('STMT', ["if", condition_exps, block_list])
        
        elif self.check_operator(token_num + 1, ["を"]):
            var = Expression('VAR', [self.tokens[token_num][1]])
            new_token_num = self.token(token_num + 1, "を")
            new_token_num, start_value = self.assign(new_token_num)
            new_token_num = self.token(new_token_num, "から")
            new_token_num, stop_value = self.assign(new_token_num)
            new_token_num = self.token(new_token_num, "まで")
            new_token_num, step_value = self.assign(new_token_num)

            if self.check_operator(new_token_num, ["ずつ増やしながら繰り返す:"]):
                new_token_num = self.token(new_token_num, "ずつ増やしながら繰り返す:")
                new_token_num = self.token(new_token_num, "\r\n")
                level = self.count_level(new_token_num)
                new_token_num, block = self.block(new_token_num, level)

                return new_token_num, Expression('STMT', ["forup", var, start_value, stop_value, step_value, block])
            elif self.check_operator(new_token_num, ["ずつ減らしながら繰り返す:"]):
                new_token_num = self.token(new_token_num, "ずつ減らしながら繰り返す:")
                new_token_num = self.token(new_token_num, "\r\n")
                level = self.count_level(new_token_num)
                new_token_num, block = self.block(new_token_num, level)

                return new_token_num, Expression('STMT', ["fordown", var, start_value, stop_value, step_value, block])
            else:
                raise ParserError("for文が適切に終わっていません。")
            
        new_token_num, expression = self.assign(token_num)
        if self.check_operator(new_token_num, ["の間繰り返す:"]):
            new_token_num = self.token(new_token_num, "の間繰り返す:")
            new_token_num = self.token(new_token_num, "\r\n")
            level = self.count_level(new_token_num)
            new_token_num, block = self.block(new_token_num, level)

            return new_token_num, Expression('STMT', ["while", expression, block])
        elif self.check_operator(new_token_num, ["のすべての値を"]):
            new_token_num = self.token(new_token_num, "のすべての値を")
            new_token_num, val = self.assign(new_token_num)
            new_token_num = self.token(new_token_num, "にする")

            return new_token_num, Expression('STMT', ["resetarray", expression, val])

        return new_token_num, expression
    
    def program(self, token_num: int) -> tuple[int, Expression]:
        new_token_num = token_num
        stmts = []
        while self.tokens[new_token_num][0] != 'EOF':
            new_token_num, stmt = self.statement(new_token_num)
            stmts.append(stmt)
            if self.check_operator(new_token_num, [","]):
                new_token_num = self.token(new_token_num, ",")
            while self.check_operator(new_token_num, ["\r\n"]):
                new_token_num = self.token(new_token_num, "\r\n")
        
        return 0, Expression('PROGRAM', [stmts])
                                                         
    def check_operator(self, token_num: int, operators: list[str]) -> bool:
        if token_num >= len(self.tokens):
            return False

        flag = False
        for operator in operators:
            flag = self.tokens[token_num][1] == operator or flag
            
        return flag
    
    def token(self, token_num: int, token: str) -> int:
        if self.check_operator(token_num, [token]):
            return token_num + 1
        raise ParserError("不明なトークンです。{0}\n正しいトークンは {1}。".format(self.tokens[token_num], token))
    
    def block(self, token_num: int, level: int, iscontinuation: bool = False) -> tuple[int, list[Expression]]:
        new_token_num = token_num
        expressions: list[tuple[int, Expression]] = []
        while True:
            for l in range(level - 1):
                new_token_num = self.token(new_token_num, "┃")

            if(self.check_operator(new_token_num, ["┗"])):
                new_token_num = self.token(new_token_num, "┗")
                new_token_num, exp = self.assign(new_token_num)
                expressions.append(exp)
                return (new_token_num, expressions)
            
            try:
                new_token_num = self.token(new_token_num, "┃")
                new_token_num, stmt = self.statement(new_token_num)
                new_token_num = self.token(new_token_num, "\r\n")
                expressions.append(stmt)
            except ParserError as e:
                if iscontinuation:
                    return new_token_num, expressions
                raise ParserError("文の終わりが見つかりません。")
            
    def count_level(self, token_num: int) -> int:
        level = 0
        while self.check_operator(token_num + level, ["┃", "┗"]):
            level += 1
        if level == 0:
            raise ParserError("ブロックが見つかりません。")
        return level
