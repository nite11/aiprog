import roughWork as rw

content=''

def getFile(filename):
    with open(filename,'r') as f:
        global content
        content=f.read().lower()##.splitlines()    
    
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
print(varList)

##print(constraints)

equationList=equations.split(",")
constraintList=constraints.split(",")






for k in range(len(constraintList)):
    constraintList[k]=rw.resolveBrackets(constraintList[k],rw.makeConstraint)
    constraintList[k]=rw.makeConstraint(constraintList[k])
    constraintList[k]=constraintList[k].replace('[','(').replace(']',')')
       ## x>5orx<-5andy>0,z<0


equationList=rw.formatEq(equationList)
print("equationList: ",equationList)
print("constraintList: ",constraintList)







    






