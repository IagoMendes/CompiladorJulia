# Compilador Julia

## Basic number calculator (+ and -) v1.0.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/v1.0/Diagrams/diagrama1.pdf

EBNF:

    EXPRESSION = NUMBER, {("+" | "-"), NUMBER};


## Improved calculator (/ and *) v1.1.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/v1.0/Diagrams/diagrama2.pdf

EBNF:

    EXPRESSION = TERM, {("+" | "-"), TERM};
    TERM = NUMBER, {("*" | "/"), NUMBER};


## Added parenthesis to the expression, along with negative numbers v1.2.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/v1.0/Diagrams/diagrama3.png

EBNF:

    EXPRESSION = TERM, { ("+" | "-"), TERM } ;
    TERM = FACTOR, { ("*" | "/"), FACTOR } ;
    FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;


## Implementing AST and support for files v2.0.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/v1.0/Diagrams/diagrama3.png

EBNF:

    EXPRESSION = TERM, { ("+" | "-"), TERM } ;
    TERM = FACTOR, { ("*" | "/"), FACTOR } ;
    FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;


## Variables, Command Block and Println v2.1.1

Syntactic diagram: https://github.com/IagoMendes/CompiladorJulia/blob/v1.0/Diagrams/diagrama4.png

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


## Version Control
v(Major).(Minor).(Build)
