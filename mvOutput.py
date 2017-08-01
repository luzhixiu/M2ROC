import os
import re
from shutil import copyfile
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
    
def extraNumber(str):
    num=[int(s) for s in str.split("_") if s.isdigit()]
    print num[0]
    return num[0]

newFolder="static/"

workdir=os.path.join(os.getcwd(),'OUTPUT_LOU/')
print(os.getcwd())
print (workdir)
for file in os.listdir(workdir):
    print (workdir+file)
    if hasNumbers(file):
	num=extraNumber(file)
        copyfile(workdir+file,os.path.join(os.getcwd(),newFolder,str(num)+".png")) 

    else:
        copyfile(workdir+file,os.path.join(os.getcwd(),newFolder,"auc.png")) 

