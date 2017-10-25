#!/usr/bin/env python3
# coding: utf-8

# authors
authors = []
with open('../reviewData/author.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        authors.append(line.split()[0])
# papers
papers = []
with open('../reviewData/paper.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        papers.append(line.split()[0])


var_id = 0

# PositiveReview
positive_review_rel = dict()
with open('../reviewData/positiveReview.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        [reviewer, paper, truth] = line.split()
        positive_review_rel[(reviewer, paper)] = (False, var_id)
        var_id += 1

# PositiveSummary
positive_summary_rel = dict()
with open('../reviewData/positiveSummary.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        [paper, truth] = line.split()
        positive_summary_rel[paper]= (True, float(truth))
        
# Acceptable
acceptable_rel = dict()
with open('../reviewData/acceptable.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        [paper, truth] = line.split()
        acceptable_rel[paper] = (False, var_id)
        var_id += 1

# Submits
submits_rel = dict()
with open('../reviewData/submits.txt') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        [author, paper, truth] = line.split()
        submits_rel[(author, paper)] = (True, float(truth))

# Presents
presents_rel = dict()
for a in authors:
    presents_rel[a] = (False, var_id)
    var_id += 1


rules = []
# 5: PositiveReview(R1, P) & PositiveReview(R2, P) & R1!=R2 -> PositiveSummary(P)
for p in papers:
    body = [positive_review_rel[('r0', p)] + (False,),
            positive_review_rel[('r1', p)] + (False,)]
    head = positive_summary_rel[p] + (False,)
    rules.append((5, body, head))


# 5: !PositiveReview(R1,P) & !PositiveReview(R2, P) & A1!=A2 -> !PositiveSummary(P)
for p in papers:
    body = [positive_review_rel[('r0', p)] + (True,),
            positive_review_rel[('r1', p)] + (True,)]
    head = positive_summary_rel[p] + (True,)
    rules.append((5, body, head))


# 5: Acceptable(P) & Reviews(R, P) -> PositiveReview(R, P)
for r, p in positive_review_rel:
    body = [acceptable_rel[p] + (False,), (True, 1.0, False)]
    head= positive_review_rel[(r, p)] + (False,)
    rules.append((5, body, head))

# 5: !Acceptable(P) & Reviews(R, P) -> !PositiveReview(R, P)
for r, p in positive_review_rel:
    body = [acceptable_rel[p] + (True,), (True, 1.0, False)]
    head= positive_review_rel[(r, p)] + (True,)
    rules.append((5, body, head))


# 1: !Acceptable(P)
for p in papers:
    body = []
    head = acceptable_rel[p] + (True,)
    rules.append((5, body, head))

# inf: Acceptable(P) & Submits(A, P) -> Presents(A)
for a, p in submits_rel:
    body = [acceptable_rel[p] + (False,), 
            (True, 1.0, False)]
    head = [presents_rel[a] + (False,)]
    rules.append((None, body, head))

