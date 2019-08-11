import os, sys
SCRIPTDIR = os.path.dirname(__file__)
ENGINDIR = os.path.join(SCRIPTDIR, '..', '..', 'engines')
sys.path.append(os.path.abspath(ENGINDIR))
from fpsl_cvxpy import mapInference, fairMapInference

from grounding import ground
from evaluation import evaluate, accuracy

def runModel(dataPath,epsilon,fairMeasureCode):
    rules, hard_rules, counts, _ = ground(dataPath)
    results = mapInference(rules, hard_rules)
    print (results)
    print(evaluate(results, counts, fairMeasureCode))
    results = fairMapInference(rules, hard_rules, counts, epsilon,fairMeasureCode)
    print (results)
    print(evaluate(results, counts,fairMeasureCode))
    
    

def runExperiment(dataPath, resultPath):
    epsilons = [0.001,0.005, 0.01, 0.05, 0.1,0.5]
    fairMeasureCodes = ['RD', 'RR', 'RC']
    i=1
    text = ''
    while i<=3:
        print (i)
        text+='dataset No.'+str(i)+'\n' 
        text+='---------------------------'+'\n'
        text+='---------------------------'+'\n'
        rules, hard_rules, counts, atoms = ground(dataPath+str(i)+'/')
        for code in fairMeasureCodes:
            print(code)
            results = mapInference(rules, hard_rules)
            accuracyScore = accuracy(dataPath+str(i)+'/', results, atoms)
            score = evaluate(results, counts,code)
            
            text+='----------'+code+'---------------'+'\n'
            text+='----------PSL--------------'+'\n'
            line = ''
            for epsilon in epsilons:
                text+=str(score)+'\t'
                line+=str(accuracyScore)+'\t'
            
            text+='\n'+line+'\'+----------FairPSL----------'+'\n'
            line = ''
            for epsilon in epsilons:
                print(epsilon)
                results = fairMapInference(rules, hard_rules, counts, epsilon,code)
                accuracyScore = accuracy(dataPath+str(i)+'/', results, atoms)
                line+=str(accuracyScore)+'\t'
                score = evaluate(results, counts,code)
                text+=str(score)+'\t'
            text+='\n'
            text+=line+'\n'
        text+='---------------------------'+'\n'
        text+='---------------------------'+'\n'
        i+=1 
    with open(resultPath, 'w') as f:
        print(text, file=f) 
                
            
dataPath = './data/1' 
resultPath = './results.txt'
runExperiment(dataPath, resultPath)    
   