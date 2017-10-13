# -*- coding: utf-8 -*-
import os
from sets import Set
from pydoc import classname
import sysconfig
import sys
from matplotlib.font_manager import path
userFolder=sys.argv[2]
path=os.path.join(os.getcwd(),userFolder, sys.argv[1])

print "file path is %s"%path
print "user folder is %s"%userFolder

f=open(path,"r")
lines=f.readlines()
f.close()

arffStringList=list()
fileName=os.path.basename(f.name).split(".")[0]
relation="@RELATION "+fileName
arffStringList.append(relation)
numberOfAttribute=len(lines[0].split(","))-1
for i in range(1,numberOfAttribute+1):
    arffStringList.append("@ATTRIBUTE "+str(i)+" REAL")

classSet=Set()
classList=list()
for line in lines:
    className=line.split(",")[numberOfAttribute]
    if className not in classSet:
        classSet.add(className)
        classList.append(className)
        
AttributeClass="@ATTRIBUTE class {"
for i in classList:  
    if '\n' in i:
        i=i[:len(i)-2]
    AttributeClass+=i    
    AttributeClass+=","
AttributeClass=AttributeClass[0:len(AttributeClass)-1]
AttributeClass+="}"


arffStringList.append(AttributeClass)
arffStringList.append("@DATA")

writePath=os.path.join(os.getcwd(),userFolder,fileName+".arff")
print writePath
f=open(writePath,"w")
for s in arffStringList:
    f.write(s+"\n")
for line in lines:
    f.write(line)
f.close()
print "csv to arff finished"
        





