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

class UnOp(Node):  # Single children  
    def __init__(self, value):
        self.value = value
        self.children = [None] # 0 = child

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate()
        elif self.value == '-':
            return - self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = None
    
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self, value):
        self.value = value
        self.children = None
    
    def Evaluate(self):
        pass
