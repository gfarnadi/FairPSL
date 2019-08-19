#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function
import os, shutil
import numpy 
import random
from random import shuffle


def saveFile(path, content):
    with open(path, 'a') as out:
        out.write(content + '\n')

def generate_qualification(user_dict, quality_file, promotion_file, quality_rate):
    #TODO: IF FILE EXISTS, READ, OTHRWISE MAKE
    quality_dict = {}
    if os.path.isfile(quality_file):
        with open(quality_file, 'r') as qf:
            lines = qf.readlines()
            for line in lines:
                info = line.split('\t')
                score = info[1].strip()
                quality_dict[info[0]] = float(score) 
    with open(promotion_file, "w") as pf:
        with open(quality_file,"w") as qf:
            for user in user_dict.keys():
                if random.random()<quality_rate:
                    quality_dict[user] = 1
                    print('%s\t1'%(user),file=qf)
                    print('%s\t1'%(user),file=pf)
                else:
                    quality_dict[user] = 0
                    print('%s\t0'%(user),file=qf)
                    print('%s\t0'%(user),file=pf)
    return quality_dict



def read_user_data(user_file):
    user_dict = {}
    with open(user_file, "r") as uf:
        lines = uf.readlines()
        for line in lines:
            info = line.split('\t')
            user_dict[info[0]] = info[1].strip()
    return user_dict



def read_manager_data(manager_file):
    manager_dict = {}
    with open(manager_file, 'r') as mf:
        lines= mf.readlines()
        for line in lines:
            info = line.split('\t')
            user1 = info[0].strip()
            user2 = info[1].strip()
            if user2 in manager_dict.keys():
                manager_dict[user2].append(user1)
            else:
                manager_dict[user2] = [user1]
    return manager_dict



