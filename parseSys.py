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
constraints=constraints.strip().replace("\n", "").replace(" ", "")
print(equations)
print(constraints)




