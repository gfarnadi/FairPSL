from fair_grounding import fairGrounding
from inference import mapInference, fairMapInference
from fair_evaluation import evaluate


def runModel(dataPath):
    rules, hard_rules, counts = fairGrounding(dataPath)
    results = mapInference(rules, hard_rules)
    print (results)
    print(evaluate(results, counts))
    results = fairMapInference(rules, hard_rules, counts)
    print (results)
    print(evaluate(results, counts))
    
    
    
dataPath = './reviewData/'    
runModel(dataPath)