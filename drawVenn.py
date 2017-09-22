import os
topFeature=3

def concatenate(path):
    f=open(path,"r")
    lines=f.readlines()

    strList=list()
    for line in lines:
        splitList=line.split(",")
        for i in (range(len(splitList)-1)):
            if i>=len(strList):
                strList.append(splitList[i])
            else:
                strList[i]=strList[i]+","+splitList[i]
    return strList




rawpath=os.path.join(os.getcwd(),"raw.csv")
rawList=concatenate(rawpath)
listToIndex=dict()
for i in range(len(rawList)):

    listToIndex[rawList[i]]=i

for key in listToIndex.iterkeys():
    print len(key)

rankedFolder=os.path.join(os.getcwd(),"FeatureSelected")
flist=os.listdir(rankedFolder)
for f in flist:
    path=os.path.join(rankedFolder,f)
#     print path
    strList=concatenate(path)
    for s in strList:
        print len(s)

    









