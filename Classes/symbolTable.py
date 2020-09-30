class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def getter(self, value):
        if (value in self.table):
            return self.table[value]
        else:
            raise NameError('Tried to access unknown identifier')

    def setter(self, key, value):
        self.table[key] = value
