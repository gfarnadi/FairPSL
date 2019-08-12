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

def mapInference(rules, hard_rules, solver='cvxopt'):
    
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
    problem.solve(solver=solver_map[solver])

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results

def fairMapInference(rules, hard_rules, counts,epsilon,fairMeasureCode, solver='cvxopt'):
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
    problem.solve(solver=solver_map[solver])

    results = dict()
    for vid in var_ids:
        results[vid] = vid_dict[vid].value
    return results

def calculate(counts,vid_dict):
    n1 = 0.0
    n2 = 0.0
    a = 0.0
    c = 0.0
    for f1,f2,d in counts:
        f1f2 = max(f1+f2-1, 0)
        f1nf2 = max(f1-f2, 0)
        n1 += f1f2
        n2 += f1nf2
        if d[0]:
            a += max(f1f2 - d[1], 0)
            c += max(f1nf2 - d[1], 0)
        else:
            if f1f2 == 1:
                a += 1 - vid_dict[d[1]] 
            if f1nf2 == 1:
                c += 1 - vid_dict[d[1]]

    return a,c,n1,n2

def riskDifferenceObjective(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return GAMMA * cvxpy.pos(((n2/(n1*n2)*a-n1/(n1*n2)*c)))+cvxpy.pos(-((n2/(n1*n2)*a-n1/(n1*n2)*c)))

def riskRatioObjective(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return GAMMA * cvxpy.pos(n2*a-(1+epsilon)*c*n1) + cvxpy.pos((1-epsilon)*c*n1-n2*a)

def riskChanceObjective(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return GAMMA * cvxpy.pos(n1*n2-n2*a - (1+epsilon)*(n1*n2-n1*c)) + cvxpy.pos(((1-epsilon)*(n1*n2 -n1*c)+ n2*a-n1*n2))

def riskDifferenceConstraints(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((n2*a - n1*c - n1*n2*epsilon) <= 0)
    constraints.append((n2*a - n1*c + n1*n2*epsilon) >= 0)
    return constraints

def riskRatioConstraints(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((n2*a - (1+epsilon)*n1*c) <= 0)
    constraints.append((n2*a - (1-epsilon)*n1*c) >= 0)
    return constraints
    
def riskChanceConstraints(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((-n2*a + (1+epsilon)*n1*c - epsilon*n1*n2) <= 0)
    constraints.append((-n2*a + (1-epsilon)*n1*c + epsilon*n1*n2) >= 0)
    return constraints

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
