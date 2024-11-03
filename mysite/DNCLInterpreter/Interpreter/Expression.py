import math
import random

# エラー処理用の例外クラス
class ExpressionError(Exception):
    def __init__(self, message):
        super().__init__(message)

# 変数管理用のクラス
class Environment:
    __variables: dict[str, any] = {}
    
    @staticmethod
    def get(var: str):
        return Environment.__variables[var]
    
    @staticmethod
    def set(var: str, val: any):
        Environment.__variables[var] = val

# 入出力管理用のクラス
class IOProcess:
    __output: list[str] = []
    __input: list[any] = []
    __index: int = 0

    @staticmethod
    def init():
        IOProcess.__output.clear()
        IOProcess.__input.clear()
    
    @staticmethod
    def input(s: str):
        def try_convert_to_float(value):
            try:
                return float(value)
            except ValueError:
                return value
        IOProcess.__input = s.split("\r\n")
        IOProcess.__input = list(map(try_convert_to_float, IOProcess.__input))
        IOProcess.__index = 0

    @staticmethod
    def output(s: str):
        IOProcess.__output.append(s)

    @staticmethod
    def get_input() -> any:
        IOProcess.__index += 1
        return IOProcess.__input[IOProcess.__index - 1]

    @staticmethod
    def get_output():
        return IOProcess.__output

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
                s = "".join(map(lambda c : str(c.evaluate()), self.children[1:]))
                IOProcess.output(s)
        elif self.type == 'INPUT':
            print('INPUT')
            return IOProcess.get_input()
        elif self.type == 'ARRAY':
            contents = []
            for content in self.children:
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
                child1 = self.children[1].evaluate()
                child2 = self.children[2].evaluate()
                if type(child1) == str or type(child2) == str:
                    return str(child1) + str(child2)
                return child1 + child2
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
                if self.children[1].type != 'VAR':
                    raise ExpressionError("=の左辺が変数ではありません")
                Environment.set(self.children[1].children[0], self.children[2].evaluate())
                return self.children[2].evaluate()
            
        elif self.type == 'STMT':
            if self.children[0] == "if":
                for i, block in enumerate(self.children[1]):
                    if not (self.children[1][i] is None or self.children[1][i].evaluate() == 0):
                        for j, expression in enumerate(self.children[2][i]):
                            expression.evaluate()
                        return None
                    elif self.children[1][i] is None:
                        for j, expression in enumerate(self.children[2][i]):
                            expression.evaluate()
                        return None
                return None
            
            elif self.children[0] == "forup":
                var = self.children[1]
                start_value = self.children[2]
                stop_value = self.children[3]
                step_value = self.children[4]
                block = self.children[5]
                for i in range(start_value.evaluate(), stop_value.evaluate() + 1, step_value.evaluate()):
                    if var.type != 'VAR':
                        raise ExpressionError("変数が指定されていません。")
                    Environment.set(var.children[0], i)
                    for stmt in block:
                        stmt.evaluate()
                return None
            
            elif self.children[0] == "fordown":
                var = self.children[1]
                start_value = self.children[2]
                stop_value = self.children[3]
                step_value = self.children[4]
                block = self.children[5]
                for i in range(start_value.evaluate(), stop_value.evaluate() - 1, -step_value.evaluate()):
                    if var.type != 'VAR':
                        raise ExpressionError("変数が指定されていません。")
                    Environment.set(var.children[0], i)
                    for stmt in block:
                        stmt.evaluate()
                return None
            
            elif self.children[0] == "while":
                con = self.children[1]
                block = self.children[2]
                while con.evaluate() != 0:
                    for stmt in block:
                        stmt.evaluate()
                return None
            
            elif self.children[0] == "resetarray":
                array_name = self.children[1]
                val = self.children[2]
                if array_name.type != 'VAR':
                    raise ExpressionError("変数が指定されていません。")
                array = Environment.get(array_name.children[0])
                array = list(map(lambda x : val.evaluate(), array))
                Environment.set(array_name.children[0], array)
                return None

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