def generate_opinion(user_dict, quality_dict, manager_dict,opinion_equal_mp, opinion_equal_mn, opinion_notequal_mp, opinion_notequal_mn, opinion_equal_p, opinion_equal_n, opinion_notequal_p, opinion_notequal_n, opinion_file):
    opinion_dict = {}
    with open(opinion_file, 'w') as ff:
        for user1,label1 in user_dict.items():
            for user2, label2 in user_dict.items():
                if user1==user2: continue
                if user2 in manager_dict.keys():
                    if user1 in manager_dict[user2]:
                        if quality_dict[user2]==1:
                            if label1==label2:
                                if random.random()<opinion_equal_mp:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                            else:
                                if random.random()<opinion_notequal_mp:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                        else:
                            if label1==label2:
                                if random.random()<opinion_equal_mn:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                            else:
                                if random.random()<opinion_notequal_mn:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0

                    else:     
                        if quality_dict[user2]==1:
                            if label1==label2:
                                if random.random()<opinion_equal_p:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                            else:
                                if random.random()<opinion_notequal_p:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                        else:
                            if label1==label2:
                                if random.random()<opinion_equal_n:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                            else:
                                if random.random()<opinion_notequal_n:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                else:
                    if quality_dict[user2]==1:
                            if label1==label2:
                                if random.random()<opinion_equal_p:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                            else:
                                if random.random()<opinion_notequal_p:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                    else:
                            if label1==label2:
                                if random.random()<opinion_equal_n:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0
                            else:
                                if random.random()<opinion_notequal_n:
                                    print('%s\t%s\t1'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 1
                                else:
                                    print('%s\t%s\t0'%(user1,user2), file =ff)
                                    opinion_dict[(user1,user2)] = 0

    return opinion_dict



def generate_submission(user_file, ingroup_file, manager_file, quality_file, opinion_file, submit_file, promotion_file, submission_rate_A, submission_rate_B, opinion_equal_p, opinion_equal_n, opinion_equal_mn, opinion_equal_mp, opinion_notequal_p, opinion_notequal_n, opinion_notequal_mp, opinion_notequal_mn, quality_rate, performance_rate_p, performance_rate_n, performance_file):
    user_dict = read_user_data(user_file)
    generate_ingroup(user_dict, ingroup_file)
    quality_dict = generate_qualification(user_dict, quality_file, promotion_file, quality_rate)
    manager_dict = read_manager_data(manager_file)
    opinion_dict = generate_opinion(user_dict, quality_dict, manager_dict,opinion_equal_mp, opinion_equal_mn, opinion_notequal_mp, opinion_notequal_mn, opinion_equal_p, opinion_equal_n, opinion_notequal_p, opinion_notequal_n, opinion_file)
    with open(submit_file, "w") as sf:
        for key, opinion in opinion_dict.items():
            user1 = key[0]
            user2 = key[1]
            if user_dict[user1] =='A':
                if random.random()<submission_rate_A:
                    print('%s\t%s\t%d'%(user1,user2,opinion), file =sf)

            else:
                if random.random()<submission_rate_B:
                    print('%s\t%s\t%d'%(user1,user2,opinion), file =sf)
    performance_dict = generate_performance(quality_dict, performance_rate_p, performance_rate_n, performance_file)
    info_e, info_em = generate_discrimination_score(user_dict, manager_dict, opinion_dict, quality_dict, performance_dict)
    return info_e, info_em



def generate_performance(quality_dict, performance_rate_p, performance_rate_n, performance_file):
    performance_dict = {}
    #TODO: IF FILE EXISTS, READ, OTHRWISE MAKE
    if os.path.isfile(performance_file):
        with open(performance_file, 'r') as pf:
            lines = pf.readlines()
            for line in lines:
                info = line.split('\t')
                score = info[1].strip()
                performance_dict[info[0]] = float(score)
    else:
        with open(performance_file, 'w') as pf:
            for user,quality in quality_dict.items():
                if quality_dict[user]==1:
                    if random.random()<performance_rate_p:
                        print('%s\t%d'%(user,1), file =pf)
                        performance_dict[user] = 1
                    else:
                        print('%s\t%d'%(user,0), file =pf)
                        performance_dict[user] = 0
                else:
                    if random.random()<performance_rate_n:
                        print('%s\t%d'%(user,1), file =pf)
                        performance_dict[user] = 1
                    else:
                        print('%s\t%d'%(user,0), file =pf)
                        performance_dict[user] = 0
    return performance_dict



def generate_ingroup(user_dict, ingroup_file):
    with open(ingroup_file, 'w') as igf:
        for user1, label1 in user_dict.items():
            for user2, label2 in user_dict.items():
                if label1==label2:
                    print('%s\t%s\t%d'%(user1,user2,1), file =igf)
                else:
                    print('%s\t%s\t%d'%(user1,user2,0), file =igf)


# In[2]:


def generate_discrimination_score(employees, manager_dict, opinion_dict, quality_dict, performance_dict):
    info_e = []
    opinion_e = {}
    for e1 in employees.keys():
        opinion_e[e1] = 0
        for e2 in employees.keys():
            if e1==e2:continue
            opinion_e[e1]+=float(opinion_dict[(e2,e1)])
        opinion_e[e1] = float(opinion_e[e1])/float(len(employees))
        info_e.append((opinion_e[e1], performance_dict[e1], quality_dict[e1]))
    
    info_em = []
    opinion_em = {}
    for e in employees.keys():
        opinion_em[e] = 0
        if e in manager_dict.keys():
            for m in manager_dict[e]:
                opinion_em[e]+=float(opinion_dict[(m,e)])
            opinion_em[e] = float(opinion_em[e])/float(len(manager_dict[e]))
            info_em.append((opinion_em[e], performance_dict[e], quality_dict[e]))
        else:
            info_em.append((None, performance_dict[e], quality_dict[e]))
    return info_e, info_em


# In[3]:


def run(theta, folder_name):
    i=1
    while i<=len(theta):
        user_file = '../data/parameters/'+folder_name+'/'+str(i)+'/label.txt'
        quality_file = '../data/parameters/'+folder_name+'/'+str(i)+'/quality.txt'
        opinion_file='../data/parameters/'+folder_name+'/'+str(i)+'/opinion.txt'
        submit_file = '../data/parameters/'+folder_name+'/'+str(i)+'/submit.txt'
        promotion_file = '../data/parameters/'+folder_name+'/'+str(i)+'/promotion.txt'
        performance_file = '../data/parameters/'+folder_name+'/'+str(i)+'/performance.txt'
        manager_file='../data/parameters/'+folder_name+'/'+str(i)+'/manager.txt'
        ingroup_file = '../data/parameters/'+folder_name+'/'+str(i)+'/ingroup.txt'
        opinion_equal_mp = theta[i-1][1]
        opinion_equal_mn = theta[i-1][3]
        opinion_notequal_mp =theta[i-1][0]
        opinion_notequal_mn =theta[i-1][2]
        opinion_equal_p = theta[i-1][1]
        opinion_equal_n = theta[i-1][3]
        opinion_notequal_p =theta[i-1][0]
        opinion_notequal_n =theta[i-1][2]
        submission_rate_A = 0.6
        submission_rate_B = 0.6
        quality_rate = 0.4
        performance_rate_p = 0.6
        performance_rate_n = 0.1
        info_e, info_em = generate_submission(user_file, ingroup_file, manager_file, quality_file, opinion_file, submit_file, promotion_file, submission_rate_A, submission_rate_B, opinion_equal_p, opinion_equal_n, opinion_equal_mn, opinion_equal_mp, opinion_notequal_p, opinion_notequal_n, opinion_notequal_mp, opinion_notequal_mn, quality_rate, performance_rate_p, performance_rate_n, performance_file)
        i+=1
        #generate_performance(quality_dict, performance_rate_p, performance_rate_n, performance_file)


# In[4]:


def get_discrimination_score(info_e, info_em):
    score = 0
    for item in info_e:
        if item[0]>=0.5 and item[2]==1:
            score+=1
        elif item[0]<0.5 and item[2]==0:
            score+=1
    disc_1 = float(score)/float(len(info_e))
    print(disc_1)
    score = 0
    for item in info_em:
        if item[0]==None:continue
        if item[0]>=0.5 and item[2]==1:
            score+=1
        elif item[0]<0.5 and item[2]==0:
            score+=1
    disc_2 = float(score)/float(len(info_e))
    print(disc_2)        


# In[5]:


'''
theta = [[0.0,1.0,0.0,0.0],[0.33,1.0,0.0,0.0],[0.66,1.0,0.0,0.0], [1.0,1.0,0.0,0.0], [1.0,1.0,0.0,0.33], [1.0,1.0,0.0,0.66], [1.0,1.0,0.0,1.0]]
#folder_name = 'GC-parameters'
#run(theta, folder_name)
folder_name = 'Uni_param'
run(theta, folder_name)
'''

'''
theta = [[0.0,1.0,0.1,0.1],[0.2,1.0,0.1,0.1],[0.4,1.0,0.1,0.1], [0.6,1.0,0.1,0.1], [0.8,1.0,0.1,0.1], [1.0,1.0,0.1,0.1]]
folder_name = 'GC-parameters1'
run(theta, folder_name)
folder_name = 'Uni-parameters1'
run(theta, folder_name)

theta = [[1.0,0.0,0.1,0.1],[1.0,0.2, 0.1,0.1],[1.0,0.4,0.1,0.1], [1.0,0.6,0.1,0.1], [1.0,0.8,0.1,0.1], [1.0,1.0,0.1,0.1]]
folder_name = 'GC-parameters2'
run(theta, folder_name)
folder_name = 'Uni-parameters2'
run(theta, folder_name)
'''


# In[ ]:




