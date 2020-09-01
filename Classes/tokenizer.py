from Classes.token import Token

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
    
    def selectNext(self):
        numberToken = ""
        resToken = None
        isNumber = False

        if (self.actual != None):
            if (self.position == len(self.origin) and self.actual.type != 'EOF'): # Garantindo o final da string como EOF sem entrar em loop
                resToken = Token('', 'EOF')
                self.actual = resToken
                return resToken

        while(True): 
            if (self.position >= len(self.origin)):
                break

            pos = self.position
            if (self.origin[pos].isnumeric()) and (len(numberToken) == 0 or numberToken.isnumeric()):
                isNumber = True
                numberToken += self.origin[pos]
                self.position += 1   

            elif (self.origin[pos] == '+' and not isNumber):
                resToken = Token(self.origin[pos], 'PLUS')
                self.position += 1
                break

            elif (self.origin[pos] == '-' and not isNumber):
                resToken = Token(self.origin[pos], 'MINUS')
                self.position += 1
                break

            else:
                break

        if isNumber:
            resToken = Token(numberToken, 'INT')
        
        self.actual = resToken
        return resToken
