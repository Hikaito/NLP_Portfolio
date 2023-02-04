# Code by Jordan Frimpter

# Python Input Processing Project

import os
import pickle
import sys
import re

# local file name for pickle file
pickle_file = "out.pickle"


class Person:
    """data container class"""
    def __init__(self, last, first, mi, id_in, phone):
        """Accepts the arguments for data containment and stores as variables
        no error checking is performed because all data classes can be stored as strings
        Expects arguments to be the desired format; class has no self-intellect
        Args:
            last: string item of last name
            first: string item of first name
            mi: string item of middle initial
            id_in: string item of id input
            phone: string item of phone number
        Example:
            >>>person = Person("Smith", "John", "E", "ab1234", "000-000-0000")
        """
        # store variables
        self.last = last
        self.first = first
        self.mi = mi
        self.id_in = id_in  # note: naming this field 'id' will shadow an existing built-in variable
        self.phone = phone

    def __str__(self):
        """Builds internal information into display format and returns as a string
        Permits values that aren't strings internally, as long as they can be cast to strings; returns a string
        Returns string with formatting
        """
        return "Employee id: " + str(self.id_in) + "\n\t" + str(self.first) + " " + str(self.mi) + " " + str(
            self.last) + "\n\t" + str(self.phone)

    def __repr__(self):
        """returns string representation without complex formatting"""
        return str(self.id_in) + ", " + str(self.first) + ", " + str(self.mi) + ", " + str(
            self.last) + ", " + str(self.phone)

    def display(self):
        """Prints string representation of self to screen"""
        print(self)


def validate_id(id_candidate):
    """Generates a valid id in XXDDDD format, where X is uppercase alphabet and D is digit
    Validates file input if possible, and prompts user if not
    Args:
        id_candidate: id string read from file
    Returns: string
        a valid id in the proper format, either from file or user input
    Example:
        >>>validate_id('xx0000')
        >>>'XX0000'
    """

    # type-check id: if id is not a string, make it an empty string
    if type(id_candidate) != str:
        id_candidate = ""

    while True:
        # match ID to regex for content and length
        match = re.search("^[a-zA-Z]{2}[0-9]{4}$", id_candidate)

        # if there is a match to the regex, return uppercase version of the id string
        if match:
            return id_candidate.upper()

        # if the token count for the ID is incorrect or the contents are not valid, reject with message to user
        print("ID invalid: " + id_candidate)
        print("ID is two letters followed by 4 digits")
        id_candidate = input("Please enter a valid id:")    # prompt user for new input


def validate_phone(phone):
    """Generates a valid phone number from file input or user prompting
    Accepts any phone number with 10 numbers in a generally accepted phone number format,
        such as (000) - 000 - 0000 or 000.000-0000 in addition to 000-000-0000
    Args:
        phone: string of candidate phone number
    Returns: string
        valid phone number in 000-000-0000 format
    Example:
        >>>validate_id("(000) - 000 - 0000")
        >>>"000-000-0000"
    """

    # type-check id: if number is not a string, make it an empty string
    if type(phone) != str:
        phone = ""

    # validation loop
    while True:
        # match if it resembles a phone number, capture the number groups for reformatting
        match = re.search("^\(?\s*([0-9]{3})\s*\)?\s*[+.-]?\s*([0-9]{3})\s*[+.-]?\s*([0-9]{4})$", phone)

        # if phone number was found, return phone number with proper format from capture groups
        if match:
            return match.group(1) + "-" + match.group(2) + "-" + match.group(3)

        # if the token count is incorrect or the contents are not valid, reject
        print("Phone " + phone + " is invalid")
        print("Enter phone number in form 123-456-7890")
        phone = input("Enter phone number:")    # prompt new input from user


def process_input(path):
    """Process input file function by opening a data file and reading each line into a Person object stored in a dict
        Expected format: first line is header, following lines have the pattern of
        Last,First,MiddleInitial,ID,OfficePhone
        or Last,First,ID,OfficePhone
    Args:
        path: a string of a data file's absolute path (expected to be a file that exists)
    Returns:
        dict of Person objects, where the person's id is the key and the Person object is the value
    Example:
        >>>process_input("D:\desktop\file.dat")
    """

    # open and read file
    file = open(path, "r")  # open file for reading

    # exit prematurely if file could not be read
    if not file.readable():
        print("File " + path + " was not readable. Exiting program.")
        sys.exit("unreadable file")

    # divide input into a set of lines
    lines = file.read().split('\n')

    # generate dictionary
    people = {}

    # process every line in the file, disregarding the first line
    for line in lines[1:]:
        tokens = line.split(',')    # split line on comma

        token_count = len(tokens)  # collect number of tokens

        # abandon line if improper token count identified
        if not (token_count == 4 or token_count == 5):
            print("Invalid line token count; expected 4 or 5, received " + str(token_count) + "; Line skipped. Line: "
                  + line)
            continue

        # extend tokens array if middle name is absent
        if token_count == 4:
            tokens = tokens[0:2] + [""] + tokens[2:]

        # strip all tokens of leading and trailing whitespace
        for i in range(token_count):
            tokens[i] = tokens[i].strip()

        # validate last name----------------------------
        # if no last name, reject line
        if not tokens[0]:
            print("Missing last name; rejecting line")
            continue
        # test first character for alphabet; reject if not alphabet
        if not tokens[0][0].isalpha():
            print("Invalid last name '" + tokens[0] + "'; rejecting line")
            continue
        # force leading letter uppercase and following letters lowercase
        tokens[0] = tokens[0][0].upper() + tokens[0][1:].lower()

        # validate first name----------------------------
        # if no first name, reject line
        if not tokens[1]:
            print("Missing first name; rejecting line")
            continue
        # test first character for alphabet; reject if not alphabet
        if not tokens[1][0].isalpha():
            print("Invalid first name '" + tokens[1] + "'; rejecting line")
            continue
        # force leading letter uppercase and following letters lowercase
        tokens[1] = tokens[1][0].upper() + tokens[1][1:].lower()

        # validate middle initial----------------------------
        # if no middle name, middle name is single character
        if not tokens[2]:
            tokens[2] = "X"

        # if a middle name was read in from file, process middle name
        else:
            # if middle name is not alphabet, reject
            if not tokens[2][0].isalpha():
                print("Invalid middle name; rejecting line")
                continue
            # if middle name is alphabet, force single token capital case
            tokens[2] = tokens[2][0].upper()

        # validate id----------------------------
        tokens[3] = validate_id(tokens[3])

        # validate phone----------------------------
        tokens[4] = validate_phone(tokens[4])

        # detect employee ID overwrite and display warning
        if tokens[3] in people:
            print("WARNING: ID " + tokens[3] + " already exists in records; existing information is being overwritten.")

        # if line was not rejected, create person object and add to dictionary with id as key
        people[tokens[3]] = Person(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])

    return people


def main():
    """Main function for project
    Opens file, reads in person objects, saves as pickle file and validates as pickle file
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

        # process file into a dictionary of person objects
        people = process_input(path)

        # pickle the file
        pickle.dump(people, open(pickle_file, 'wb'))  # save binary pickle file

        # open the pickled file
        from_pickle = pickle.load(open(pickle_file, 'rb'))  # read binary pickle file

        # confirm file's contents by displaying in display format
        for person in from_pickle:
            from_pickle[person].display()
            print("")


# executes main function
if __name__ == "__main__":
    main()
