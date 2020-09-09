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


## Version Control
v(Major).(Minor).(Build)
