import math
import random

# エラー処理用の例外クラス
class ExpressionError(Exception):
    def __init__(self, message):
        super().__init__(message)

# 変数管理用のクラス
class Environment:
    __variables: dict[str, any] = []
    
    @staticmethod
    def get(var: str):
        return Environment.__variables[var]
    
    @staticmethod
    def set(var: str, val: any):
        Environment.__variables[var] = val

# 入出力管理用のクラス
class IOProcess:
    __output: list[str] = []
    
    @staticmethod
    def output(s: str):
        IOProcess.__output.append(s)

    @staticmethod
    def input() -> str:
        pass

# Expression クラス
class Expression:
    def __init__(self, type: str, children: list):
        self.type = type
        self.children = children

    def evaluate(self):
        if self.type == 'NUMBER':
            return self.children[0]
        elif self.type == 'STRING':
            return self.children[0]
        elif self.type == 'VAR':
            return Environment.get(self.children[0])
        elif self.type == 'FUNC':
            if self.children[0] == "要素数":
                return len(self.children[1].evaluate())
            elif self.children[0] == "整数":
                return round(self.children[1].evaluate())
            elif self.children[0] == "乱数":
                return random.random()
            elif self.children[0] == "表示する":
                IOProcess.output(self.children[1].evaluate())
        elif self.type == 'INPUT':
            return IOProcess.input()
        elif self.type == 'ARRAY':
            contents = []
            for content in self.children[0]:
                contents.append(content.evaluate())
            return contents
        elif self.type == 'ELM':
            return (self.children[0].evaluate())[self.children[1].evaluate()]
        elif self.type == 'OP':
            if self.children[0] == "**":
                return math.pow(self.children[1].evaluate(), self.children[2].evaluate())
            elif self.children[0] == "*":
                return self.children[1].evaluate() * self.children[2].evaluate()
            elif self.children[0] == "/":
                return self.children[1].evaluate() / self.children[2].evaluate()
            elif self.children[0] == "%":
                return self.children[1].evaluate() % self.children[2].evaluate()
            elif self.children[0] == "+":
                return self.children[1].evaluate() + self.children[2].evaluate()
            elif self.children[0] == "-":
                return self.children[1].evaluate() - self.children[2].evaluate()
            elif self.children[0] == "==":
                return self.children[1].evaluate() == self.children[2].evaluate()
            elif self.children[0] == "!=":
                return self.children[1].evaluate() != self.children[2].evaluate()
            elif self.children[0] == "<":
                return self.children[1].evaluate() < self.children[2].evaluate()
            elif self.children[0] == ">":
                return self.children[1].evaluate() > self.children[2].evaluate()
            elif self.children[0] == "<=":
                return self.children[1].evaluate() <= self.children[2].evaluate()
            elif self.children[0] == ">=":
                return self.children[1].evaluate() >= self.children[2].evaluate()
            elif self.children[0] == "not":
                if self.children[1].evaluate() == 0:
                    return 1
                else:
                    return 0
            elif self.children[0] == "and":
                if self.children[1].evaluate() == 0 or self.children[2].evaluate() == 0:
                    return 0
                else:
                    return 1
            elif self.children[0] == "or":
                if self.children[1].evaluate() == 0 and self.children[2].evaluate() == 0:
                    return 0
                else:
                    return 1
            elif self.children[0] == "=":
                if self.children[1][0] != 'VAR':
                    raise ExpressionError("=の左辺が変数ではありません")
                Environment.set(self.children[1].children[0], self.children[2].evaluate())
                return self.children[2].evaluate()
        elif self.type == 'STMT':
            pass

        elif self.type == 'PROGRAM':
            for stmt in self.children[0]:
                stmt.evaluate()
            return 0
    
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
