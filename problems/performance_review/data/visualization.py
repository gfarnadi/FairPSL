#!/usr/bin/env python
# coding: utf-8

# In[30]:


import networkx as nx
import matplotlib.pyplot as plt


# In[27]:


def visualize_hierachy(edge_file, label_file):
    G= nx.read_edgelist(edge_file)
    labels = {}
    with open(label_file, 'r') as lf:
        lines = lf.readlines()
        for line in lines:
            info = line.split('\t')
            labels[info[0]] = info[1].strip()
    pos=nx.spring_layout(G)
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    #plt.axis('off')
    plt.savefig('../data/')
    plt.show()


# In[29]:


edge_file='../data/2/manager.txt'
label_file = '../data/2/label.txt'
visualize_hierachy(edge_file,label_file)


# In[32]:


all_score_1 = [0.723, 0.822, 0.812, 0.911, 0.931, 0.871, 0.742]
all_score_2 = [0.713, 0.812, 0.802, 0.911, 0.921, 0.881, 0.742]
protected_score_1 = [0.667, 0.778, 0.889, 0.778, 0.889, 0.667, 0.111]
protected_score_2 = [0.555, 0.778, 0.889, 0.913, 0.924, 0.667, 0.111]
unprotected_score_1 = [0.739, 0.826, 0.804, 0.924, 0.924, 0.891, 0.804]
unprotected_score_2 = [0.728, 0.815, 0.793, 0.889, 0.889, 0.902, 0.783]
dataset = ['#1', '#2','#3','#4','#5','#6','#7']


# In[44]:


plt.plot(dataset,all_score_1, linewidth=2.0, label='PSL')
plt.plot(dataset,all_score_2, linewidth=2.0,  color='r', label='FairPSL')
plt.ylabel('ROC')
plt.xlabel('Dataset')
plt.legend()
plt.show()


# In[45]:


plt.plot(dataset,protected_score_1, linewidth=2.0, label='PSL')
plt.plot(dataset,protected_score_2, linewidth=2.0,  color='r', label='FairPSL')
plt.ylabel('ROC')
plt.xlabel('Dataset')
plt.legend()
plt.show()


# In[46]:


plt.plot(dataset,unprotected_score_1, linewidth=2.0, label='PSL')
plt.plot(dataset,unprotected_score_2, linewidth=2.0,  color='r', label='FairPSL')
plt.ylabel('ROC')
plt.xlabel('Dataset')
plt.legend()
plt.show()


# In[58]:


plt.figure(figsize=(15,3))
plt.subplot(1,3,1)
plt.plot(dataset,all_score_1, "o-", linewidth=2.0, label='PSL')
plt.plot(dataset,all_score_2,  "o-", linewidth=2.0,  color='r', label='FairPSL')
plt.ylabel('ROC')
plt.xlabel('Dataset')
plt.legend()
plt.title('ALL')

plt.subplot(1,3,2)
plt.plot(dataset,protected_score_1,  "o-", linewidth=2.0, label='PSL')
plt.plot(dataset,protected_score_2,  "o-", linewidth=2.0,  color='r', label='FairPSL')
plt.ylabel('ROC')
plt.xlabel('Dataset')
plt.legend()
plt.title('Protected')


plt.subplot(1,3,3)
plt.plot(dataset,unprotected_score_1,  "o-", linewidth=2.0, label='PSL')
plt.plot(dataset,unprotected_score_2,  "o-", linewidth=2.0,  color='r', label='FairPSL')
plt.ylabel('ROC')
plt.xlabel('Dataset')
plt.legend()
plt.title('Unprotected')

plt.savefig("../data/roc.pdf", bbox_inches="tight")


# In[90]:


import numpy as np

labels = ['G1', 'G2', 'G3', 'G4', 'G5']
men_means = [20, 34, 30, 35, 27]
women_means = [25, 32, 34, 20, 25]

all_score_1 = [0.723, 0.822, 0.812, 0.911, 0.931, 0.871, 0.742]
all_score_2 = [0.713, 0.812, 0.802, 0.911, 0.921, 0.881, 0.742]
protected_score_1 = [0.667, 0.778, 0.889, 0.778, 0.889, 0.667, 0.111]
protected_score_2 = [0.555, 0.778, 0.889, 0.913, 0.924, 0.667, 0.111]
unprotected_score_1 = [0.739, 0.826, 0.804, 0.924, 0.924, 0.891, 0.804]
unprotected_score_2 = [0.728, 0.815, 0.793, 0.889, 0.889, 0.902, 0.783]
dataset = ['#1', '#2','#3','#4','#5','#6','#7']


x = np.arange(len(dataset))  # the label locations
width = 0.35  # the width of the bars



fig, (ax1,ax2,ax3) = plt.subplots(1,3)
fig.set_size_inches(15, 3)
rects1 = ax1.bar(x - width/2, all_score_1, width, label='PSL')
rects2 = ax1.bar(x + width/2, all_score_2, width, color='r', label='FairPSL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('AUC')
ax1.set_ylim([0.0,1])
ax1.set_title('All')
ax1.set_xticks(x)
ax1.set_xticklabels(dataset)
#ax1.legend()



rects1 = ax2.bar(x - width/2, protected_score_1, width, label='PSL')
rects2 = ax2.bar(x + width/2, protected_score_2, width, color='r', label='FairPSL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax2.set_ylabel('AUC')
ax2.set_ylim([0.0,1])
ax2.set_title('Protected')
ax2.set_xticks(x)
ax2.set_xticklabels(dataset)
#ax2.legend()

rects1 = ax3.bar(x - width/2, unprotected_score_1, width, label='PSL')
rects2 = ax3.bar(x + width/2, unprotected_score_2, width, color='r', label='FairPSL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax3.set_ylabel('AUC')
ax3.set_ylim([0.0,1])
ax3.set_title('Unprotected')
ax3.set_xticks(x)
ax3.set_xticklabels(dataset)
ax3.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.savefig("../data/roc.pdf", bbox_inches="tight")


# In[ ]:




