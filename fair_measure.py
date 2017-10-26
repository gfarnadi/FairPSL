import cvxpy

epsilon = 0.001
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
            '''TODO: This should be fixed and calculation of a and c should be based on max functions!'''
            #a+= cvxpy.pos(f1f2 + vid_dict[d[1]] -1)
            #c+= cvxpy.pos(f1nf2 + vid_dict[d[1]] -1)
            a+= f1f2 + vid_dict[d[1]] -1
            c+= f1nf2 + vid_dict[d[1]] -1
    return a,c,n1,n2

def riskDifference(counts,vid_dict):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return cvxpy.pos(((n2/(n1*n2)*a - n1/(n1*n2)*c)))+cvxpy.pos(-((n2/(n1*n2)*a - n1/(n1*n2)*c)))

def riskRatio(counts,vid_dict):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return cvxpy.pos(n2*a - (1+epsilon)*c*n1) + cvxpy.pos((1-epsilon)*c*n1 - n2*a)

def riskChance(counts,vid_dict):
    a,c,n1,n2 = calculate(counts,vid_dict)
    return cvxpy.pos(n1*n2-n2*a - (1+epsilon)*(n1*n2-n1*c)) + cvxpy.pos(((1-epsilon)*(n1*n2 - n1*c)+ n2*a - n1*n2))