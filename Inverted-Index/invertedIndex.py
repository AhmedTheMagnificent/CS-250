import numpy as np
import json
import pandas as pd
import os
import re

NUM_BARRELS = 1000
barrelFiles = []

with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "r") as file:
    forwardIndex = json.load(file)
    
def buildInvertedIndex(forwardIndex, lexicon, invertedIndex):
    barrels = [None] * NUM_BARRELS
    for document in forwardIndex:
        documentID = document.key()
        for wordID, frequency in document.items():
            invertedIndex[wordID] = {documentID: frequency}
            barrel_number = int(wordID % NUM_BARRELS)
            barrel_filename = f"barrel_{str(barrel_number).zfill(4)}.json"
            barrel_path = os.path.join(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Barrels", barrel_filename)
            if not os.path.exists(barrel_path):
                with open(barrel_path, "w") as file:
                    json.dump({}, file)
                barrelFiles.append(barrel_filename)
                
            
    
    
print(data)