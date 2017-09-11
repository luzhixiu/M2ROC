import os

inputFolder="/home/lu/eclipse-workspace/LabTool/FeatureSelected"

flist=os.listdir(inputFolder)
for fname in flist:
    path=os.path.join(inputFolder,fname)
    labelDict=dict()
    with open(path,"r") as f:
        lines=f.readlines()
        labelSet=set()
        for line in lines:
            splitList=line.split(",")
            labelSet.add(splitList[len(splitList)-1])
        print fname
        i=0   
        for item in labelSet:
            labelDict[item]=i
            i+=1
        
    with open(path,"w") as f:
        for line in lines:
            splitList=line.split(",")
            splitList[len(splitList)-1]= labelDict[splitList[len(splitList)-1]]
            writeString=",".join(str(x) for x in splitList)
            print writeString
            f.write(writeString+"\n")
            
     
        
        
            
            
    