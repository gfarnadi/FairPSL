#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

def read_link_data(knows_fname, knows_target_fname, likes_fname, lived_fname):
    people = set()    
    interests = set()
    places = set()
            
    with open(knows_fname) as knows_file:
        for line in knows_file:
            line = line.strip()
            if not line: continue
            line = line.split('\t')
            people.add(line[0])
            people.add(line[1])
            
            
    with open(likes_fname) as likes_file:
        for line in likes_file:
            line = line.strip()
            if not line: continue
            line = line.split('\t')            
            people.add(line[0])
            interests.add(line[1])
            
    with open(lived_fname) as lived_file:
        for line in lived_file:
            line = line.strip()
            if not line: continue
            line = line.split('\t')
            people.add(line[0])            
            places.add(line[1])
            
            
    with open(knows_target_fname) as knows_file:
        for line in knows_file:
            line = line.strip()
            if not line: continue
            line = line.split('\t')
            people.add(line[0])
            people.add(line[1])
                
    return people, interests, places
    
def get_rules():

    (people, interests, places) = read_link_data('./data/knows_obs.txt',
                                                 './data/knows_targets.txt',
                                                 './data/likes_obs.txt',
                                                 './data/lived_obs.txt')
    grounded_rules = []                                        
    
    # 20:  Lived(P1,L) & Lived(P2,L) & P1!=P2   -> Knows(P1,P2)
    grounded_rules += ['20: Lived(%s,%s) & Lived(%s,%s) -> Knows(%s,%s)'%(A,C,B,C,A,B) 
                    for A in people
                    for B in people
                    for C in places
                    if A!=B]
    
    
    # 5:  Lived(P1,L1) & Lived(P2,L2) & P1!=P2 & L1!=L2  -> !Knows(P1,P2)
    grounded_rules += ['5: Lived(%s,%s) & Lived(%s,%s) -> ~Knows(%s,%s)'%(A,C,B,D,A,B) 
                    for A in people
                    for B in people
                    for C in places
                    for D in places
                    if A!=B
                    ]
    
    # 10:  Likes(P1,L) & Likes(P2,L) & P1!=P2  -> Knows(P1,P2)
    grounded_rules += ['10: Likes(%s,%s) & Likes(%s,%s) -> Knows(%s,%s)'%(A,C,B,C,A,B)
                    for A in people
                    for B in people
                    for C in interests
                    if A!=B
                    ]
    
    # 5:   Knows(P1,P2) & Knows(P2,P3) & P1!=P3 -> Knows(P1,P3)
    grounded_rules += ['5: Knows(%s,%s) & Knows(%s,%s) -> Knows(%s,%s)'%(A,B,B,C,A,C)
                    for A in people
                    for B in people
                    for C in people
                    if (A!=B and B!=C and A!=C)]
    
    
    # 10000: Knows(P1,P2) -> Knows(P2,P1)
    grounded_rules += ['10000: Knows(%s,%s) -> Knows(%s,%s)'%(A,B,B,A)
                    for A in people
                    for B in people
                    if A!=B]
    
    # 5:  !Knows(P1,P2)
    grounded_rules += ['5: ~Knows(%s,%s)'%(A,B)
                    for A in people
                    for B in people
                    if A!=B]
                        
    return grounded_rules

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s [output_file]'%(sys.argv[0]))
        exit(1)
    
    grounded_rules = get_rules()        
    with open(sys.argv[1], 'w') as f:
        for rule in grounded_rules:
            print(rule, file=f)
        
        
    