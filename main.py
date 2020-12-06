import sys
from Classes.parser import Parser
from Classes.pre import PreOps
from Classes.symbolTable import *

def main():

    if (len(sys.argv) > 1):
        #if sys.argv[1].lower().endswith('.jl'):
        juliaFile = open(sys.argv[1], 'r')
        operation = juliaFile.read()
        
        #for operation in juliaFile:    
        # Pre processing string
        newString = PreOps.filter(operation)

        # Parsing string
        result = Parser.run(newString)

        # Evaluating the result
        table = SymbolTable()
        result.Evaluate(table)

        #else:
        #    raise NameError(f"Expected Julia extension")
        
    else: 
        return
    return

if __name__ == "__main__":
    main()