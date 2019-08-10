#!/usr/bin/env python
# coding: utf-8

# In[29]:


def fairGrounding(dataPath, data_folder):
    ######################### Loading Data ######################### 
    ##Here (,) -> if the atom is observed => (True,) otherwise (False,)
    # employees --> Observed
    employees = []
    with open(dataPath+'employee.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0]) 
            
    # label --> Observed
    labels = dict()
    with open(dataPath+'label.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, label] = line.split()
            labels[employee] = label
            

    # Performance --> Observed
    performance_rel = dict()
    with open(dataPath+'performance.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            performance_rel[employee] = (True, float(truth))
            
    # Manager --> Observed
    manager_to_employee = dict()
    employee_to_manager = dict()
    with open(dataPath+'manager.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [supervisor, employee] = line.split()
            manager_to_employee.setdefault(supervisor,[]).append(employee)
            employee_to_manager.setdefault(employee,[]).append(supervisor)
           
    # Ingroup --> Observed
    ingroup = dict()
    with open(dataPath+'ingroup.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee1, employee2, truth] = line.split()
            ingroup[(employee1, employee2)] = float(truth)
            
            
    # Submitted opinion --> Observed
    submit_rel = dict()
    with open(dataPath+'submit.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            submit_rel[(provider, reciever)]= (True, float(truth))
    
    var_id = 0
  
    # opinion --> hidden
    opinion = dict()
    opinion_truth = dict()
    opinion_rel = dict()
    with open(dataPath+'opinion.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            opinion_truth[(provider, reciever)] = (var_id, truth)
            opinion_rel[(provider, reciever)] = (False, var_id)
            var_id += 1

    # True Quality --> hidden
    true_quality_truth = dict()
    true_quality_rel = dict()
    with open(dataPath+'quality.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            true_quality_truth[(employee)] = (var_id, truth)
            true_quality_rel[(employee)] = (False, var_id)
            var_id += 1
              
    # Promotion -> target (inference task)
    promotion_rel = dict()
    promotion_truth = dict()
    for e in employees:
        promotion_rel[e] = (False, var_id)
        var_id += 1

    with open(dataPath+'promotion.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            promotion_truth[employee] = float(truth)  
        
    ######################### Grounding the model #########################  
    ##Here (,) -> if the atom is negated => (True,) otherwise (False,)
    ##And (,,) -> the first one is weight of the rule, and the second is the body and the third is the head of the rule
    rules = []
    hardrules = []
    
    # 1: True_Quality(e) -> Performance(e)
    for e in employees:
        body = [true_quality_rel[e] + (False,)]
        head = [performance_rel[(e)] + (False,)]
        rules.append((1, body, head))

    # 1: ~True_Quality(e) -> ~Performance(e)
    for e in employees:
        body = [true_quality_rel[e] + (True,)]
        head = [performance_rel[(e)] + (True,)]
        rules.append((1, body, head))
                    
    # \infty: Submit(e1,e2) -> Opinion(e1,e2)                  
    for e1 in employees:
        for e2 in employees:
            if e1==e2: continue
            body = [submit_rel[(e1,e2)]+(False,)]
            head = [opinion_rel[(e1,e2)] + (False,)]
            hardrules.append((None, body, head))

                
    # \infty : ~Submit(e1,e2)-> ~Opinion(e1,e2)                  
    for e1 in employees:
        for e2 in employees:
            if e1==e2: continue
            body = [submit_rel[(e1,e2)]+(True,)]
            head = [opinion_rel[(e1,e2)] + (True,)]
            hardrules.append((None, body, head))
           
    # 1: Quality(e1)  & Employee(e1) & Employee(e2) -> Opinion(e1,e2) 
    for e1 in employees:
        for e2 in employees:
            if (e1==e2): continue
            body = [true_quality_rel[e1]+ (True,)] 
            head = [opinion_rel[(e1,e2)]+ (True,)]
            rules.append((1, body, head))
            
    # 1: ~Quality(e)  & Employee(m) & Employee(e) -> ~opinion(m,e) 
    for e1 in employees:
        for e2 in employees:
            if (e1==e2): continue
            body = [true_quality_rel[e1]+ (False,)] 
            head = [opinion_rel[(e1,e2)]+ (False,)]
            rules.append((1, body, head))                

    
    #1: Opinion(e1,e2) & Manager(m,e1) -> Opinion(m,e2)
    for m, emp in manager_to_employee.items():
        for e1 in emp:
            for e2 in employees:
                if e1==e2: continue
                body = [opinion_rel[e1,e2]+ (False,)] 
                head = [opinion_rel[(m,e2)]+ (False,)]
                rules.append((1, body, head))
                
    #1: ~Opinion(e1,e2) & Manager(m,e1) -> ~Opinion(m,e2)
    for m, emp in manager_to_employee.items():
        for e1 in emp:
            for e2 in employees:
                if e1==e2: continue
                body = [opinion_rel[e1,e2]+ (True,)] 
                head = [opinion_rel[(m,e2)]+ (True,)]
                rules.append((1, body, head))
                
    #1: opinion(m,e) & Manager(m,e) -> Quality(e) 
    for m, emp in manager_to_employee.items():
        for e in emp:
            body = [opinion_rel[(m,e)]+ (False,)] 
            head = [true_quality_rel[e]+ (False,)]
            rules.append((1, body, head))
    
    #1: ~opinion(m,e) & Manager(m,e) -> ~Quality(e) 
    for m, emp in manager_to_employee.items():
        for e in emp:
            body = [opinion_rel[(m,e)]+ (True,)] 
            head = [true_quality_rel[e]+ (True,)]
            rules.append((1, body, head))   
                
                
    #\infty: Quality(e) -> Promotion(e)
    for e in employees:
        body = [true_quality_rel(e)+ (False,)]
        head = [promotion_rel(e) + (False,)]
        hardrules.append((None, body, head))
            
    #\infty: ~Quality(e) -> ~Promotion(e)
    for e in employees:
        body = [true_quality_rel(e)+ (True,)]
        head = [promotion_rel(e) + (True,)]
        hardrules.append((None, body, head))
                
    # 1: !Promotion(P)                
    for e in employees:
        body = []
        head = [promotion_rel[e] + (True,)]
        rules.append((1, body, head))
    
    
    #atoms = dict(review=positive_review_rel,acceptable=acceptable_rel, presents=presents_rel)
    # F1: ingroup(e,m) F2:manager(m,e)
    # d: promotion(e)
    counts = []
    for e in employees:
        managers_e = employee_to_manager[e]
        for m in managers_e:
            F1 = ingroup[(m,e)]
            F2 = manager[(m,e)]
            d = promotion_rel[e]
            counts.append((F1, F2, d))  
    
    atoms = {}
    atoms['quality']   =  true_quality_truth
    atoms['promotion']   =  promotion_truth
    #atoms = dict(review=positive_review_rel,acceptable=acceptable_rel, presents=presents_rel)
    
    return rules, hard_rules, counts, atoms


# In[ ]:




