#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join as ojoin
import numpy as np
import sys

def read_accept(path):
    outdict = dict()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            line = line.split()
            paper = line[0][1:-1]
            truth = float(line[1])
            outdict[paper] = truth
    return outdict
    
def read_present(path):
    outdict = dict()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            line = line.split()
            author = line[0][1:-1]
            truth = float(line[1])
            outdict[author] = truth
    return outdict

def read_review(path):
    outdict = dict()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            line = line.split()
            reviewer = line[0][1:-1]
            paper = line[1][1:-1]
            truth = float(line[2])
            outdict[(reviewer, paper)] = truth
    return outdict


def compare_dicts(d1, d2):
    if set(d1.keys()) != set(d2.keys()):
        print('different keys')
    for k in d1: 
        v1 = d1[k]
        v2 = d2[k]
        if not np.isclose(v1, v2):
            print(k, v1, v2)
            
def compare(cli_out, py_out):
    print('presents')
    cli_present = read_present(ojoin(cli_out, 'PRESENTS.txt'))
    py_present = read_present(ojoin(py_out, 'PRESENTS.txt'))
    compare_dicts(cli_present, py_present)

    print('acceptable')
    cli_accept = read_accept(ojoin(cli_out, 'ACCEPTABLE.txt'))
    py_accept = read_accept(ojoin(py_out, 'ACCEPTABLE.txt'))
    compare_dicts(cli_accept, py_accept)

    print('positiveReview')
    cli_rev = read_review(ojoin(cli_out, 'POSITIVEREVIEW.txt'))
    py_rev = read_review(ojoin(py_out, 'POSITIVEREVIEW.txt'))
    compare_dicts(cli_rev, py_rev)

if __name__ == '__main__':
    
    cvx_output = './output/fpsl_cvxpy'
    lp_output = './output/fpsl_pulp'
    compare(lp_output, cvx_output)
