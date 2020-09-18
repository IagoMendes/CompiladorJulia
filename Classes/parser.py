from Classes.tokenizer import Tokenizer
from Classes.node import IntVal, UnOp, BinOp, NoOp, Node

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
            if (Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS'):
                result = BinOp(Parser.tokens.actual.value, [result, None])
                
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseTerm() # Right Child

            else:
                raise NameError(f"Got type {Parser.tokens.actual.type} when expecting PLUS or MINUS")

        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        
        while (Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV"):
            if (Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'DIV'):
                result = BinOp(Parser.tokens.actual.value, [result, None])
                
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseFactor() # Right Child

            else:
                raise NameError(f"Got type {Parser.tokens.actual.type} when expecting MULT or DIV")

        return result

    @staticmethod
    def parseFactor():
        result = None

        if (Parser.tokens.actual.type == 'INT'):
            result = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == 'MINUS' or Parser.tokens.actual.type == 'PLUS'):
            result = UnOp(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            result.children[0] = Parser.parseFactor()

        elif (Parser.tokens.actual.type == 'OPEN_P'):
            Parser.tokens.selectNext()
            result = Parser.parseExpression()

            if (Parser.tokens.actual.type == 'CLOSE_P'):
                Parser.tokens.selectNext()
            else:
                raise NameError("Expected to Close Parenthesis")

        else:
            raise NameError(f"Invalid Syntax")

        return result
    