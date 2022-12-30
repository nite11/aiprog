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
equations=equations.strip().replace("\n", "").replace("=", "==")

varList=[]

for c in equations:
    if c.isalpha() and c not in varList:
        varList.append(c)



constraints=constraints.strip().replace("\n", "").replace(" ", "")
##print(equations)
print(varList)

##print(constraints)

equationList=equations.split(",")
constraintList=constraints.split(",")

def makeConstraint(constraint):
    l=len(constraint)
    while l>1:
        for i in range(len(constraint)):
            if constraint[i]=="and":
                constraint[i-1]=f"And({constraint[i-1]},{constraint[i+1]})"
                constraint[i]=''
                constraint[i+1]=''
                l-=2

        for i in range(len(constraint)):
            if constraint[i]=="or":
                constraint[i-1]=f"Or({constraint[i-1]},{constraint[i+1]})"
                constraint[i]=''
                constraint[i+1]=''
                l-=2
    return constraint[0]


for k in range(len(constraintList)):
    constraintList[k]=re.split('(or|and)', constraintList[k])
    constraintList[k]=makeConstraint(constraintList[k])
       ## x>5orx<-5andy>0,z<0

print("constraintList: ",constraintList)
print("equationList: ",equationList)






    






