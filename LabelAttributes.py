
f=open("/home/lu/eclipse-workspace/LabTool/rawiris.csv","r")
lines=f.readlines()

hashList=list()



for line in lines:
	splitList=line.split(",")
	for i in range(len(splitList)-1):
		if i<len(hashList):
			hashList[i]+=float(splitList[i])
		else:
			hashList.append(float(splitList[i]))

start=0
end=len(lines)-1
mid=(start+end)/2

splitList=lines[0].split(",")
for i in range(len(splitList)-1):
	hashList[i]*= (float(splitList[i])+1)
	
splitList=lines[mid].split(",")
for i in range(len(splitList)-1):
	hashList[i]*= (float(splitList[i])+1)	
	
	
splitList=lines[end].split(",")
for i in range(len(splitList)-1):
	hashList[i]*= (float(splitList[i])+1)	
	
print hashList
	

