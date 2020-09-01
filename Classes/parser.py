from Classes.tokenizer import Tokenizer

class Parser:
    tokens = None

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()

    @staticmethod
    def parseExpression():
        result = 0
        actualToken = Parser.tokens.selectNext()

        if (actualToken.type == 'INT'):
            result = int(actualToken.value)

            actualToken = Parser.tokens.selectNext()
            if (actualToken.type != "INT"): 

                while (actualToken.type == 'PLUS' or actualToken.type == 'MINUS'):

                    if (actualToken.type == 'PLUS'):
                        actualToken = Parser.tokens.selectNext()
                        if (actualToken.type == 'INT'):
                            result += int(actualToken.value)
                        else:
                            raise NameError(f"INT expected, instead got type {actualToken.type}")

                    if (actualToken.type == 'MINUS'):
                        actualToken = Parser.tokens.selectNext()
                        if (actualToken.type == 'INT'):
                            result -= int(actualToken.value)
                        else:
                            raise NameError(f"INT expected, instead got type {actualToken.type}")

                    actualToken = Parser.tokens.selectNext()
                    if (actualToken != None):        
                        if (actualToken.type == "INT"):
                            raise NameError(f"Operation expected, instead got type {actualToken.type}")
                    else:
                        break

            else: 
                raise NameError(f"Operation expected, instead got type {actualToken.type}")

            return result
        else:
            raise NameError("Expected number")