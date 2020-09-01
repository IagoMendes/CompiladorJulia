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
        
        Parser.tokens.selectNext()
        if (Parser.tokens.actual.type == 'INT'):
            result = int(Parser.tokens.actual.value)

            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type != "INT"): 

                while (Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS'):

                    if (Parser.tokens.actual.type == 'PLUS'):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == 'INT'):
                            result += int(Parser.tokens.actual.value)
                        else:
                            raise NameError(f"INT expected, instead got type {Parser.tokens.actual.type}")

                    if (Parser.tokens.actual.type == 'MINUS'):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == 'INT'):
                            result -= int(Parser.tokens.actual.value)
                        else:
                            raise NameError(f"INT expected, instead got type {Parser.tokens.actual.type}")

                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual != None):        
                        if (Parser.tokens.actual.type == "INT"):
                            raise NameError(f"Operation expected, instead got type {Parser.tokens.actual.type}")
                    else:
                        break

            else: 
                raise NameError(f"Operation expected, instead got type {Parser.tokens.actual.type}")

            return result
        else:
            raise NameError("Expected number")