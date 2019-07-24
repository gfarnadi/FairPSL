#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, shutil
import numpy 
import random
from random import shuffle


# In[ ]:


def saveFile(path, content):
    with open(path, 'a') as out:
        out.write(content + '\n')


# In[ ]:


def removeFolderContents(folderPath):
    for the_file in os.listdir(folderPath):
        file_path = os.path.join(folderPath, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


# In[ ]:


def generate_data():
    

