import parserFunctions as pf
from z3 import *





def parseFile(filename):
    with open(filename,'r') as f:
        #global content
        content=f.read().lower()##.splitlines()    

    global varList,equationList,constraintList ##number of variables

    equations=""
    constraints=""

    if content.find("such")!=-1:
        equations=content[content.find("solve")+5:content.find("such")]
        constraints=content[content.find("that")+4:content.find(".")]
    else:
        equations=content[content.find("solve")+5:content.find(".")]
        

    equations=equations.strip().replace("\n", "").replace("=", "==").replace(" ", "").replace("!==", "!=")
    if equations.find("and") !=-1 or equations.find("or")  !=-1:
        equations="User error: equations are not allowed to contain composite boolean expressions"



    v=''
    
    for c in equations:
        if c.isalpha():
            v+=c
        else:
            v+=' '
    varList=v.split(' ')  
    varList=[i for i in varList if i != '']   
    varList=list(dict.fromkeys(varList))  #remove duplicates
          

    constraints=constraints.strip().replace("\n", "").replace(" ", "").replace("=", "==").replace("!==", "!=")
    ##print(equations)
    print("varList:",varList)

    ##print(constraints)

    equationList=equations.split(",")
    constraintList=constraints.split(",")
    
    for k in range(len(constraintList)):
        constraintList[k]=pf.resolveBrackets(constraintList[k],pf.makeConstraint)
        constraintList[k]=pf.makeConstraint(constraintList[k])
        constraintList[k]=constraintList[k].replace('[','(').replace(']',')')
        ## x>5orx<-5andy>0,z<0


    equationList=pf.formatEq(equationList)
    print("equationList: ",equationList)
    print("constraintList: ",constraintList)

def solve(filename):
    parseFile(filename)
    
    for i in range(len(varList)):
        exec(f"{varList[i]}=Int('{varList[i]}')")
         
    
    #print(len(varList))
    s = Solver()   
    for eq in equationList:
        s.add(eval(eq))

    for con in constraintList:
        if con!='':
            s.add(eval(con))


    #s.add(t==7,u==7,x==1,z==0)
    if s.check()!=sat:
        print("The system has no solution.")

    numOfSol=0
    while s.check()==sat and numOfSol<1:
        numOfSol+=1
        m=s.model()
        d={}
        
        cons=""
        #print(m)    
        for l in range(len(varList)):
            d.update({m[l]:m[m[l]]})
            cons+=f"{m[l]}!={m[m[l]]},"        
            
        #print(cons)
        s.add(eval(cons))
        print(d)
    if s.check()==sat:
        print("The system has more than 1 solution.")
    else:
        print("The system has only 1 solution.")

if __name__ == '__main__':
    solve('sys.txt')









    






