import os
import numpy 
import random

def saveFile(path, content):
    with open(path, 'a') as out:
        out.write(content + '\n')


def dataGenerator(dataPath):
    paperSize = 100
    inistituteSize = 20
    numberOfReviewerPerPaper = 2
    studentProb = 0.7
    studentAcceptableProb = 0.2
    nonStudentAcceptableProb = 0.4
    highRankProb = 0.5
    n = 10
    p = 0.5
    reviewProbability = [0.15,0.05,0.20,0.15,0.85,0.30,0.85,0.70]
    summaryProbability = [0.0,0.20,0.20,0.90]
    authorStringIndex = 'a'
    paperStringIndex = 'p'
    instituteStringIndex = 'i'
    reviewerStringIndex = 'r'
    ####
    print('generate simple attributes')
    authorDict = fileGenerator(paperSize, dataPath+'author.txt', authorStringIndex)
    paperDict = fileGenerator(paperSize, dataPath+'paper.txt', paperStringIndex)
    submitDict = submitGenerator(paperSize, dataPath+'submits.txt',authorStringIndex, paperStringIndex)
    inistitueDict = fileGenerator(inistituteSize, dataPath+'inistitue.txt', instituteStringIndex) 
    ###
    print('generate simple relations')
    studentDict = studentGenerator(paperSize,studentProb,authorStringIndex, dataPath+'student.txt')
    reviewDict = reviewerGenerator(paperSize, numberOfReviewerPerPaper,reviewerStringIndex, paperStringIndex, dataPath+'reviews.txt')
    acceptableDict = acceptableGenerator(paperSize,studentProb, studentAcceptableProb, nonStudentAcceptableProb, paperStringIndex, dataPath+'acceptable.txt')
    highRankDict = highRankInstituteGenerator(inistituteSize, highRankProb, instituteStringIndex, dataPath+'highRank.txt')
    ###
    print('generate complex relations')
    affilitaionDict = affiliationGenerator(paperSize, authorDict, inistitueDict, n , p ,authorStringIndex,inistituteSize, instituteStringIndex, dataPath+'affiliation.txt' )
    positiveDict = positiveReviewGenerator(paperDict,submitDict,affilitaionDict, highRankDict, studentDict, acceptableDict, reviewProbability, numberOfReviewerPerPaper, reviewerStringIndex, dataPath+'positiveReview.txt')
    summaryGenerator(paperDict, positiveDict, reviewerStringIndex, summaryProbability, dataPath+'positiveSummary.txt')
    
    
def fileGenerator(size, filePath, stringIndex):
    fileDict = {}
    index=0
    text=''
    while index<size:
        key = stringIndex+str(index)
        text+=key+'\t'+'1.0'+'\n'
        fileDict[key] = 1.0
        index+=1
    saveFile(filePath, text)  
    return fileDict

def submitGenerator(size, filePath,authorStringIndex, paperStringIndex):
    submitDict={}
    index=0
    text=''
    while index<size:
        text+=authorStringIndex+str(index)+'\t'+paperStringIndex+str(index)+'\t'+'1.0'+'\n'
        submitDict[paperStringIndex+str(index)] = authorStringIndex+str(index)
        index+=1
    saveFile(filePath, text)
    return submitDict
      
def studentGenerator(authorSize,studentProb,authorStringIndex, dataPath):
    studentDict = {}
    studentSize = authorSize * studentProb
    index = 0
    studentText = ''
    while index<studentSize:
        studentText+=authorStringIndex+str(index)+'\t'+'1.0'+'\n' 
        studentDict[authorStringIndex+str(index)] = 1.0
        index+=1
    while index<authorSize:
        studentText+=authorStringIndex+str(index)+'\t'+'0.0'+'\n' 
        studentDict[authorStringIndex+str(index)] = 0.0
        index+=1
    saveFile(dataPath, studentText) 
    return studentDict  
   
       
def reviewerGenerator(authorSize, numberOfReviewerPerPaper,reviewerStringIndex, paperStringIndex, dataPath):    
    reviewDict = {}   
    index = 0
    reviewerText = ''
    while index<authorSize:
        r=0
        while r<numberOfReviewerPerPaper:
            reviewerText+=reviewerStringIndex+str(r)+'\t'+paperStringIndex+ str(index)+'\t'+'1.0'+'\n' 
            reviewDict[reviewerStringIndex+str(r)+paperStringIndex+ str(index)] = 1.0
            r+=1
        index+=1
    saveFile(dataPath, reviewerText)
    return reviewDict


def acceptableGenerator(authorSize,studentProb, studentAcceptableProb, nonStudentAcceptableProb, paperStringIndex, dataPath):
    acceptableDict = {}
    index = 0
    acceptableText = ''
    studentSize = authorSize * studentProb
    studentAcceptableSize = studentSize * studentAcceptableProb
    nonStudentAcceptableSize = (authorSize - studentSize) * nonStudentAcceptableProb
    while index<studentSize:
        if index<studentAcceptableSize:
            acceptableText += paperStringIndex+ str(index)+'\t'+'1.0'+'\n' 
            acceptableDict[paperStringIndex+ str(index)] = 1.0
        else:
            acceptableText += paperStringIndex+ str(index)+'\t'+'0.0'+'\n' 
            acceptableDict[paperStringIndex+ str(index)] = 0.0
        index+=1
    indexNonStudent = 0
    while index<authorSize:
        if indexNonStudent<nonStudentAcceptableSize:
            acceptableText += paperStringIndex+ str(index)+'\t'+'1.0'+'\n' 
            acceptableDict[paperStringIndex+ str(index)] = 1.0
        else:
            acceptableText += paperStringIndex+ str(index)+'\t'+'0.0'+'\n' 
            acceptableDict[paperStringIndex+ str(index)] = 0.0
        index+=1
        indexNonStudent+=1
    saveFile(dataPath, acceptableText)
    return acceptableDict
    
