import re
import random
from collections import defaultdict, Counter


class TrigramModel:
    #This is the below code for TrigramModel class where the model is predicting the next word using the prior two words. 
    # N=3, meaning that it will predict using the last two words, w1 and w2.

    def __init__(self):
        # Special tokens used for Beginning, End and unknown tokens,
        self.BOS = "<s>" # Beginning of sentence
        self.EOS = "</s>" # End of sentence
        self.UNK = "<unk>" # Unknown

        # Counters for single, bigram and trigram
        self.word_counts = Counter()
        self.bigram_counts = Counter()
        self.trigram_counts = defaultdict(Counter)

        # Vocabulary
        self.vocab = set()

    #############################################   
    # Traning the model 
    ############################################# 

    def fit(self, text: str):
        #First I have cleaned the text, then split it into sentences, build a vocabulary from those words, and finally count every group of three words that appear together..

        # Reset
        self.word_counts.clear()
        self.bigram_counts.clear()
        self.trigram_counts.clear()
        self.vocab.clear()

        # 1. Basic cleaning
        cleaned = text.lower()
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        if not cleaned:
            self.vocab.update({self.BOS, self.EOS, self.UNK})
            return

        # 2. Split into sentences
        sentences = re.split(r"[.!?]+", cleaned)
        sentences = [s.strip() for s in sentences if s.strip()]

        # 3. Tokenize
        tokenized_sentences = []
        for s in sentences:
            words = re.findall(r"[a-zA-Z']+", s)
            if words:
                tokenized_sentences.append(words)

        if not tokenized_sentences:
            self.vocab.update({self.BOS, self.EOS, self.UNK})
            return

        # 4. Build vocabulary of all words from training text
        for sent in tokenized_sentences:
            self.vocab.update(sent)

        # Add special tokens
        self.vocab.update({self.BOS, self.EOS, self.UNK})

        # 5. Padding + count n-grams
        for sent in tokenized_sentences:
            padded = [self.BOS, self.BOS] + sent + [self.EOS]

            for i in range(len(padded) - 2):
                w1, w2, w3 = padded[i], padded[i + 1], padded[i + 2]

                self.word_counts[w1] += 1
                self.bigram_counts[(w1, w2)] += 1
                self.trigram_counts[(w1, w2)][w3] += 1

    #############################################   
    # Generate Function of Trigram Model
    #############################################   

    def generate(self, prior_text, max_length=50):
       
        # I have modified the generation function to add one more argument called prior_text. Instead of generating the text from scratch/start, I am using last two words of prior_text and generating the next word in continuation of prior_text.
        # prior_text is sent as argument in the test case itself

        if not self.trigram_counts:
            return ""  # When no training data is present.
        
        try:      
            # cleaning and splitting of prior_text  
            # print(" before split - ", prior_text)
            prior_text = prior_text.lower()
            prior_text = re.sub(r"[^a-zA-Z0-9\s.!?']", " ", prior_text)
            prior_text = re.sub(r"\s+", " ", prior_text).strip()
            prior_text = prior_text.split()[-2:]
            # print(" after split - ", prior_text)
            w1,w2 = prior_text[0], prior_text[1]
        except:
            # when prior_text is empty
            w1, w2 = self.BOS, self.BOS

        print("w1,w2" , w1, w2)
        output = []

        for _ in range(max_length):
            next_word = self.sample_next(w1, w2)

            if not next_word or next_word == self.EOS:
                break

            output.append(next_word)
            w1, w2 = w2, next_word  

        return " ".join(output) if output else ""

    #############################################   
    # Sampling logic
    #############################################   
    def sample_next(self, w1, w2):
        
        # this function will first try trigram continuation first if that doesnt exist then it will go for bigram otherwise unigram. 

        #  trigram 
        if (w1, w2) in self.trigram_counts:
            trigram_cont = self.trigram_counts[(w1, w2)]
            if trigram_cont:
                return self.sample_from_counts(trigram_cont)

        #  bigram 
        bigram_cont = {w3: self.bigram_counts[(w2, w3)]
                       for (x, w3) in self.bigram_counts if x == w2}
        if bigram_cont:
            return self.sample_from_counts(bigram_cont)

        # unigram 
        unigram_cont = {w: count for w, count in self.word_counts.items()
                        if w not in {self.BOS, self.UNK}}

        if unigram_cont:
            return self.sample_from_counts(unigram_cont)

        return self.EOS  # if nothing is working then..

    #############################################   
    # General sample 
    #############################################   
    def sample_from_counts(self, counter):
        
        # Given a Counter of (word -> count),
        # sample a next word using weighted random selection.
        # Ignore <unk> when generating actual text.
        

        # this will removee Unknown from outputs unless it is the only option left..
        items = [(w, c) for w, c in counter.items() if w != self.UNK]
        if not items:
            items = list(counter.items())  # if nothing left, allow Unknown

        total = sum(c for _, c in items)

        # Weighted random selection
        r = random.random()
        cumulative = 0.0

        for word, count in items:
            cumulative += count / total
            if r <= cumulative:
                return word

        return items[-1][0]  #


    
























