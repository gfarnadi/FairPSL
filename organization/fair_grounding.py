#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def fairGrounding(dataPath, data_folder):
    # employees
    employees = []
    with open(dataPath+'employee.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0])
            
    # label
    employees = []
    with open(dataPath+'employee.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0])
    

    var_id = 0
    
    # Feedback
    feedback = dict()
    with open(dataPath+data_folder+'feedback.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            feedback[(provider, reciever)] = (var_id,truth )
            var_id += 1
    
    # Submitted Feedback
    submitted_feedback = dict()
    with open(dataPath+data_folder+'submit.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [provider, reciever, truth] = line.split()
            submitted_feedback[(provider, reciever)]= (True, float(truth))
            
    # True Quality
    true_quality = dict()
    with open(dataPath+data_folder+'quality.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, truth] = line.split()
            true_quality[(employee)] = (True, float(truth))
            
    # Ingroup
    ingroup = dict()
    with open(dataPath+data_folder+'ingroup.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee1, employee2, truth] = line.split()
            ingroup[(employee1, employee2)] = (True, float(truth))
    
    # Performance
    performance = dict()
    for e in employees:
        performance[e] = (False, var_id)
        var_id += 1
    
    
    rules = []
    # 1: True_Quality(e) -> Performance(e)
    for e in employees:
        body = [true_quality[e] + (True,),
        head = [performance[(e)] + (True,)]
        rules.append((1, body, head))

    # 1: ~True_Quality(e) -> ~Performance(e)
    for e in employees:
        body = [true_quality[e] + (False,),
        head = [performance[(e)] + (False,)]
        rules.append((1, body, head))
                    
    # 1: True_Quality(e) -> Positive_feedback(m,e)                  
    for p in papers:
        for r1 in paper_to_reviwer[p]:
            for r2 in paper_to_reviwer[p]:
                body = [positive_summary_rel[p] + (True,),
                        positive_review_rel[(r1, p)] + (True,)]
                head = [positive_review_rel[(r2, p)] + (True,)]
                rules.append((1, body, head))

    # 1: ~True_Quality(e) -> ~Positive_feedback(m,e) 
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_summary_rel[p] + (False, )]
            head = [positive_review_rel[(r, p)] + (False,)]
            rules.append((1, body, head))

    # 1:              
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_summary_rel[p] + (True, )]
            head = [positive_review_rel[(r, p)] + (True,)]
            rules.append((1, body, head))
                    
    # 1: 
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_review_rel[(r, p)] + (False,)]
            head = [acceptable_rel[p] + (False,)]
            rules.append((1, body, head))

    # 1:    
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_review_rel[(r, p)] + (True,)]
            head = [acceptable_rel[p] + (True,)]
            rules.append((1, body, head))
        
    # 1: 
    for r in reviewer_to_paper:
        for p1 in reviewer_to_paper[r]:
            for p2 in reviewer_to_paper[r]:
                if p1 == p2: continue
                body = [positive_review_rel[(r, p1)] + (False,),
                        acceptable_rel[p1] + (False,),
                        acceptable_rel[p2] + (False,)]
                head = [positive_review_rel[(r, p2)] + (True,)]
                rules.append((1, body, head))
                
     

    # 1: 	!Promotion(P)                
    for e in employees:
        body = []
        head = [acceptable_rel[p] + (True,)]
        rules.append((1, body, head))
                
    hard_rules = []
    # Acceptable(P) & Submits(A, P) -> Presents(A)
    for a, p in submits_rel:
        body = [acceptable_rel[p] + (False,), 
                (True, 1.0, False)]
        head = [presents_rel[a] + (False,)]
        hard_rules.append((None, body, head))
        
    # !Acceptable(P) & Submits(A,P) -> !Presents(A)
    for a, p in submits_rel:
        body = [acceptable_rel[p] + (True,), 
                (True, 1.0, False)]
        head = [presents_rel[a] + (True,)]
        hard_rules.append((None, body, head))
    
    affiliation_dict = dict()
    with open(dataPath+'affiliation.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [author, institute, truth] = line.split()
            assert(float(truth)==1)
            affiliation_dict[author] = institute
            
    high_rank_rel = dict()
    with open(dataPath+'highRank.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [institute, truth] = line.split()
            high_rank_rel[institute] = float(truth)
            
    student_rel = dict()
    with open(dataPath+'student.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [author, truth] = line.split()
            student_rel[author] = float(truth)
            
    # F1: student(u) F2:Affiliation(v, u) & highRank(u)
    # d: presents(A)
    counts = []
    for a in authors:
        F1 = student_rel[a]
        F2 = high_rank_rel[affiliation_dict[a]]
        d = presents_rel[a]
        counts.append((F1, F2, d))  
    
    atoms = {}
    atoms['review']   =  positive_review_truth
    atoms['acceptable']   =  acceptable_truth
    #atoms = dict(review=positive_review_rel,acceptable=acceptable_rel, presents=presents_rel)
    
    return rules, hard_rules, counts, atoms

