# key: [type, value]
class SymbolTable:
    def __init__(self):
        self.table = {}
    
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
            