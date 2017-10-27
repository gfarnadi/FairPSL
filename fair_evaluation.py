
def calculate(counts,result):
    n1 = 0.0
    n2 = 0.0
    a = 0.0
    c = 0.0
    for f1,f2,d in counts:
        f1f2 = max(f1+f2-1,0)
        f1nf2 = max(f1-f2,0)
        n1 += f1f2
        n2 += f1nf2
        if d[0]:
            a+= max(f1f2 + d[1] -1,0)
            c+= max(f1nf2 + d[1] -1,0)
        else:
            if f1f2==1:
                a+= result[d[1]] 
            else:
                a+= 0
            if f1nf2==1:
                c+= f1nf2 + result[d[1]] -1
            else:
                c+=0
        
    p1 = (a/n1)
    p2 = (c/n2)
    return p1,p2

def evaluate(result, counts):
    p1,p2 = calculate(counts,result)
    RR = p1-p2
    RD = p1/p2
    RC = (1-p1)/(1-p2)
    return RR,RD,RC
    