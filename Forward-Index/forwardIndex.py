import os
import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")


class DocumentID_URL_Mapping():
    def __init__(self):
        self.path = r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\URLs.json"
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
urlMapper = DocumentID_URL_Mapping()

try:
    with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "r") as file:
        content = file.read().strip()  # Remove any leading/trailing whitespace
        if not content:  # Check if the file is empty
            lexicon = {}  # Initialize an empty dictionary
        else:
            lexicon = json.loads(content)  # Parse JSON if content exists
        wordID = max(lexicon.values()) + 1 if lexicon else 1
except FileNotFoundError:
    lexicon = {}
    wordID = 1
    
try:
    with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "r") as file:
        forwardIndex = json.load(file)
        documentID = max(map(int, forwardIndex.keys())) + 1 if forwardIndex else 1
except FileNotFoundError:
    forwardIndex = {}
    documentID = 1

def preprocess(content):
    content = content.replace("\n", " ")
    content = content.replace("\t", " ")
    content = re.sub(r"[^A-Za-z\s]", " ", content)
    content = re.sub(r"\s+", " ", content)
    content = content.lower()
    content = word_tokenize(content)
    content = [lemmatizer.lemmatize(word) for word in content if word not in stopwords.words("english") and len(word) > 2]
    return content
            
def lexiconBuilder(words, lexicon, startID):

    for word in words:
        if word not in lexicon:
            lexicon[word] = startID
            startID += 1
    
    return lexicon, startID



def buildForwardIndex(documents, lexicon, forwardIndex):
    path = r"A:\ProgrmmingStuff\nela-gt-2022\newsdata"
    global wordID, documentID
    
    for document in documents:
        
        articles = os.path.join(path, document)
        with open(articles, "r") as file:
            A = json.load(file)
        for article in A:
            title = preprocess(article["title"])
            content = preprocess(article["content"])
            URL = article["url"]
            lexi, wordID = lexiconBuilder(title + content, lexicon, wordID)
            lexicon.update(lexi)
            urlMapper.addToDocumentIndex(documentID, URL)
            
            title_ids = [lexicon[word] for word in title]
            content_ids = [lexicon[word] for word in content]
            frequency = FreqDist(title_ids * 10 + content_ids)
            dictionary = {}
            for word in set(title + content):
                dictionary[lexicon[word]] = frequency[lexicon[word]]
            
            forwardIndex[documentID] = dictionary                
            documentID += 1
        print(lexicon)
            

print(os.listdir())
files = os.listdir(r"A:\ProgrmmingStuff\nela-gt-2022\newsdata") 
buildForwardIndex(files[:2], lexicon, forwardIndex)
with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "w") as file:
    json.dump(lexicon, file)             
with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "w") as file:
    json.dump(forwardIndex, file)
    
urlMapper.saveDocumentIndex()
