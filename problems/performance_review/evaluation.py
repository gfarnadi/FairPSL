
def calculate(counts,result):
    n1 = 0.0
    n2 = 0.0
    a = 0.0
    c = 0.0
    for f1,f2,d in counts:
        f1f2 = max(f1+f2-1,0)
        nf1f2 = max(-f1+f2,0)
        n1 += f1f2
        n2 += nf1f2
        if d[0]:
            a+= max(f1f2 - d[1],0)
            c+= max(nf1f2 - d[1],0)
        else:
            if f1f2==1:
                a+= 1-result[d[1]] 
            else:
                a+= 0
            if nf1f2==1:
                c+= 1-result[d[1]]
            else:
                c+=0
    if (a==n1):
        p1=1
    else: 
        p1 = (a/n1)
    if (c==n2):
        p2 =1
    else:
        p2 = (c/n2)
    return p1,p2

def evaluate(result, counts, fairMeasureCode):
    p1,p2 = calculate(counts,result)
    if fairMeasureCode=='RR':
        RR = p1/p2
        return RR
    elif fairMeasureCode == 'RD':
        RD = p1-p2
        return RD
    elif fairMeasureCode =='RC':
        RC = (1-p1)/(1-p2)
        return RC
  
def accuracy(dataPath, result, atoms): 
    employees = []
    with open(dataPath+'employee.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0])
    vardic = atoms['promotion']
    score = 0.0
    for e in employees:
        var = vardic[e][0]
        if var in result:
            predict = float(result[var])
            truth = float(vardic[e][1])
            if round(predict, 1)>=0.5:
                if truth ==1.0:
                    score+=1.0
            else:
                if truth ==0.0:
                    score+=1.0
    score = (float(score) / float(len(employees)))
    return score


def accuracy_all(dataPath, result, atoms): 
    employees = []
    with open(dataPath+'employee.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0])
    labels = dict()
    with open(dataPath+'label.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            [employee, label] = line.split()
            labels[employee] = label
    vardic = atoms['promotion']
    score = 0.0
    score_A = 0.0
    score_B = 0.0
    size_A = 0.0
    size_B = 0.0
    for e in employees:
        if labels[e] =='A':
            size_A+=1
        else:
            size_B+=1
        var = vardic[e][0]
        if var in result:
            predict = float(result[var])
            truth = float(vardic[e][1])
            if round(predict, 1)>=0.5:
                if truth ==1.0:
                    score+=1.0
                    if labels[e] =='A':
                        score_A+=1
                    else:
                        score_B+=1   
            else:
                if truth ==0.0:
                    score+=1.0
                    if labels[e] =='A':
                        score_A+=1
                    else:
                        score_B+=1
                        
    score = (float(score) / float(len(employees)))
    score_A = (float(score_A) / float(size_A))
    score_B = (float(score_B) / float(size_B))
    return score, score_A, score_B

def accuracy_opinion(dataPath, result, atoms): 
    employees = []
    with open(dataPath+'employee.txt') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            employees.append(line.split()[0])
    vardic = atoms['opinion']
    score = 0.0
    for e1 in employees:
        for e2 in employees:
            if e1==e2: continue
            var = vardic[(e1,e2)][0]
            if var in result:
                predict = float(result[var])
                truth = float(vardic[(e1,e2)][1])
                if round(predict, 1)>=0.5:
                    if truth ==1.0:
                        score+=1.0
                else:
                    if truth ==0.0:
                        score+=1.0
    size = (float(len(employees))*float(len(employees)))- float(len(employees))
    score = (float(score) / size)
    return score

