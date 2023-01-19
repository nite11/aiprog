import re
import string

#global d
d = dict.fromkeys(string.ascii_uppercase, '')
#print(d)

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

def resolveBrackets(expr):  ##x>5or(x<-5andy<0)
    position=[]   ##to capture the position of  parenthesis
    for j in range(len(expr)):
        if expr[j]==')' or expr[j]=='(':
            position.append([j,expr[j]])
        
    ##print(position)
    i=1
    while(len(position)>0):    
        position=[]   ##to capture the position of  parenthesis
        for j in range(len(expr)):
            if expr[j]==')' or expr[j]=='(':
                position.append([j,expr[j]])    
        ##print(i)
        ##print(position)
        if position[i][1]==')':
            ##print(constraint[position[i-1][0]+1:position[i][0]])
            expr=expr[0:position[i-1][0]] +\
                    putBrackets(expr[position[i-1][0]+1:position[i][0]]) +\
                    expr[position[i][0]+1:]
            ##print(constraint)
            position.pop(i-1)
            position.pop(i-1)
            i-=1                
        else:
            i+=1 

    ##print("success")    
    return expr

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
    #print(len(expr))
    
    
    position=matchBrackets(expr) 
    #print(position,expr)
    for i in range(len(position)-1):

        if position[i+1][0]==position[i][0]-1 and position[i+1][1]==position[i][1]+1:
                expr = expr[:position[i+1][1]] + ' ' + expr[position[i+1][1]+1:]
                expr = expr[:position[i+1][0]] + ' ' + expr[position[i+1][0]+1:]
    if position[-1][0]==0 and position[-1][1]==len(expr)-1 and len(position)>1:
        return expr[2:-2]
    else:
        return expr[1:-1]

def matchBrackets(expr):
    position=[]
    openBr=[]
    for i in range(len(expr)):
        if expr[i]=='(':
            openBr.append(i)
        if expr[i]==')':
            position.append([openBr.pop(),i])  

    return position


def format(expr):
    expr=resolveBrackets(expr)    
    expr=unPack(putBrackets(expr)).replace('timesm','*-').replace('times','*').replace('[','(').replace(']',')')
    expr=removeBrackets(expr).replace(' ','')    
    d = dict.fromkeys(string.ascii_uppercase, '')
    return expr

def formatEq(equationList):
    eqList=[]
    for eq in equationList:
        eq=eq.split('==')
        eqList.append(f"{format(eq[0])}=={format(eq[1])}")
        print(eq)
    return eqList


     
    

    


    



