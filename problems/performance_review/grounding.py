from os.path import join as ojoin

def ground(data_path):

    employees = []
    with open(ojoin(data_path, 'employee.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0]) 
            
    labels = dict()
    with open(ojoin(data_path, 'label.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, label] = line.split()
            labels[employee] = label
            
    performance_rel = dict()
    with open(ojoin(data_path, 'performance.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            performance_rel[employee] = (True, float(truth))
            
    manager_to_employee = dict()
    employee_to_manager = dict()
    manager = dict()
    with open(ojoin(data_path, 'manager.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [supervisor, employee] = line.split()
            manager_to_employee.setdefault(supervisor,[]).append(employee)
            employee_to_manager.setdefault(employee,[]).append(supervisor)
            manager[(supervisor, employee)] = 1
           
    ingroup = dict()
    with open(ojoin(data_path, 'ingroup.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee1, employee2, truth] = line.split()
            ingroup[(employee1, employee2)] = float(truth)
            
    submit_rel = dict()
    with open(ojoin(data_path, 'submit.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            submit_rel[(provider, reciever)]= (True, float(truth))
    
    var_id = 0
  
    opinion_truth = dict()
    opinion_rel = dict()
    with open(ojoin(data_path, 'opinion.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            opinion_truth[(provider, reciever)] = (var_id, truth)
            opinion_rel[(provider, reciever)] = (False, var_id)
            var_id += 1

    true_quality_truth = dict()
    true_quality_rel = dict()
    with open(ojoin(data_path, 'quality.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            true_quality_truth[employee] = (var_id, float(truth))
            true_quality_rel[employee] = (False, var_id)
            var_id += 1
              
    promotion_rel = dict()
    promotion_truth = dict()
    with open(ojoin(data_path, 'promotion.txt')) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            promotion_truth[employee] = (var_id, float(truth))  
            promotion_rel[employee] = (False, var_id)
            var_id += 1
        
    rules = []
    hard_rules = []
    
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
            if (e1,e2) in submit_rel.keys():
                body = [submit_rel[(e1,e2)]+(False,)]
                head = [opinion_rel[(e1,e2)] + (False,)]
                hard_rules.append((None, body, head))

                
    # \infty : ~Submit(e1,e2)-> ~Opinion(e1,e2)                  
    for e1 in employees:
        for e2 in employees:
            if e1==e2: continue
            if (e1,e2) in submit_rel.keys():
                body = [submit_rel[(e1,e2)]+(True,)]
                head = [opinion_rel[(e1,e2)] + (True,)]
                hard_rules.append((None, body, head))

    '''    
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
    '''
    
    #1: Opinion(m,e2) & Manager(m,e1) -> Opinion(e1,e2)
    for m, emp in manager_to_employee.items():
        for e1 in emp:
            for e2 in employees:
                if e1==e2 or m==e2: continue
                body = [opinion_rel[m,e2]+ (False,)] 
                head = [opinion_rel[(e1,e2)]+ (False,)]
                rules.append((1, body, head))
                
    #1: ~Opinion(m,e2) & Manager(m,e1) -> ~Opinion(e1,e2)
    for m, emp in manager_to_employee.items():
        for e1 in emp:
            for e2 in employees:
                if e1==e2 or m==e2: continue
                body = [opinion_rel[m,e2]+ (True,)] 
                head = [opinion_rel[(e1,e2)]+ (True,)]
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
        body = [true_quality_rel[e]+ (False,)]
        head = [promotion_rel[e] + (False,)]
        hard_rules.append((None, body, head))
            
    #\infty: ~Quality(e) -> ~Promotion(e)
    for e in employees:
        body = [true_quality_rel[e]+ (True,)]
        head = [promotion_rel[e] + (True,)]
        hard_rules.append((None, body, head))
                
    # 1: !Promotion(P)                
    for e in employees:
        body = []
        head = [promotion_rel[e] + (True,)]
        rules.append((1, body, head))
    
    
    # F1: ???
    # F2 = 1
    # d: promotion(e)
    counts = []
    for e in employees:
        F1 = 1
        if e in employee_to_manager.keys():
            managers_e = employee_to_manager[e]
            for m in managers_e:
                if ingroup[(m,e)] == 1:
                    F1 = 0
        d = promotion_rel[e]
        if e in manager_to_employee.keys():
            F2 = 0
        else:
            F2 = 1
        counts.append((F1, F2, d))  
    
    atoms = {}
    atoms['quality']   =  true_quality_truth
    atoms['promotion']   =  promotion_truth
    atoms['opinion']   =  opinion_truth

    return rules, hard_rules, counts, atoms
