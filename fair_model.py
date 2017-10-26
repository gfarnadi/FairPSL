from fair_grounding import fairGrounding
from inference import mapInference, fairMapInference

def runModel(dataPath):
    rules, hard_rules, counts = fairGrounding(dataPath)
    results = mapInference(rules, hard_rules)
    print (results)
    results = fairMapInference(rules, hard_rules, counts)
    print (results)
    
    
    
    
dataPath = './reviewData/'    
runModel(dataPath)