import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

class Preprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, content):
        """Preprocess content by tokenizing, removing stopwords, and lemmatizing"""
        content = content.replace("\n", " ").replace("\t", " ")
        content = re.sub(r"[^A-Za-z\s]", " ", content)
        content = re.sub(r"\s+", " ", content).lower()
        tokens = word_tokenize(content)
        stop_words = set(stopwords.words("english"))
        return [self.lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
