from Classes.tokenizer import Tokenizer

class Parser:
    tokens = None

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.parseExpression()

        if Parser.tokens.actual.type == "EOF":
            return result
        else:
            raise NameError(f"Last token isn't EOF")

    @staticmethod
    def parseTerm():
        termResult = 0
        Parser.tokens.selectNext()

        if (Parser.tokens.actual.type == 'INT'):
            termResult = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

            while (Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'DIV'):
                if (Parser.tokens.actual.type == 'MULT'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == 'INT'):
                        termResult *= int(Parser.tokens.actual.value)
                    else:
                        raise NameError(f"INT expected, instead got type {Parser.tokens.actual.type}")

                if (Parser.tokens.actual.type == 'DIV'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == 'INT'):
                        termResult /= int(Parser.tokens.actual.value)
                    else:
                        raise NameError(f"INT expected, instead got type {Parser.tokens.actual.type}")
                
                Parser.tokens.selectNext()  
            return int(termResult)
        else:
            raise NameError("Expected number")

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        
        while (Parser.tokens.actual.type != "EOF"):
            if (Parser.tokens.actual.type == 'PLUS'):
                result += Parser.parseTerm()
            elif (Parser.tokens.actual.type == 'MINUS'):
                result -= Parser.parseTerm()
            else:
                raise NameError(f"INT expected, instead got type {Parser.tokens.actual.type}")

        return result