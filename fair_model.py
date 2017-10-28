from fair_grounding import fairGrounding
from inference import mapInference, fairMapInference
from fair_evaluation import evaluate
from data_generator import saveFile

def runModel(dataPath,epsilon,fairMeasureCode):
    rules, hard_rules, counts, _ = fairGrounding(dataPath)
    results = mapInference(rules, hard_rules)
    print (results)
    print(evaluate(results, counts))
    results = fairMapInference(rules, hard_rules, counts, epsilon,fairMeasureCode)
    print (results)
    print(evaluate(results, counts,fairMeasureCode))
    
    

def runExperiment(dataPath, resultPath):
    epsilons = [0.001,0.005, 0.01, 0.05, 0.1,0.5]
    fairMeasureCodes = ['RD', 'RR', 'RC', 'accuracy']
    i=1
    text = ''
    while i<=3:
        print (i)
        text+='dataset No.'+str(i)+'\n' 
        text+='---------------------------'+'\n'
        text+='---------------------------'+'\n'
        rules, hard_rules, counts, atoms = fairGrounding(dataPath+str(i)+'/')
        for code in fairMeasureCodes:
            print(code)
            results = mapInference(rules, hard_rules)
            if code =='accuracy':
                score = accuracy(dataPath+str(i)+'/', results, atoms)
            else:
                score = evaluate(results, counts,code)
            
            text+='----------'+code+'---------------'+'\n'
            text+='----------PSL--------------'+'\n'
            for epsilon in epsilons:
                text+=str(score)+'\t'
            text+='\n'+'----------FairPSL----------'+'\n'
            for epsilon in epsilons:
                print(epsilon)
                results = fairMapInference(rules, hard_rules, counts, epsilon,code)
                if code =='accuracy':
                    score = accuracy(dataPath+str(i)+'/', results, atoms)
                else:
                    score = evaluate(results, counts,code)
                text+=str(score)+'\t'
            text+='\n'
        text+='---------------------------'+'\n'
        text+='---------------------------'+'\n'
        i+=1  
    saveFile(resultPath,text)
            
                
            
dataPath = './reviewData' 
resultPath = './results.txt'
runExperiment(dataPath, resultPath)    
   