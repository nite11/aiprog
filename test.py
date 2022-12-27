from z3 import *
x = Int('x')
y = Int('y')

s = Solver()
##s.add(4 * x == 20)
s.add(x * y == 10)
s.add(x<10)

for i in range(2):
    print(s.check())
    print(s.model())
    s.add(x!=s.model()[x])

while s.check()==sat:
    print(s.model())
    s.add(x!=s.model()[x])



