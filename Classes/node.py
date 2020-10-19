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
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == '/':
            return int(self.children[0].Evaluate() / self.children[1].Evaluate())
        elif self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == '||':
            return self.children[0].Evaluate() or self.children[1].Evaluate() 
        elif self.value == '&&':
            return self.children[0].Evaluate() and self.children[1].Evaluate()
        elif self.value == '==':
            return self.children[0].Evaluate() == self.children[1].Evaluate() 
        elif self.value == '<':
            return self.children[0].Evaluate() < self.children[1].Evaluate() 
        elif self.value == '>':
            return self.children[0].Evaluate() > self.children[1].Evaluate() 
        

class UnOp(Node):  # Single children  
    def __init__(self, value):
        self.value = value
        self.children = [None] # 0 = child

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate()
        elif self.value == '-':
            return - self.children[0].Evaluate()
        elif self.value == '!':
            return not(self.children[0].Evaluate())

class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = None
    
    def Evaluate(self):
        return self.value

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
    def __init__(self, children):
        self.children = children # 0 = Identifier & 1 = Expression

    def Evaluate(self):
        table.setter(self.children[0], self.children[1].Evaluate())

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
        print(self.children[0].Evaluate())
        
