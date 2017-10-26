from fair_grounding import fairGrounding
from inference import mapInference, fairMapInference

def runModel(dataPath):
    rules, hard_rules, counts = fairGrounding(dataPath)
    results = mapInference(rules, hard_rules)
    print (results)
    
    
    
dataPath = './reviewData/'    
runModel(dataPath)