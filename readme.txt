Nitesh Agrawal 22105578

To solve the system of equations, execute the following code.
The file that contains the system has to be in the same folder along with the modules solver.py and parserFunctions.py

>>> import solver
>>> sol=solver.solve("sys.txt") 


Task: Grammar of Systems 
(Grammar.txt)
I have used EBNF and used this website to test my grammar. 
https://mdkrajnak.github.io/ebnftest/
Some things about the grammar that I have used, (there were many variants online; I don't know which is the 
standard one):
{} means repeat 0 or more times
[] means optional (0 or 1 time) 
["-"] to account for negative factors
#'[0-9]+' Here I have used the regular expression to generate the terminals

factor  =  constant |  variable | ["-"]["("] {s} expr {s} [")"]
constant  = ["-"]#'[0-9]+'
variable  = ["-"]#'[a-z]+'



Task: Implement classes for representing the equations and constraints 
(symbolic.py)
I did not understand this task. As a result, I have not used these classes, the solver works without this module.
But I have removed the dead code, and introduced a subclass for subtraction. 
Implementing these classes would be the potential extension that could be made to my code, to make the code 
more generalized and easily reusable for other applications. Right now it is highly customized.

Task: Parsing and Using the Z3 Solver
(solver.py and parserFunctions.py)
I made my own parser. I have done a lot of testing. I believe it can handle complex equations.
I used the examples in test.txt file to test the parser. (test.txt)
For the constraint part the parser can understand a very long string of inequalities with a lot of parentheses pairs.
But it cannot handle very complex constraints such as 
-2 * -x + y*-y -z - u - 3*-v > 0
For example, it won't apply the right association rule when parsing this constraint.
It is possible to make the constraint parsing more robust by reusing the code that I wrote for equations, 
but I did not want to make my code more complex. Also, from the examples that I saw in the project description,
I am hoping that the constraints won't be too complex.

I have included comments in the code. This is how the parser works:
It removes all the spaces from the input file. Identifies and separates equations and constraints.
Then it searches for the parentheses, so that it can prioritize the processing of what is inside the parentheses.
This processing is different for equations and constraints. 
For each side of the equation, it finds the multiplications and consolidates the operands with the multiplication 
symbol in between into 1 factor. After this what is left is a string of factors with either + or - between them. 
Parentheses are placed in this string to make it align to the right. 
To make it Z3 compatible, I just replaced ‘=’ with ‘==’. 
Also a list of variables is extracted from the equations and converted to Z3 integer variables.

For constraints, the processing is simpler, as I am expecting only atomic inequalities or 
inequalities compounded with ‘and’ or ‘or’. So the parser processes these complex constraints 
by prioritizing ‘and’ over ‘or’. These are directly translated to the Z3 boolean format. 
For example, x>0 and y<0 is converted to And(x>0,y<0). These are then fed to the solver.