from __future__ import print_function
import pulp

solver_map = {
    'gurobi': pulp.GUROBI_CMD(msg=False)
}

#FIXME when adding constraints, use a map to match to your own id
class Math_prob:
    def __init__(self, var_ids):
        self.num_vars = 0
        self.num_cons_linear = 0
        self.num_cons_nonlinear = 0
        self.vars = dict()
        self.vid_dict = dict()
        self.cons_linear = dict()
        self.objective = dict()
        self.solutions = dict()
        
        for vid in var_ids:
            self.vid_dict[self.add_var()] = vid
            
    def add_var(self, lower=0, upper=1):
        self.vars[self.num_vars] = (lower, upper)
        self.num_vars += 1
        return self.num_vars - 1
        
    def get_vars(self):
        variables = [(var_id, self.vars[var_id][0], self.vars[var_id][1]) for var_id in self.vars]
        return variables
     
    def get_objective(self):
        objective = [(var_id, self.objective[var_id]) for var_id in self.objective]
        return objective
    
    def get_linear_cons(self):
        conss = [self.cons_linear[i] for i in self.cons_linear]
        return conss
    
    def get_solutions(self):
        return self.solutions
        
    def add_linear_constraint(self, var_indices, var_coefs, constant):
        self.cons_linear[self.num_cons_linear] = (var_indices, var_coefs, constant)
        self.num_cons_linear += 1
        return self.num_cons_linear - 1
    
    def add_to_objective(self, entity, weight):
        if not entity[0]:
            if entity[1] in self.objective:
                self.objective[entity[1]] += weight
            else:
                self.objective[entity[1]] = weight
    
    def print_cons_linear(self):
        for cons in self.cons_linear:
            print ('%d:\t' %(cons), end='')
            v, co, c = self.cons_linear[cons]
            for i in range(len(v)):
                if co[i] >= 0:
                    if i > 0:
                        print(' + ',end='')
                else:
                    print(' - ',end='')
                if abs(co[i]) != 1 :
                    print(abs(co[i]),end='') 
                print(' x_%d' %(v[i]),end='')
            if c != 0:
                if c > 0:
                    print(' + ',end='')
                else:
                    print(' - ',end='')
                print ('%f' %abs(c),end='')
            print(' <= 0')
            
    def print_objective(self):
        first = True
        for v in self.objective:
            c = self.objective[v]
            if not first:
                print (' + ',end='')
            else:
                first = False
            if c != 1:
                print('%.3f ' %c,end='')
            print('x_%d' %v,end='')
        print()
        
    def pulp_solve(self, solver_name):
        problem = pulp.LpProblem('PSL', pulp.LpMinimize)

        vs = self.get_vars()
        our_vars = dict()
        v = []
        for i in range(len(vs)):
            v.append(pulp.LpVariable('%d' %vs[i][0], vs[i][1], vs[i][2]))
            our_vars[vs[i][0]] = v[i]

        ob = self.get_objective()
        problem.objective = pulp.LpAffineExpression([(our_vars[ob[i][0]], ob[i][1]) for i in range(len(ob))])

        css = self.get_linear_cons()
        for i in range(len(css)):
            ids, coefs, cnst = css[i]
            c = pulp.LpConstraint(
                pulp.LpAffineExpression([(our_vars[ids[j]], coefs[j]) for j in range(len(coefs))], 
                                        constant=cnst)
                , sense=-1)
            problem.constraints[i] = c
        
        if solver_name:
            problem.solve(solver_map[solver_name])
        else:
            problem.solve()
    
        self.solutions.clear()
        for variable in problem.variables():
            vnum = int(variable.name)
            if vnum in self.vid_dict:
                vid = self.vid_dict[vnum]
                self.solutions[vid] = variable.varValue
        self.obj_val = pulp.value(problem.objective)

def calculate_ac_info(counts):
    n1 = 0
    n2 = 0
    a_const = 0
    a_vars = []
    c_const = 0
    c_vars = []
    for f1, f2, d in counts:
        if f1 == 1 and f2 == 1:
            n1 += 1
            if d[0]:
                a_const += d[1]
            else:
                a_vars.append(d[1])
        
        if f1 == 0 and f2 == 1:
            n2 += 1
            if d[0]:
                c_const += d[1]
            else:
                c_vars.append(d[1])
    
    return n1, n2, a_const, a_vars, c_const, c_vars

def add_RD_constraints(problem, delta, ac_info):
    n1, n2, a_const, a_vars, c_const, c_vars = ac_info
    var_ids = a_vars + c_vars
    
    coefs = [-n2] * len(a_vars) + [n1] * len(c_vars)
    const_part = - (n2 * a_const) + (n1 * c_const) - (n1 * n2 * delta)
    problem.add_linear_constraint(var_ids, coefs, const_part)

    coefs = [n2] * len(a_vars) + [-n1] * len(c_vars)
    const_part = (n2 * a_const) - (n1 * c_const) - (n1 * n2 * delta)
    problem.add_linear_constraint(var_ids, coefs, const_part)

