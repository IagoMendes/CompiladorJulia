from Classes.symbolTable import SymbolTable

table = SymbolTable()

class Node:
    def __init__(self, value):
        self.value = value
        self.children = [] # 0 = left child & 1 = right child

    def Evaluate(self):
        raise NotImplementedError


class BinOp(Node): # Two children   
    def __init__(self, value, children):
        self.value = value
        self.children = children # 0 = left child & 1 = right child

    def Evaluate(self):
        res0 = self.children[0].Evaluate()
        res1 = self.children[1].Evaluate()

        if self.value == '+':
            if (res0[0] == res1[0]):
                return [res0[0], res0[1] + res1[1]]
            elif (res0[0] == "STRING" or res1[0] == "STRING"):
                raise NameError (f'Unable perform {res0[0]} + {res1[0]}')
            return ['INT', res0[1] + res1[1]]

        elif self.value == '-':
            if (res0[0] == "STRING" or res1[0] == "STRING"):
                raise NameError (f'Unable perform {res0[0]} - {res1[0]}')
            return ['INT', res0[1] - res1[1]]

        elif self.value == '/':
            if (res0[0] == "STRING" or res1[0] == "STRING"):
                raise NameError (f'Unable perform {res0[0]} / {res1[0]}')
            return ['INT', int(res0[1] / res1[1])]

        elif self.value == '*':
            if (res0[0] == "STRING" or res1[0] == "STRING"):
                if (res0[0] == "BOOL"):
                    if (res0[1] == 1):
                        res0[1] = "true"
                    else:
                        res0[1] = "false"

                if (res1[0] == "BOOL"):
                    if (res1[1] == 1):
                        res1[1] = "true"
                    else:
                        res1[1] = "false"
                
                return ["STRING", str(res0[1]) + str(res1[1])]
            else:
                return ['INT', res0[1] * res1[1]]

        elif self.value == '||':
            if (res0[1] or res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '&&':
            if (res0[0] == "STRING" or res1[0] == "STRING"):
                raise NameError (f'Unable perform {res0[0]} && {res1[0]}')

            if (res0[1] and res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '==':
            if (res0[1] == res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '<':
            if (res0[1] < res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '>':
            if (res0[1] > res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]
            

class UnOp(Node):  # Single children  
    def __init__(self, value):
        self.value = value
        self.children = [None] # 0 = child

    def Evaluate(self):
        if self.value == '+':
            return ['INT', self.children[0].Evaluate()[1]]
        elif self.value == '-':
            return ['INT', -self.children[0].Evaluate()[1]]
        elif self.value == '!':
            if not(self.children[0].Evaluate()[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]
            

class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = None
    
    def Evaluate(self):
        return ["INT", self.value]


class BoolVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = None
    
    def Evaluate(self):
        if (self.value == "true"):
            return ["BOOL", 1]
        if (self.value == "false"):
            return ["BOOL", 0]


class StringVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = None
    
    def Evaluate(self):
        return ["STRING", self.value]


class NoOp(Node):
    def __init__(self):
        self.children = None
    
    def Evaluate(self):
        pass


class Identifier(Node):
    def __init__(self, value):
        self.value = value
    
    def Evaluate(self):
        return table.getter(self.value)


class Assignment(Node): # Two children   
    def __init__(self, children, value):
        self.children = children # 0 = Identifier & 1 = Expression/Type
        self.value = value

    def Evaluate(self):
        if (self.value == "::"):
            table.setter(self.children[0], self.children[1], None)

        elif (self.value == "="):
            res = self.children[1].Evaluate()
            if (res[0] == table.getter(self.children[0])[0]):
                table.setter(self.children[0], res[0], res[1])
            else:
                raise NameError(f"Types for variable {self.children[0]} don't match")


class Statement(Node):  
    def __init__(self):
        self.children = [] 

    def Evaluate(self):
        for i in range(len(self.children)):
            self.children[i].Evaluate()


class Print(Node):  # Single children  
    def __init__(self, children):
        self.children = [children] # 0 = child

    def Evaluate(self):
        res = self.children[0].Evaluate()
        if (res[0] == "BOOL"):
            if (res[1] == 1):
                print(True)
            elif (res[1] == 0):
                print(False)
        else:
            print(self.children[0].Evaluate()[1])


class Read(Node):
    def __init__(self):
        self.children = None

    def Evaluate(self):
        self.value = int(input())
        return ['INT', self.value]


class While(Node):
    def __init__(self, children):
        self.children = children # 0 = RelEx & 1 = Block

    def Evaluate(self):
        while (self.children[0].Evaluate()[1]):
            self.children[1].Evaluate()


class If(Node): 
    def __init__(self, children):
        self.children = children

    def Evaluate(self):
        if (self.children[0].Evaluate()[0] != 'STRING'):
            if (self.children[2] is None):
                if (self.children[0].Evaluate()[1]):
                    self.children[1].Evaluate()
            else:
                if (self.children[0].Evaluate()[1]):
                    self.children[1].Evaluate()
                else:
                    self.children[2].Evaluate()
        else:
            raise NameError("Cannot use string as single argument.")
