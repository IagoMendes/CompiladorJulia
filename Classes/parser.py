from Classes.tokenizer import Tokenizer
from Classes.node import IntVal, UnOp, BinOp, NoOp, Node, Assignment, Identifier, Statement, Print

class Parser:
    tokens = None

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()

        return Parser.parseBlock()
    
    @staticmethod
    def parseBlock():
        stat = Statement()
        while (Parser.tokens.actual.type != "EOF"):
            stat.children.append(Parser.parseCommand())
        
        return stat

    @staticmethod
    def parseCommand():
        result = None

        if (Parser.tokens.actual.type == "LINE_END"):
            Parser.tokens.selectNext()
            if (not result):
                result = NoOp()

        elif (Parser.tokens.actual.type == 'IDENTIFIER'):
            iden = Parser.tokens.actual.value
            Parser.tokens.selectNext()

            if (Parser.tokens.actual.type == 'EQUAL'):
                result = Assignment([iden, None])
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseExpression()
            else:
                raise NameError('Expected "=", received ' + Parser.tokens.actual.type)
        
        elif (Parser.tokens.actual.type == 'PRINT'):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == 'OPEN_P'):
                Parser.tokens.selectNext()
                result = Print(Parser.parseRelExpression())

                if (Parser.tokens.actual.type == 'CLOSE_P'):
                    Parser.tokens.selectNext()
                else:
                    raise NameError("Expected to Close Parenthesis")
            else:
                raise NameError("Expected Parenthesis")
        
        else:
            raise NameError(f"Unexpected token {Parser.tokens.actual.type}")
        
        return result
  
    @staticmethod
    def parseRelExpression():
        result = Parser.parseExpression()
        
        if (Parser.tokens.actual != None):
            while (Parser.tokens.actual.type == "EQUAL_I" or Parser.tokens.actual.type == "LESSER" or Parser.tokens.actual.type == "GREATER"):
                if (Parser.tokens.actual.type == "EQUAL_I" or Parser.tokens.actual.type == "LESSER" or Parser.tokens.actual.type == "GREATER"):
                    result = BinOp(Parser.tokens.actual.value, [result, None])
                    
                    Parser.tokens.selectNext()
                    result.children[1] = Parser.parseTerm() # Right Child

                else:
                    raise NameError(f"Got type {Parser.tokens.actual.type} when expecting <, > or ==")
        else:
            raise NameError(f"Invalid Syntax")            
        return result

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        
        if (Parser.tokens.actual != None):
            while (Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR"):
                if (Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS' or Parser.tokens.actual.type == "OR"):
                    result = BinOp(Parser.tokens.actual.value, [result, None])
                    
                    Parser.tokens.selectNext()
                    result.children[1] = Parser.parseTerm() # Right Child

                else:
                    raise NameError(f"Got type {Parser.tokens.actual.type} when expecting PLUS or MINUS")
        else:
            raise NameError(f"Invalid Syntax")            
        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        
        if (Parser.tokens.actual != None):
            while (Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND"):
                if (Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'DIV' or Parser.tokens.actual.type == "AND"):
                    result = BinOp(Parser.tokens.actual.value, [result, None])
                    
                    Parser.tokens.selectNext()
                    result.children[1] = Parser.parseFactor() # Right Child

                else:
                    raise NameError(f"Got type {Parser.tokens.actual.type} when expecting MULT or DIV")
        else:
            raise NameError(f"Invalid Syntax")
        return result

    @staticmethod
    def parseFactor():
        result = None

        if (Parser.tokens.actual.type == 'INT'):
            result = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == 'IDENTIFIER'):
            result = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == 'MINUS' or Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == "NOT"):
            result = UnOp(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            result.children[0] = Parser.parseFactor()

        elif (Parser.tokens.actual.type == 'OPEN_P'):
            Parser.tokens.selectNext()
            result = Parser.parseRelExpression()

            if (Parser.tokens.actual.type == 'CLOSE_P'):
                Parser.tokens.selectNext()
            else:
                raise NameError("Expected to Close Parenthesis")

        else:
            raise NameError(f"Invalid Syntax")

        return result
    