def add_RR_constraints(problem, delta, ac_info):
    n1, n2, a_const, a_vars, c_const, c_vars = ac_info
    var_ids = a_vars + c_vars
    
    nd = (1+delta) * n1
    coefs = [-n2] * len(a_vars) + [nd] * len(c_vars)
    const_part = - (n2 * a_const) + (nd * c_const) - (n1 * n2 * delta)
    problem.add_linear_constraint(var_ids, coefs, const_part)
    
    nd = (1-delta) * n1
    coefs = [n2] * len(a_vars) + [-nd] * len(c_vars)
    const_part = (n2 * a_const) - (nd * c_const) - (n1 * n2 * delta)
    problem.add_linear_constraint(var_ids, coefs, const_part)

def add_RC_constraints(problem, delta, ac_info):
    n1, n2, a_const, a_vars, c_const, c_vars = ac_info
    var_ids = a_vars + c_vars
    
    nd = (1+delta) * n1    
    coefs = [n2] * len(a_vars) + [-nd] * len(c_vars)
    const_part = (n2 * a_const) - (nd * c_const)
    problem.add_linear_constraint(var_ids, coefs, const_part)

    nd = (1-delta) * n1
    coefs = [-n2] * len(a_vars) + [nd] * len(c_vars)
    const_part = -(n2 * a_const) + (nd * c_const)
    problem.add_linear_constraint(var_ids, coefs, const_part)


   
def psl_rule(problem, rule, signs, hard=False):
    body = rule[:-1]
    head = rule[-1]    
    body_neg_stat = signs[:-1]
    head_neg_stat = signs[-1] 
    

    var_ids = []
    coefs = []
    const_part = 1
    y = None
    
    if not hard:    
        y = problem.add_var()
        var_ids.append(y)
        coefs.append(-1)
    
    isconst, val = head
    if isconst:
        if head_neg_stat:
            const_part += (-1+val)
        else:
            const_part += -val
    else:
        var_ids.append(val)
        if head_neg_stat:
            const_part -= 1
            coefs.append(1)
        else:
            coefs.append(-1)

    if body:
        for i in range(len(body)):
            isconst, val = body[i]
            if isconst:
                if body_neg_stat[i]:
                    const_part -= val
                else:
                    const_part -= (1-val)
            else:
                if val in var_ids:
                    var_index = var_ids.index(val)
                else:
                    var_ids.append(val)
                    coefs.append(0)
                    var_index = len(var_ids)-1
                if body_neg_stat[i]:
                    coefs[var_index] -= 1
                else:
                    coefs[var_index] += 1
                    const_part -= 1
    problem.add_linear_constraint(var_ids, coefs, const_part)
    return (False,y)
    
def check_rule(rule, signs):
    if not False in [isconst for (isconst,_) in rule]: return False

    body = rule[:-1]
    head = rule[-1]    
    body_neg_stat = signs[:-1]
    head_neg_stat = signs[-1] 

    min_val = 0
    for i in range(len(body)):
        isconst, val = body[i]
        if isconst:
            if body_neg_stat[i]: val = 1-val
            min_val += 1-val

    isconst, val = head
    if isconst:
        if head_neg_stat: val = 1-val
        min_val += val

    return min_val < 1

def add_rule(rule, signs, weight, problem):
    if check_rule(rule, signs): 
        if weight:
            Dist = psl_rule(problem, rule, signs)
            problem.add_to_objective(Dist, weight)
        else:
            psl_rule(problem, rule, signs, True)

def create_problem(r_list):
    var_ids = set()
    for _, body, head in r_list:
        var_ids |= set([b[1] for b in body if not b[0]])
        var_ids |= set([h[1] for h in head if not h[0]])
        
    problem = Math_prob(var_ids)
    for weight, body, head in r_list:
        assert (len(head) == 1)
        rule = tuple([b[:-1] for b in body] + [h[:-1] for h in head])
        signs = tuple([b[-1] for b in body] + [h[-1] for h in head])
        add_rule(rule, signs, weight, problem)
    return problem

def map_inference(rules, hard_rules, solver=''):
    r_list = rules + hard_rules
    problem = create_problem(r_list)
    problem.pulp_solve(solver)
    return problem.solutions

constraint_func = {
    'RD': add_RD_constraints,
    'RR': add_RR_constraints,
    'RC': add_RC_constraints
    }

def fair_map_inference(rules, hard_rules, counts, delta, fairness_measure, solver=''):
    r_list = rules + hard_rules
    problem = create_problem(r_list)
    ac_info = calculate_ac_info(counts)
    add_fairness_constraints = constraint_func[fairness_measure]
    add_fairness_constraints(problem, delta, ac_info)
    problem.pulp_solve(solver)
    return problem.solutions
    
if __name__ == '__main__':
        exit(1)
