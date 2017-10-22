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
def map_inference(r_list):
    var_ids = set()
    for _, body, head in r_list:
        var_ids |= set([b[1] for b in body if not b[0]])
        var_ids |= set([h[1] for h in head if not h[0]])
        
    constraints = []
    vid_dict = dict()
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

        # pos(x) is equivalent to max{x, 0}
        f += weight * cvxpy.pos(expr)
        
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve()
    
    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results
