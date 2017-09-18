import os
import sys



# take in a file
# label the attributes by their hashing 
# feature select them through script(export.sh)
# format the data for processing(rid the weka markers)
#recover the hash 
# process the files (cv.py)

# take in a file

f=open(os.path.join(os.getcwd(),"rawiris.csv"),"r")
f=open(os.path.join(os.getcwd(),"rawiris.csv"),"r")
baseName=os.path.basename(f.name)
commandString="python csvToarff.py "+baseName
print commandString
os.system(commandString)

f=open(os.path.join(os.getcwd(),"rawiris.arff"),"r")



outputFolder=os.path.join(os.getcwd(),"FeatureSelected")
scriptPath=os.path.join(os.getcwd(),"RankFeature.sh")
print scriptPath
from subprocess import call
# call(["./RankFeature.sh",f.name,outputFolder]) call doesnt work, quited trying after spending half an hour on it
command="./RankFeature.sh "+f.name+" "+outputFolder
os.system(command) #works like a charm!

# format the data for processing(rid the weka markers)
import Format

# process the files (cv.py)
import cv






 