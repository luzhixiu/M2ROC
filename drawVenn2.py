# -*- coding: utf-8 -*-
#system ask for two argument: filename and number of topFeatures selected  
import sys
import os
import matplotlib as mpl
from numpy import *
# from cv import topFeature
mpl.use('Agg')


import matplotlib.pyplot as plt
import venn


userFolder=sys.argv[1]
topFeature=int(sys.argv[2])
os.chdir(os.path.join(os.getcwd(),userFolder))

outputFile = open(os.path.join(os.getcwd(),"venn.txt"), 'w')
orig_stdout = sys.stdout
# sys.stdout=outputFile


# topFeature=3

def getTopFeature(path):
    f=open(path,"r")
    myList=[]
    for line in f:
        splitList=line.split(" ")
        if splitList[0]=="@ATTRIBUTE" or splitList[0]=="@attribute"  and "{" not in splitList[2]:
            myList.append(splitList[1])
    return myList[0:topFeature]

def getMaxFeature(path):
    f=open(path,"r")
    cnt=0
    for line in f:
        cnt+=1
        splitList=line.split(" ")
        if 'class' in splitList[1]:
            break
    return cnt-2
# take in a list of feature list, return elements that appear in all list
def findIntercetion(mylist):
    setList=[]
    for featureList in mylist:
        featureSet=set(featureList)
        setList.append(featureSet)
    return set.intersection(*setList)
    
    
    


fpath=os.path.join(os.getcwd(),'raw.arff')
getTopFeature(fpath)
maxFeature=getMaxFeature(fpath)
outputFolder=os.path.join(os.getcwd(),"FeatureSelected")
command="../RankFeature.sh "+"raw.arff "+outputFolder
os.system(command)
flist=os.listdir(outputFolder)
sets=[]
labels=[]

for f in flist:
    fpath=os.path.join(os.getcwd(),outputFolder,f)
    featureSet=getTopFeature(fpath)
    sets.append(featureSet)
    label=os.path.basename(f).split(".")[0]
    labels.append(label)

#number of features wont go past thousands, gonna use n^2 
print sets
for n in range(1,maxFeature+1):
    cnt=0;
#     print n
    for ls in sets: ##came up with some bad variable names, sets is a list of list of features selected by different methods
        if ls.count(str(n))>0:
            cnt+=1
    print "Feature %d is selected by %d methods"%(n,cnt)


             
  
vennLabel=venn.get_labels(sets,fill=['number','logic'])
vennLabel=venn.get_labels(sets,fill=['number'])

# labels.sort(reverse=True)


inv_map = {}
for k, v in vennLabel.iteritems():
    inv_map[v] = inv_map.get(v, [])
    inv_map[v].append(k)

fig, ax = venn.venn5(vennLabel, names=labels)
fig.savefig('venn5.png', bbox_inches='tight')

vennList=[]
keyList=[]
for key in reversed(range(1,topFeature+1)):
    key=str(key)

    
    if inv_map.has_key(key):
        
        for bin in inv_map.get(key):
            
            positiveFeatureList=[]
            outputString=''
            for i in range(len(bin)): 
                if '1' in bin[i]:
                    outputString+=labels[i]+' & '
            
                    positiveFeatureList.append(sets[i])#find the digits with one and the set it concludes 
            outputString=outputString[:len(outputString)-2]   
            print outputString,           
            interception=findIntercetion(positiveFeatureList)
            print str(list(interception))
            
            
            



plt.close()
sys.stdout = orig_stdout
outputFile.close()


        
        
    