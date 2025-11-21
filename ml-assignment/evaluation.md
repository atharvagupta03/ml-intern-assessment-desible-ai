# Evaluation Summary

This project implements a trigram language model that predicts the next word based on the previous two words. The model was designed to be clean, structured, and aligned with how classical N-gram models work in NLP. Below are the core design decisions and the reasoning behind them.

A. Storage of N-gram Counts

To keep track of word patterns, I used Python’s built-in collection types.
Unigrams and bigrams are stored using simple Counter objects, while trigrams use a defaultdict(Counter).
This structure lets me update counts quickly during training and makes it easy to look up the possible next words for any (w1 w2) pair.
Using defaultdict(Counter) also saves from manually creating nested dictionaries every time a new bigram appears.


-----------


B. Text Cleaning, Padding, and Handling Unknown Words

Before training, the raw text is cleaned in several steps:
1. Converted to lowercase, 
2. Unwanted characters removed while preserving apostrophes,
3. Collapsed multiple spaces,
4. Split into sentences using < ., !, and ? >,
5. Tokenized into words using a simple regex
6. A vocabulary is built from all observed tokens. An <unk> (unknown) token is included, but it is excluded from generation whenever other options exist.


-----------


C. Conditional Generation and Sampling Strategy

The assignment’s tests expect the model to continue text from a given prior_text, rather than generating from scratch.
To support this, the generate() function was extended to:
1. Clean the prior_text
2. Extract its last two words
3. Use them as the starting context (w1, w2)
From this context, the model predicts the continuation word by word.
->> and for next-word prediction, I implemented probabilistic sampling based on actual frequency counts, not greedy selection. This produces more natural sentence continuations instead of repetitive or deterministic output.


-----------


D. Backoff Logic: Trigram → Bigram → Unigram

Real text often contains contexts not seen in training.
To handle this, I implemented a simple backoff approach:
1. Try trigram continuation using (w1, w2)
2. If unavailable, fall back to bigram continuation using only w2
3. If that also fails, fall back further to unigram frequencies
This ensures the model always produces output, even when the prior context is rare or absent in the training text.


-----------


E. Additional Design Considerations which i did in the model code

<unk> (unknown) is removed from the sampling pool unless it is the only available option.
The output is always guaranteed to be a non-empty string, matching the unit tests’ expectations. The implementation aligns with the expected behavior in the test cases, including conditional continuation using "Alice in Wonderland" as the training corpus. The structure of the model allows clear separation between data preparation, training, and generation.


-----------


Conclusion ->

Overall, the model follows the usual steps of a trigram language model — cleaning the text, building a vocabulary, counting word patterns, and predicting the next word using probabilities. My main goal was to make sure the model behaves correctly and works smoothly with the tests, especially the ones that ask it to continue a sentence from a given prompt. As a result, the model is able to pick up the context from the training text and generate meaningful continuations.