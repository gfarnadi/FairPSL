import cvxpy

gamma = 100


def calculate(counts,vid_dict):
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
                a+= vid_dict[d[1]] 
            else:
                a+= 0
            if f1nf2==1:
                c+= f1nf2 + vid_dict[d[1]] -1
            else:
                c+=0
    return a,c,n1,n2

def riskDifferenceObjective(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return gamma* cvxpy.pos(((n2/(n1*n2)*a-n1/(n1*n2)*c)))+cvxpy.pos(-((n2/(n1*n2)*a-n1/(n1*n2)*c)))

def riskRatioObjective(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return gamma* cvxpy.pos(n2*a-(1+epsilon)*c*n1) + cvxpy.pos((1-epsilon)*c*n1-n2*a)

def riskChanceObjective(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return gamma* cvxpy.pos(n1*n2-n2*a - (1+epsilon)*(n1*n2-n1*c)) + cvxpy.pos(((1-epsilon)*(n1*n2 -n1*c)+ n2*a-n1*n2))



def riskDifferenceConstraints(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append(((n2/(n1*n2)*a - n1/(n1*n2)*c))>0)
    constraints.append(((n2/(n1*n2)*a - n1/(n1*n2)*c))<0)
    return constraints



def riskRatioConstraints(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((1-epsilon)*(n1*c)- n2*a>0)
    constraints.append((1+epsilon)*(n1*c)- n2*a <0)
    return constraints
    
    
    
def riskChanceConstraints(counts,vid_dict,epsilon):
    a,c,n1,n2 = calculate(counts,vid_dict)
    constraints = []
    constraints.append((1+epsilon)*(n1*n2-n1*c)-(n1*n2-n2*a)>0)
    constraints.append((1-epsilon)*(n1*n2-n1*c)-(n1*n2-n2*a)<0)
    return constraints
    
    
    
    
    





