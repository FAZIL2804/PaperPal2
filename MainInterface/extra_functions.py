import nltk
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
from nltk.corpus import wordnet
import re
import pyttsx3

def clean_text(text):
    return re.sub('[^a-zA-Z]', '', text).lower()

def get_definition(word):
    synsets = wordnet.synsets(clean_text(word))
    if synsets:
        definition = synsets[0].definition()
        return definition
    else:
        return None

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name()!=word:
                synonyms.append(lemma.name())
    return synonyms

def get_word_pronunciation(word):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    engine.say(word)
    engine.runAndWait()



    
