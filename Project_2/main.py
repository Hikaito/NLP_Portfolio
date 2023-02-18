# Code by Jordan Frimpter

# Python Input Processing Project
import os
import sys
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from random import randint


def run_game(input_list: list[str]):
    """
    Function to run game loop
    Input:
        input_list (list[str]): the set of words used to run the game
    Example:
        >>>run_game(["these", "are", "the", "words", "for", "the", "game"])
    """

    # type check input for being a list
    if type(input_list) != list:
        print("ERROR: run_gam() requires a list as a parameter.")
        return

    # type check input for having at least one item
    if len(input_list) < 1:
        print("ERROR: run_gam() requires a list with at least one element.")
        return

    # type check input for being a list of strings
    for token in input_list:
        if type(token) != str:
            print("ERROR: run_gam() requires a list composed only of string types (str).")
            return

    score = 5
    user_in = ""
    round_count = 1
    # loop while score is positive and escape character isn't met
    while score > 0 and user_in != "!":
        # round start ------------------------------
        print("============\nRound {}\n".format(round_count))

        random_word = input_list[randint(0, 49)]
        random_word_clone = "_" * len(random_word)
        reject_letters = ""     # collects failed guesses
        success_guesses = ""  # collects successful guesses

        # guess loop ------------------------------
        # repeat guess loop while input is not to exit or the word is not complete
        while user_in != "!" and '_' in random_word_clone:
            print("Word:\n\t" + random_word_clone)
            # print list of failed letters, if applicable
            if reject_letters:
                reject_print = ""
                for letter in reject_letters:
                    reject_print += "'{}', ".format(letter)
                reject_print = reject_print[:-2]
                print("Letters guessed: {}".format(reject_print))
            user_in = input("Enter a letter: ")  # get user input

            # if input was exit, exit
            if user_in == "!":
                print("Game over: all letters exhausted. Word was '{0}'. Final score: {1}".format(random_word, score))
                print("Game Ended. \nFinal Score: {0}\nRounds Won:{1}".format(score, round_count - 1))
                return

            # reject user input that is not a single character; restart input loop
            if len(user_in) != 1:
                print("Please enter a single character.")
                continue

            # force lowercase letter
            user_in = user_in.lower()

            # if input was already guessed, demand new input
            if user_in in reject_letters or user_in in success_guesses:
                # if all 26 letters have been exhausted, end the game
                if (len(reject_letters) + len(success_guesses)) >= 26:
                    print("Game over: all letters exhausted. Word was '{0}'. Final score: {1}".format(random_word, score))
                    print("Game Ended. \nFinal Score: {0}\nRounds Won:{1}".format(score, round_count - 1))
                    return
                # if not all words exhausted, demand new input and restart input loop
                print("'{}' has already been guessed. Try again.".format(user_in))
                continue

            # if the input was in the word, add to score and the display word
            if user_in in random_word:
                for i in range(len(random_word)):
                    if random_word[i] == user_in:
                        random_word_clone = random_word_clone[:i] + user_in + random_word_clone[i+1:]
                score += 1
                success_guesses += user_in
                print("Correct! Score is now {0}".format(score))
            else:
                # if letter was not in word, decrement score
                score -= 1
                reject_letters += user_in
                # if score is 0, end game
                if score <= 1:
                    print("Score reached 0; Game Over.")
                    return

            # print spacer
            print("============")

        # loop reset ------------------------------
        print("---Press any key to continue or '!' (at any time) to exit---")
        user_in = input()

        round_count += 1  # increment rounds

    # Exit screen
    print("Game Ended. \nFinal Score: {0}\nRounds Won:{1}".format(score, round_count - 1))

