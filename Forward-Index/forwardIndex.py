import os
import json
import hashlib
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")


class DocumentID_URL_Mapping:
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


class Checksum:
    def __init__(self):
        self.path = r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\CheckSum.json"
        self.checkSums = self.load_checkSum()
        
    def load_checkSum(self):
        try:
            with open(self.path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def resolve_documentID(self, checkSum):
        """Resolve document ID from checksum"""
        return self.checkSums.get(checkSum, None)
    
    def add_checksum(self, checksum, documentID):
        """Add checksum and its corresponding documentID to the checksum index"""
        if checksum not in self.checkSums:
            self.checkSums[checksum] = documentID
            self.save_checkSum()

    def save_checkSum(self):
        """Save checksum mappings to file"""
        with open(self.path, "w") as file:
            json.dump(self.checkSums, file)


class DocumentProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.urlMapper = DocumentID_URL_Mapping()
        self.checksumHandler = Checksum()
        self.lexicon = self.load_lexicon()
        self.forwardIndex = self.load_forward_index()
        self.wordID = max(self.lexicon.values()) + 1 if self.lexicon else 1
        self.documentID = max(map(int, self.forwardIndex.keys())) + 1 if self.forwardIndex else 1
        self.path = r"A:\ProgrmmingStuff\nela-gt-2022\newsdata"

    def load_lexicon(self):
        try:
            with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "r") as file:
                content = file.read().strip()
                return json.loads(content) if content else {}
        except FileNotFoundError:
            return {}

    def load_forward_index(self):
        try:
            with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def preprocess(self, content):
        """Preprocess content by tokenizing, removing stopwords, and lemmatizing"""
        content = content.replace("\n", " ").replace("\t", " ")
        content = re.sub(r"[^A-Za-z\s]", " ", content)
        content = re.sub(r"\s+", " ", content).lower()
        tokens = word_tokenize(content)
        return [self.lemmatizer.lemmatize(word) for word in tokens if word not in stopwords.words("english") and len(word) > 2]

    def lexiconBuilder(self, words):
        """Build the lexicon and return updated lexicon with word IDs"""
        for word in words:
            if word not in self.lexicon:
                self.lexicon[word] = self.wordID
                self.wordID += 1
        return self.lexicon

    def generate_checksum(self, content):
        """Generate checksum for a given content"""
        return hashlib.sha256(content.encode()).hexdigest()

    def buildForwardIndex(self, documents):
        """Build the forward index for given documents"""
        for document in documents:
            article_path = os.path.join(self.path, document)
            with open(article_path, "r") as file:
                articles = json.load(file)
            
            for article in articles:
                title = self.preprocess(article["title"])
                content = self.preprocess(article["content"])
                URL = article["url"]
                full_content = title + content
                
                # Generate checksum for the document
                checksum = self.generate_checksum(' '.join(full_content))
                
                # Check if this document has already been processed
                existing_docID = self.checksumHandler.resolve_documentID(checksum)
                if existing_docID:
                    print(f"Document {document} with checksum {checksum} already exists in the index. Skipping.")
                    continue
                
                # Add to lexicon and forward index
                self.lexicon = self.lexiconBuilder(title + content)
                self.urlMapper.addToDocumentIndex(self.documentID, URL)
                
                # Build the word frequency distribution
                title_ids = [self.lexicon[word] for word in title]
                content_ids = [self.lexicon[word] for word in content]
                frequency = FreqDist(title_ids * 10 + content_ids)
                dictionary = {self.lexicon[word]: frequency[self.lexicon[word]] for word in set(title + content)}
                
                self.forwardIndex[self.documentID] = dictionary
                self.checksumHandler.add_checksum(checksum, self.documentID)
                self.documentID += 1

            print(f"Current Lexicon: {self.lexicon}")
        
        # Save the results
        self.save_results()

    def save_results(self):
        """Save the lexicon, forward index, and document index"""
        with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\Lexicon.json", "w") as file:
            json.dump(self.lexicon, file)
        with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "w") as file:
            json.dump(self.forwardIndex, file)
        self.urlMapper.saveDocumentIndex()
        self.checksumHandler.save_checkSum()


# Run the document processing
if __name__ == "__main__":
    documentProcessor = DocumentProcessor()
    files = os.listdir(r"A:\ProgrmmingStuff\nela-gt-2022\newsdata") 
    documentProcessor.buildForwardIndex(files[:2])  # Process the first 10 files
