import os
from cvxpy import *
import numpy
from dataHandler import loadDataToDB,makeAtomDictionary


def readLines(file_name):
    items = []
    if os.path.exists(file_name):
        f = open(file_name)
        lines = f.readlines()
        f.close()
        for line in lines:
            item = line.replace('\n', '')
            items.append(item)
        return items
    else:
        return None 

def saveFile(path, content):
    with open(path, 'a') as out:
        out.write(content + '\n')
         
     
def makeTextDataDictionary(dataTextFile):
    dataDictionary = {}
    dataLines = readLines(dataTextFile)
    for line in dataLines:
        items = line.split('\t')
        dataDictionary[item[0].replace(' ','')] = items[1].replace(' ','')
    return dataDictionary


def extractPotentialFunction(modelTextFile, dataTextFolder):
    dataDictionary = makeAtomDictionary(loadDataToDB(dataTextFolder))
    rules = readLines(modelTextFile)
    groundedRules = grounding(rules, dataDictionary)
    potentialFunctions = []
    atomVariableDict = {}
    for groundedRule in groundedRules:
        potentialFunction = parseRule(groundedRule, atomVariableDict, dataDictionary)
        potentialFunctions.append(potentialFunction)
    return potentialFunctions


def grounding(rules, dataDictionary):
    groundedRules = []
    for rule in rules:
     # should be implemented
        pass   
    return groundedRules
    

def mapInference(potentialFunctions,atomVariableDict):
    objective = Minimize(sum_entries(potentialFunctions))
    constraints = []
    prob = Problem(objective, constraints)
    # The optimal objective is returned by prob.solve().
    result = prob.solve()
    # The optimal value for x is stored in x.value.
    results = x.value
    return results
 
def RunModel(modelTextFile, dataTextFile, resultTextFile):  
    potentialFunctions = extractPotentialFunction(modelTextFile, dataTextFile)
    results = mapInference(potentialFunctions)
    saveFile(resultTextFile,results)
    
      
def parseRule(groundedRule, atomVariableDict, dataDictionary):
    ruleContent = rule.split('->')
    headAtom = ruleContent[1].replace(' ','')
    if headAtom in dataDictionary:
        variable = dataDictionary[headAtom]
    else:
        lastIndexNumber = atomVariableDict['index']
        variable = 'x'+str(lastIndexNumber)
        atomVariableDict['index'] = lastIndexNumber+1
        atomVariableDict[headAtom] = variable
    bodyAtoms = ruleContent[0]
    atoms = bodyAtoms.split('&')
    lastIndexNumber = atomVariableDict['index']
    atomSet = []
    for atom in atoms:
        #if item is negated
        atom = atom.replace(' ','')
        if atom.startswith('~'):
            atom = atom.repalce('~', '')
            negation = True
        if atom in atomVariableDict:
            variable = atomVariableDict[atom]
        else:
            if atom in dataDictionary:
                variable = dataDictionary[atom]
            else:
                lastIndexNumber = atomVariableDict['index']
                variable = 'x'+str(lastIndexNumber)
                atomVariableDict['index'] = lastIndexNumber+1
                atomVariableDict[atom] = variable
        if negation:
            atomSet.append(1-variable)
        else:
            atomSet.append(variable)
        negation = False
    #first calculate the function for the the body atoms
    n = len(atomSet)
    if n>=2:
        function = max_entries(atomSet[0]+atomSet[1]-1,0)
        i = 3
        while i<=n:
            function = max_entries(function+atomSet[i]-1,0)
            i+=1
        potentialFunction = max_entries(atomVariableDict[headAtom] - function, 0)
    else:
        potentialFunction = max_entries(atomVariableDict[headAtom] - atomSet[0], 0)
    return potentialFunction
        




    