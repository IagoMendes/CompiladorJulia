from Classes.token import Token

tokens = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "(": "OPEN_P",
    ")": "CLOSE_P",
    "\n": "LINE_END",
    "=": "EQUAL",
    "<": "LESSER",
    ">": "GREATER",
    "!": "NOT",
    ":": "COLON"
}

keywords = {
    "println"  : "PRINT",
    "if"       : "IF",
    "else"     : "ELSE",
    "elseif"   : "ELSEIF",
    "while"    : "WHILE",
    "end"      : "END",
    "local"    : "LOCAL",
    "Int"      : "INT",
    "Bool"     : "BOOL",
    "true"     : "TRUE",
    "false"    : "FALSE"
}

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
    
    def selectNext(self):
        if (self.position == len(self.origin)):
            self.actual = Token('', 'EOF')
            return
        
        elif (self.origin[self.position] == " "):
            self.position += 1
            self.selectNext()

        elif (self.origin[self.position] in tokens):
            self.actual = Token(self.origin[self.position], tokens[self.origin[self.position]])
            self.position += 1
            
            if (self.position < len(self.origin)):
                if (self.origin[self.position] == "="):
                    self.actual = Token("==", "EQUAL_I")
                    self.position += 1

                elif (self.origin[self.position] == ":"):
                    self.actual = Token("::", "COLON_I")
                    self.position += 1

        elif (self.origin[self.position] == "&"):
            self.position += 1

            if (self.position < len(self.origin)):
                if (self.origin[self.position] == "&"):
                    self.actual = Token("&&", "AND")
                    self.position += 1
            else:
                raise NameError("Error with character '&'")

        elif (self.origin[self.position] == "|"):
            self.position += 1
            if (self.position < len(self.origin)):
                if (self.origin[self.position] == "|"):
                    self.actual = Token("||", "OR")
                    self.position += 1
            else:
                raise NameError("Error with character '|'")

        elif (self.origin[self.position].isnumeric()):
            resToken = ""
            while (self.position < len(self.origin) and (self.origin[self.position].isnumeric())):
                resToken += self.origin[self.position]
                self.position += 1
                if (self.origin[self.position].isalpha() or self.origin[self.position] == "_"):
                    raise NameError("Error creating number, found character")
            self.actual = Token(resToken, "INT")

        elif (self.origin[self.position].isalpha()):
            resToken = ""
            while (self.position < len(self.origin) and \
                  (self.origin[self.position].isnumeric() or \
                   self.origin[self.position].isalpha() or \
                   self.origin[self.position] == "_")):
                resToken += self.origin[self.position]
                self.position += 1

            if resToken in keywords:
                self.actual = Token(resToken, keywords[resToken])
            else:
                self.actual = Token(resToken, "IDENTIFIER")

        else:
            raise NameError("Unknown token")
        
        return