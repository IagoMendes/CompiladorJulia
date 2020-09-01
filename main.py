import sys
from Classes.parser import Parser

def main():
    string = ""
    if (len(sys.argv) > 1):
        string = sys.argv[1].replace(" ", "")

    result = Parser.run(string)

    sys.stdout.write(str(result))

if __name__ == "__main__":
    main()