import sys
import os


def preprocessFile(path):
    f=open(path,"r")
    lines=f.readlines()
    f.close()
    f=open(path,"w")
    start=False 
    for line in lines:
        if start and  not line.isspace():
            print line
            f.write(line)       
        if "@data" in line:
            start=True
            
print os.getcwd()
inputFolder=os.path.join(os.getcwd(),"FeatureSelected")
flist=os.listdir(inputFolder)
for f in flist:
    path=os.path.join(inputFolder,f)
    preprocessFile(path)