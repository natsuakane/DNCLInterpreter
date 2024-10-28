# エラー処理用の例外クラス
class ExpressionError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Expression クラス
class Expression:
    def __init__(self, type: str, children: list):
        self.type = type
        self.children = children
    
    def print(self) -> str:
        if self.type == 'NUMBER':
            return str(self.children[0])
        if self.type == 'STRING':
            return '"'+self.children[0]+'"'
        if self.type == 'VAR':
            return self.children[0]
        if self.type == 'FUNC':
            s = "(name:{0}".format(self.children[0])
            for i, param in enumerate(self.children[1:]):
                s += ", child{0}:{1}".format(i, param.print())
            s += ")"
            return s
        if self.type == 'OP':
            if len(self.children) == 3:
                return "(op:{0}, child1:{1}, child2:{2})".format(self.children[0], self.children[1].print(), self.children[2].print())
            
            return "(op:{0}, child:{1}".format(self.children[0], self.children[1].print())
