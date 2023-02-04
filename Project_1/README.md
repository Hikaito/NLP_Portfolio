# Text Processing in Python

### Use
* [Python Text Processing Script](https://github.com/Hikaito/NLP_Portfolio/blob/main/Project_1/main.py)

This script reads comma separated values from a datafile given as a system argument
and prompts the user for validation for certain value fields; the information from the datafile is
stored in data container objects and exported as a pickle file.


## Use
The script can be tested with the prompt `main.py [filepath for datafile]` from within the directory with `main.py`.
An example of this in the presented project would be `main.py data\data.csv` in a Windows environment.
From a command line in the directory, this would be `Python3 main.py data\data.csv`.

The script produces a pickle file whose default name is `out.p`; the global variable `pickle_file`
can be changed to export to a different filename or absolute path location.

The input file is expected to be a comma separated file with lines in the format `Last,First,Middle Initial,ID,Office Phone` for 5 elements
or `Last,First,ID,Office Phone` for 4 fields (the script will automatically add a middle initial if necessary).
Lines are separated with `\n` characters.

## Analysis
Python is a strong language for text based processing because its built in mechanisms for string processing are very flexible and simple to work with.
The syntax is designed to make text processing simple and straightforward, which really benefits the readability and writability with the language.
It is not without its caveats, however.
Python as an interpreted language is extremely slow with some operations and less than speedy with the rest.
Although the underlying code for libraries can be written in C and made very efficient, the benefits of such efficiency are often lost by abstraction.
Python with its dynamic type checking will accept any datatype assignment to variables without complaint, only to break later when the variables do not have the properties of the type the code was written to manipulate.
The main cost of dynamic typing with python is that the code to type-check variables is bulky and required at the top of every function, adding unnecessary overhead to simple tasks.
It is a very good language for beginners because of its dynamic typing.

While working on this project, I learned to write more ‘Pythonic’ code.
I had prior experience with Python from several machine learning projects I’ve worked on, but one can never know everything there is to know about a language.
Working with code is a process of constant learning.
In particular, I improved my knowledge of docstring usage and type-checking in Python code to write more robust functions.
