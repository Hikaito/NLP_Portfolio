# Code by Jordan Frimpter

# Python Input Processing Project
import os
import sys
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
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
        if not token:
            print("ERROR: run_gam() expects a list with no empty strings.")
            return

    # force wordlist to be lowercase
    input_list = [token.lower() for token in input_list]

    # print game header
    print("\n\n<<<===  Word Guessing Game ===>>>")
    print("Ready? Begin.")

    score = 5
    user_in = ""
    round_count = 0
    # loop while score is positive and escape character isn't met
    while score > 0 and user_in != "!":
        # round start ------------------------------
        print("============\nRound {}\n".format(round_count + 1))

        # collect a random word, prepare the word guess arrays
        random_word = input_list[randint(0, 49)]
        random_word_clone = "_" * len(random_word)
        reject_letters = ""   # collects failed guesses
        success_guesses = ""  # collects successful guesses

        # guess loop ------------------------------
        # repeat guess loop while input is not to exit or the word is not complete
        while '_' in random_word_clone:
            # print the word being guessed
            print("Word:\n\t" + random_word_clone)

            # if there are letters in the rejects list, prepare and display the failed letters guessed line
            # print list of failed letters, if applicable
            if reject_letters:
                reject_print = ""
                for letter in reject_letters:
                    reject_print += "{}, ".format(letter)
                reject_print = reject_print[:-2]
                print("Incorrect letters guessed: {}".format(reject_print))

            # get user input
            user_in = input("Guess a letter: ")

            # if input was exit, exit
            if user_in == "!":
                print("\n\nGame Ended. Word was '{2}'.\nFinal Score: {0}\nRounds Won: {1}".format(score, round_count, random_word))
                return

            # reject user input that is not a single character and is not alpha; restart input loop
            if len(user_in) != 1 or not user_in.isalpha():
                print("Please enter a single character.")
                continue

            # force lowercase letter
            user_in = user_in.lower()

            # if input was already guessed, demand new input
            if user_in in reject_letters or user_in in success_guesses:
                # if all 26 letters have been exhausted, end the game
                if (len(reject_letters) + len(success_guesses)) >= 26:
                    print("\n\nGame Ended: all letters exhausted. Word was '{2}'.\nFinal Score: {0}\nRounds Won: {1}".format(score, round_count, random_word))
                    return
                # if not all words exhausted, demand new input and restart input loop
                print("'{}' has already been guessed. Try again. Score is {}".format(user_in, score))
                continue

            # if the input was in the word, add to the score
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
                print("Incorrect guess. Score is now {0}".format(score))
                # if score is 0, end game
                if score < 1:
                    print("\n\nGame Ended: score reached zero. Word was '{2}'.\nFinal Score: {0}\nRounds Won: {1}".format(score, round_count, random_word))
                    return

            # print spacer
            print("============")

        #------logic for completed a round------

        # print user message
        print("Word '{}' successfully guessed.".format(random_word))

        # increment round
        round_count += 1  # increment rounds

        # loop reset ------------------------------
        print("---Press any key to continue or '!' (at any time) to exit---")
        user_in = input()

        # exit if '!'
        if user_in == "!":
            break

    # Exit screen
    print("\n\nGame Ended. \nFinal Score: {0}\nRounds Won: {1}".format(score, round_count))

def tokenize(text: str) -> tuple[list[str], list[str]]:
    """
    Collects tokens and nouns from input text and prints lexical diversity and other statistics in the process
    Input:
        text (str) is the contents to tokenize
    Output:
        list of tokens (str): list of strings of raw tokens parsed from text
        list of nouns (str): list of strings of lowercase nouns in the text (with duplicates permitted)
    Example:
        >>>tokenize("This is a string")
        >>>[['This', 'is', 'a', 'String'], ['string']]
    """
    # -----------------------------------------------------

    # lowercase the text
    text = text.lower()

    # collect words as tokens
    tokens = word_tokenize(text)

    # -----------------------------------------------------
    # calculate lexical diversity and output it (I)
    # -----------------------------------------------------
    # calculate score
    token_set = set(tokens)
    lex_diversity_score = len(token_set) / len(tokens)

    # print the diversity score
    print("Lexical Diversity of tokens (lowercased) to number of tokens: {:.2f}".format(lex_diversity_score))

    # -----------------------------------------------------
    # reduce tokens to only those that are alphabetic with size greater than 5 and not in the NLTK stopword list
    # -----------------------------------------------------
    # get stopwords
    stop_set = stopwords.words('english')

    # evict all tokens that are not alphabetic, longer than 5, and not in the stop word set
    tokens_limited = [token for token in tokens if (token.isalpha() and len(token) > 5 and token not in stop_set)]

    # -----------------------------------------------------
    # calculate lexical diversity and output it (II)
    # -----------------------------------------------------
    # calculate score
    token_set = set(tokens_limited)
    lex_diversity_score = len(token_set) / len(tokens)

    # print the diversity score
    print("Lexical Diversity of screened but unlemmatized tokens to total tokens: {:.2f}".format(lex_diversity_score))

    # calculate score
    lex_diversity_score = len(token_set) / len(tokens_limited)

    # print the diversity score
    print("Lexical Diversity of screened but unlemmatized tokens to number of unlemmatized tokens: {:.2f}".format(lex_diversity_score))

    # -----------------------------------------------------
    # lemmatize the tokens; create a set of unique lemmas
    # -----------------------------------------------------

    word_lemmatize = WordNetLemmatizer()
    lemmas = [word_lemmatize.lemmatize(token) for token in tokens_limited]

    # -----------------------------------------------------
    # perform pos tagging on the unique lemmas
    # -----------------------------------------------------
    unique_lemmas = set(lemmas)

    tagged = nltk.pos_tag(unique_lemmas)

    # -----------------------------------------------------
    # extract tokens that are nouns
    # -----------------------------------------------------
    # get dictionary for unique lemmas
    lemma_dict = {}
    for token_pair in tagged:
        lemma_dict[token_pair[0]] = token_pair[1]

    # copy only tokens whose first letter in POS (parts of speech) is N (noun)
    nouns = [token for token in lemmas if (lemma_dict[token][0] == 'N')]

    # -----------------------------------------------------
    # calculate lexical diversity and output it (III)
    # -----------------------------------------------------
    # calculate score
    token_set = set(nouns)
    lex_diversity_score = len(token_set) / len(tokens)

    # print the diversity score
    print("Lexical Diversity of nouns to total tokens: {:.2f}".format(lex_diversity_score))

    # calculate again
    lex_diversity_score = len(token_set) / len(nouns)

    # print the diversity score
    print("Lexical Diversity of nouns to number of nouns: {:.2f}".format(lex_diversity_score))

    # -----------------------------------------------------
    # print 20 tagged lemmas, and the token and noun count
    # -----------------------------------------------------
    # print the first 20 tagged lemmas
    print("POS tagging for 20 of the unique lemmas:")
    print(tagged[0:20])

    print("Total Tokens: {0}\nTotal Lemmatized Nouns: {1}".format(len(tokens), len(nouns)))
    print("Total Unique tokens: {0}\nTotal Unique Nouns: {1}".format(len(set(tokens)), len(set(nouns))))

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

