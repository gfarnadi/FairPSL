#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../..')
from fair_grounding import fairGrounding
from inference import mapInference
from os.path import join as ojoin

def run_model(data_path, out_path):
    rules, hard_rules, counts, atoms = fairGrounding(data_path)
    results = mapInference(rules, hard_rules)
    
    reviews = atoms['review']
    with open(ojoin(out_path, 'POSITIVEREVIEW.txt'), 'w') as f:
        for (review, paper), (_, vid) in reviews.items():
            print("'%s'\t'%s'\t%f"%(review, paper, results[vid]), file=f)
        
    acceptable = atoms['acceptable']
    with open(ojoin(out_path, 'ACCEPTABLE.txt'), 'w') as f:
        for paper, (_, vid) in acceptable.items():
            print("'%s'\t%f"%(paper, results[vid]), file=f)
        
    presents = atoms['presents']
    with open(ojoin(out_path, 'PRESENTS.txt'), 'w') as f:
        for author, (_, vid) in presents.items():
            print("'%s'\t%f"%(author, results[vid]), file=f)

if __name__ == '__main__':
    run_model('../reviewData/', './pypsl_output')
