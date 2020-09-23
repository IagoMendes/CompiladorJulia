import sys
from Classes.parser import Parser
from Classes.pre import PreOps

def main():

    if (len(sys.argv) > 1):
        #if sys.argv[1].lower().endswith('.jl'):
        juliaFile = open(sys.argv[1])

        for operation in juliaFile:
            # Pre processing string
            newString = PreOps.filter(operation)

            # Parsing string
            result = Parser.run(newString)

            # Printing out the result
            sys.stdout.write(str(result.Evaluate()))

        #else:
        #    raise NameError(f"Expected Julia extension")
    else: 
        return
 
    return

if __name__ == "__main__":
    main()