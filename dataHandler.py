import os
import csv, sqlite3
import pandas
from os import listdir
from os.path import isfile, join
from model import readLines
from conda_build.metadata import trues
import atomPredicateClass
import ruleClass


def loadDataToDB(folderPath):
    files = [f for f in listdir(folderPath)]
    dataDictionary = {}
    for f in files:
        predicateSymbol = f.replace('.txt', '')
        lines = readLines(join(folderPath, f))
        dict = {}
        for line in lines:
            items = line.split('\t')
            n= len(items)
            truthValue = items[n-1]
            args = items[:n-1]
            #we do not allow more than 2 args
            if len(args)==2:
                if args[0] in dict:
                    arg1Dict = dict[args[0]]
                    #arg2Dict = dict[args[1]]
                else:
                    arg1Dict = {}
                    #arg2Dict = {}
                arg1Dict[args[1]] = truthValue
               # arg2Dict[args[0]] = truthValue
                dict[args[0]] = arg1Dict
                #dict[args[1]] =arg2Dict
            elif len(args)==1:
                arg1Dict = {}
                arg1Dict[args[0]] = truthValue
                dict[args[0]] = arg1Dict
        dataDictionary[predicateSymbol] = dict
    return dataDictionary
            
 
def makeAtomDictionary(dataDictionary): 
    atomDictionary = {} 
    for predicate in dataDictionary:
         predicateDict = dataDictionary[predicate]
         for arg in predicateDict:
             atom = predicate+'('+arg
             values = predicateDict[arg]
             if len(values)==1:
                 atom = predicate+'('+arg+')'
                 atomDictionary[atom] = values[0]
             else:
                 atom = predicate+'('+arg+','+values[0]+')'
                 atomDictionary[atom] = values[1]
    return atomDictionary

  
def parseRule(rule):
    #predict structure: symbol, args, IsNegated
    ruleContent = rule.split('->')
    headAtom = ruleContent[1].replace(' ','')
    bodyAtoms = ruleContent[0]
    headPredicate = pargeAtom(headAtom)
    atoms = bodyAtoms.split('&')
    bodyAtomList = []
    for atom in atoms:
        #if item is negated
        atom = atom.replace(' ','')
        atomPredicate = parseAtom(atom)
        atomList.append(atomPredicate) 
    ruleStruct = Rule(headPredicate, bodyAtomList)
    return ruleStruct
   
def parseAtom(atom):
    if atom.startswith('~'):
        isNegated = True
    else:
        isNegated = False
    atom = atom.replace('~','')
    items = atom.split('(')
    symbol = items[0]
    args = items[1].replace(')','').split(',')  
    atomPredicate = AtomPredicate(symbol,args,isNegated)  
    return atomPredicate       
                   
def groundRule(rule, dataDictionary):
    groundedRules = []
    ruleStruct = parseRule(rule)
    # we only consider rules with one or two atoms and one atom as head
    
    if len(ruleStruct.getBody()) == 0:
        #type 1: A
        groundedRules = groundTypeOne(ruleStruct, dataDictionary)
    elif len(ruleStruct.getBody())==1:
        #type2: A -->B
        groundedRules = groundTypeTwo(ruleStruct, dataDictionary)
    elif len(ruleStruct.getBody())==1:
        #type3: A & B --> C
        groundedRules = groundTypeThree(ruleStruct, dataDictionary)
    else:
        print ('We cannot support these type of rules!')
    return groundedRules



def groundTypeOne(ruleStruct, dataDictionary):
    #type 1: A
    groundedRules = []
    headPredicate = ruleStruct.getHead()
    predicateSymbol = headPredicate.getSymbolName()
    valueDictionary = dataDictionary(predicateSymbol)
    for key in valueDictionary:
        groundedRule = predicateSymbol+'('+key+')'
        if headPredicate.getIsNegated:
            groundedRules.append('~'+groundedRule)
        else:
            groundedRules.append(groundedRule)
    return groundedRules
        
        
