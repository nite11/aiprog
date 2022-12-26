from z3 import *
x = Int('x')
y = Int('y')

s = Solver()
s.add(4 * x == 20)
s.add(x * y == 40)
s.add(x<10)
print(s.check())

print(s.model())
##print_sol(s)