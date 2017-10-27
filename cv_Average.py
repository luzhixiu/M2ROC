
from sklearn import svm, datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from numpy import*
import copy
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
from numpy import genfromtxt
from Tkinter import *
import matplotlib as mpl
import configparser
import os
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from collections import defaultdict
import configparser
mpl.use('Agg') #turn off graphic display for the server
#Config set up
title="ROC"
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('config.txt')
Classifier=settings.get('SectionOne','classifier')
if len(Classifier)!=0:
    cls=Classifier

N_estimator=settings.get('SectionOne','number of estimators')
if len(N_estimator)!=0:
    NumberOfEstimators=int(N_estimator)

fold=3
fold_setting=settings.get('SectionOne','fold')
if len(fold_setting)!=0:
    fold=int(fold_setting)
else:
    print "Error EMPTY FOLD"

if len(N_estimator)!=0:
    NumberOfEstimators=int(N_estimator)



AverageRead=settings.get('SectionOne','average the result')
print AverageRead

if AverageRead.find("e")>0:
    showClassROC=False
if AverageRead.find("o")>0:
    print "show is set to true"
    showClassROC=True



chosenFeature=int(settings.get('SectionOne','top feature'))
topFeature=chosenFeature
print "TopFeature Chosen "+ str(topFeature)

PlotLegendSize=float(settings.get('SectionOne','plot lengend size'))
legendSize=PlotLegendSize

LineWidth=float(settings.get('SectionOne','Plot line width'))
lw=LineWidth

DataSetName=str(settings.get('SectionOne','dataSet type name'))

NoiseLevel=int(settings.get('SectionOne','noise Level'))
addNoise=NoiseLevel


# preset some variables
# lw=1.5 #linewidth
# cls="SVM" #classifier
# title="Receiver operating characteristic example"
# showClassROC=False
# NumberOfEstimators=10 #this is only used for random forest
# addNoise=0

# topFeature=4
# legendSize=10

inputFolder=os.path.join(os.getcwd(),"FeatureSelected")

#some local config 
mpl.rcParams['axes.color_cycle'] = ['red','plum','steelblue','orange','yellow','green','cyan','blue','purple','black']
np.set_printoptions(suppress=True)
random_state = np.random.RandomState(0)






def NumberLabels():
    flist=os.listdir(inputFolder)
    for fname in flist:
        path=os.path.join(inputFolder,fname)
        labelDict=dict()
        with open(path,"r") as f:
            lines=f.readlines()
            labelSet=set()
            for line in lines:
                splitList=line.split(",")
                labelSet.add(splitList[len(splitList)-1])
            print fname
            i=0   
            for item in labelSet:
                labelDict[item]=i
                i+=1
            
        with open(path,"w") as f:
            for line in lines:
                splitList=line.split(",")
                splitList[len(splitList)-1]= labelDict[splitList[len(splitList)-1]]
                writeString=",".join(str(x) for x in splitList)
                f.write(writeString+"\n")
        


def loadMaxFeature():
        flist=os.listdir(inputFolder)
        workdir=os.getcwd()
        maxAttribute=0
        for f in flist:
            path=os.path.join(workdir,inputFolder,f)
            rawdata=genfromtxt(path,delimiter=',')  
            if maxAttribute<rawdata.shape[1]-1:
                maxAttribute=rawdata.shape[1]-1
        return maxAttribute
            
def process(X,y,classN):
#     print "process class %d"%(classN)
    global classifier
    cv = KFold(n_splits=fold)
    global all_test,all_probas
    class_test=class_probas=np.array([])
    for train, test in cv.split(X):
        class_test=np.append(class_test,y[test])
        all_test=np.append(all_test,y[test])
#         print X[train]
        probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
        class_probas=np.append(class_probas,probas_[:, 1])
        all_probas=np.append(all_probas,probas_[:, 1])


    class_fpr_micro, class_tpr_micro, _ = roc_curve(class_test.ravel(), class_probas.ravel())
    class_fpr[classN],class_tpr[classN],_=roc_curve(class_test, class_probas)

    roc_auc_class_micro = auc(class_fpr_micro,class_tpr_micro)
    print roc_auc_class_micro
    global showClassROC
    if showClassROC:
        print "Not gonna Average the result"
        plt.plot(class_fpr_micro, class_tpr_micro,label='Class %d micro-average ROC curve (area = {%0.2f})'%(classN,roc_auc_class_micro),linewidth=lw)

    
def loadClassifier(cls):
    global classifier,title
    if cls=="SVM":
        title="Support Vector Machine"
        classifier= svm.SVC(kernel='linear', probability=True)
    if cls=="NB":
        title="Naive Bayes"
        classifier =GaussianNB()
    if(cls=='RF'):
        title="Random Forest"
        classifier = RandomForestClassifier(n_estimators=int(NumberOfEstimators))   
        
