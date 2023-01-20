from z3 import *

x, y, u, z = Ints('x y u z')



s = Solver()
s.add(x*x - z ==u)
s.add(x + u == 0)
s.add(y - 5*z == 3)
#s.add(y  == 3)

s.check()
print(s.model())
s.add(Or())
print(s.check())
print(s.model())



##print(s)

