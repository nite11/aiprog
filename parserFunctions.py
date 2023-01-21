import re
import string

#global d
d = dict.fromkeys(string.ascii_uppercase, '')
space=' '

def exprAlpha(expr):            #to convert an expression to an Alphabet
    #print(d)
    for key in d.keys():
        if d[key]=='':
            d[key]='[' + expr + ']'
            #print(d)
            return key

def unPack(key):    
    expr=d[key]
    expr=[x for x in expr]
    for i in range(len(expr)):
        if expr[i].isupper():
            expr[i]=unPack(expr[i])     

    return (''.join(expr))


def putBrackets(expr):
    expr=re.split('(\*|\+|\-)', expr)
    expr=[j for j in expr if j!= '']
    
    expr1=''
    #print(expr)
    i=len(expr)-1
    
    while expr.count('*')>0:
            expr=[j for j in expr if j!= '']
            #print(expr,i)
            i-=1        
            if expr[i]=='-' and expr[i-1]=='*':
                expr[i]=exprAlpha(f"{expr[i-2]}timesm{expr[i+1]}")
                expr[i-1]=''
                expr[i+1]=''
                expr[i-2]=''
                i-=2
            if expr[i]=='*':
                expr[i]=exprAlpha(f"{expr[i-1]}times{expr[i+1]}")
                expr[i-1]=''
                expr[i+1]=''
                i-=1

    for e in expr:
        expr1+=e 

    return exprAlpha(rightAss(expr1))

def resolveBrackets(expr,func):  ##x>5or(x<-5andy<0)
    position=matchBrackets(expr) 
    i=0
    #print(position,expr)
    while i < len(position):
        #print(position,len(position))
        expr=expr[0:position[i][0]] +\
                    func(expr[position[i][0]+1:position[i][1]]) +\
                    expr[position[i][1]+1:]
        
        position=matchBrackets(expr)
        #print(expr)
    ##print("success")    
    return expr

def makeConstraint(constraint):
    constraint=re.split('(or|and)', constraint)
    #print(constraint)
    
    i=0
    while constraint.count('and')>0:
        i+=1
        if constraint[i]=="and":
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

def rightAss(expr):
    expr=re.split('(\+|\-)', expr)
    expr=[j for j in expr if j!= '']
    #print(expr)
    if expr[0]=='-':
        expr[1]=f"[-{expr[1]}]"
        expr.pop(0)
    
    while len(expr)>1:
        expr[-3]=f"[{expr[-3]}{expr[-2]}{expr[-1]}]"
        expr.pop()
        expr.pop()

    return (''.join(expr))

def removeBrackets(expr):
    position=matchBrackets(expr) 
    #print(position,expr)
    for i in range(len(position)-1):

        if position[i+1][0]==position[i][0]-1 and position[i+1][1]==position[i][1]+1:
                expr = expr[:position[i+1][1]] + space + expr[position[i+1][1]+1:]
                expr = expr[:position[i+1][0]] + space + expr[position[i+1][0]+1:]
    if position[-1][0]==0 and position[-1][1]==len(expr)-1 and len(position)>1:
        return expr[2:-2]
    else:
        return expr[1:-1]

def matchBrackets(expr):
    position=[]
    openBr=[]
    #print(expr)
    for i in range(len(expr)):
        if expr[i]=='(':
            openBr.append(i)
        if expr[i]==')':
            position.append([openBr.pop(),i])  
    #print(position)
    return position


def format(expr):
    expr=resolveBrackets(expr,putBrackets)    
    #print(expr)
    expr=unPack(putBrackets(expr)).replace('timesm','*-').replace('times','*').replace('[','(').replace(']',')')
    expr=removeBrackets(expr).replace(space,'')    
    global d
    d = dict.fromkeys(string.ascii_uppercase, '')
    return expr

def formatEq(equationList):
    eqList=[]
    for eq in equationList:
        eq=eq.split('==')
        eqList.append(f"{format(eq[0])}=={format(eq[1])}")
        #print(eq)
    return eqList

def formatCon(constraintList):
    for k in range(len(constraintList)):
        constraintList[k]=resolveBrackets(constraintList[k],makeConstraint)
        constraintList[k]=makeConstraint(constraintList[k])
        constraintList[k]=constraintList[k].replace('[','(').replace(']',')')
    return constraintList


     
    

    


    



