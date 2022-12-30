import parseSys

from z3 import *

for i in range(len(parseSys.varList)):
    exec(f"{parseSys.varList[i]}=Int('{parseSys.varList[i]}')")


s = Solver()   
for eq in parseSys.equationList:
    s.add(eval(eq))

for con in parseSys.constraintList:
    s.add(eval(con))



numOfSol=0
while s.check()!=unsat and numOfSol<2:
    numOfSol+=1
    m=s.model()
    l=0
    cons=""
    print(m)    
    while l <len(m.decls()):
        cons+=f"{m[l]}!={m[m[l]]},"
        l+=1
    ##print(cons)
    s.add(eval(cons))
print(s.check())
print("Number of solutions found so far:",numOfSol)

