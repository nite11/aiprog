import math

class Expr:
    def __add__(self, other):
        if isinstance(other, int):
            other = Con(other)

        if isinstance(other, str):
            other = Var(other)
            
        if isinstance(other, Expr):
            return Plus(self, other)

        print(f"Non-matching types for +: {type(self)} and {type(other)}")
        return None

    def __minus__(self, other):
        if isinstance(other, int):
            other = Con(other)

        if isinstance(other, str):
            other = Var(other)
            
        if isinstance(other, Expr):
            return Minus(self, other)

        print(f"Non-matching types for -: {type(self)} and {type(other)}")
        return None

    def __mul__(self, other):
        if isinstance(other, int):
            other = Con(other)

        if isinstance(other, str):
            other = Var(other)
            
        if isinstance(other, Expr):
            return Times(self, other)

        print(f"Non-matching types for *: {type(self)} and {type(other)}")
        return None

    def simplify(self):
        return self
    
class Con(Expr):
    def __init__(self, val : int):
        self.val = val

    def ev(self, env={}):
        return self.val

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        if isinstance(other, Con):
            return self.val == other.val

        return False

    def vars(self):
        return []

class Var(Expr):
    def __init__(self, name : str):
        self.name = name

    def ev(self, env={}):
        return env[self.name]

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.name == other.name

        return False

    def vars(self):
        return [self.name]

class BinOp(Expr):
    def __init__(self, left : Expr, right : Expr):
        self.left  = left
        self.right = right

    def ev(self, env={}):
        return self.op(self.left.ev(env), self.right.ev(env))

    def __str__(self):
        return f"({self.left} {self.name} {self.right})"

    def __eq__(self, other):
        if isinstance(other, BinOp) and self.name == other.name:
            return self.left == other.left and self.right == other.right

        return False

    def vars(self):
        return self.left.vars() + self.right.vars()

def simplify_and_evaluate(expr):
    simple = expr.simplify()
    if simple.vars() == []:
        return (simple, simple.ev())
    else:
        return (simple, None)
    
class Plus(BinOp):

    name = '+'
    
    def op(self, x, y):
        return x + y

    def simplify(self):
        (simple_left,  ev_l) = simplify_and_evaluate(self.left)
        (simple_right, ev_r) = simplify_and_evaluate(self.right)
        
        if ev_l != None and ev_r != None:
           return Con(ev_l + ev_r)
       
        if ev_l == 0:
            return simple_right
        if ev_r == 0:
            return simple_left
       
        return simple_left + simple_right

class Minus(BinOp):

    name = '-'
    
    def op(self, x, y):
        return x - y

    def simplify(self):
        (simple_left,  ev_l) = simplify_and_evaluate(self.left)
        (simple_right, ev_r) = simplify_and_evaluate(self.right)
        
        if ev_l != None and ev_r != None:
           return Con(ev_l - ev_r)
       
        if ev_l == 0:
            return Con(0) - simple_right
        if ev_r == 0:
            return simple_left
       
        return simple_left - simple_right
    
class Times(BinOp):

    name = '*'
    
    def op(self, x, y):
        return x * y

    def simplify(self):
        (simple_left,  ev_l) = simplify_and_evaluate(self.left)
        (simple_right, ev_r) = simplify_and_evaluate(self.right)
        
        if ev_l != None and ev_r != None:
           return Con(ev_l * ev_r)
       
        if ev_l == 0 or ev_r == 0:
            return Con(0)

        if ev_l == 1:
            return simple_right
        
        if ev_r == 1:
            return simple_left
       
        return simple_left * simple_right
    
    
e1 = Minus(Con(-7),Minus(Var('x'), Var('y')))
env = {'x' : 2, 'y' : -1,'z': 9}
print(e1)
print(e1.ev(env))