import parseSys

from z3 import *

numVar=0 ##number of variables
for i in range(len(parseSys.varList)):
    exec(f"{parseSys.varList[i]}=Int('{parseSys.varList[i]}')")
    numVar+=1



s = Solver()   
for eq in parseSys.equationList:
    s.add(eval(eq))

for con in parseSys.constraintList:
    if con!='':
        s.add(eval(con))


##s.add(x!=0)

numOfSol=0
while s.check()==sat and numOfSol<3:
    numOfSol+=1
    m=s.model()
    l=0
    cons=""
    print(m)    
    while l <numVar:
        cons+=f"{m[l]}!={m[m[l]]},"
        l+=1
    ##print(cons)
    s.add(eval(cons))
print(s.check())
print("Number of solutions found so far:",numOfSol)

