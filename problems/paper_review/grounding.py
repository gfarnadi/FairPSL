from os.path import join as ojoin

def ground(data_path):
    # authors
    authors = []
    author_fname = ojoin(data_path, 'author.txt')
    with open(author_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            authors.append(line.split()[0])
    # papers
    papers = []
    papers_fname = ojoin(data_path, 'paper.txt')
    with open(papers_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            papers.append(line.split()[0])

    var_id = 0
    
    # PositiveReview
    paper_to_reviwer = dict()
    reviewer_to_paper = dict()
    positive_review_rel = dict()
    positive_review_truth = dict()
    positive_review_fname = ojoin(data_path, 'positiveReview.txt')
    with open(positive_review_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [reviewer, paper, truth] = line.split()
            if paper in paper_to_reviwer:
                paper_to_reviwer[paper].append(reviewer)
            else:
                paper_to_reviwer[paper] = [reviewer]
            if reviewer in reviewer_to_paper:
                reviewer_to_paper[reviewer].append(paper)
            else:
                reviewer_to_paper[reviewer] = [paper]
            positive_review_rel[(reviewer, paper)] = (False, var_id)
            positive_review_truth[(reviewer, paper)] = (var_id, truth)
            var_id += 1
    
    # PositiveSummary
    positive_summary_rel = dict()
    positive_summary_fname = ojoin(data_path, 'positiveSummary.txt')
    with open(positive_summary_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [paper, truth] = line.split()
            positive_summary_rel[paper]= (True, float(truth))
            
    # Acceptable
    acceptable_rel = dict()
    acceptable_truth = dict()
    acceptable_fname = ojoin(data_path, 'acceptable.txt')
    with open(acceptable_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [paper, truth] = line.split()
            acceptable_rel[paper] = (False, var_id)
            acceptable_truth[paper] = (var_id, truth)
            var_id += 1
    
    # Submits
    submits_rel = dict()
    submits_fname = ojoin(data_path, 'submits.txt')
    with open(submits_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [author, paper, truth] = line.split()
            submits_rel[(author, paper)] = (True, float(truth))
    
    # Presents
    presents_rel = dict()
    presents_truth = dict()
    for a in authors:
        presents_rel[a] = (False, var_id)
        presents_truth[a] = (var_id, None)
        var_id += 1
    
    
    rules = []
    # 1: PositiveSummary(P) & Reviews(R1,P) & Reviews(R2,P) & 
    #     PositiveReview(R1,P) -> PositiveReview(R2,P)
    for p in papers:
        for r1 in paper_to_reviwer[p]:
            for r2 in paper_to_reviwer[p]:
                body = [positive_summary_rel[p] + (False,),
                        positive_review_rel[(r1, p)] + (False,)]
                head = [positive_review_rel[(r2, p)] + (False,)]
                rules.append((1, body, head))

    # 1: !PositiveSummary(P) & Reviews(R1,P) & Reviews(R2,P) & 
    #      PositiveReview(R1,P) -> !PositiveReview(R2,P)
    for p in papers:
        for r1 in paper_to_reviwer[p]:
            for r2 in paper_to_reviwer[p]:
                body = [positive_summary_rel[p] + (True,),
                        positive_review_rel[(r1, p)] + (False,)]
                head = [positive_review_rel[(r2, p)] + (True,)]
                rules.append((1, body, head))
                    
    # 1: !PositiveSummary(P) & Reviews(R1,P) & Reviews(R2,P) & 
    #      !PositiveReview(R1,P) -> !PositiveReview(R2,P)                
    for p in papers:
        for r1 in paper_to_reviwer[p]:
            for r2 in paper_to_reviwer[p]:
                body = [positive_summary_rel[p] + (True,),
                        positive_review_rel[(r1, p)] + (True,)]
                head = [positive_review_rel[(r2, p)] + (True,)]
                rules.append((1, body, head))

    # 1:  PositiveSummary(P) & Reviews(R,P) -> PositiveReview(R,P)  
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_summary_rel[p] + (False, )]
            head = [positive_review_rel[(r, p)] + (False,)]
            rules.append((1, body, head))

    # 1:  !PositiveSummary(P) & Reviews(R,P) -> !PositiveReview(R,P)            
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_summary_rel[p] + (True, )]
            head = [positive_review_rel[(r, p)] + (True,)]
            rules.append((1, body, head))
                    
    # 1: PositiveReview(R,P) & Reviews(R,P) -> Acceptable(P)
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_review_rel[(r, p)] + (False,)]
            head = [acceptable_rel[p] + (False,)]
            rules.append((1, body, head))

    # 1: !PositiveReview(R,P) & Reviews(R,P) -> !Acceptable(P)    
    for p in papers:
        for r in paper_to_reviwer[p]:                  
            body = [positive_review_rel[(r, p)] + (True,)]
            head = [acceptable_rel[p] + (True,)]
            rules.append((1, body, head))
        
    # 1:	Reviews(R,P1) & Reviews(R,P2) & PositiveReview(R,P1) & 
    #       Acceptable(P1) & Acceptable(P2) & (P1!=P2) -> !PositiveReview(R,P1)
    for r in reviewer_to_paper:
        for p1 in reviewer_to_paper[r]:
            for p2 in reviewer_to_paper[r]:
                if p1 == p2: continue
                body = [positive_review_rel[(r, p1)] + (False,),
                        acceptable_rel[p1] + (False,),
                        acceptable_rel[p2] + (False,)]
                head = [positive_review_rel[(r, p2)] + (True,)]
                rules.append((1, body, head))
                
    # 1:	Reviews(R,P1) & Reviews(R,P2) & !PositiveReview(R,P1) & 
    #       Acceptable(P1) & Acceptable(P2) & (P1!=P2) -> PositiveReview(R,P1)            
    for r in reviewer_to_paper:
        for p1 in reviewer_to_paper[r]:
            for p2 in reviewer_to_paper[r]:
                if p1 == p2: continue
                body = [positive_review_rel[(r, p1)] + (True,),
                        acceptable_rel[p1] + (False,),
                        acceptable_rel[p2] + (False,)]
                head = [positive_review_rel[(r, p2)] + (False,)]
                rules.append((1, body, head))    

    # 1: 	!Acceptable(P)                
    for p in papers:
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
    affiliation_fname = ojoin(data_path, 'affiliation.txt')
    with open(affiliation_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [author, institute, truth] = line.split()
            assert(float(truth)==1)
            affiliation_dict[author] = institute
            
    high_rank_rel = dict()
    high_rank_fname = ojoin(data_path, 'highRank.txt')
    with open(high_rank_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [institute, truth] = line.split()
            high_rank_rel[institute] = float(truth)
            
    student_rel = dict()
    student_fname = ojoin(data_path, 'student.txt')
    with open(student_fname) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [author, truth] = line.split()
            student_rel[author] = float(truth)
            
    # F1:Affiliation(v, u) & highRank(u)
    # F2: student(u) 
    # d: presents(A)
    counts = []
    for a in authors:
        F1 = high_rank_rel[affiliation_dict[a]]
        F2 = student_rel[a]
        d = presents_rel[a]
        counts.append((F1, F2, d))  
    
    atoms = {}
    atoms['review']   =  positive_review_truth
    atoms['acceptable']   =  acceptable_truth
    atoms['presents'] = presents_truth
    
    return rules, hard_rules, counts, atoms








