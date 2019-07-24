#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy

def compare_dicts(d1, d2):
    k1 = set(d1.keys())
    assert (k1 == set(d2.keys()))
    for k in k1:
        v0 = d1[k]
        v1 = d2[k]
        if not numpy.isclose(v0, v1):
            print(k, v0, v1)
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: %s [output1] [output2]'%sys.argv[0])
        exit(1)
        
    outdicts = [dict(), dict()]
    outfiles = sys.argv[1:]
    
    for i in (0, 1):
        with open(outfiles[i]) as f:
            for line in f:
                line = line.strip().split(',')
                outdicts[i][tuple(line[:-1])] = float(line[-1])
                
    compare_dicts(outdicts[0], outdicts[1])
    