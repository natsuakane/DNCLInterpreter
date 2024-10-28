from Expression import Expression

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
            return (token_num + 1, Expression('VAR', [content]))
        elif type == 'OTHERCHARS':
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
                    raise ParserError("不明なトークンです。{0}".format(self.tokens[new_token_num]))
                
                return (new_token_num + 1, Expression('FUNC', [content] + params))
            return (token_num + 1, Expression('VAR', [content]))
        elif content == "(":
            new_token_num, expression = self.assign(token_num + 1)
            if self.tokens[new_token_num][1] != ")":
                raise ParserError("不明なトークンです。{0}".format(self.tokens[new_token_num]))
            return (new_token_num + 1, expression)
        else:
            raise ParserError("不明なトークンです。{0}".format(content))
    
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
                                                         
    def check_operator(self, token_num: int, operators: list[str]) -> bool:
        if token_num >= len(self.tokens):
            return False

        flag = False
        for operator in operators:
            flag = self.tokens[token_num][1] == operator or flag
            
        return flag
