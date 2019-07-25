#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, shutil
import numpy 
import random
from random import shuffle


# In[2]:


def generate_qualification(user_dict, quality_file, quality_rate):
    quality_dict = {}
    with open(quality_file,'w') as qf:
        for user in user_dict.keys():
            if random.random()<(1-quality_rate):
                quality_dict[user] = 0
                print('%s\t0'%(user), file=qf)
            else:
                quality_dict[user] = 1
                print('%s\t1'%(user), file=qf)
    return quality_dict


# In[3]:


def read_user_data(user_file):
    user_dict = {}
    with open(user_file, "r") as uf:
        lines = uf.readlines()
        for line in lines:
            info = line.split('\t')
            user_dict[info[0]] = info[1]
    return user_dict


# In[4]:


def generate_data(user_file, quality_file, feedback_file, submission_rate_f, submission_rate_m, feedback_equal_p, feedback_equal_n, feedback_notequal_p, feedback_notequal_n, quality_rate):
    user_dict = read_user_data(user_file)
    quality_dict = generate_qualification(user_dict, quality_file, quality_rate)
    with open(feedback_file, "w") as ff:
        #user1: is feedback giver and user2: is feedback reciever
        for user1,label1 in user_dict.items():
            for user2, label2 in user_dict.items():
                if user1==user2:
                    pass
                else:
                    if label1=='f':
                        if random.random()<submission_rate_f:
                            if label1==label2:
                                if quality_dict[user2]==1:
                                    if random.random()<feedback_equal_p:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                                else:
                                    if random.random()<feedback_equal_n:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                            else:
                                if quality_dict[user2]==1:
                                    if random.random()<feedback_notequal_p:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                                else:
                                    if random.random()<feedback_notequal_n:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                    else:
                        if random.random()<submission_rate_m:
                            if label1==label2:
                                if quality_dict[user2]==1:
                                    if random.random()<feedback_equal_p:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                                else:
                                    if random.random()<feedback_equal_n:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                            else:
                                if quality_dict[user2]==1:
                                    if random.random()<feedback_notequal_p:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                                else:
                                    if random.random()<feedback_notequal_n:
                                        print('%s\t%s\t1'%(user1,user2), file =ff)
                                    else:
                                        print('%s\t%s\t0'%(user1,user2), file =ff)
                                


# In[5]:


user_file = './data/gender.txt'
quality_file = './data/1/quality.txt'
feedback_file='./data/1/feedback.txt'
feedback_equal_p = 0.9
feedback_equal_n = 0.05
feedback_notequal_p =0.5
feedback_notequal_n =0.01
submission_rate_f = 0.1
submission_rate_m = 0.3
quality_rate = 0.3
generate_data(user_file, quality_file, feedback_file, submission_rate_f, submission_rate_m, feedback_equal_p, feedback_equal_n, feedback_notequal_p, feedback_notequal_n, quality_rate)


# In[ ]:




