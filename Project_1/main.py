# Code by Jordan Frimpter

# Python Input Processing Project

import os
import pickle
import sys
import re

# local file name for pickle file
pickleFile = "out.p"

class Person:
    """data container class"""
    def __init__(self, last, first, mi, id_in, phone):
        """Accepts the arguments for data containment and stores as variables

        no error checking is performed because all data classes can be stored as strings"""
        # store variables
        self.last = last
        self.first = first
        self.mi = mi
        self.id_in = id_in
        self.phone = phone

    def __str__(self):
        """Builds internal information into display format and returns as a string

        Permits values that aren't strings internally, as long as they can be cast to strings
        returns a string
        """
        # if middle initial has a value, include it in the string
        if self.mi:
            return "Employee id: " + str(self.id_in) + "\n\t" + str(self.first) + " " + str(self.mi) + " " + str(
                self.last) + "\n\t" + str(self.phone)
        # if middle initial doesn't have a value, don't include it in the string
        return "Employee id: " + str(self.id_in) + "\n\t" + str(self.first) + " " + str(self.last) + "\n\t" + str(
            self.phone)

    def __repr__(self):
        """returns call to __str__(self)"""
        return self.__str__()

    def display(self):
        """Prints string representation of self to screen"""
        print(self)

def validateId(idCandidate):
    """Generates a valid id
    input: id string read from file
    output: valid id, either from file or user"""

    # typecheck id: if id is not a string, make it an empty string
    if type(idCandidate) != str:
        idCandidate = ""

    while True:
        # match ID to regex for content and length
        match = re.search("^[a-zA-Z]{2}[0-9]{4}$", idCandidate)

        # if there is a match to the regex, return uppercase version of the id string
        if match:
            return idCandidate.upper()

        # if the token count for the ID is incorrect or the contents are not valid, reject
        print("ID invalid: " + idCandidate)
        print("ID is two letters followed by 4 digits")
        print("Please enter a valid id:")
        idCandidate = input()    # get new input from user

def validatePhone(phone):
    """Generates a valid phone number
    Accepts any phone number with 10 numbers in a generally accepted phone number format, such as (000) - 000 - 0000 or 000.000.0000
    in addition to 000-000-0000
    input: string read from file
    output: valid phone number, either from file or user"""

    # typecheck id: if number is not a string, make it an empty string
    if type(phone) != str:
        phone = ""

    while True:
        # match if it resembles a phone number, capture the number groups for reformatting
        match = re.search("^\(?\s*([0-9]{3})\s*[+.-]?\)?\s*[\s+.-]?\s*([0-9]{3})\s*[+.-]?\s*([0-9]{4})$", phone)

        # if phone number was found, return phone number with proper format
        if match:
            return match.group(1) +  "-" + match.group(2) + "-" + match.group(3)

        # if the token count is incorrect or the contents are not valid, reject
        print("Phone " + phone + " is invalid")
        print("Enter phone number in form 123-456-7890:")
        phone = input()    # get new input from user

def processInput(path):
    """Process input file function
    inputs: a string path to an existing file.
        Expected format: first line is header, following lines have the pattern of
            Last,First,MiddleInitial,ID,OfficePhone
            or Last,First,ID,OfficePhone
    outputs: dictionary of People objects
    """

    people = {}

    # open and read file
    file = open(path, "r")  # open file for reading
    # exit prematurely if file could not be read
    if not file.readable():
        print("File " + path + " was not readable. Exiting program.")
        sys.exit("unreadable file")

    # divide input into a set of lines
    lines = file.read().split('\n')

    # process every line in the file, disregarding the first line
    for line in lines[1:]:
        tokens = line.split(',')    # split line on comma

        tokenCount = len(tokens) # collect number of tokens

        # abandon line if improper token count identified
        if not (tokenCount == 4 or tokenCount == 5):
            print("Invalid line token count; expected 4 or 5, received " + str(tokenCount) + "; Line skipped. Line: " + line)
            continue

        # extend tokens array if middle name is absent
        if tokenCount == 4:
            tokens = tokens[0:2] + [""] + tokens[2:]

        # strip all tokens of leading and trailing whitespace
        for i in range(tokenCount):
            tokens[i] = tokens[i].strip()

        # validate last name----------------------------
        # if no last name, reject line
        if not tokens[0]:
            print("Missing last name; rejecting line")
            continue
        # test first character for alphabet; reject if not alphabet
        if not tokens[0][0].isalpha():
            print("Invalid last name; rejecting line")
            continue
        # force leading letter uppercase
        tokens[0] = tokens[0][0].upper() + tokens[0][1:].lower()

        # validate first name----------------------------
        # if no first name, reject line
        if not tokens[1]:
            print("Missing first name; rejecting line")
            continue
        # test first character for alphabet; reject if not alphabet
        if not tokens[1][0].isalpha():
            print("Invalid first name; rejecting line")
            continue
        # force leading letter uppercase
        tokens[1] = tokens[1][0].upper() + tokens[1][1:].lower()

        # validate middle initial----------------------------
        # if no middle name, middle name is single character
        if not tokens[2]:
            tokens[2] = "X"
        else:
            # if middle name is not alphabet, reject
            if not tokens[2][0].isalpha():
                print("Invalid middle name; rejecting line")
                continue
            # if middle name is alphabet, force single token capital case
            tokens[2] = tokens[2][0].upper()

        # validate id----------------------------
        tokens[3] = validateId(tokens[3])

        # validate phone----------------------------
        tokens[4] = validatePhone(tokens[4])

        # if line was not rejected, create person object
        people[tokens[3]] = Person(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])

    return people

def main():
    """Project_1

    Input expected as a sysarg; exits prematurely if absent
    """

    #exit prematurely if too few arguments
    if len(sys.argv) < 2:
        print("Expected 1 sysarg, recieved 0. Exiting program")
        sys.exit("Too few arguments")

    # exit prematurely if too many arguments
    elif len(sys.argv) > 2:
        # counts arguments after program name
        print("Expected 1 sysarg, recieved " + str(len(sys.argv) - 1) + "; Exiting program.")
        sys.exit("Too many arguments")

    # continue to code if there is one argument
    path = os.path.join(os.getcwd(), sys.argv[1])

    # validate file exists
    if not os.path.exists(path):
        print("File " + path + " was not found. Exiting program.")
        sys.exit("nonexistent file")

    # process file
    people = processInput(path)

    # print people
    for person in people:
        people[person].display()
        print("\n")

    print(people)

    # pickle the file
    pickle.dump(people, open(pickleFile, 'wb')) # save binary pickle file

    # open the file
    fromPickle = pickle.load(open(pickleFile, 'rb')) # read binary pickle file

    # confirm file
    print(fromPickle)

# executes main function
if __name__ == "__main__":
    main()
