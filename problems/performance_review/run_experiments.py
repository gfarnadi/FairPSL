#!/usr/bin/env python

import os, sys
SCRIPTDIR = os.path.dirname(__file__)
ENGINDIR = os.path.join(SCRIPTDIR, '..', '..', 'engines')
sys.path.append(os.path.abspath(ENGINDIR))
from fpsl_pulp import map_inference, fair_map_inference

from grounding import ground
from evaluation import evaluate, accuracy, accuracy_all

def runExperiment(dataPath, resultPath):
    epsilons = [0.001, 0.005, 0.01, 0.05, 0.1,0.5]
    fairMeasureCodes = ['RD', 'RR', 'RC']
    i=1
    text = ''
    while i<=6:
        print (i)
        text+='dataset No.'+str(i)+'\n' 
        text+='---------------------------'+'\n'
        text+='---------------------------'+'\n'
        rules, hard_rules, counts, atoms = ground(dataPath+str(i)+'/')
        for code in fairMeasureCodes:
            print(code)
            results = map_inference(rules, hard_rules, solver='gurobi')
            #accuracyScore = accuracy(dataPath+str(i)+'/', results, atoms)
            accuracyScore, accuracy_A, accuracy_B= accuracy_all(dataPath+str(i)+'/', results, atoms)
            score = evaluate(results, counts, code)
            
            text+='----------'+code+'---------------'+'\n'
            text+='----------PSL--------------'+'\n'
            line = ''
            line_A = ''
            line_B = ''
            for epsilon in epsilons:
                text+=str(score)+'\t'
                line+=str(accuracyScore)+'\t'
                line_A+=str(accuracy_A)+'\t'
                line_B+=str(accuracy_B)+'\t'  
            
            text+='\n'+line+'\n'+line_A+'\n'+line_B+'\n'+'----------FairPSL----------'+'\n'

            line = ''
            line_A = ''
            line_B = ''
            for epsilon in epsilons:
                print(epsilon)
                results = fair_map_inference(rules, hard_rules, counts, epsilon,code, solver='gurobi')
                #accuracyScore = accuracy(dataPath+str(i)+'/', results, atoms)
                accuracyScore, accuracy_A, accuracy_B = accuracy_all(dataPath+str(i)+'/', results, atoms)
                line+=str(accuracyScore)+'\t'
                line_A+=str(accuracy_A)+'\t'
                line_B+=str(accuracy_B)+'\t'    
                score = evaluate(results, counts,code)
                text+=str(score)+'\t'
            text+='\n'
            text+=line+'\n'+line_A+'\n'+line_B+'\n'
        text+='---------------------------'+'\n'
        text+='---------------------------'+'\n'
        i+=1 
    with open(resultPath, 'w') as f:
        print(text, file=f) 
                
            
dataPath = './data/parameters/GC-parameters1/' 
resultPath = './results_GC-parameters1.txt'
runExperiment(dataPath, resultPath)    

dataPath = './data/parameters/Uni-parameters1/' 
resultPath = './results_Uni-parameters1.txt'
runExperiment(dataPath, resultPath) 
   
dataPath = './data/parameters/GC-parameters2/' 
resultPath = './results_GC-parameters2.txt'
runExperiment(dataPath, resultPath) 

dataPath = './data/parameters/Uni-parameters2/' 
resultPath = './results_Uni-parameters2.txt'
runExperiment(dataPath, resultPath) 