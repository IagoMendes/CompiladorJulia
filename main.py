import sys
from Classes.parser import Parser
from Classes.pre import PreOps

def main():

    # Getting string from terminal 
    string = ""
    if (len(sys.argv) > 1):
        string = sys.argv[1]
    else: 
        return

    # Pre processing string
    newString = PreOps.filter(string)

    # Parsing string
    result = Parser.run(newString)

    # Printing out the result
    sys.stdout.write(str(result))
    return

if __name__ == "__main__":
    main()