def groundTypeTwo(ruleStruct, dataDictionary): 
    #type2: A -->B  
    groundedRules = []
    headPredicate = ruleStruct.getHead()
    bodyPredicate = ruleStruct.getBody()[0]
    headArgs = headPredicate.getArguments()
    bodyArgs = bodyPredicate.getArguments()
    correctFormat = 0
    for arg in headArgs:
        if arg in bodyArgs:
            correctFormat += 0
        else:
            correctFormat += 1
    if (len(headArgs)==len(bodyArgs) and correctFormat ==0):
        if len(headArgs)==1:
            #one argument
            headDictionary = dataDictionary[headPredicate.getSymbolName()]
            bodyDictionary = dataDictionary[bodyPredicate.getSymbolName()]
            for arg1 in bodyDictionary:
                groundHead = AtomPredicate(headPredicate.getSymbolName(), [arg1], headPredicate.getIsNegated())
                groundBody = AtomPredicate(bodyPredicate.getSymbolName(), [arg1], bodyPredicate.getIsNegated())
                groundRule = Rule(groundHead, [groundBody])
                groundedRules.append(groundRule.getTextRule())
        elif len(headArgs)==2:
            #two arguments
            headDictionary = dataDictionary[headPredicate.getSymbolName()]
            bodyDictionary = dataDictionary[bodyPredicate.getSymbolName()]
            for arg1 in headDictionary:
                if arg1 in bodyDictionary:
                    arg2Dict = headDictionary[arg1]
                    for key in arg2Dict:
                        groundHead = AtomPredicate(headPredicate.getSymbolName(), [arg1, key], headPredicate.getIsNegated())
                        groundBody = AtomPredicate(bodyPredicate.getSymbolName(), [arg1, key], bodyPredicate.getIsNegated())
                        groundRule = Rule(groundHead, [groundBody])
                        groundedRules.append(groundRule.getTextRule())
        else:
            print('We do not support predicate with more than two arguments or less than one argument!')
    else:
        print('The format of the rule {r} is not correct!', ruleStruct.getTextRule())
    return groundedRules   
        
 

def groundTypeThree(ruleStruct, dataDictionary):  
    #type3: A & B & ...--> C 
    groundedRules = []
    headPredicate = ruleStruct.getHead()
    bodyPredicates = ruleStruct.getBody()
    headArgs = headPredicate.getArguments()
    bodySize = len(bodyPredicates)
    argsDict1 = {}
    argsDict2 = {}
    for body in bodyPredicates:
        args  = body.getArguments()
        if (len(args) ==1):
            if args[0] in argsDict:
                predicatelist = argsDict1[args[0]]
            else:
                predicatelist = []
            predicatelist.append(body)
            argsDict1[args[0]] = predicatelist
        elif (len(args) ==2):
            if args[0] in argsDict:
                predicatelist = argsDict1[args[0]]
            else:
                predicatelist = []
            predicatelist.append(body)
            argsDict1[args[0]] = predicatelist
            ####
            if args[1] in argsDict:
                predicatelist = argsDict2[args[1]]
            else:
                predicatelist = []
            predicatelist.append(body)
            argsDict2[args[1]] = predicatelist
    argList = []        
    for key in argsDict1:
        if key not in argList:
            argList.append(key)
    for key in argsDict2:
        if key not in argList:
            argList.append(key)
    correctFormat = 0
    for arg in headArgs:
        if arg in argList:
            correctFormat +=0
        else:
            correctFormat +=1
    if (len(headArgs) ==1 and correctFormat == 0):
        if (len(argList) % 2 ==1):
            argGroundedDict = makeGroundDictionary(ruleStruct, dataDictionary, argsDict1, argsDict2) 
            groundedRules = getGroundedRules(argGroundedDict)
        else:
             print('The format of the rule {r} is not correct!', ruleStruct.getTextRule())
            
    elif (len(headArgs) ==2 and correctFormat == 0):
        if (len(argList) % 2 ==0):
            argGroundedDict = makeGroundDictionary(ruleStruct, dataDictionary, argsDict1, argsDict2)
            groundedRules = getGroundedRules(argGroundedDict)
        else:
             print('The format of the rule {r} is not correct!', ruleStruct.getTextRule())
 
    else:
        print('We do not support predicate with more than two arguments or less than one argument!')    
    return groundedRules     
        


