# -*- coding: utf-8 -*-
#system ask for two argument: filename and number of topFeatures selected  
import sys
import os
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import venn


userFolder=sys.argv[1]
topFeature=sys.argv[2]
os.chdir(os.path.join(os.getcwd(),userFolder))

topFeature=3

def getTopFeature(path):
    f=open(path,"r")
    myList=list()
    for line in f:
        splitList=line.split(" ")
        if splitList[0]=="@ATTRIBUTE" or splitList[0]=="@attribute"  and "{" not in splitList[2]:
            myList.append(splitList[1])
    return myList[0:topFeature]

fpath=os.path.join(os.getcwd(),'raw.csv')
getTopFeature(fpath)
outputFolder=os.path.join(os.getcwd(),"FeatureSelected")
command="../RankFeature.sh "+"raw.csv "+outputFolder
print "command： "+command
os.system(command)
flist=os.listdir(outputFolder)
sets=list()
labels=list()

for f in flist:
    fpath=os.path.join(os.getcwd(),outputFolder,f)
    print fpath
    set=getTopFeature(fpath)
    sets.append(set)
    label=os.path.basename(f).split(".")[0]
    labels.append(label)
    
vennLabel=venn.get_labels(sets,fill=['number','logic'])
vennLabel=venn.get_labels(sets,fill=['number'])
fig, ax = venn.venn5(vennLabel, names=labels)
fig.savefig('venn5.png', bbox_inches='tight')

plt.close()



        
        
    