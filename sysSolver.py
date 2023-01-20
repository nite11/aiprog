import parseSys as ps
from z3 import *

def solve(filename):
    ps.getFile(filename)
    numVar=0 ##number of variables
    for i in range(len(ps.varList)):
        exec(f"{ps.varList[i]}=Int('{ps.varList[i]}')")
        numVar+=1

    s = Solver()   
    for eq in ps.equationList:
        s.add(eval(eq))

    for con in ps.constraintList:
        if con!='':
            s.add(eval(con))


    #s.add(t==7,u==7,x==1,z==0)
    if s.check()!=sat:
        print("The system has no solution.")

    numOfSol=0
    while s.check()==sat and numOfSol<1:
        numOfSol+=1
        m=s.model()
        d={}
        l=0
        cons=""
        #print(m)    
        while l <numVar:
            d.update({m[l]:m[m[l]]})
            cons+=f"{m[l]}!={m[m[l]]},"        
            l+=1
        ##print(cons)
        s.add(eval(cons))
        print(d)
    if s.check()==sat:
        print("The system has more than 1 solution.")
    else:
        print("The system has only 1 solution.")

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])

