# import os
# import nltk
# import json
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk.probability import FreqDist
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer, WordNetLemmatizer

# class DocID_URL_Mapping():
#     def __init__(self):
#         self.documentIndexPath = ""
#         self.mappings = self.loadDocumentIndex()
        
#     def addToDocumentIndex(self, docID, URL):
#         if str(URL) not in self.mappings:
#             self.mappings[docID] = URL
#             print(f"Document ID : {docID} and the corresponding URL : {URL} added to the Document Index")
#         else:
#             print("Already Exists...!!")
            
#     def loadDocumentIndex(self):
#         try:
#             with open(self.documentIndexPath, "r") as file:
#                 return json.load(file)
#         except FileNotFoundError:
#             return {}
        
#     def saveDocumentIndex(self):
#         with open(self.documentIndexPath, "w") as file:
#             json.dump(self.mappings, file, indent=2)
            
# class DocId_Date_Mapping():
#     def __init__(self):
#         self.documentIndexPath = ""
#         self.mappings = loadDocIDDateFile()
        
#     def addDocumentIndexDataFile(self, DocID, date):
#         if str(DocID) not in self.mappings:
#             mappings[DocID] = date
#             print(f"Document ID : {docID} and the corresponding Date : {date} added to the Document Index")
#         else:
#             print("Already Exists...!!")
    
#     def loadDocIDDateFile(self):
#         try:
#             with open(self.documentIndexPath, "r") as file:
#                 return json.load(file)
#         except FileNotFoundError:
#             return {}
        
#     def saveDocIDDateFile(self):
#         with open(self.documentIndexPath, "w") as file:
#             json.dump(self.mappings, file, indent=2)
            
            
# class Lexicon()


# with open(r"dsa_data\abcnews.json", "r") as file:
#     data = json.load(file)
    
# stopWords = set(stopwords.words('english'))

# for article in data:
#     title = article.get("title")
#     content = article.get("content")
#     wordToIndex = f"{title} {content}"
#     tokens = word_tokenize(wordToIndex)
#     freqDistribution = FreqDist(tokens)
    
import json
import nltk

class DocID_URL_Mapping():
    def __init__(self):
        self.documentIndexPath = r"A:\ProgrammingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\URLs.json"
        self.mappings = self.loadDocumentIndex()
        
    def addToDocumentIndex(self, docID, URL):
        if str(URL) not in self.mappings:
            self.mappings[docID] = URL
            print(f"Document ID : {docID} and the corresponding URL : {URL} added to the Document Index")
        else:
            print("Already Exists...!!")
            
    def loadDocumentIndex(self):
        try:
            with open(self.documentIndexPath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def saveDocumentIndex(self):
        with open(self.documentIndexPath, "w") as file:
            json.dump(self.mappings, file, indent=2)
        
class DocID_Date_Mapping():
    def __init__(self):
        self.documentIndexPath = r"A:\ProgrammingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Dates.json"
        self.mappings = self.loadDocumentIndex()
        
    def addToDocumentIndex(self, docID, date):
        if str(date) not in self.mappings:
            self.mappings[docID] = date
            print(f"Document ID : {docID} and the corresponding Date : {date} added to the Document Index")
        else:
            print("Already Exists...!!")
            
    def loadDocumentIndex(self):
        try:
            with open(self.documentIndexPath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def saveDocumentIndex(self):
        with open(self.documentIndexPath, "w") as file:
            json.dump(self.mappings, file, indent=2)
        
        
        
with open(r"dsa_data/activistpost.json", "r") as file:
    data = json.load(file)

    
urlmapper = DocID_URL_Mapping()
datemapper = DocID_Date_Mapping()
for dat in data:
    urlmapper.addToDocumentIndex(dat["id"], dat["url"])
    datemapper.addToDocumentIndex(dat["id"], dat["date"])
    
urlmapper.saveDocumentIndex()
datemapper.saveDocumentIndex()