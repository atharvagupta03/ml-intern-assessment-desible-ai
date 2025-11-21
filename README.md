# Trigram Language Model – Assignment

This project implements a trigram language model from scratch.
A trigram model predicts the next word based on the previous two words.
The model is trained on text, and it can also continue generating text from a given prompt.

The project also includes test cases that use the Alice in Wonderland text to verify the model's behavior.

# Project Structure

ml-assignment/
│
├── src/
│   └── ngram_model.py          (main trigram model code)
│
├── tests/
│   ├── test_ngram.py           (test file)
│   └── alice.txt               (training text used by tests)
│
├── evaluation.md               (summary of design choices)
└── README.md

# How the Model Works

1. The text is cleaned: lowercased, unwanted characters removed, and split into sentences.
2. Words are extracted from each sentence.
3. A vocabulary is built from all words in the training text.
4. The model counts unigrams, bigrams, and trigrams.
5. During generation, the model looks at the last two words and predicts the next one using probability.
6. If a trigram continuation is not available, it falls back to bigram counts, and then to unigram counts.
7. The model supports conditional generation, meaning it can continue from any given prior text.

# How To Run Tests

Go to the project root folder:

1. cd ml-assignment

2. Run tests using pytest:

    PYTHONPATH=. pytest

Or run the test file directly:

    PYTHONPATH=. python3 tests/test_ngram.py


# Requirements

The project uses only Python's built-in libraries.
No external dependencies are needed.
