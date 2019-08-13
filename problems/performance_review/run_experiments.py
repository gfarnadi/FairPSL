#!/usr/bin/env python

import os, sys
SCRIPTDIR = os.path.dirname(__file__)
ENGINDIR = os.path.join(SCRIPTDIR, '..', '..', 'engines')
sys.path.append(os.path.abspath(ENGINDIR))
from fpsl_pulp import map_inference, fair_map_inference

from grounding import ground
from evaluation import evaluate, accuracy

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
            results = map_inference(rules, hard_rules, solver='gurobi')
            accuracyScore = accuracy(dataPath+str(i)+'/', results, atoms)
            score = evaluate(results, counts, code)
            
            text+='----------'+code+'---------------'+'\n'
            text+='----------PSL--------------'+'\n'
            line = ''
            for epsilon in epsilons:
                text+=str(score)+'\t'
                line+=str(accuracyScore)+'\t'
            
            text+='\n'+line+'\n'+'----------FairPSL----------'+'\n'
            line = ''
            for epsilon in epsilons:
                print(epsilon)
                results = fair_map_inference(rules, hard_rules, counts, epsilon,code, solver='gurobi')
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
                
            
dataPath = './data/' 
resultPath = './results.txt'
runExperiment(dataPath, resultPath)    
   