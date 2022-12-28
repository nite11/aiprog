from z3 import *
x1, x2 = Ints('x1 x2')


s = Solver()
s.add(Or(x1*x2==10 , Or(x1==6,x2==x1)))
numOfSol=0
while s.check()!=unsat and numOfSol<11:
    numOfSol+=1
    m=s.model()
    l=0
    cons=""
    print(m)    
    while l <len(m.decls()):
        cons+=f"{m[l]}!={m[m[l]]},"
        l+=1
    print(cons)
    s.add(eval(cons))
print(s.check())
print("Number of solutions found so far:",numOfSol)

