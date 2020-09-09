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

        while(True):
            if (self.position == len(self.origin)):
                resToken = Token('', 'EOF')
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
            
            elif (self.origin[pos] == '*' and not isNumber):
                resToken = Token(self.origin[pos], 'MULT')
                self.position += 1
                break

            elif (self.origin[pos] == '/' and not isNumber):
                resToken = Token(self.origin[pos], 'DIV')
                self.position += 1
                break

            elif (self.origin[pos] == '(' and not isNumber):
                resToken = Token(self.origin[pos], 'OPEN_P')
                self.position += 1
                break

            elif (self.origin[pos] == ')' and not isNumber):
                resToken = Token(self.origin[pos], 'CLOSE_P')
                self.position += 1
                break

            elif (self.origin[pos].isspace() and isNumber):
                self.position += 1
                break
            
            elif (self.origin[pos].isspace()):
                self.position += 1

            else:
                break

        if isNumber:
            resToken = Token(numberToken, 'INT')
        
        self.actual = resToken
        return
