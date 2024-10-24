import os
import nltk
import json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

class DocID_URL_Mapping():
    def __init__(self):
        self.path = r"A:\ProgrammingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\URLs.json"
        self.mappings = self.loadDocumentIndex()
        
    def addToDocumentIndex(self, docID, URL):
        if str(URL) not in self.mappings:
            self.mappings[docID] = URL
            print(f"Document ID : {docID} and the corresponding URL : {URL} added to the Document Index")
        else:
            print("Already Exists...!!")
            
    def loadDocumentIndex(self):
        try:
            with open(self.path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def saveDocumentIndex(self):
        with open(self.path, "w") as file:
            json.dump(self.mappings, file)
        

lemmatizer = WordNetLemmatizer()
            
def preprocess(content):
    content = content.replace("\n", " ")
    content = content.replace("\t", " ")
    content = re.sub(r"[^A-Za-z\s]", " ", content)
    content = re.sub(r"\s+", " ", content)
    content = content.lower()
    content = word_tokenize(content)
    content = [lemmatizer.lemmatize(word) for word in content if word not in stopwords.words("english") and len(word) > 2]
    return content
            
with open(r"A:\ProgrammingStuff\dsa_data\activistpost.json", "r") as file:
    data = json.load(file)
    


def lexiconBuilder(words):
    try:
        with open(r"A:\ProgrammingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "r") as file:
            IDs = json.load(file)
            IDnumber = max(IDs.values()) + 1 if IDs else 1
    except FileNotFoundError:
        IDs = {}
        IDnumber = 1
    
    for word in words:
        if word not in IDs:
            IDs[word] = IDnumber
            IDnumber += 1
    
    with open(r"A:\ProgrammingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "w") as file:
        json.dump(IDs, file)
        

 
lexiconBuilder(data)

documentID = 0
def buildForwardIndex(documents):
    forwardIndex = dict()
    path = r"A:\ProgrammingStuff\dsa_data"
    urlMapper = DocID_URL_Mapping()
    for document in documents:
        articles = os.path.join(path, document)
        with open(articles, "r") as f:
            A = json.load(f)
            for article in A:
                title = preprocess(article["title"])
                content = preprocess(article["content"])
                URL = article["URL"]
                lexiconBuilder(title + content)
                try:
                    with open(r"A:\ProgrammingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "r") as file:
                        lexicon = json.load(file)
                except FileNotFoundError:
                    return {}
                urlMapper.addToDocumentIndex()
                title_ids = [lexicon[word] for word in title]
                content_ids = [lexicon[word] for word in content]
                frequency = FreqDist(title_ids * 10 + content_ids)
                dictionary = {}
                for word in set(title + content):
                    dictionary[lexicon[word]] = frequency[lexicon[word]]
                forwardIndex[documentID] = dictionary
                urlMapper.addToDocumentIndex(documentID, URL)
                documentID += 1
    return forwardIndex


files = os.listdir(r"dsa_data")     
# buildForwardIndex([data])
i = 0
for j in files:
    if j.endswith('.json'):
        i += 1
print(i)