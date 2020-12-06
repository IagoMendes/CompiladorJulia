# Compilador Julia

## Basic number calculator (+ and -) v1.0.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama1.pdf

EBNF:

    EXPRESSION = NUMBER, {("+" | "-"), NUMBER};


## Improved calculator (/ and *) v1.1.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama2.pdf

EBNF:

    EXPRESSION = TERM, {("+" | "-"), TERM};
    TERM = NUMBER, {("*" | "/"), NUMBER};


## Added parenthesis to the expression, along with negative numbers v1.2.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama3.png

EBNF:

    EXPRESSION = TERM, { ("+" | "-"), TERM } ;
    TERM = FACTOR, { ("*" | "/"), FACTOR } ;
    FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;


## Implementing AST and support for files v2.0.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama3.png

EBNF:

    EXPRESSION = TERM, { ("+" | "-"), TERM } ;
    TERM = FACTOR, { ("*" | "/"), FACTOR } ;
    FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;


## Variables, Command Block and Println v2.1.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama4.png

EBNF:

    BLOCK = { COMMAND } ;
    COMMAND = ( λ | ASSIGNMENT | PRINT), "\n" ;
    ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
    PRINT = "printl", "(", EXPRESSION, ")" ;
    EXPRESSION = TERM, { ("+" | "-"), TERM } ;
    TERM = FACTOR, { ("*" | "/"), FACTOR } ;
    FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
    IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
    NUMBER = DIGIT, { DIGIT } ;
    LETTER = ( a | ... | z | A | ... | Z ) ;
    DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;


## If, While and logical operations (!, &&, ||, ==, >, <) v2.2.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama5.png

EBNF:

    BLOCK = { COMMAND };
    COMMAND = ( ASSIGNMENT | PRINT | IF | WHILE );
    ASSIGNMENT = IDENTIFIER, “=”, ( RELEX | “readline()”);
    PRINT = “println”, “(“, RELEX, “)”;
    WHILE = “while”, RELEX, BLOCK, “end”;
    IF = “if”, RELEX, BLOCK, { ELSE | ELSEIF }, “end”;
    ELSEIF = “elseif”, RELEX, BLOCK, { ELSE | ELSEIF };
    ELSE = “else”, BLOCK;
    RELEX = EXPRESSION, { (“==” | “<” | “>”), EXPRESSION };
    EXPRESSION = TERM, { (“+” | “-” | “||”), TERM };
    TERM = FACTOR, { (“*” | “/” | “&&”), FACTOR };
    FACTOR = ( ( “+” | “-” | “!”), FACTOR) | NUMBER | IDENTIFIER | “(“, RELEX, “)”;
    IDENTIFIER = LETTER, { LETTER | DIGIT | “_” };
    NUMBER = DIGIT, { DIGIT };
    LETTER = ( a | … | z | A | … | Z );
    DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );


## Variable types and Strings v2.3.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama6.png

EBNF:

    BLOCK = { COMMAND };
    COMMAND = ( LOCAL | ASSIGNMENT | PRINT | IF | WHILE );
    LOCAL = "local", IDENTIFIER, "::", TYPE;
    ASSIGNMENT = IDENTIFIER, “=”, ( RELEX | “readline()”);
    PRINT = “println”, “(“, RELEX, “)”;
    WHILE = “while”, RELEX, BLOCK, “end”;
    IF = “if”, RELEX, BLOCK, { ELSE | ELSEIF }, “end”;
    ELSEIF = “elseif”, RELEX, BLOCK, { ELSE | ELSEIF };
    ELSE = “else”, BLOCK;
    RELEX = EXPRESSION, { (“==” | “<” | “>”), EXPRESSION };
    EXPRESSION = TERM, { (“+” | “-” | “||”), TERM };
    TERM = FACTOR, { (“*” | “/” | “&&”), FACTOR };
    FACTOR = ( ( “+” | “-” | “!”), FACTOR) | NUMBER | BOOL | STRING | IDENTIFIER | “(“, RELEX, “)”;
    IDENTIFIER = LETTER, { LETTER | DIGIT | “_” };
    NUMBER = DIGIT, { DIGIT };
    LETTER = ( a | … | z | A | … | Z );
    DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
    TYPE = "Int" | "Bool" | "String"; 
    BOOL = "true" | "false";
    STRING = '"', {.*?}, '"';
    

## Functions v2.4.0

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/master/Diagrams/diagrama7.png

EBNF:

    MAIN = { BLOCKF | COMMAND };
    BLOCK = { COMMAND };
    COMMAND = ( LOCAL | ASSIGNMENT | PRINT | IF | WHILE | FUNCTIONCALL | ( "return", RELEX ) );
    BLOCKF = "function", IDENTIFIER, "(", (IDENTIFIER, "::", TYPE), {",", IDENTIFIER, "::", TYPE}, ")", "::", TYPE, "\n", { COMMAND }, "end";
    FUNCTIONCALL = IDENTIFIER, "(", ( RELEX ), {",", RELEX}, ")";
    LOCAL = "local", IDENTIFIER, "::", TYPE;
    ASSIGNMENT = IDENTIFIER, “=”, ( RELEX | “readline()”);
    PRINT = “println”, “(“, RELEX, “)”;
    WHILE = “while”, RELEX, BLOCK, “end”;
    IF = “if”, RELEX, BLOCK, { ELSE | ELSEIF }, “end”;
    ELSEIF = “elseif”, RELEX, BLOCK, { ELSE | ELSEIF };
    ELSE = “else”, BLOCK;
    RELEX = EXPRESSION, { (“==” | “<” | “>”), EXPRESSION };
    EXPRESSION = TERM, { (“+” | “-” | “||”), TERM };
    TERM = FACTOR, { (“*” | “/” | “&&”), FACTOR };
    FACTOR = ( ( “+” | “-” | “!”), FACTOR) | NUMBER | BOOL | STRING | IDENTIFIER | “(“, RELEX, “)” | FUNCTIONCALL;
    IDENTIFIER = LETTER, { LETTER | DIGIT | “_” };
    NUMBER = DIGIT, { DIGIT };
    LETTER = ( a | … | z | A | … | Z );
    DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
    TYPE = "Int" | "Bool" | "String"; 
    BOOL = "true" | "false";
    STRING = '"', {.*?}, '"';

## Assembly v3.0.0

Simpler compiler (without functions, strings and "readline"), but generates .asm file for julia code.


## Version Control
v(Major).(Minor).(Build)
