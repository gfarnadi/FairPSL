#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import print_function
import os, shutil
import numpy 
import random
from random import shuffle




def saveFile(path, content):
    with open(path, 'a') as out:
        out.write(content + '\n')





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



def generate_submission(user_file, ingroup_file, manager_file, quality_file, opinion_file, submit_file, promotion_file, submission_rate_A, submission_rate_B, opinion_equal_p, opinion_equal_mn, opinion_notequal_mp, opinion_notequal_mn, quality_rate):
    user_dict = read_user_data(user_file)
    generate_ingroup(user_dict, ingroup_file)
    quality_dict = generate_qualification(user_dict, quality_file, quality_rate)
    manager_dict = read_manager_data(manager_file)
    opinion_dict = generate_opinion(user_dict, quality_dict, manager_dict,opinion_equal_mp, opinion_equal_mn, opinion_notequal_mp, opinion_notequal_mn, opinion_equal_p, opinion_equal_n, opinion_notequal_p, opinion_notequal_n, opinion_file)
    with open(promotion_file, "w") as pf:
        with open(submit_file, "w") as sf:
            for key, opinion in opinion_dict.items():
                user1 = key[0]
                user2 = key[1]
                if user_dict[user1] =='A':
                    if random.random()<submission_rate_A:
                        print('%s\t%s\t%d'%(user1,user2,opinion), file =sf)
                        print('%s\t%s\t%d'%(user1,user2,opinion), file =pf)
                else:
                    if random.random()<submission_rate_B:
                        print('%s\t%s\t%d'%(user1,user2,opinion), file =sf)
                        print('%s\t%s\t%d'%(user1,user2,opinion), file =pf)
    return quality_dict



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



def generate_ingroup(user_dict, ingroup_file):
    with open(ingroup_file, 'w') as igf:
        for user1, label1 in user_dict.items():
            for user2, label2 in user_dict.items():
                if label1==label2:
                    print('%s\t%s\t%d'%(user1,user2,1), file =igf)
                else:
                    print('%s\t%s\t%d'%(user1,user2,0), file =igf)


# In[ ]:


'''
user_file = '../organization/data/1/label.txt'
quality_file = '../organization/data/1/quality.txt'
opinion_file='../organization/data/1/opinion.txt'
submit_file = '../organization/data/1/submit.txt'
promotion_file = '../organization/data/1/promotion.txt'
performance_file = '../organization/data/1/performance.txt'
manager_file='../organization/data/1/manager.txt'
ingroup_file = '../organization/data/1/ingroup.txt'
opinion_equal_mp = 0.9
opinion_equal_mn = 0.05
opinion_notequal_mp =0.6
opinion_notequal_mn =0.01
opinion_equal_p = 0.8
opinion_equal_n = 0.05
opinion_notequal_p =0.5
opinion_notequal_n =0.01
submission_rate_A = 0.1
submission_rate_B = 0.2
quality_rate = 0.3
performance_rate_p = 0.6
performance_rate_n = 0.1
quality_dict = generate_submission(user_file, ingroup_file, manager_file, quality_file, opinion_file, submit_file, promotion_file, submission_rate_A, submission_rate_B, opinion_equal_p, opinion_equal_mn, opinion_notequal_mp, opinion_notequal_mn, quality_rate)
generate_performance(quality_dict, performance_rate_p, performance_rate_n, performance_file)
'''

