# key: [type, value]
class SymbolTable:
    def __init__(self):
        self.table = {'RETURN': [None, None]}
        self.functions = {}
    
    def getter(self, value):
        if (value in self.table):
            return self.table[value]
        else:
            raise NameError('Tried to access unknown identifier')

    def setter(self, key, varType, value):
        if (value == None):
            self.table[key] = [varType, None]
        
        else:
            if (key in self.table):
                if (varType == self.table[key][0]):
                    self.table[key][1] = value
            else:
                raise NameError(f"Expected definition for variable {key}")

    def funcGetter(self, key):
        if (key in self.functions):
            return self.functions[key]
        else:
            raise NameError(f"Function {key} not declared")   

    def funcSetter(self, key, funcType, function):
        if ((key not in self.functions) and (key not in self.table)):
            self.functions[key] = [funcType, function]
        else:
            raise NameError("Function IDENTIFIER already in use")  

    def returnGetter(self):
        return self.table["RETURN"]

    def returnSetter(self, retType, value):
        self.table["RETURN"] = [retType, value]   

