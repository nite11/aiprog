import re

with open('sys.txt','r') as f:
    contentL=f.read().lower()##.splitlines()    
    f.seek(0)
    content=f.read()

equations=""
constraints=""

if contentL.find("such")!=-1:
    equations=content[contentL.find("solve")+5:contentL.find("such")]
    constraints=content[contentL.find("that")+4:contentL.find(".")]
else:
    equations=content[contentL.find("solve")+5:contentL.find(".")]
    
##add code to verify that equations does not have and or
##add code for 2 ands and 1 or
equations=equations.strip().replace("\n", "").replace("=", "==").replace(" ", "").replace("!==", "!=")
if equations.find("and") !=-1 or equations.find("or")  !=-1:
    equations="User error: eqautions are not allowed to contain composite boolean expressions"


varList=[]

for c in equations:
    if c.isalpha() and c not in varList:
        varList.append(c)



constraints=constraints.strip().replace("\n", "").replace(" ", "").replace("=", "==").replace("!==", "!=")
##print(equations)
print(varList)

##print(constraints)

equationList=equations.split(",")
constraintList=constraints.split(",")

def resolveBrackets(constraint):  ##x>5or(x<-5andy<0)
    position=[]   ##to capture the position of  parenthesis
    
    for j in range(len(constraint)):
        if constraint[j]==')' or constraint[j]=='(':
            position.append([j,constraint[j]])

        
    ##print(position)
    i=1
    while(len(position)>0):    
        position=[]   ##to capture the position of  parenthesis
    
        for j in range(len(constraint)):
            if constraint[j]==')' or constraint[j]=='(':
                position.append([j,constraint[j]])    
        ##print(i)
        ##print(position)
        if position[i][1]==')':
            ##print(constraint[position[i-1][0]+1:position[i][0]])
            constraint=constraint[0:position[i-1][0]] + \
                    makeConstraint(constraint[position[i-1][0]+1:position[i][0]]) + \
                    constraint[position[i][0]+1:]
            ##print(constraint)
            position.pop(i-1)
            position.pop(i-1)
            i-=1

                
        else:
            i+=1 
        
            
    ##print("success")    
    return constraint

def makeConstraint(constraint):
    constraint=re.split('(or|and)', constraint)
    l=len(constraint)
    i=-1
    while constraint.count('and')>0:
        i+=1
        if constraint[i]=="and":
                constraint[i-1]=f"And({constraint[i-1]},{constraint[i+1]})"
                constraint.pop(i)
                constraint.pop(i)
                l-=2
                i=-1
        
    i=-1
    while constraint.count('or')>0:
        i+=1
        if constraint[i]=="or":
                constraint[i-1]=f"Or({constraint[i-1]},{constraint[i+1]})"
                constraint.pop(i)
                constraint.pop(i)
                l-=2
                i=-1       
                
        

        
    return constraint[0]


for k in range(len(constraintList)):
    constraintList[k]=resolveBrackets(constraintList[k])
    
    constraintList[k]=makeConstraint(constraintList[k])
       ## x>5orx<-5andy>0,z<0

print("constraintList: ",constraintList)
print("equationList: ",equationList)






    






