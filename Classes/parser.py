from Classes.tokenizer import Tokenizer
from Classes.node import *

class Parser:
    tokens = None
    count = 0

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        res = Parser.parseBlockF()

        if (Parser.tokens.actual.type == "EOF"):
            return res
        else:
            raise NameError("Expected EOF, please check your syntax")
    
    @staticmethod
    def parseBlock():
        stat = Statement()

        while (Parser.tokens.actual.type != "EOF" and Parser.tokens.actual.type != "END" and 
               Parser.tokens.actual.type != "ELSE" and Parser.tokens.actual.type != "ELSEIF"):    
            stat.children.append(Parser.parseCommand())
                
        return stat

    @staticmethod
    def parseBlockF():
        stat = Statement()

        while (Parser.tokens.actual.type != "EOF"):
            if (Parser.tokens.actual.type == "FUNCTION"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "IDENTIFIER"):
                    func = FunctionDeclaration(Parser.tokens.actual.value, None)
                    stat.children.append(func)
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "OPEN_P"):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == "IDENTIFIER"):
                            arguments = [Parser.tokens.actual.value]
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.type == "COLON_I"):
                                Parser.tokens.selectNext()
                                if (Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                                    arguments.append(Parser.tokens.actual.type)
                                    func.children.append(arguments)
                                    Parser.tokens.selectNext()
                                    while (Parser.tokens.actual.type == "COMMA"):
                                        Parser.tokens.selectNext()
                                        if (Parser.tokens.actual.type == "IDENTIFIER"):
                                            arguments = [Parser.tokens.actual.value]
                                            Parser.tokens.selectNext()
                                            if (Parser.tokens.actual.type == "COLON_I"):
                                                Parser.tokens.selectNext()
                                                if (Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                                                    arguments.append(Parser.tokens.actual.value)
                                                    func.children.append(arguments)
                                                    Parser.tokens.selectNext()
                                                else:
                                                    raise NameError("Missing type for function argument")
                                            else:
                                                raise NameError("Use '::' to declare type")
                                        else:
                                            raise NameError("Use Identifier after comma")                                
                                else:
                                    raise NameError("Missing type for function argument")
                            else:
                                raise NameError("Use '::' to declare type")
                        if (Parser.tokens.actual.type == "CLOSE_P"):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.type == "COLON_I"):
                                Parser.tokens.selectNext()
                                if (Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                                    func.funcType = Parser.tokens.actual.type
                                    Parser.tokens.selectNext()
                                    if (Parser.tokens.actual.type == "LINE_END"):
                                        Parser.tokens.selectNext()
                                        func.children.append(Parser.parseBlock())
                                        if (Parser.tokens.actual.type == "END"):
                                            Parser.tokens.selectNext()
                                            if (Parser.tokens.actual.type == "LINE_END"):
                                                Parser.tokens.selectNext()
                                            else:
                                                raise NameError("Expected \\n")
                                        else:
                                            raise NameError("Use 'end' to end function")
                                    else:
                                        raise NameError("Skip line after declaring function type")
                                else:
                                    raise NameError("Use INT, STRING or BOOL to define function type")
                            else:
                                raise NameError("After closing parenthesis, use '::'+TYPE to define type")
                        else:
                            raise NameError("Function expected IDENTIFIER or ')'")
                    else:
                        raise NameError("Expected '(' after IDENTIFIER")
                else:
                    raise NameError("Expected IDENTIFIER for Function")
            else:
                stat.children.append(Parser.parseCommand())  
        return stat

    @staticmethod
    def parseCommand():
        result = None

        if (Parser.tokens.actual.type == "LINE_END"):
            Parser.tokens.selectNext()
            if (not result):
                result = NoOp()

        elif (Parser.tokens.actual.type == 'LOCAL'):
            Parser.tokens.selectNext()

            if (Parser.tokens.actual.type == 'IDENTIFIER'):
                result = Assignment([Parser.tokens.actual.value, None], None)
                Parser.tokens.selectNext()

                if (Parser.tokens.actual.type == 'COLON_I'):
                    result.value = Parser.tokens.actual.value
                    Parser.tokens.selectNext()

                    if (Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                        result.children[1] = Parser.tokens.actual.type
                        Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == 'IDENTIFIER'):
            identifier = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "OPEN_P"):
                result = FunctionCall(identifier)
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type != "CLOSE_P"):
                    result.children.append(Parser.parseRelExpression())
                    while (Parser.tokens.actual.type == "COMMA"):
                        Parser.tokens.selectNext()
                        result.children.append(Parser.parseRelExpression())
                
                if (Parser.tokens.actual.type == "CLOSE_P"):
                    Parser.tokens.selectNext()
                else:
                    raise NameError("Function expected ')' or argument")
            
            elif (Parser.tokens.actual.type == 'EQUAL'):
                result = Assignment([identifier, None], Parser.tokens.actual.value)
                Parser.tokens.selectNext()

                if (Parser.tokens.actual.type == 'READ'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == 'OPEN_P'):
                        Parser.tokens.selectNext()
                        result.children[1] = Read()

                        if (Parser.tokens.actual.type == 'CLOSE_P'):
                            Parser.tokens.selectNext()
                        else:
                            raise NameError("Expected to Close Parenthesis")       
                else:
                    result.children[1] = Parser.parseRelExpression()
            else:
                raise NameError('Expected "=" or function call, received ' + Parser.tokens.actual.type)
        
        elif (Parser.tokens.actual.type == 'RETURN'):
            Parser.tokens.selectNext()
            result = Return([Parser.parseRelExpression()])
      
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
        
        elif (Parser.tokens.actual.type == 'WHILE'):
            Parser.tokens.selectNext()
            result = While([Parser.parseRelExpression(), None])

            if (Parser.tokens.actual.type == 'LINE_END'):
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseBlock()

                if (Parser.tokens.actual.type == 'END'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == 'LINE_END'):
                        Parser.tokens.selectNext()
                else:
                    raise NameError("Expected End")

        elif (Parser.tokens.actual.type == 'IF'):
            Parser.tokens.selectNext()
            result = If([Parser.parseRelExpression(), None, None])

            if (Parser.tokens.actual.type == 'LINE_END'):
                Parser.tokens.selectNext()
                atual = 0
                result.children[1] = Parser.parseBlock()

                if (Parser.tokens.actual.type == 'ELSEIF'):
                    while(Parser.tokens.actual.type == "ELSEIF"):
                        Parser.tokens.selectNext()
                        newIf = If([Parser.parseRelExpression(), None, None])

                        if (Parser.tokens.actual.type == 'LINE_END'):
                            Parser.tokens.selectNext()
                            newIf.children[1] = Parser.parseBlock()

                        if (atual == 0):
                            result.children[2] = newIf
                            atual = newIf
                        else:
                            atual.children[2] = newIf
                            atual = newIf               
                
                if (Parser.tokens.actual.type == 'ELSE'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == 'LINE_END'):
                        Parser.tokens.selectNext()
                        if (atual == 0):
                            result.children[2] = Parser.parseBlock()
                        else:
                            atual.children[2] = Parser.parseBlock()

                if (Parser.tokens.actual.type == 'END'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == 'LINE_END'):
                        Parser.tokens.selectNext()

                else:
                    raise NameError("Expected End, Else or Elseif")
            
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
                    result.children[1] = Parser.parseExpression() # Right Child

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

        elif (Parser.tokens.actual.type == 'STRING'):
            result = StringVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == 'IDENTIFIER'):
            identifier = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == 'OPEN_P'):
                result = FunctionCall(identifier)
                Parser.tokens.selectNext()

                if (Parser.tokens.actual.type != 'CLOSE_P'):
                    result.children.append(Parser.parseRelExpression())
                    while (Parser.tokens.actual.type == "COMMA"):
                        Parser.tokens.selectNext()
                        result.children.append(Parser.parseRelExpression())

                if (Parser.tokens.actual.type == 'CLOSE_P'):
                    Parser.tokens.selectNext()
                else:
                    raise NameError("Function call missing CLOSE_P or arguments")
            else:
                result = Identifier(identifier) 

        elif (Parser.tokens.actual.type == 'TRUE' or Parser.tokens.actual.type == 'FALSE'):
            result = BoolVal(Parser.tokens.actual.value)
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
    
    