def tokenize(text: str) -> tuple[list[str], list[str]]:
    """
    Calculate tokens and nouns
    Collects tokens and nouns from input text and prints lexical diversity
    Input:
        text (str) is the contents to tokenize
    Output:
        list of tokens (str): list of strings of raw tokens parsed from text
        list of nouns (str): list of strings of nouns in the text (with duplicates permitted)
    Example:
        >>>tokenize("This is a string")
        >>>[['This', 'is', 'a', 'string'], ['string']]
    """
    # collect words as tokens
    tokens = word_tokenize(text)

    # convert to lowercase
    tokens = [token.lower() for token in tokens]

    # -----------------------------------------------------
    # calculate lexical diversity and output it (I)
    # -----------------------------------------------------
    lex_diversity = {}

    # count instances of each token: if not in dict, add 1 instance. If token is key in dict, increment
    for item in tokens:
        if item in lex_diversity:
            lex_diversity[item] = lex_diversity[item] + 1
        else:
            lex_diversity[item] = 1

    # calculate lexical diversity: get a sum of all tokens and then divide by the token count
    lex_diversity_count = 0
    for item in lex_diversity:
        lex_diversity_count += lex_diversity[item]
    lex_diversity_score = len(lex_diversity) / lex_diversity_count

    # print the diversity score
    print("Lexical Diversity of raw tokens: {:.2f}".format(lex_diversity_score))

    # -----------------------------------------------------
    # reduce tokens to only those that are alphabetic with size greater than 5 and not in the NLTK stopword list
    # -----------------------------------------------------
    # get stopwords
    stop_set = stopwords.words('english')

    # evict all tokens that are not alphabetic
    tokens_limited = [token for token in tokens if (token.isalpha() and len(token) > 5 and token not in stop_set)]

    # -----------------------------------------------------
    # calculate lexical diversity and output it (II)
    # -----------------------------------------------------
    lex_diversity = {}

    # count instances of each token: if not in dict, add 1 instance. If token is key in dict, increment
    for item in tokens_limited:
        if item in lex_diversity:
            lex_diversity[item] = lex_diversity[item] + 1
        else:
            lex_diversity[item] = 1

    # calculate lexical diversity: get a sum of all tokens and then divide by the token count
    lex_diversity_count = 0
    for item in lex_diversity:
        lex_diversity_count += lex_diversity[item]
    lex_diversity_score =  len(lex_diversity) / lex_diversity_count

    # print the diversity score
    print("Lexical Diversity of screened but unlemmatized tokens: {:.2f}".format(lex_diversity_score))

    # -----------------------------------------------------
    # lemmatize the tokens; create a set of unique lemmas
    # -----------------------------------------------------

    word_lemmatizer = WordNetLemmatizer()
    lemmas = [word_lemmatizer.lemmatize(token) for token in tokens_limited]

    # -----------------------------------------------------
    # perform pos tagging on the unique lemmas and print the first 20 tagged
    # -----------------------------------------------------
    unique_lemmas = set(lemmas)

    tagged = nltk.pos_tag(unique_lemmas)

    # print
    print("POS tagging for 20 of the unique lemmas:")
    print(tagged[0:20])

    # -----------------------------------------------------
    # extract tokens that are nouns
    # -----------------------------------------------------
    # get dictionary for series
    lemma_dict = {}
    for token_pair in tagged:
        lemma_dict[token_pair[0]] = token_pair[1]

    # copy only tokens whose first letter in POS (parts of speech) is N (noun)
    nouns = [token for token in lemmas if (lemma_dict[token][0] == 'N')]

    # -----------------------------------------------------
    # calculate lexical diversity and output it (III)
    # -----------------------------------------------------
    lex_diversity = {}

    # count instances of each token: if not in dict, add 1 instance. If token is key in dict, increment
    for item in nouns:
        if item in lex_diversity:
            lex_diversity[item] = lex_diversity[item] + 1
        else:
            lex_diversity[item] = 1

    # calculate lexical diversity: get a sum of all tokens and then divide by the token count
    lex_diversity_count = 0
    for item in lex_diversity:
        lex_diversity_count += lex_diversity[item]
    lex_diversity_score =  len(lex_diversity) / lex_diversity_count

    # print the diversity score
    print("Lexical Diversity of Nouns: {:.2f}".format(lex_diversity_score))

    # -----------------------------------------------------
    # print tokens and nouns count
    # -----------------------------------------------------
    print("Total tokens: {0}\nLemmatized Nouns Number: {1}".format(len(tokens), len(nouns)))

    # -----------------------------------------------------
    # return tokens (raw) and nouns (processed)
    # -----------------------------------------------------

    return tokens, nouns



def main():
    """Main function for project
    Opens file, reads and processes input from file and initiates game loop
    Input (implicit):
        sys.argv[1] must be a filename; terminates if not exactly 2 system arguments (including program name)
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
        file = open(path, "r")  # open file for reading

        # exit prematurely if file could not be read
        if not file.readable():
            print("File " + path + " was not readable. Exiting program.")
            sys.exit("unreadable file")

        # tokenize text if file can be read
        [_, nouns] = tokenize(file.read())

        # collect and count the nouns
        counted_nouns = {}
        for token in nouns:
            if token in counted_nouns:
                counted_nouns[token] += 1
            else:
                counted_nouns[token] = 1

        # collect the 50 most common nouns
        common_nouns = [["", 0]] * 50
        for key in counted_nouns:
            # selection sort
            i = 0
            value = counted_nouns[key]
            # skip if outright less than the last index:
            if value > common_nouns[49][1]:
                # find insertion point
                while i < 50 and value < common_nouns[i][1]:
                    i += 1
                # if insertion point valid, insert and pass down until all things are sorted
                if i < 50:
                    insert = [key, value]
                    remove = ["", 0]
                    while i < 50:
                        removed = common_nouns[i]
                        common_nouns[i] = insert
                        insert = removed
                        i += 1

        # isolate the nouns from their counts
        common_nouns = [token for [token, _] in common_nouns]

        # Print the 50 most common nouns
        print("==========\n50 most common nouns:\n{0}".format(common_nouns))

        # execute game loop
        run_game(common_nouns)


# executes main function
if __name__ == "__main__":
    main()

