import numpy as np
import json
import pandas as pd
import os
import re

NUM_BARRELS = 1000
barrelFiles = []

with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "r") as file:
    forwardIndex = json.load(file)
    
def buildInvertedIndex(forwardIndex):
    barrels = [None] * NUM_BARRELS
    for documentID, data in forwardIndex.items():

        for wordID, frequency in data.items():
            barrel_number = int(wordID) % NUM_BARRELS
            barrel_filename = f"barrel_{str(barrel_number).zfill(4)}.json"
            barrel_path = os.path.join(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Barrels", barrel_filename)
            print(barrel_number)
            if not os.path.exists(barrel_path):
                with open(barrel_path, "w") as file:
                    json.dump({}, file)
                barrelFiles.append(barrel_filename)
                
            
                
            if barrels[barrel_number] is None:
                with open(barrel_path, "r+") as file:
                    barrels[barrel_number] = json.load(file)
                
            if wordID not in barrels[barrel_number]:
                barrels[barrel_number][wordID] = {}
            barrels[barrel_number][wordID].update({documentID: frequency})
            
            with open(barrel_path, "w") as file:
                json.dump(barrels[barrel_number], file)
            
                
            

buildInvertedIndex(forwardIndex)