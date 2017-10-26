# -*- coding: utf-8 -*-
import cvxpy

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
        

    f_soft, constraints_soft = pslObjective(var_ids, vid_dict, rules) 
    if (len(hard_rules)>0):
        f_hard, constraints_hard = pslObjective(var_ids, vid_dict, hard_rules)
    else:
        f_hard = 0
        constraints_hard = []
        
    f=f_soft+f_hard
    constraints= constraints_soft+ constraints_hard
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve()

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results


def fairMapInference(rules, hard_rules, counts):
    vid_dict = dict()
    var_ids = set()
    
    allRules = rules+hard_rules
    for _, body, head in allRules:
        var_ids |= set([b[1] for b in body if not b[0]])
        var_ids |= set([h[1] for h in head if not h[0]])  
        

    f_soft, constraints_soft = pslObjective(var_ids, vid_dict, rules) 
    if (len(hard_rules)>0):
        f_hard, constraints_hard = pslObjective(var_ids, vid_dict, hard_rules)
    else:
        f_hard = 0
        constraints_hard = []
        
    f_fair, constraints_fair = fairObjective(var_ids, vid_dict, counts)
    
    f=f_soft+f_hard+f_fair
    constraints= constraints_soft+ constraints_hard + constraints_fair
    
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve()

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results


def fairObjective(var_ids, vid_dict, counts):
    pass

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
        if weight == None: 
            f += hardWeight * cvxpy.pos(expr)
        else:      
            # pos(x) is equivalent to max{x, 0}
            f += weight * cvxpy.pos(expr)
    return f, constraints



