#!/usr/bin/env python3

import os, shutil
import numpy 
import random
from random import shuffle

def saveFile(path, content):
    with open(path, 'a') as out:
        out.write(content + '\n')

def removeFolderContents(folderPath):
    for the_file in os.listdir(folderPath):
        file_path = os.path.join(folderPath, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    
def dataGenerator(dataPath):
    removeFolderContents(dataPath)
    ##Initial setup
    inistituteSize = 20
    reviewerSize = 30
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
    inistitueDict = fileGenerator(inistituteSize, dataPath+'inistitue.txt', instituteStringIndex)
    paperSize, submissionDict = instituteSubmission(inistitueDict, n , p )
    print ('number of submissions: '+ str(paperSize))
    authorDict = fileGenerator(paperSize, dataPath+'author.txt', authorStringIndex)
    paperDict = fileGenerator(paperSize, dataPath+'paper.txt', paperStringIndex)
    presentDict = fileGenerator(paperSize, dataPath+'presents.txt', authorStringIndex)
    reviewerDict = fileGenerator(reviewerSize, dataPath+'reviewer.txt', reviewerStringIndex)
    submitDict = submitGenerator(paperSize, dataPath+'submits.txt',authorStringIndex, paperStringIndex)
    affilitaionDict = affiliationGenerator(submissionDict, paperSize, n , p ,authorStringIndex, instituteStringIndex, dataPath+'affiliation.txt' )
    ###
    print('generate simple relations')
    studentDict = studentGenerator(paperSize,studentProb,authorStringIndex, dataPath+'student.txt')
    reviewDict = reviewerGenerator(paperSize, reviewerSize, numberOfReviewerPerPaper,reviewerStringIndex, paperStringIndex, dataPath+'reviews.txt')
    acceptableDict = acceptableGenerator(paperSize,studentProb, studentAcceptableProb, nonStudentAcceptableProb, paperStringIndex, dataPath+'acceptable.txt')
    highRankDict = highRankInstituteGenerator(inistituteSize, highRankProb, instituteStringIndex, dataPath+'highRank.txt')
    ###
    print('generate complex relations')
    positiveDict = positiveReviewGenerator(paperDict,submitDict,reviewDict, affilitaionDict, highRankDict, studentDict, acceptableDict, reviewProbability, numberOfReviewerPerPaper, reviewerStringIndex, dataPath+'positiveReview.txt')
    summaryGenerator(paperDict, positiveDict, reviewDict, numberOfReviewerPerPaper, summaryProbability, dataPath+'positiveSummary.txt')

def instituteSubmission(inistitueDict, n , p ):
    submissionDict = {}
    paperSize = 0
    for inistitue in inistitueDict:
        numberOfSubmission = numpy.random.binomial(n , p)
        paperSize+=numberOfSubmission
        submissionDict[inistitue] = numberOfSubmission
    return paperSize,submissionDict
        
   
def affiliationGenerator(submissionDict, paperSize, n , p ,
                         authorStringIndex, instituteStringIndex, 
                         dataPath ):
    affilitaionDict = {}
    text=''
    index = 0
    authorList = [i for i in range(paperSize)]
    shuffle(authorList) 
    for inistitue in submissionDict:
        numberOfSubmission = submissionDict[inistitue]
        i = 0
        while i<numberOfSubmission:
            id = authorStringIndex+str(authorList[index])
            text+= id+'\t'+inistitue+'\t'+'1.0'+'\n'
            affilitaionDict[id] = inistitue
            index+=1
            i+=1
    saveFile(dataPath, text)
    return  affilitaionDict
    
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
   
       
def reviewerGenerator(authorSize, reviewerSize, numberOfReviewerPerPaper,reviewerStringIndex, paperStringIndex, dataPath):    
    reviewDict = {}   
    index = 0
    reviewerText = ''
    while index<authorSize:
        r=0
        while r<numberOfReviewerPerPaper:
            reviewerId = random.randint(0, reviewerSize-1)
            if paperStringIndex+ str(index) in reviewDict:
                reviewers = reviewDict[paperStringIndex+ str(index)]
                while reviewers[0] == reviewerStringIndex+str(reviewerId):
                    reviewerId = random.randint(0, reviewerSize-1)
            else:
                reviewers = []
            reviewers.append(reviewerStringIndex+str(reviewerId))
            reviewerText+=reviewerStringIndex+str(reviewerId)+'\t'+paperStringIndex+ str(index)+'\t'+'1.0'+'\n' 
            reviewDict[paperStringIndex+ str(index)] = reviewers
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
    

    

'''
    Gives a tuple of True/False according to the binary representation
    of the number:

    __numbits(0, 3) -> (False, False, False)
    __numbits(1, 3) -> (False, False, True)
    ...
    __numbits(6, 3) -> (True,  True,  False)
    __numbits(7, 3) -> (True,  True,  True)
'''
def __num2bits(n, nbits):
    bits = [False] * nbits
    for i in range(1, nbits + 1):
        bits[nbits - i] = bool(n % 2)
        n >>= 1
    return tuple(bits)

    
def positiveReviewGenerator(paper_dict, submit_dict, reviewDict,
                              affiliation_dict, high_rank_dict,
                              student_dict, acceptable_dict,
                              review_probability, num_reviews_per_paper,
                              reviewer_string_index, data_path):
    prob_dict = dict()
    for i in range(8):
        prob_dict[__num2bits(i, 3)] = review_probability[i]
        
    text = ''
    positive_dict = dict()
    for paper in paper_dict:
        author = submit_dict[paper]
        affilitaion = affiliation_dict[author]
        is_high_rank = bool(high_rank_dict[affilitaion])
        is_student = bool(student_dict[author])
        is_acceptable = bool(acceptable_dict[paper])
        prob_key = (is_acceptable, is_high_rank, is_student)
        for reviewer in reviewDict[paper]:
            key = reviewer + paper
            random_number = random.random()
            if random_number  < prob_dict[prob_key]:
                positive_dict[key] = 1.0
            else:
                positive_dict[key] = 0.0
            text += (reviewer +
                    '\t' + paper + '\t' + str(positive_dict[key]) + '\n')

    saveFile(data_path, text)
    return positive_dict   
    
def summaryGenerator(paper_dict, positive_dict, reviewDict,
                      num_reviews_per_paper,
                      summary_probability, data_path):
    prob_dict = dict()
    for i in range(2**num_reviews_per_paper):
        prob_dict[__num2bits(i, num_reviews_per_paper)] = summary_probability[i]
    
    text = ''
    for paper in paper_dict:
        key = []
        for reviewer in reviewDict[paper]:
            review_key = reviewer + paper
            review = bool(positive_dict[review_key])
            key.append(review)
            
        key = tuple(key)
        random_number = random.random()
        summary = float(random_number < prob_dict[key])
        text += paper + '\t' + str(summary) + '\n'
    saveFile(data_path, text)
 
           
dataPath = './reviewData/'            
dataGenerator(dataPath)   

 





       