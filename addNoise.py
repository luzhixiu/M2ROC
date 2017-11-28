from numpy import genfromtxt
import numpy as np
from sklearn.utils import shuffle
rawdata=genfromtxt("rawcsv.original",delimiter=',',dtype=str) 
shuffle(rawdata)
n_features=rawdata.shape[1]-1
data=rawdata[:,0:n_features]
label=rawdata[:,n_features:n_features+1]
n_samples=data.shape[0]

print label[0]
random_state = np.random.RandomState(0)
data = np.c_[data, random_state.randn(n_samples, 20 * n_features)]

noisedData=np.concatenate((data, label), axis=1)
print np.array(noisedData).shape
outputString=""
for sample in noisedData:
    for feature in sample:
        outputString+=(str(feature)+",")
    outputString=outputString[:-1]
    outputString+="\n"    
 

f=open("noisedData.csv","wb+")
f.write(outputString)
f.close()
