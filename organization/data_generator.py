#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, shutil
import numpy 
import random
from random import shuffle
from __future__ import print_function


# In[2]:


def generate_qualification(user_dict, quality_file, quality_rate):
    quality_dict = {}
    with open(quality_file,"w") as qf:
        for user in user_dict.keys():
            if random.random()<quality_rate:
                quality_dict[user] = 1
                print('%s\t1'%(user),file=qf)
            else:
                quality_dict[user] = 0
                print('%s\t0'%(user),file=qf)
    return quality_dict


# In[3]:


def read_user_data(user_file):
    user_dict = {}
    with open(user_file, "r") as uf:
        lines = uf.readlines()
        for line in lines:
            info = line.split('\t')
            user_dict[info[0]] = info[1].strip()
    return user_dict


# In[4]:


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


# In[5]:


def generate_feedback(user_dict, quality_dict, manager_dict,feedback_equal_mp, feedback_equal_mn, feedback_notequal_mp, feedback_notequal_mn, feedback_equal_p, feedback_equal_n, feedback_notequal_p, feedback_notequal_n, feedback_file):
    feedback_dict = {}
    with open(feedback_file, 'w') as ff:
        for user1,label1 in user_dict.items():
                for user2, label2 in user_dict.items():
                    if user1==user2:
                        pass
                    else:
                        if user2 in manager_dict.keys():
                            if user1 in manager_dict[user2]:
                                if quality_dict[user2]==1:
                                    if label1==label2:
                                        if random.random()<feedback_equal_mp:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                                    else:
                                        if random.random()<feedback_notequal_mp:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                                else:
                                    if label1==label2:
                                        if random.random()<feedback_equal_mn:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                                    else:
                                        if random.random()<feedback_notequal_mn:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                            
                            else:     
                            
                                if quality_dict[user2]==1:
                                    if label1==label2:
                                        if random.random()<feedback_equal_p:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                                    else:
                                        if random.random()<feedback_notequal_p:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                                else:
                                    if label1==label2:
                                        if random.random()<feedback_equal_n:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
                                    else:
                                        if random.random()<feedback_notequal_n:
                                            print('%s\t%s\t1'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 1
                                        else:
                                            print('%s\t%s\t0'%(user1,user2), file =ff)
                                            feedback_dict[(user1,user2)] = 0
    return feedback_dict


# In[6]:


def generate_submission(user_file, ingroup_file, manager_file, quality_file, feedback_file, submit_file, submission_rate_A, submission_rate_B, feedback_equal_p, feedback_equal_mn, feedback_notequal_mp, feedback_notequal_mn, quality_rate):
    user_dict = read_user_data(user_file)
    generate_ingroup(user_dict, ingroup_file)
    quality_dict = generate_qualification(user_dict, quality_file, quality_rate)
    manager_dict = read_manager_data(manager_file)
    feedback_dict = generate_feedback(user_dict, quality_dict, manager_dict,feedback_equal_mp, feedback_equal_mn, feedback_notequal_mp, feedback_notequal_mn, feedback_equal_p, feedback_equal_n, feedback_notequal_p, feedback_notequal_n, feedback_file)
    with open(submit_file, "w") as sf:
        for feedback, opinion in feedback_dict.items():
            user1 = feedback[0]
            user2 = feedback[1]
            if user_dict[user1] =='A':
                if random.random()<submission_rate_A:
                    print('%s\t%s\t%d'%(user1,user2,opinion), file =sf)
            else:
                if random.random()<submission_rate_B:
                    print('%s\t%s\t%d'%(user1,user2,opinion), file =sf)
    return quality_dict


# In[7]:


def generate_performance(quality_dict, performance_rate_p, performance_rate_n, performance_file):
    with open(performance_file, 'w') as pf:
        for user,quality in quality_dict.items():
            if quality_dict[user]==1:
                if random.random()<performance_rate_p:
                    print('%s\t%d'%(user,1), file =pf)
                else:
                    print('%s\t%d'%(user,0), file =pf)
                    
            else:
                if random.random()<performance_rate_n:
                    print('%s\t%d'%(user,1), file =pf)
                else:
                    print('%s\t%d'%(user,0), file =pf)
                    
                


# In[8]:


def generate_ingroup(user_dict, ingroup_file):
    with open(ingroup_file, 'w') as igf:
        for user1, label1 in user_dict.items():
            for user2, label2 in user_dict.items():
                if label1==label2:
                    print('%s\t%s\t%d'%(user1,user2,1), file =igf)
                else:
                    print('%s\t%s\t%d'%(user1,user2,0), file =igf)


# In[9]:


user_file = './data/gender.txt'
quality_file = './data/1/quality.txt'
feedback_file='./data/1/feedback.txt'
submit_file = './data/1/submit.txt'
performance_file = './data/1/performance.txt'
manager_file='./data/manager.txt'
ingroup_file = './data/1/ingroup.txt'
feedback_equal_mp = 0.9
feedback_equal_mn = 0.05
feedback_notequal_mp =0.6
feedback_notequal_mn =0.01
feedback_equal_p = 0.8
feedback_equal_n = 0.05
feedback_notequal_p =0.5
feedback_notequal_n =0.01
submission_rate_A = 0.1
submission_rate_B = 0.2
quality_rate = 0.3
performance_rate_p = 0.6
performance_rate_n = 0.1
quality_dict = generate_submission(user_file, ingroup_file, manager_file, quality_file, feedback_file, submit_file, submission_rate_A, submission_rate_B, feedback_equal_p, feedback_equal_mn, feedback_notequal_mp, feedback_notequal_mn, quality_rate)
generate_performance(quality_dict, performance_rate_p, performance_rate_n, performance_file)


# In[ ]:




