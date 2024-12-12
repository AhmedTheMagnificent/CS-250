import json
import os

NUM_BARRELS = 1000
barrelFiles = []

def buildInvertedIndex(forwardIndex):
    barrels = [None] * NUM_BARRELS
    for documentID, data in forwardIndex.items():
        for wordID, frequency in data.items():
            barrel_number = int(wordID) % NUM_BARRELS
            barrel_filename = f"barrel_{str(barrel_number).zfill(4)}.json"
            barrel_path = os.path.join(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Inverted-Index\Barrels", barrel_filename)
            print(barrel_number)
            
            # Load the barrel file if not already loaded
            if barrels[barrel_number] is None:
                if not os.path.exists(barrel_path):
                    barrels[barrel_number] = {}
                    # Initialize the empty barrel file if it doesn't exist
                    with open(barrel_path, "w") as file:
                        json.dump(barrels[barrel_number], file)
                    barrelFiles.append(barrel_filename)
                else:
                    with open(barrel_path, "r") as file:
                        barrels[barrel_number] = json.load(file)
            
            # Add the wordID and its frequency to the barrel
            if wordID not in barrels[barrel_number]:
                barrels[barrel_number][wordID] = {}
            barrels[barrel_number][wordID].update({documentID: frequency})
    
    # After processing all words, write the updated barrels back to disk
    for barrel_number in range(NUM_BARRELS):
        if barrels[barrel_number] is not None:
            barrel_filename = f"barrel_{str(barrel_number).zfill(4)}.json"
            barrel_path = os.path.join(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Inverted-Index\Barrels", barrel_filename)
            with open(barrel_path, "w") as file:
                json.dump(barrels[barrel_number], file)

# Example usage with forwardIndex:
with open(r"A:\ProgrmmingStuff\CS-250-Data-Structures-and-Algorithms\Forward-Index\ForwardIndex.json", "r") as file:
    forwardIndex = json.load(file)

buildInvertedIndex(forwardIndex)
