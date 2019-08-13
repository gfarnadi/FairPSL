#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, random
import queue


# In[2]:


def hierachy_generator(k, size):
    index = 0
    hierachy_dict = {}
    sub_ordinates_dict = {}
    employees = []
    root = 'e'+str(index)
    index+=1
    employees.append(root)
    hierachy_dict[root] = []
    sub_ordinates_dict[root] = []
    return_nodes = queue.Queue()
    return_nodes.put(root)
    while index<size:
        node = return_nodes.get()
        hierachy_dict, sub_ordinates_dict, employees, return_nodes, index = generate_sub_ordinates(hierachy_dict, sub_ordinates_dict, employees, node, return_nodes, k , index)
    return hierachy_dict, sub_ordinates_dict, employees, index


# In[3]:


def generate_sub_ordinates(hierachy_dict, sub_ordinates_dict, employees, node, return_nodes, k , index):
    while len(hierachy_dict[node])<k:
        node_new = 'e'+str(index)
        employees.append(node_new)
        index+=1
        return_nodes.put(node_new)
        hierachy_dict[node].append(node_new)
        hierachy_dict[node_new] = []
        sub_ordinates_dict[node_new] = [node]
        for m in sub_ordinates_dict[node]:
            if m in sub_ordinates_dict[node_new]:continue
            if m==node_new: continue
            sub_ordinates_dict[node_new].append(m)
    return hierachy_dict, sub_ordinates_dict, employees, return_nodes, index


# In[4]:


def generate_label(hierachy_dict, sub_ordinates_dict, employees, manager_file, label_file, employees_file, delta):
    junior_employees = []
    with open(manager_file, 'w') as mf:
        for e, ms in sub_ordinates_dict.items():
            for m in ms:
                print('%s\t%s'%(m,e), file=mf)
                
    for m,emp in hierachy_dict.items():
        if len(emp)==0:
            junior_employees.append(m)
    size_A = 0        
    with open(label_file, 'w') as lf:
        for e in junior_employees:
            if random.random()<delta:
                print('%s\tA'%(e), file=lf)
                size_A+=1
            else:
                print('%s\tB'%(e), file=lf)
        for e in employees:
            if e in junior_employees:continue
            print('%s\tB'%(e), file=lf)
    print(size_A)        
    with open(employees_file, 'w') as ef:
        for e in employees:
            print('%s\t1'%(e), file = ef)


# In[5]:


def run_generator(k, size, manager_file, label_file, employees_file, delta):
    hierachy_dict, sub_ordinates_dict, employees, index = hierachy_generator(k, size)
    print(len(employees))
    print(len(hierachy_dict.keys()))
    print(len(sub_ordinates_dict.keys()))
    generate_label(hierachy_dict, sub_ordinates_dict, employees, manager_file, label_file, employees_file, delta)


# In[6]:


k = 3
size = 200
manager_file = '../data/test/manager.txt'
label_file = '../data/test/label.txt'
employees_file = '../data/test/employee.txt'
delta = 0.8
run_generator(k, size, manager_file, label_file, employees_file, delta)


# In[ ]:




