import re
import string

d = dict.fromkeys(string.ascii_uppercase, '')   #declare a dictionary with capital letters as keys
space=' '

def exprAlpha(expr):            #to convert a factor into an uppercase alphabet, and store in the dictionary
    for key in d.keys():
        if d[key]=='':
            d[key]='[' + expr + ']'
            return key

def unPack(key):        #to retrieve the factor from the dictionary
    expr=d[key]
    expr=[x for x in expr]
    for i in range(len(expr)):
        if expr[i].isupper():
            expr[i]=unPack(expr[i])     

    return (''.join(expr))


def putBrackets(expr):          #to prioritize * over + and -, the operands and the * are made into a factor 
    expr=re.split('(\*|\+|\-)', expr)
    expr=[j for j in expr if j!= '']
    i=len(expr)-1           #starting with the end for right association
    
    while expr.count('*')>0:
            expr=[j for j in expr if j!= '']
            i-=1        
            if expr[i]=='-' and expr[i-1]=='*':
                expr[i]=exprAlpha(f"{expr[i-2]}timesm{expr[i+1]}")  #example, 2*-x becomes 2timesmx
                expr[i-1]=''
                expr[i+1]=''
                expr[i-2]=''
                i-=2
            if expr[i]=='*':
                expr[i]=exprAlpha(f"{expr[i-1]}times{expr[i+1]}")   #example, 2*x becomes 2timesx
                expr[i-1]=''
                expr[i+1]=''
                i-=1

    return exprAlpha(rightAss(''.join(expr)))

def resolveBrackets(expr,func):     #to prioritize parentheses over anything else, func argument determines 
                                    #whether the processing has to be done for equations or constraints
    position=matchBrackets(expr)    #generates a list of pairs of positions of matching parentheses
    while 0 < len(position):        
        expr=expr[0:position[0][0]] +\
                    func(expr[position[0][0]+1:position[0][1]]) +\
                    expr[position[0][1]+1:]
        position=matchBrackets(expr) #the processing of expr in the previous step removes the pair of parentheses
            
    return expr

def makeConstraint(constraint):     #to make and-or constraints in the Z3 boolean format
    constraint=re.split('(or|and)', constraint)
    i=0
    while constraint.count('and')>0:    # and is prioritized over or
        i+=1
        if constraint[i]=="and":        #square brackets are used so that they do not interfere with parentheses
                constraint[i-1]=f"And[{constraint[i-1]},{constraint[i+1]}]"      
                constraint.pop(i)
                constraint.pop(i)
                i-=1

    i=0
    while constraint.count('or')>0:
        i+=1
        if constraint[i]=="or":
                constraint[i-1]=f"Or[{constraint[i-1]},{constraint[i+1]}]"
                constraint.pop(i)
                constraint.pop(i)
                i-=1

    return constraint[0]

def rightAss(expr):     #to right associate the equations
    expr=re.split('(\+|\-)', expr)
    expr=[j for j in expr if j!= '']
    if expr[0]=='-':            #hanging '-' is linked to the following factor to make a negative factor using []  
        expr[1]=f"[-{expr[1]}]"
        expr.pop(0)
    
    while len(expr)>1:
        expr[-3]=f"[{expr[-3]}{expr[-2]}{expr[-1]}]"
        expr.pop()
        expr.pop()

    return (''.join(expr))

def removeBrackets(expr):   #to remove excess parentheses
    position=matchBrackets(expr) 
    for i in range(len(position)-1):
        if position[i+1][0]==position[i][0]-1 and position[i+1][1]==position[i][1]+1:
                expr = expr[:position[i+1][1]] + space + expr[position[i+1][1]+1:]
                expr = expr[:position[i+1][0]] + space + expr[position[i+1][0]+1:]
    if position[-1][0]==0 and position[-1][1]==len(expr)-1 and len(position)>1:
        return expr[2:-2]
    else:
        return expr[1:-1]

def matchBrackets(expr):    #creates a list of pairs of positions of matching parentheses
    position=[]
    openBr=[]
    for i in range(len(expr)):
        if expr[i]=='(':
            openBr.append(i)
        if expr[i]==')':
            position.append([openBr.pop(),i])  #captures the inside-most parentheses pair first
    
    return position


def format(expr):
    expr=resolveBrackets(expr,putBrackets)    
    expr=unPack(putBrackets(expr)).replace('timesm','*-').replace('times','*').replace('[','(').replace(']',')')
    expr=removeBrackets(expr).replace(space,'')    
    global d
    d = dict.fromkeys(string.ascii_uppercase, '')
    return expr

def formatEq(equationList):
    eqList=[]
    for eq in equationList:
        eq=eq.split('==')
        eqList.append(f"{format(eq[0])}=={format(eq[1])}") #to format both sides of the equation
        
    return eqList

def formatCon(constraintList):
    for k in range(len(constraintList)):
        constraintList[k]=resolveBrackets(constraintList[k],makeConstraint)
        constraintList[k]=makeConstraint(constraintList[k])
        constraintList[k]=constraintList[k].replace('[','(').replace(']',')')
    return constraintList