def makeGroundDictionary(ruleStruct, dataDictionary,argsDict1, argsDict2):
    argGroundedDict = {}
    for arg in argsDict1:
        bodyList = argsDict1[arg]
        for body in bodyList:
            predicate = body.getSymbolName()
            dictArgument = dataDictionary[predicate]
            for dictValue in dictArgument:
                for key in dictValue:
                    if key in argGroundedDict:
                        groudnedList = argGroundedDict[arg]
                    else:
                        groudnedList = []
                    groudnedList.append(key)  
                    argGroundedDict[arg] = groudnedList
            if len(body.getArguments)==2:
                arg2 = body.getArguments()[1]
                for dictValue in dictArgument:
                    for key in dictValue:
                        dictArg2 = dictValue[key]
                        for argKey in dictArg2:
                            if argKey in argGroundedDict:
                                groudnedList = argGroundedDict[argKey]
                            else:
                                groudnedList = []
                            groudnedList.append(argKey)  
                            argGroundedDict[argKey] = groudnedList
    return argGroundedDict


def getGroundedRules(ruleStruct, argGroundedDict, headPredicate, bodyPredicates):
    groundedRules =[]
    groundedRules2 =[]
    finalGroundedRules =[]
    #here we limit the size to 3 
    if (len(headPredicate.getArguments())==1):
        argHead1 = headPredicate.getArguments()[0]
    else: 
        argHead1 = headPredicate.getArguments()[0]
        argHead2 = headPredicate.getArguments()[1]
    grounedValues = argGroundedDict[argHead1]
    for value in grounedValues:
        groundHead = AtomPredicate(headPredicate.getSymbolName(), [value], headPredicate.getIsNegated())
        groundBodies = []
        for body in bodyPredicates:
            if argHead in body.getArguments():
                groundBody = AtomPredicate(body.getSymbolName(), [value], body.getIsNegated())
            else:
                groundBody = AtomPredicate(body.getSymbolName(), [], body.getIsNegated())
            groundBodies.append(groundBody)
        groundRule = Rule(groundHead, groundBodies)
        groundedRules.append(groundRule.getTextRule())
    groundedRules2 =[]
    if (len(headPredicate.getArguments())==2): 
        grounedValues = argGroundedDict[argHead2]
        for value in grounedValues:
            for rule in groundedRules:
                head = rule.getHead()
                values = head.getArguments()
                values.append(value)
                groundHead = AtomPredicate(headPredicate.getSymbolName(), values, headPredicate.getIsNegated())
                bodies = rule.getBody()
                groundBodies = []
                index = 0
                for body in bodyPredicates:
                    if argHead2 in body.getArguments():
                        argBody = body.getArguments()
                        if argBody[1] == argHead2:
                            groundBody = AtomPredicate(body.getSymbolName(), bodies[index].getArguments().append(value), body.getIsNegated())
                        else:
                            tempValue = [value].append(bodies[index].getArguments()[0])
                            groundBody = AtomPredicate(body.getSymbolName(), tempValue, body.getIsNegated())
                    else:
                        groundBody = AtomPredicate(body.getSymbolName(), [], body.getIsNegated())
                    index+=1
                    groundBodies.append(groundBody)
                groundRule = Rule(groundHead, groundBodies)
                groundedRules2.append(groundRule.getTextRule())
    if (len(headPredicate.getArguments())==1):
        finalGroundedRules = groundBodies(groundedRules, argGroundedDict, headPredicate.getArguments(), bodyPredicates) 
    else:
        finalGroundedRules = groundBodies(groundedRules2, argGroundedDict, headPredicate.getArguments(), bodyPredicates) 
    return finalGroundedRules          
                
def groundBodies(groundedRules, argGroundedDict, headArgs, bodyPredicates):
    finalGroundedRules = []
    for arg in argGroundedDict:
        if (arg not in headArgs):
            for rule in groundedRules:
                groundHead = rule.getHead()
                groundBodies = rule.getBody()
                for value in groundedRules[arg]:
                    index = 0
                    for body in bodyPredicates:
                        if arg in body.getArguments():
                            argBody = body.getArguments()
                            if argBody[1] == arg:
                                groundBody = AtomPredicate(body.getSymbolName(), groundBodies[index].getArguments().append(value), body.getIsNegated())
                            else:
                                tempValue = [value].append(groundBodies[index].getArguments()[0])
                                groundBody = AtomPredicate(body.getSymbolName(), tempValue, body.getIsNegated())
                        else:
                            groundBody = AtomPredicate(body.getSymbolName(), [], body.getIsNegated())
                        index+=1
                        groundBodies.append(groundBody)
                    groundRule = Rule(groundHead, groundBodies)
                    finalGroundedRules.append(groundRule.getTextRule())
        groundedRules = finalGroundedRules 
        finalGroundedRules = []   
    return groundedRules
            
            

