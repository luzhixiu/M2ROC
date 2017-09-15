import os




# take in a file
# label the attributes by their hashing 
# feature select them through script(export.sh)
# format the data for processing(rid the weka markers)
#recover the hash 
# process the files (cv.py)

# take in a file
import os
path=os.path.join(os.getcwd(),"rawiris.csv")
f=open(path,"r")


print f.name

# label the attributes by their hashing
import LabelAttributes as LA
originHash=LA.hashList

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






 
