from z3 import *
a, b = Reals('a b')
x1, x2 = Ints('x1 x2')
c = Int('c')
x = Real('x')
T = lambda x: x**2 + a*x + b

con_roots = ForAll(x, (T(x) == 0) == Or(x == x1, x == x2))
con_c = T(c) == 30
s = Solver()
s.add(con_roots)
s.add(con_c)
con_max = If(T(c-1) > T(c+1), T(c-1), T(c+1)) == 42
s.add(con_max)
def solve(s):
    if s.check() == sat:
        return s.model()
    else:
        print("OOPS!")
        return None
##print(s.check())
print(solve(s))
