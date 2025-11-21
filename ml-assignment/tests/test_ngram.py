# import pytest
from src.ngram_model import TrigramModel
import re




# I have given the prior_text in all the test case functions as refernce
def load_and_clean_text(filepath):
    # This function reads the text file i.e alice in wonderland txt file present in the folder, cleans the content, removes extra spaces from it, splits it into sentences, and combines it all into one neatly formatted string.

    #############################################   
    # read the text file
    #############################################   
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    #############################################   
    # lowerrcase all the text present in alice.txt file
    #############################################   
    text = text.lower()

    #############################################   
    #  remove weird characters
    #  keeps alphabets, numbers, punctuation
    #############################################   
    # text = re.sub(r"[^a-z0-9.!?\s]", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s.!?']", " ", text)

    #############################################   
    # remove multiple spaces
    #############################################   
    text = re.sub(r"\s+", " ", text).strip()

    #############################################   
    # split into sentences
    #############################################   
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    #############################################   
    # join everything into a SINGLE big string
    #############################################   
    final_text = " . ".join(sentences)

    return final_text






def test_fit_and_generate():
    # test function for test cases
    text = load_and_clean_text("tests/alice.txt")
    # print(text[:20000])
    model = TrigramModel()
    # text = "I am a test sentence. This is another test sentence."
    model.fit(text)
    prior_text = "alice lives in wonderland. she is sitting"
    # print("entered test_fit_and_generate function after model.fit")
    generated_text = model.generate(prior_text)
    # print("this is before generate_answer print statement")
    print("text generated :" + generated_text)
    
    assert isinstance(generated_text, str)
    assert len(generated_text.split()) > 0

def test_empty_text():
    text = load_and_clean_text("tests/alice.txt")
    model = TrigramModel()
    prior_text = ""
    model.fit(text)
    generated_text = model.generate(prior_text)
    print("text generated :" + generated_text)
    
    assert isinstance(generated_text, str)
    assert len(generated_text.split()) > 0


def test_short_text():
    text = load_and_clean_text("tests/alice.txt")
    model = TrigramModel()
    prior_text = "I am"
    model.fit(text)
    generated_text = model.generate(prior_text)
    print("text generated :" + generated_text)

    assert isinstance(generated_text, str)
    assert len(generated_text.split()) > 0


# below is the test function calls and their generated outputs.
print("----test1---------------")
test_fit_and_generate()
# prior_text -> alice lives in wonderland. she is sitting
# generated_text -> on the bank with her friend

print("----test2---------------")
test_empty_text()
# prior_text -> 
# generated_text -> they are waiting on the ground near the right words said poor alice

print("----test3---------------")
test_short_text()
# prior_text -> I am
# generated_text -> among mad people alice remarked
