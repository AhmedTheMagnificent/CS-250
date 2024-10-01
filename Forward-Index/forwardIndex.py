import os
import nltk
import json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

with open(r"dsa_data\abcnews.json", "r") as f:
    data = json.load(f)
    
stopWords = set(stopwords.words('english'))

for article in data:
    title = article.get("title")
    content = article.get("content")
