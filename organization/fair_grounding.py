#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
    Performance = dict()
    with open(dataPath+'performance.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            Performance[employee2] = float(truth)  
            
    # Manager --> Observed
    manager = dict()
    with open(dataPath+'manager.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [supervisor, employee, truth] = line.split()
            submitted_feedback[(supervisor, employee)]= (True, float(truth))
    
       
    # Ingroup --> Observed
    ingroup = dict()
    with open(dataPath+'ingroup.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            ingroup[(employee1, employee2)] = (True, float(truth))
            
            
    # Submitted Feedback --> Observed
    submitted_feedback = dict()
    with open(dataPath+'submit.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            submitted_feedback[(provider, reciever)]= (True, float(truth))
    
     var_id = 0
  
    # Feedback --> hidden
    feedback = dict()
    feedback_truth = dict()
    feedback_rel = dict()
    with open(dataPath+'feedback.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            feedback_truth[(provider, reciever)] = (var_id, truth)
            feedback_rel[(provider, reciever)] = (false, var_id)
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
            true_quality_rel[(employee)] = (false, var_id)
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
        body = [true_quality_rel[e] + (False,),
        head = [performance[(e)] + (False,)]
        rules.append((1, body, head))

    # 1: ~True_Quality(e) -> ~Performance(e)
    for e in employees:
        body = [true_quality_rel[e] + (True,),
        head = [performance[(e)] + (True,)]
        rules.append((1, body, head))
                    
    # \infty: Submit(m,e) -> Feedback(m,e)                  
    for key,value in submitted_feedback.items():
        (m,e) = key
        body = [submitted_feedback[(m,e)]+(False,)]
        head = [feedback_rel[(m,e)] + (False,)]
        hardrules.append((None, body, head))
                
                
    # \infty : ~Submit(m,e) -> ~Feedback(m,e)                  
    for key,value in submitted_feedback.items():
        (m,e) = key
        body = [submitted_feedback[(m,e)]+ (True,)]
        head = [Feedback_rel[(m,e)] + (True,)]
        hardrules.append((None, body, head))
           
    # 1: Quality(e)  & Employee(m) & Employee(e) -> Feedback(m,e) 
    for e in employees:
        for m in employees:
            if (m==e): continue
            body = [true_quality_rel[e]]+ (True,)] 
            head = [feedback_rel[(m,e)]+ (True,)]
            rules.append((1, body, head))
            
    # 1: ~Quality(e)  & Employee(m) & Employee(e) -> ~Feedback(m,e) 
    for e in employees:
        for m in employees:
            if (m==e): continue
            body = [true_quality_rel[e]]+ (False,)] 
            head = [feedback_rel[(m,e)]+ (False,)]
            rules.append((1, body, head))                

    
    #1: Feedback(u,x) & Manager(v,u) -> Feedback(v,x)
    for key in manager.keys():
        (v,u) = key
        for x in employees:
            if ((x==u) or (x==v)):continue
            body = [feedback_rel[(v,u)]]+ (False,)] 
            head = [feedback_rel[(v,x)]+ (False,)]
            rules.append((1, body, head))
                
    #1: ~Feedback(u,x) & Manager(v,u) -> ~Feedback(v,x)  
    for key in manager.keys():
        (v,u) = key
        for x in employees:
            if ((x==u) or (x==v)):continue
            body = [feedback_rel[(v,u)]]+ (True,)] 
            head = [feedback_rel[(v,x)]+ (True,)]
            rules.append((1, body, head))
    
    #1: Feedback(m,e) & Manager(m,e) -> Quality(e) 
    for key in manager.keys():
        (m,e) = key
        body = [feedback_rel[(m,e)]]+ (False,)] 
        head = [true_quality_rel[e]+ (False,)]
        rules.append((1, body, head))
    
    #1: ~Feedback(m,e) & Manager(m,e) -> ~Quality(e) 
    for key in manager.keys():
        (m,e) = key
        body = [feedback_rel[(m,e)]]+ (True,)] 
        head = [true_quality_rel[e]+ (True,)]
        rules.append((1, body, head))    
                
    #\infty: Quality(e) -> Promotion(e)
    for e in employees:
        body = [true_quality_rel(e)]+ (False,)]
        head = [promotion_rel(e)] + (False,)]
        hardrules.append((None, body, head))
        

    #\infty: Quality(e) -> Promotion(e)
    for e in employees:
        body = [true_quality_rel(e)]+ (False,)]
        head = [promotion_rel(e)] + (False,)]
        hardrules.append((None, body, head))
            
    #\infty: ~Quality(e) -> ~Promotion(e)
    for e in employees:
        body = [true_quality_rel(e)]+ (True,)]
        head = [promotion_rel(e)] + (True,)]
        hardrules.append((None, body, head))
                
    # 1: 	!Promotion(P)                
    for e in employees:
        body = []
        head = [promotion_rel[e] + (True,)]
        rules.append((1, body, head))
 
    # F1: ingroup(u,v) F2:manager(u,v)
    # d: promotion(e)
    counts = []
    for key in manager.keys():
        (u,v) = key
        F1 = ingroup[(u,v)]
        F2 = manager[(u,v)]
        d = promotion_rel[v]
        counts.append((F1, F2, d))  
    
    #atoms = {}
    #atoms['review']   =  true_quality_truth
    #atoms['promotion']   =  promotion_truth
    #atoms = dict(review=positive_review_rel,acceptable=acceptable_rel, presents=presents_rel)
    
    return rules, hard_rules, counts, atoms










# In[ ]:




