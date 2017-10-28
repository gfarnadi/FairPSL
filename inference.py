# -*- coding: utf-8 -*-
import cvxpy
from fair_measure import riskDifferenceConstraints,riskRatioConstraints,riskChanceConstraints,riskDifferenceObjective,riskRatioObjective,riskChanceObjective
'''
 - *r_list* is a list of tuples (weight, body, head)
 - *body* and *head* are lists of tuples (is_constant, value/id, is_negated)
 - *is_constant* is a flag, True if the truth value is known, False otherwise
 - *value/id* equals the truth value if it is known, 
   and is the id of the corresponding variable otherwise
 - *is_negated* is a flag, True if the atom is negated in the rule, 
   False otherwise
'''

hardWeight = 10000


def mapInference(rules, hard_rules):
    
    vid_dict = dict()
    var_ids = set()
    
    allRules = rules+hard_rules
    for _, body, head in allRules:
        if (len(body)>0):
            var_ids |= set([b[1] for b in body if not b[0]])
        if (len(head)>0):
            var_ids |= set([h[1] for h in head if not h[0]])  
        

    f, bounds = pslObjective(var_ids, vid_dict, rules) 

    hard_constraints = []
    if len(hard_rules) > 0:
        hard_constraints = psl_hard_constraints(vid_dict, hard_rules)
        
    constraints = bounds + hard_constraints
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve()

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results


def fairMapInference(rules, hard_rules, counts,epsilon,fairMeasureCode):
    vid_dict = dict()
    var_ids = set()
    
    allRules = rules+hard_rules
    for _, body, head in allRules:
        var_ids |= set([b[1] for b in body if not b[0]])
        var_ids |= set([h[1] for h in head if not h[0]])  
        

    f, bounds = pslObjective(var_ids, vid_dict, rules) 
    hard_constraints = []
    if len(hard_rules) > 0:
        hard_constraints = psl_hard_constraints(vid_dict, hard_rules)
        
    fairness_constraints = fairConstraints(vid_dict, counts,epsilon,fairMeasureCode)
    
    constraints= bounds + hard_constraints + fairness_constraints
    
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve()

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results


def fairObjective(vid_dict, counts,epsilon,fairMeasureCode):
    if fairMeasureCode=='RD':
        return riskDifferenceObjective(counts,vid_dict,epsilon)
    elif fairMeasureCode=='RR':
        return riskRatioObjective(counts,vid_dict,epsilon)
    elif fairMeasureCode=='RC':
        return riskChanceObjective(counts,vid_dict,epsilon)   
    else:
        print('Error: fairMeasureCode is not correct, you need to choose between RD, RR and RC.')


def fairConstraints(vid_dict, counts,epsilon,fairMeasureCode):
    if fairMeasureCode=='RD':
        return riskDifferenceConstraints(counts,vid_dict,epsilon)
    elif fairMeasureCode=='RR':
        return riskRatioConstraints(counts,vid_dict,epsilon)
    elif fairMeasureCode=='RC':
        return riskChanceConstraints(counts,vid_dict,epsilon)    
    else:
        print('Error: fairMeasureCode is not correct, you need to choose between RD, RR and RC.') 

    
def pslObjective(var_ids, vid_dict, r_list):
    constraints = []
    
    for vid in var_ids:
        var = cvxpy.Variable()
        vid_dict[vid] = var
        constraints += [0 <= var, var <= 1]

    f = 0        
    for weight, body, head in r_list:
        expr = 1
        for b in body:
            if b[0]:
                y = b[1]
            else:
                y = vid_dict[b[1]]
            if b[2]:
                expr -= y
            else:
                expr -= (1-y)
        for h in head:
            if h[0]:
                y = h[1]
            else:
                y = vid_dict[h[1]]
            if h[2]:
                expr -= (1-y)
            else:
                expr -= y
        f += weight * cvxpy.pos(expr)
        
    return f, constraints


def psl_hard_constraints(vid_dict, r_list):
    constraints = []
    
    for _, body, head in r_list:
        expr = 1
        for b in body:
            if b[0]:
                y = b[1]
            else:
                y = vid_dict[b[1]]
            if b[2]:
                expr -= y
            else:
                expr -= (1-y)
        for h in head:
            if h[0]:
                y = h[1]
            else:
                y = vid_dict[h[1]]
            if h[2]:
                expr -= (1-y)
            else:
                expr -= y

        constraints.append(expr <= 0)
    return constraints
