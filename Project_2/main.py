# Code by Jordan Frimpter

# Python Input Processing Project
import os
import sys
from nltk import word_tokenize

def tokenize(text: str) -> str:
    """
    Calculate token stuff
    Input:
        text (str) is the contents to tokenize
    Output:
        ???
    Example:
        >>>main()
    """
    # collect words as tokens
    tokens = word_tokenize(text)
    return tokens

def main():
    """Main function for project
    Opens file
    Input (implicit):
        sys.argv[1] must be a filename; terminates if not exactly 2 system arguments
    Example:
        >>>main()
    """

    #exit prematurely if too few arguments to program call
    if len(sys.argv) < 2:
        print("Expected 1 sys.argv, received 0. Exiting program")
        sys.exit("Too few arguments")

    # exit prematurely if too many arguments to program call
    elif len(sys.argv) > 2:
        # counts arguments after program name
        print("Expected 1 sys.argv, received " + str(len(sys.argv) - 1) + "; Exiting program.")
        sys.exit("Too many arguments")

    else:
        # continue to code if there is one argument

        #get path of file from input and current working directory
        path = os.path.join(os.getcwd(), sys.argv[1])

        # validate file exists; exit if not found
        if not os.path.exists(path):
            print("File " + path + " was not found. Exiting program.")
            sys.exit("nonexistent file")

        # open file





# executes main function
if __name__ == "__main__":
    main()

