from z3 import *
x, y,z = Ints('x y z')


s = Solver()
s.add(x + y + z == 10,x - z == 5)
s.add (Or(x>5,And(x<-5,y>0)))
s.add(z<0)
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

