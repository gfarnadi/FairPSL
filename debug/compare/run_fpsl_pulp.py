#!/usr/bin/env python

import os, sys
SCRIPTDIR = os.path.dirname(__file__)

ENGINDIR = os.path.join(SCRIPTDIR, '..', '..', 'engines')
sys.path.append(os.path.abspath(ENGINDIR))
from fpsl_pulp import solve_mip

PROBLEMDIR = os.path.join(SCRIPTDIR, '..', '..', 'problems', 'paper_review')
sys.path.append(os.path.abspath(PROBLEMDIR))
from grounding import ground

from os.path import join as ojoin


if __name__ == '__main__':
    data_path = ojoin(PROBLEMDIR, 'data', '1')
    rules, hard_rules, _, atoms = ground(data_path)
    all_rules = rules + hard_rules
    
    results = solve_mip(all_rules)
    out_path = ojoin('output', 'fpsl_pulp')
        
    reviews = atoms['review']
    with open(ojoin(out_path, 'POSITIVEREVIEW.txt'), 'w') as f:
        for (review, paper), (vid, _) in reviews.items():
            print("'%s'\t'%s'\t%f"%(review, paper, results[vid]), file=f)
        
    acceptable = atoms['acceptable']
    with open(ojoin(out_path, 'ACCEPTABLE.txt'), 'w') as f:
        for paper, (vid, _) in acceptable.items():
            print("'%s'\t%f"%(paper, results[vid]), file=f)

    presents = atoms['presents']
    with open(ojoin(out_path, 'PRESENTS.txt'), 'w') as f:
        for author, (vid, _) in presents.items():
            print("'%s'\t%f"%(author, results[vid]), file=f)            
