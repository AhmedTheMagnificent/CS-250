import os
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import time
import sys

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")


def preprocess(content):
    """Preprocess content by tokenizing, removing stopwords, and lemmatizing"""
    content = content.replace("\n", " ").replace("\t", " ")
    content = re.sub(r"[^A-Za-z\s]", " ", content)
    content = re.sub(r"\s+", " ", content).lower()
    tokens = word_tokenize(content)
    return [self.lemmatizer.lemmatize(word) for word in tokens if word not in stopwords.words("english") and len(word) > 2]
    
def load_lexicon():
    path = r"Forward-Index\Lexicon.json"
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError):
        return None
    
def load_forward_index():
    path = r"Forward-Index\ForwardIndex.json"
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError):
        return None
    
def load_inverted_index(barrel):
    path = rf"Inverted-Index\Barrels\{barrel}.json"
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError):
        return None
        

