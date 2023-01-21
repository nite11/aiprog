import parserFunctions as pf
from z3 import *

def parseFile(filename):
    with open(filename,'r') as f:
        content=f.read().lower() 

    global varList,equationList,constraintList 

    equations=""
    constraints=""

    if content.find("such")!=-1:
        equations=content[content.find("solve")+5:content.find("such")]
        constraints=content[content.find("that")+4:content.find(".")]
    else:
        equations=content[content.find("solve")+5:content.find(".")]
        

    equations=equations.strip().replace("\n", "").replace("=", "==").replace(" ", "")#.replace("!==", "!=")
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
    varList=list(dict.fromkeys(varList))  #to remove duplicates
    print("varList:",varList)          

    constraints=constraints.strip().replace("\n", "").replace(" ", "").replace("=", "==")#.replace("!==", "!=")
    
    equationList=equations.split(",")
    constraintList=constraints.split(",")
           
    equationList=pf.formatEq(equationList)
    constraintList=pf.formatCon(constraintList)
    print("equationList: ",equationList)
    print("constraintList: ",constraintList)

def solve(filename):
    parseFile(filename)
    
    for i in range(len(varList)):
        exec(f"{varList[i]}=Int('{varList[i]}')") #to create the Z3 integer variables
    
    s = Solver()   
    for eq in equationList:
        s.add(eval(eq))

    for con in constraintList:
        if con!='':
            s.add(eval(con))


    if s.check()!=sat:
        print("The system has no solution.")
    else:
        m=s.model()
        d={}        
        cons="Or("    
        for l in range(len(varList)):
            d.update({m[l]:m[m[l]]})        #to add variable:value pair to the dictionary
            cons+=f"{m[l]}!={m[m[l]]},"     #to form a constraint to add to the model to check for another solution
        cons+=")"    
        s.add(eval(cons))
        print(d)
        if s.check()==sat:
            print("The system has more than 1 solution.")
        else:
            print("The system has only 1 solution.")
        return d
        
#if __name__ == '__main__':
#    solve(sys.argv[1])