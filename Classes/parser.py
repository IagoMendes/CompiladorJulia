from Classes.tokenizer import Tokenizer

class Parser:
    tokens = None

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()

        result = Parser.parseExpression()
        if Parser.tokens.actual.type == "EOF":
            return result
        else:
            raise NameError(f"Last token isn't EOF")
    
    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        
        while (Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS"):
            if (Parser.tokens.actual.type == 'PLUS'):
                Parser.tokens.selectNext()
                result += Parser.parseTerm()

            elif (Parser.tokens.actual.type == 'MINUS'):
                Parser.tokens.selectNext()
                result -= Parser.parseTerm()

            else:
                raise NameError(f"Got type {Parser.tokens.actual.type} when expecting PLUS or MINUS")

        return int(result)

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        
        while (Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV"):
            if (Parser.tokens.actual.type == 'MULT'):
                Parser.tokens.selectNext()
                result *= Parser.parseFactor()

            elif (Parser.tokens.actual.type == 'DIV'):
                Parser.tokens.selectNext()
                result /= Parser.parseFactor()

            else:
                raise NameError(f"Got type {Parser.tokens.actual.type} when expecting MULT or DIV")

        return int(result)


    @staticmethod
    def parseFactor():
        result = 0

        if (Parser.tokens.actual.type == 'INT'):
            result = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
        
        elif (Parser.tokens.actual.type == 'OPEN_P'):
            Parser.tokens.selectNext()
            result = Parser.parseExpression()

            if (Parser.tokens.actual.type == 'CLOSE_P'):
                Parser.tokens.selectNext()
            else:
                raise NameError("Expected to Close Parenthesis")

        elif (Parser.tokens.actual.type == 'MINUS'):
            Parser.tokens.selectNext()
            result -= Parser.parseFactor()

        elif (Parser.tokens.actual.type == 'PLUS'):
            Parser.tokens.selectNext()
            result += Parser.parseFactor()

        else:
            raise NameError(f"Invalid Syntax")

        return int(result)
    