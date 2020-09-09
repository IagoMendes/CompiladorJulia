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


## Version Control
v(Major).(Minor).(Build)
