# N-Gram Language Classification
This project was built as a collaboration of myself and [Henry Kim](https://github.com/6henrykim).

This program classifies text language based on unigram and bigram presence in a language training corpus.
This program is divided into two parts.

* [Part 1 Code](https://github.com/Hikaito/NLP_Portfolio/blob/main/Project_4/n-gram-language-model/part1.py)
* [Part 2 Code]()
* [More about N-Grams](https://github.com/Hikaito/NLP_Portfolio/blob/main/Project_4/N-Grams.pdf)

## Part 1
The first portion of this program reads from three language training files and creates pickle files of the counts of each unigram and bigram.
The program lowercases all tokens before calculations take place and sets all arabic integer numbers to `"NUM"`" instead.

The `count_unigrams_and_bigrams` function accepts the argument of a file path and generates a dictionary of the unigram and bigram count in the file described by the path.

The `main` function uses `count_unigrams_and_bigrams` to generate pickle files of the dictionaries of unigram and bigram counts.
The files used to generate the pickle files can be changed with the `training_data` variable at the top of `main`.
The output file format is `[input file].unigrams.pickle` for the unigram count dictionary pickle file
and `[input file].bigrams.pickle` for the bigram count dictionary pickle file.

This function can take some time to run on large corpuses.

## Part 2
The second portion of this program predicts the language of a sample text and collects metrics of accuracy.

The `compute_log_prob` function computes the log probability of text belonging to a given language from the following arguments:
* text: the text to predict a language for
* unigram_dict: the unigram count dictionary of the language being tested
* bigram_dict: the bigram count dictionary of the language being tested
* vocab_size: the vocabulary size of all languages being tested together (used for Laplace smoothing)

The log probability is calculated as the sum of the log base 2 probabilities of each bigram of the test text appearing in the language with laplace smoothing
 (given as `('number of occurances of bigram in training corpus' + 1) / ('number of occurences of the first element of the bigram in the training corpus' + 'vocabulary size parameter)`).
 
 
The `main` function loads in the dictionaries saved into pickle files by part 1
and calculates the most probable language for each line of text in a testbench file given as `LandId.test`.
The function saves the predictions for lines to a file `predictions.txt`.
The function outputs accuracy of classification by comparing predicted answers to real answers in a key file given as `LangId.sol`.
The function displays the lines of incorrect predictions, what prediction was made, and what the correct classification was.
