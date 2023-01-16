import parseSys as ps
import re
import string

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
    
    while len(expr)>1:
        expr[-3]=f"[{expr[-3]}{expr[-2]}{expr[-1]}]"
        expr.pop()
        expr.pop()

    return (''.join(expr))

for eq in ps.equationList:
    eq=eq.split('==')
    #print(eq[0])
    eq[0]=resolveBrackets(eq[0])    
    eq[0]=unPack(putBrackets(eq[0])).replace('timesm','*-').replace('times','*')
    print(eq[0])
    d = dict.fromkeys(string.ascii_uppercase, '')

    eq[1]=resolveBrackets(eq[1])
    print(unPack(putBrackets(eq[1])))
    d = dict.fromkeys(string.ascii_uppercase, '')


    



