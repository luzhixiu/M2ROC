# 
# pre: take in raw data raw.csv(under current dir(cwd))
# 1, raw data format to mrmr input format
# 2, run mrmr script with the right number of features, output is mrmr.txt
# 3, read mrmr.txt get the order of features
# 4, reorder feautures based on the list, add tags,save the data as mrmr.csv
# post: create mRMR.csv file in the featyreSelected fodler
import os
print "mrmr started"

outputDir=os.path.join(os.getcwd(),"FeatureSelected")
path = os.path.join(os.getcwd(),"raw.csv")
file=open(path,"r")
lines=file.readlines()

#class global values here
numberOfFeatures=0
classList=[]
#take in lines of raw data, change the format to mrmr input and save it as "mrmr.csv"
def rawToMrmrFormat(lines):
    global clasList
    global numberOfFeatures
    numberOfFeatures=len(lines[0].split(","))-1
    outputString=""
    headerLine=""
    headerLine+="class,"
    for i in range(1,numberOfFeatures+1):
        headerLine+="Feature%d,"%i
    headerLine=headerLine[:len(headerLine)-1]+"\n"
    outputString+=headerLine
    for line in lines:
        newLine=""
        splitList=line.split(",")
        className=splitList[numberOfFeatures]
        className=className.rstrip()+"\n"
        if classList.count(className)==0:     #length of classList is a small number, use n square is fine
            classList.append(className)
        newLine+=str(classList.index(className))+","
        for i in range(0,numberOfFeatures):
            newLine+=splitList[i]+","
        newLine=newLine[:len(newLine)-1]
        outputString+=newLine+"\n"
    writeFilePath=os.path.join(os.getcwd(),"mrmr.csv")
    outputFile=open(writeFilePath,"w")
    outputFile.write(outputString)
    outputFile.close()
    command="../../mrmr -i mrmr.csv -t 0.05 -n %d -m MID > mrmr.txt"%numberOfFeatures
    os.system(command)
rawToMrmrFormat(lines)

#read mrmr.txt, return a list of orders
def getNewFeatureOrder():
    f=open("mrmr.txt","r")
    lines=f.readlines()
    startIndex=0
    endIndex=0
    for i in range(len(lines)):
        line=lines[i]
        if "mRMR feature" in line:
            startIndex=i+2
            global numberOfFeatures
            endIndex=startIndex+numberOfFeatures
            break
    newFeatureList=[]
    for i in range(startIndex,endIndex):
        line=lines[i]
        splitList=line.split()
        newFeatureList.append(splitList[1])
    return newFeatureList
    
#  read raw.csv, reorder it based on ranked order, save it to $outputDir 
def reorderCsv(lines):
    outputString=""
    global classList,numberOfFeatures
    print classList
    featureList=getNewFeatureOrder()
    print featureList
    outputString+="@relation mrmr\n"
    for i in featureList:
        outputString+="@attribute %s numeric\n"%i
    classListString=str(classList)
    classListString=classListString.replace('[', '{')
    classListString=classListString.replace(']', '}')
    classListString=classListString.replace("'", '')
    outputString+="@attribute class %s"%classListString+"\n"
    outputString+="@data\n"
    for line in lines:
        outputString+=line
    
    writeFilePath=os.path.join(outputDir,"mRMR.csv")
    outputFile=open(writeFilePath,"w")
    outputFile.write(outputString)
    outputFile.close()
    writeFilePath=os.path.join(os.getcwd(),"mRMR.csv")
    outputFile=open(writeFilePath,"w")
    outputFile.write(outputString)
    outputFile.close()
    
reorderCsv(lines)
print "mrmr finished"
    
    
    
    
    
    
    
    
    
    
    
    
    



    
