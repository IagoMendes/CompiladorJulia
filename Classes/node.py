from Classes.symbolTable import SymbolTable
from Classes.compiler import Compiler

table = SymbolTable()
compiler = Compiler()

class Node:
    i = 0

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        raise NotImplementedError

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i


class BinOp(Node): # Two children   
    def __init__(self, value, children):
        super().__init__(value,children)

    def Evaluate(self):
        if self.value == '+':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("ADD EAX, EBX")
            compiler.newInstruction("MOV EBX, EAX")

            return ['INT', res0[1] + res1[1]]

        elif self.value == '-':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("SUB EAX, EBX")
            compiler.newInstruction("MOV EBX, EAX")

            return ['INT', res0[1] - res1[1]]

        elif self.value == '/':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("DIV EAX, EBX")
            compiler.newInstruction("MOV EBX, EAX")

            return ['INT', res0[1] / res1[1]]

        elif self.value == '*':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("IMUL EBX")
            compiler.newInstruction("MOV EBX, EAX")

            return ['INT', res0[1] * res1[1]]

        elif self.value == '||':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("OR EAX, EBX")
            compiler.newInstruction("MOV EBX, EAX")

            if (res0[1] or res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '&&':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("AND EAX, EBX")
            compiler.newInstruction("MOV EBX, EAX")

            if (res0[1] and res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '==':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("CMP EAX, EBX")
            compiler.newInstruction("CALL binop_je")

            if (res0[1] == res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '<':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("CMP EAX, EBX")
            compiler.newInstruction("CALL binop_jl")

            if (res0[1] > res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]

        elif self.value == '>':
            res0 = self.children[0].Evaluate()
            compiler.newInstruction("PUSH EBX")
            res1 = self.children[1].Evaluate()
            compiler.newInstruction("POP EAX")
            compiler.newInstruction("CMP EAX, EBX")
            compiler.newInstruction("CALL binop_jg")

            if (res0[1] > res1[1]):
                return ['BOOL', 1]
            else:
                return ['BOOL', 0]
            

class UnOp(Node):  # Single children  
    def __init__(self, value):
        super().__init__(value,[None])

    def Evaluate(self):
        if self.value == '+':
            return ['INT', self.children[0].Evaluate()[1]]

        elif self.value == '-':
            res = -self.children[0].Evaluate()[1]
            compiler.newInstruction("NEG EBX")
            return ['INT', res]
            
        elif self.value == '!':
            if not(self.children[0].Evaluate()[1]):
                compiler.newInstruction("NOT EBX")
                return ['BOOL', 1]
            else:
                compiler.newInstruction("NOT EBX")
                return ['BOOL', 0]
            

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value,None)
    
    def Evaluate(self):
        compiler.newInstruction(f"MOV EBX, {self.value}")
        return ["INT", self.value]


class BoolVal(Node):
    def __init__(self, value):
        super().__init__(value, None)
    
    def Evaluate(self):
        if (self.value == "true"):
            compiler.newInstruction("CALL binop_true")
            return ["BOOL", True]

        if (self.value == "false"):
            compiler.newInstruction("CALL binop_false")
            return ["BOOL", False]


class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)
    
    def Evaluate(self):
        compiler.newInstruction("NOP")
        pass


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, None)
    
    def Evaluate(self):
        res = table.getter(self.value)
        compiler.newInstruction(f"MOV EBX, [EBP - {res[2]}]")
        return res


class Assignment(Node): # Two children   
    def __init__(self, children, value):
        super().__init__(value,children)

    def Evaluate(self):
        if (self.value == "::"):
            compiler.newInstruction("PUSH DWORD 0")
            table.setter(self.children[0], self.children[1], None)

        elif (self.value == "="):
            res = self.children[1].Evaluate()
            if (res[0] == table.getter(self.children[0])[0]):
                compiler.newInstruction(f"MOV [EBP-{table.getter(self.children[0])[2]}], EBX")
                table.setter(self.children[0], res[0], res[1])
            else:
                raise NameError(f"Types for variable {self.children[0]} don't match")


class Statement(Node):  
    def __init__(self):
        super().__init__(None, [])

    def Evaluate(self):
        for i in range(len(self.children)):
            self.children[i].Evaluate()


class Print(Node):  # Single children  
    def __init__(self, children):
        super().__init__(None, [children])

    def Evaluate(self):
        self.children[0].Evaluate()
        compiler.newInstruction("PUSH EBX")
        compiler.newInstruction("CALL print")
        compiler.newInstruction("POP EBX")


class While(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self):
        compiler.newInstruction(f"loop_{self.i}: ;")
        self.children[0].Evaluate()
        compiler.newInstruction(f"CMP EBX, False ;")
        compiler.newInstruction(f"JE exit_{self.i} ;")
        self.children[1].Evaluate()
        compiler.newInstruction(f"JMP loop_{self.i} ;")
        compiler.newInstruction(f"exit_{self.i}: ;")


class If(Node): 
    def __init__(self, children):
        super().__init__(None, children)

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