def highRankInstituteGenerator(inistituteSize, highRankProb, instituteStringIndex, dataPath):
    highRankDict = {}
    index = 0
    highRankSize = inistituteSize*highRankProb
    text=''
    while index<highRankSize:
        text+=instituteStringIndex+str(index)+'\t'+'1.0'+'\n'
        highRankDict[instituteStringIndex+str(index)] = 1.0
        index+=1
    while index<inistituteSize:
        text+=instituteStringIndex+str(index)+'\t'+'0.0'+'\n'
        highRankDict[instituteStringIndex+str(index)] = 0.0
        index+=1
    saveFile(dataPath, text)
    return highRankDict

def affiliationGenerator(authorSize, authorDict, inistitueDict, n , p ,authorStringIndex,inistituteSize, instituteStringIndex, dataPath ):
    affilitaionDict = {}
    text=''
    index = 0
    for inistitue in inistitueDict:
        numberOfSubmission = numpy.random.binomial(n , p)
        i = 0
        while i<numberOfSubmission:
            if (index<authorSize):
                id = authorStringIndex+str(random.randint(1, 100))
                if id not in affilitaionDict:
                    text+= id+'\t'+inistitue+'\t'+'1.0'+'\n'
                    affilitaionDict[id] = inistitue
                index+=1
            i+=1
        if index<authorSize:
            for author in authorDict:
                if author not in affilitaionDict:
                    inistituteID = random.randint(1, inistituteSize)
                    text+= author+'\t'+instituteStringIndex+str(inistituteID)+'\t'+'1.0'+'\n'
                    affilitaionDict[author] = instituteStringIndex+str(inistituteID)
    saveFile(dataPath, text)
    return  affilitaionDict
   
 
def positiveReviewGenerator(paperDict,submitDict,affilitaionDict, highRankDict, studentDict, acceptableDict, reviewProbability, numberOfReviewerPerPaper, reviewerStringIndex, dataPath):
    positiveDict = {}
    text = ''
    for paper in paperDict:
        author = submitDict[paper]
        affilitaion = affilitaionDict[author]
        rank = highRankDict[affilitaion]
        student = studentDict[author]
        acceptable = acceptableDict[paper]
        randomNumber1 = random.random()
        randomNumber2 = random.random()
        randomNums = [randomNumber1, randomNumber2]
        index = 0
        if (acceptable == 0.0 and rank == 0.0 and student ==0.0):
            while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[0]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1
        elif (acceptable == 0.0 and rank == 0.0 and student ==1.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[1]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1
        elif (acceptable == 0.0 and rank == 1.0 and student ==0.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[2]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1
        elif (acceptable == 0.0 and rank == 1.0 and student ==1.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[3]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1  
        elif (acceptable == 1.0 and rank == 0.0 and student ==0.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[4]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1 
        elif (acceptable == 1.0 and rank == 0.0 and student ==1.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[5]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1
        elif (acceptable == 1.0 and rank == 1.0 and student ==0.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[6]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1
        elif (acceptable == 1.0 and rank == 1.0 and student ==1.0):
             while index<numberOfReviewerPerPaper:
                key = reviewerStringIndex+str(index)+paper
                if (randomNums[index]<=reviewProbability[7]):
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'1.0'+'\n'
                    positiveDict[key] = 1.0
                else:
                    text+=reviewerStringIndex+str(index)+'\t'+paper+'\t'+'0.0'+'\n'
                    positiveDict[key] = 0.0
                index+=1
        else:
            print('error')
        saveFile(dataPath, text)
        return positiveDict

#this in specificly for 2 reviews
def summaryGenerator(paperDict, positiveDict, reviewerStringIndex, summaryProbability, dataPath):
    text = ''
    for paper in paperDict:
        reviewer1 =reviewerStringIndex+str(0)+paper
        reviewer2 =reviewerStringIndex+str(1)+paper
        review1 = positiveDict[reviewer1]
        review2 = positiveDict[reviewer2]
        randomNumber = random.random()
        if (review1 == 0.0 and review2 == 0.0 ):
            if (randomNumber<=summaryProbability[0]):
                text+= paper+'\t'+'1.0'+'\n'
            else:
                text+= paper+'\t'+'0.0'+'\n'
        elif (review1 == 0.0 and review2 == 1.0):
            if (randomNumber<=summaryProbability[1]):
                text+= paper+'\t'+'1.0'+'\n'
            else:
                text+= paper+'\t'+'0.0'+'\n'
        elif (review1 == 0.0 and review2 == 1.0):
            if (randomNumber<=summaryProbability[2]):
                text+= paper+'\t'+'1.0'+'\n'
            else:
                text+= paper+'\t'+'0.0'+'\n'
        elif (review1 == 1.0 and review2 == 1.0):
            if (randomNumber<=summaryProbability[3]):
                text+= paper+'\t'+'1.0'+'\n'
            else:
                text+= paper+'\t'+'0.0'+'\n'
        saveFile(dataPath, text)
            
            
dataPath = '/Users/Gfarnadi/Movies/GitRepository/FairPSL/debug/reviewData/'            
dataGenerator(dataPath)   






       