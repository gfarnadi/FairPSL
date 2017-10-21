#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from tiny_utils import read_link_data, write_link_mpe
from tiny_mip import solve_mip
#from tiny_cvx import solve_cvx

def main(outfilename):

    (knows_rel, likes_rel,
    lived_rel, people,
    interests, places) = read_link_data('../data/knows_obs.txt',
                                               '../data/knows_targets.txt',
                                               '../data/likes_obs.txt',
                                               '../data/lived_obs.txt')
                                               
    def get_list(weight, ground_rules, signs):
        l = []
        body_length = len(signs) - 1
        for ground_rule in ground_rules:
            body = [ground_rule[i] + (signs[i],) for i in range(body_length)]
            head = [ground_rule[-1] + (signs[-1],)]
            l.append((weight, body, head))
        return l
        
    r_list = []
    
    # 20:  Lived(P1,L) & Lived(P2,L) & P1!=P2   -> Knows(P1,P2)
    ground_rules = [(lived_rel[(A, C)],
                     lived_rel[(B, C)],
                     knows_rel[(A, B)])
                    for A in people
                    for B in people
                    for C in places
                    if A!=B]
    signs = [False, False, False]
    weight = 20.0
    r_list += get_list(weight, ground_rules, signs)
    
    # 5:  Lived(P1,L1) & Lived(P2,L2) & P1!=P2 & L1!=L2  -> !Knows(P1,P2)
    ground_rules = [(lived_rel[(A, C)],
                     lived_rel[(B, D)],
                     knows_rel[(A, B)])
                    for A in people
                    for B in people
                    for C in places
                    for D in places
                    if (A!=B and C!=D)
                    ]
    signs = [False, False, True]
    weight = 5.0
    r_list += get_list(weight, ground_rules, signs)
    
    # 10:  Likes(P1,L) & Likes(P2,L) & P1!=P2  -> Knows(P1,P2)
    ground_rules = [(likes_rel[(A, C)],
                     likes_rel[(B, C)],
                     knows_rel[(A, B)])
                    for A in people
                    for B in people
                    for C in interests
                    if A!=B
                    ]
    signs = [False, False, False]
    weight = 10.0
    r_list += get_list(weight, ground_rules, signs)
    
    # 5:   Knows(P1,P2) & Knows(P2,P3) & P1!=P3 -> Knows(P1,P3)
    ground_rules = [(knows_rel[(A, B)],
                     knows_rel[(B, C)],
                     knows_rel[(A, C)])
                    for A in people
                    for B in people
                    for C in people
                    if (A!=B and B!=C and A!=C)]
    
    signs = [False, False, False]
    weight = 5.0
    r_list += get_list(weight, ground_rules, signs)
    
    
    # 10000: Knows(P1,P2) -> Knows(P2,P1)
    ground_rules = [(knows_rel[(A, B)],
                     knows_rel[(B, A)])
                    for A in people
                    for B in people
                    if A!=B]
    
    signs = [False, False]
    weight = 10000.0
    r_list += get_list(weight, ground_rules, signs)
    
    # 5:  !Knows(P1,P2)
    ground_rules = [(knows_rel[(A, B)],)
                    for A in people
                    for B in people
                    if A!=B]
    
    signs = [True]
    weight = 5.0
    r_list += get_list(weight, ground_rules, signs)
    
    solutions = solve_mip(r_list)
    write_link_mpe(outfilename, people, knows_rel, solutions)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s [outfile]'%(sys.argv[0]))
        exit(1)
    main(sys.argv[1])