def loadData(myFile):
    rawdata=genfromtxt(myFile,delimiter=',')  
    #shuffle data for randomnization  
    rawdata=shuffle(rawdata)
    numberOfAttribute=rawdata.shape[1]
    lable=rawdata[:,numberOfAttribute-1:numberOfAttribute]
    lable=np.squeeze(lable)
    data=rawdata[:,0:numberOfAttribute-1]
    global X
    X=data
    global y
    y=lable


#take in the input file(OTU table) and top features to be processed in this file
#n_feature here is the human understandable feature, starts from 1. 
#return nothing, this function loads global X and y for data and label
#if n_feature provided exceeds the max features the file contains, use all the features in the input file. In this case, this function is the same as loadFile() 
def loadTopFeature(myFile,n_feature): 
    rawdata=genfromtxt(myFile,delimiter=',')       
    rawdata=shuffle(rawdata)
    numberOfAttribute=rawdata.shape[1]-1
    global topFeature
    if n_feature>numberOfAttribute:
        n_feature=numberOfAttribute
    if n_feature<0:
        n_feature=0

    data=rawdata[:,0:n_feature]
    lable=rawdata[:,numberOfAttribute:numberOfAttribute+1]
    lable=np.squeeze(lable)
    global X
    X=data
    global y
    y=lable

#============================================Personazation Setup


#process file f, plot the average ROC curve and return the AUC value
def processFile(f):
    global X,y
    loadTopFeature(f,topFeature)
    n_samples, n_features = X.shape
    if addNoise>0:
        X = np.c_[X, random_state.randn(n_samples, addNoise * n_features)]
    data=copy.copy(X)
    label=copy.copy(y)
    #get the number of classes
    n_classes=np.unique(label)
    loadClassifier(cls)
    global all_test,all_probas,all_fpr,all_fpr,class_fpr,class_tpr

    for n in n_classes:
        #reinitialize the labels each iteration
        label=copy.copy(y)
        #binarize the labels,if the label equals the class n, set it to one,else 
        #set it to zero
        for k in range(0,label.shape[0]):
            if int(label[k])==n:
                label[k]=1
            else:
                label[k]=0
        process(data,label,n)
    
        
    # print all_test.shape
    # print all_probas.shape
    
    
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    fpr["micro"], tpr["micro"], _ = roc_curve(all_test.ravel(), all_probas.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    fname=os.path.basename(f).split(".")[0]
    plt.plot(fpr["micro"], tpr["micro"],
             label='AUC (%s) (area = {%0.2f})'%(fname,roc_auc["micro"]),  linewidth=lw)
    return roc_auc["micro"]
    # all_fpr=np.unique(np.concatenate([class_fpr[i] for i in n_classes]))
    # mean_tpr = np.zeros_like(all_fpr)
    # 
    # 
    # for i in n_classes:   
    #     mean_tpr+=interp(all_fpr,class_fpr[i],class_tpr[i])
    # print mean_tpr
    # 
    # mean_tpr /= len(n_classes) 
    # 
    # 
    # fpr["macro"] = all_fpr
    # tpr["macro"] = mean_tpr
    # 
    # 
    # roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    # 
    # plt.plot(fpr["macro"], tpr["macro"],
    #          label='macro-average ROC curve (area = {0:0.2f})'
    #                ''.format(roc_auc["macro"]),
    #          color='yellow', linestyle=':', linewidth=4)

def processFolder(folder):
    flist=os.listdir(folder)
    workdir=os.getcwd() 
    aucList=[]
    global indexToFname
    c=0
    for f in flist:
        path=os.path.join(workdir,folder,f)
        indexToFname[c]=f.split(".")[0]
        c+=1
        auc=processFile(path)
        aucList.append(auc)
    return aucList


     
X=0
y=0
NumberLabels()

originTopFeature=topFeature
aucMatrix=[]
indexToFname=dict()

# plt.show()


for i in range(originTopFeature):
    all_test=all_probas=all_fpr=all_tpr=np.array([])
    class_fpr=class_tpr=dict()
    topFeature=i+1
    aucList=processFolder(inputFolder)
    aucMatrix.append(aucList)
    
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.savefig("TOP_"+str(i+1)+"_Feature")
    plt.show()
    plt.figure()

NTL=defaultdict(list) # NTL is number to list
for featureList in aucMatrix:#featureList represents features chosen
    for k in range(len(featureList)): #k is the number of file, featureList[k] is the auc value assosited with it
        NTL[k].append(featureList[k])

for k in NTL.keys():
    xList=range(1,len(NTL[k])+1)
    yList=NTL[k]
    plt.plot(xList,yList,label=indexToFname[k],marker=".")
plt.xlim([0, originTopFeature+1])
plt.ylim([0.0, 1.05])
plt.xlabel('No. of Features')
plt.ylabel('AUC')
plt.title("AUC")
plt.legend(loc="lower right",prop={'size':legendSize})     
plt.savefig("AUC")
plt.show()    
    




   








            
    
        
        
        
    
        
