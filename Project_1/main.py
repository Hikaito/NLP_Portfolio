# Code by Jordan Frimpter

# Python Input Processing Project


# main function for python project
import os
import sys
import re

class Person:
    '''Data container class'''
    def __init__(self, last, first, mi, id, phone):
        '''Accepts the arguments for data containment and stores as variables

        no error checking is performed because all data classes can be stored as strings'''
        # store variables
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def __str__(self):
        '''Builds internal information into display format and returns as a string

        Permits values that aren't strings internally, as long as they can be cast to strings
        returns a string
        '''
        # if middle initial has a value, include it in the string
        if self.mi:
            return "Employee id: " + str(self.id) + "\n\t" + str(self.first) + " " + str(self.mi) + " " + str(
                self.last) + "\n\t" + str(self.phone)
        # if middle initial doesn't have a value, don't include it in the string
        return "Employee id: " + str(self.id) + "\n\t" + str(self.first) + " " + str(self.last) + "\n\t" + str(
            self.phone)

    def display(self):
        '''Prints string representation of self to screen'''
        print(self.__str__())

def processInput(path):
    '''Process input file function
    inputs: a string path to an existing file.
        Expected format: first line is header, following lines have the pattern of
            Last,First,MiddleInitial,ID,OfficePhone
            or Last,First,ID,OfficePhone
    outputs: dictionary of People objects
    '''

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
        # if the token count for the ID is incorrect, reject
        if not len(tokens[3]) == 6:
            print("Invalid id '" + tokens[3] + "'; rejecting line")
            continue;
        match = re.search("[a-zA-Z]{2}[0-9]{4}", tokens[3])
        if not match:
            print("Invalid id '" + tokens[3] + "'; rejecting line")
            continue
        # force uppercase
        tokens[3] = tokens[3].upper()

        # validate phone----------------------------
        # remove all whitespace
        tokens[4] = "".join(tokens[4].split())
        #FIIXME accepts improper number counts for some reason
        match = re.search("[0-9]{3}[\s+.-]*[0-9]{3}[\s+.-]*[0-9]{4}", tokens[4])
        if not match:
            print("Invalid phone number '" + tokens[4] + "'; rejecting line")
            continue
        # if line has proper number set, rebuild phone number
        tokens[4] = match.string[:3] + "-" + match.string[4:7] + "-" + match.string[8:]

        # if line was not rejected, create person object
        people[tokens[3]] = Person(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])

    return people

def main():
    """Project 1

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

# executes main function
if __name__ == "__main__":
    main()
