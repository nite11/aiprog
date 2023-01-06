import parseSys as ps
import re


def putBrackets(expr):
    expr=re.split('(\*|\+|\-)', expr)
    
    expr1=''
    #print(expr)
    i=0
    while expr.count('*')>0:
            expr=[j for j in expr if j!= '']
            i+=1        
            if expr[i]=='*' and expr[i+1]=='-':
                expr[i]=f"[{expr[i-1]}Times-{expr[i+2]}]"
                expr[i-1]=''
                expr[i+1]=''
                expr[i+2]=''
                i-=1
            if expr[i]=='*':
                expr[i]=f"[{expr[i-1]}Times{expr[i+1]}]"
                expr[i-1]=''
                expr[i+1]=''
                i-=1
        
            

    for e in expr:
        expr1+=e 

    return expr1



for eq in ps.equationList:
    eq=eq.split('==')
    #print(eq[0])
    print(putBrackets(eq[0]))
    print(putBrackets(eq[1]))



