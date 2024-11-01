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
        
        
        elif self.type == 'STRING':
            return '"'+self.children[0]+'"'
        
        
        elif self.type == 'VAR':
            return self.children[0]
        
        
        elif self.type == 'FUNC':
            s = "(func:{0}".format(self.children[0])
            for i, param in enumerate(self.children[1:]):
                s += ", child{0}:{1}".format(i, param.print())
            s += ")"
            return s
        
        
        elif self.type == 'INPUT':
            return "[input]"
        
        
        elif self.type == 'ARRAY':
            s = "["
            for i, param in enumerate(self.children):
                s += "child{0}:{1},".format(i, param.print())
            s += "]"
            return s
        
        
        elif self.type == 'ELM':
            return "{0}[{1}]".format(self.children[0].print(), self.children[1].print())
        
        
        elif self.type == 'OP':
            if len(self.children) == 3:
                return "(op:{0}, child1:{1}, child2:{2})".format(self.children[0], self.children[1].print(), self.children[2].print())
            
            return "(op:{0}, child:{1}".format(self.children[0], self.children[1].print())
        
        
        elif self.type == 'STMT':
            if self.children[0] == "if":
                s = "(stmt:if"
                for i, block in enumerate(self.children[1]):
                    if self.children[1][i] is None:
                        s += ", block{0}(con:None".format(i)
                    else:
                        s += ", block{0}(con:{1}".format(i, self.children[1][i].print())
                    
                    for j, expression in enumerate(self.children[2][i]):
                        s += ", exp{0}:{1}".format(j, expression.print())
                    s += ")"
                s += ")"
                return s
            
            elif self.children[0] == "forup":
                var = self.children[1]
                start_value = self.children[2]
                stop_value = self.children[3]
                step_value = self.children[4]
                s = "(stmt:forup, var:{0}, start:{1}, stop:{2}, step:{3}".format(var.print(), start_value.print(), stop_value.print(), step_value.print())
                for i, expression in enumerate(self.children[5]):
                    s += ", exp{0}:{1}".format(i, expression.print())
                s += ")"
                return s
            
            elif self.children[0] == "fordown":
                var = self.children[1]
                start_value = self.children[2]
                stop_value = self.children[3]
                step_value = self.children[4]
                s = "(stmt:fordown, var:{0}, start:{1}, stop:{2}, step:{3}".format(var.print(), start_value.print(), stop_value.print(), step_value.print())
                for i, expression in enumerate(self.children[5]):
                    s += ", exp{0}:{1}".format(i, expression.print())
                s += ")"
                return s
            
            elif self.children[0] == "while":
                s = "(stmlt:while, con:{0}".format(self.children[1].print())
                for i, expression in enumerate(self.children[2]):
                    s += ", exp{0}:{1}".format(i, expression.print())
                s += ")"
                return s
        

        elif self.type == 'PROGRAM':
            s = ""
            for i, expression in enumerate(self.children[0]):
                s += "PRO{0}:{1}\n".format(i, expression.print())
            return s
