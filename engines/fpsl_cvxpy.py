import cvxpy

GAMMA = 100
solver_map = {
    'cvxopt': cvxpy.CVXOPT,
    'gurobi': cvxpy.GUROBI
}

'''
 - *r_list* is a list of tuples (weight, body, head)
 - *body* and *head* are lists of tuples (is_constant, value/id, is_negated)
 - *is_constant* is a flag, True if the truth value is known, False otherwise
 - *value/id* equals the truth value if it is known, 
   and is the id of the corresponding variable otherwise
 - *is_negated* is a flag, True if the atom is negated in the rule, 
   False otherwise
'''

def map_inference(rules, hard_rules, solver='cvxopt'):
    
    vid_dict = dict()
    var_ids = set()
    
    all_rules = rules + hard_rules
    for _, body, head in all_rules:
        if (len(body)>0):
            var_ids |= set([b[1] for b in body if not b[0]])
        if (len(head)>0):
            var_ids |= set([h[1] for h in head if not h[0]])  
        

    f, bounds = psl_objective(var_ids, vid_dict, rules) 

    hard_constraints = []
    if len(hard_rules) > 0:
        hard_constraints = psl_hard_constraints(vid_dict, hard_rules)
        
    constraints = bounds + hard_constraints
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve(solver=solver_map[solver])


    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results

def fair_map_inference(rules, hard_rules, counts, delta, fairness_measure, solver='cvxopt'):
    assert(fairness_measure in ('RD', 'RR', 'RC'))
    vid_dict = dict()
    var_ids = set()
    
    all_rules = rules + hard_rules
    for _, body, head in all_rules:
        var_ids |= set([b[1] for b in body if not b[0]])
        var_ids |= set([h[1] for h in head if not h[0]])  
        

    f, bounds = psl_objective(var_ids, vid_dict, rules) 
    hard_constraints = []
    if len(hard_rules) > 0:
        hard_constraints = psl_hard_constraints(vid_dict, hard_rules)
        
    fairness_constraints = psl_fairness_constraints(vid_dict, counts, delta, fairness_measure)
    
    constraints= bounds + hard_constraints + fairness_constraints
    objective = cvxpy.Minimize(f)
    problem = cvxpy.Problem(objective, constraints)
    problem.solve(solver=solver_map[solver])

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results

def calculate(counts, vid_dict):
    n1 = 0.0
    n2 = 0.0
    a = 0.0
    c = 0.0
    for f1, f2, d in counts:
        f1f2 = max(f1+f2-1, 0)
        nf1f2 = max(-f1+f2, 0)
        n1 += f1f2
        n2 += nf1f2
        if d[0]:
            a += max(f1f2 - d[1], 0)
            c += max(nf1f2 - d[1], 0)
        else:
            if f1f2 == 1:
                a += 1 - vid_dict[d[1]] 
            if nf1f2 == 1:
                c += 1 - vid_dict[d[1]]

    return a,c,n1,n2

def psl_fairness_constraints(vid_dict, counts, delta, fairness_measure):
    if fairness_measure=='RD':
        return risk_difference_constraints(counts,vid_dict,delta)
    elif fairness_measure=='RR':
        return risk_ratio_constraints(counts,vid_dict,delta)
    elif fairness_measure=='RC':
        return risk_chance_constraints(counts,vid_dict,delta) 

def risk_difference_constraints(counts,vid_dict,delta):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((n2*a - n1*c - n1*n2*delta) <= 0)
    constraints.append((n2*a - n1*c + n1*n2*delta) >= 0)
    return constraints

def risk_ratio_constraints(counts,vid_dict,delta):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((n2*a - (1+delta)*n1*c) <= 0)
    constraints.append((n2*a - (1-delta)*n1*c) >= 0)
    return constraints
    
def risk_chance_constraints(counts,vid_dict,delta):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((-n2*a + (1+delta)*n1*c - delta*n1*n2) <= 0)
    constraints.append((-n2*a + (1-delta)*n1*c + delta*n1*n2) >= 0)
    return constraints
   
    
def psl_objective(var_ids, vid_dict, r_list):
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
