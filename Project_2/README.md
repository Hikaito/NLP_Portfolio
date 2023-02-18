# Text Game in Python

[Game Code](https://github.com/Hikaito/NLP_Portfolio/blob/main/Project_2/main.py)

## Summary
The text game accepts a text file argument.
The text file is parsed into tokens.
Tokens are all formatted to lowercase for accuracy in counting.
The wordset used for the game is composed of only the 50 most frequent lemmatized tokens tagged as nouns that are longer than 5 characters not in the NLTK stopword list with only alphabetic components.
During the word generation process, lexical diversity is calculated at several points.
Please note that the program expects there to be at least 50 unique noun tokens in the input text or the game portion will not work.

The game asks users to guess the letters in a word; it displays correct and incorrect guesses.
The game tracks the rounds the user has won and the current score, a metric of correct and incorrect guesses.
The game ends when the user enters the `!` token.

## Use
The program is tested with the prompt `Python3 main.py [file]` from within the directory with the main file.
`[file]` is replaced with the relative path of the file from the directory.
The text file should contain the text to process for the word game.

Example:
`Python3 main.py anat19.txt`

## Test Text Source
Text used for game sourced from OpenStax Anatomy and Physiology textbook (to my knowledge).

Distributed under [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)

Access for free [here](https://openstax.org/books/anatomy-and-physiology/pages/1-introduction)