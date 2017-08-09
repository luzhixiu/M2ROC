import numpy as np

from numpy import*
from scipy import interp
import copy
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from sklearn.naive_bayes import GaussianNB
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.cross_validation import KFold
from sklearn.cross_validation import LeaveOneOut
from numpy import genfromtxt
from Tkinter import *
import matplotlib as mpl
mpl.use('Agg')
import collections
import configparser
import os


#Config set up

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('LeaveOneOutConfig.txt')
Classifier=settings.get('SectionOne','Classifier')

AverageRead=settings.get('SectionOne','Average the result')

NumberOfEstimators=settings.get('SectionOne','Number of Estimators')

Threshold=settings.get('SectionOne','Threshold')
#print (Threshold)
FeastureSelectionInterVal=int(settings.get('SectionOne','Feature Selection Interval'))

showResultConfig=settings.get('SectionOne','Show results in Console')


featureRange=int(settings.get('SectionOne','Plot feature range'))

PlotLegendSize=float(settings.get('SectionOne','Plot lengend size'))

DataSetName=str(settings.get('SectionOne','DataSet type name'))

LineWidth=float(settings.get('SectionOne','Plot line width'))

processTime=0; 




mpl.rcParams['axes.color_cycle'] = ['red', 'orange','yellow','green','cyan','blue','purple','black']

class Point:
    def __init__(self):        
        self.auc = 0
        self.tf = 0
mAUC = collections.defaultdict(list)

def process(my_data,rankMethod,Nfeatures):
    global processTime
    processTime = processTime+1;     

    numberOfAttribute=shape(my_data)[1]
    target=my_data[:,numberOfAttribute-1:numberOfAttribute]
    dataLength=my_data.shape[1]
    target=my_data[:,(dataLength-1):dataLength]     
    target=np.squeeze(target)
    data=my_data[...,0:Nfeatures]
    n_classes=np.unique(target).shape[0]
    threshhold=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    threshold=Threshold
    #threshhold=[0.7,0.8,0.9]
    y_test_=[]
    y_score_=[]
    
    #=====================================================================seperate classes
#    plt.figure()
    for n in range(0,n_classes):
        x=copy.copy(data)
        y=copy.copy(target)

        #Binalize the data    
        for k in range(0,len(y)):
            if y[k]==n:
                y[k]=1
            else:
                y[k]=0
        sampleSize=x.shape[0]
        FPR_=[]
        TPR_=[]    
        
        for t in range(0,len(threshhold)):
            TP=0
            FP=0
            FN=0
            TN=0
            P=0
            N=0
            cutValue=threshhold[t]
            for i in range(0,sampleSize):
                xTrain=np.concatenate((x[0:i],x[i+1:]),axis=0)
                yTrain=np.concatenate((y[0:i],y[i+1:]),axis=0)
                yActual=y[i]
                
                probas_ = classifier.fit(xTrain,yTrain).predict_proba(x[i].reshape(1,-1))
                y_test_.append(yActual);                
                y_score_.append(probas_[:, 1])            
                probas_=np.squeeze(probas_)
                predict0=probas_[0]
                predict1=probas_[1]
                if(yActual==1):
                    P+=1
                else:
                    N+=1
    #            if (predict0>cutValue):#we predict it is 0
    #                if(yActual==0):
    #                    TN+=1;
    #                else:
    #                    FP+=1;
                if(predict1>=cutValue):#we predict it is 1
                    if(yActual==0):
                        FP+=1;
                    else:
                        TP+=1
                else:
                    if(yActual==0):
                        TN+=1;
                    else:
                        FN+=1           
    #        print(TP/float(P),FP/float(N))
            TPR=TP/float(P)
            FPR=FP/float(N)        
            FPR_.append(FPR)
            TPR_.append(TPR)
    #    print (TPR_,FPR_)
        roc_auc = auc(FPR_, TPR_,reorder=button)
#         Plot of a ROC curve for a specific class
        if'Y' in AverageRead or 'y' in AverageRead:
            plt.plot(FPR_, TPR_, label='ROC curve of class {0} (area = {1:0.2f})'
                                       ''.format(n, roc_auc))
       
    y_score_=np.asarray(y_score_)
    y_test_=np.asarray(y_test_)
    # Compute micro-average ROC curve and ROC area
    #print y_score_
    microFPR, microTPR, _ = roc_curve(y_test_, y_score_)
    microAUC = auc(microFPR, microTPR)
    
    
    plt.plot(microFPR, microTPR,
             label=rankMethod+' (AUC = {0:0.2f})'
                   ''.format(microAUC),
             linewidth=2)
    point=Point()
    point.auc=microAUC
    point.tf=Nfeatures
    mAUC[rankMethod].append(point)
#========================================================
#Controls Reordering
button=True  
#==============================================================================
#Classifier Selection   
#
if(Classifier=='SVM'):
    random_state = np.random.RandomState(0)    
    title="SVM"
    classifier =svm.SVC(kernel='linear',probability=True,random_state=random_state)

if(Classifier=='NB'):
    title="Naive Bayes"
    classifier =GaussianNB()

    
if(Classifier=='RF'):
    title="Random Forest"
    classifier = RandomForestClassifier(n_estimators=int(NumberOfEstimators))    
#==============================================================================
#Main Program


#my_data=genfromtxt('./Relief.csv',delimiter=',')
flist=os.listdir("Input(LeaveOneOut)")

selectList=[]
selectList.append(1)
p=0

while(p<=featureRange):
    p+=FeastureSelectionInterVal
    if(p<=featureRange):    
        selectList.append(p)
   
   
#print selectList    
for i in selectList:    
    print ("top features chosen "+str(i))
#    process(my_data,"Relief",i)
    for f in flist:
        data=genfromtxt(('Input(LeaveOneOut)/'+f),delimiter=',')    
        process(data,f,i)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title+' ON'+' TOP '+str(i)+' Features'+' '+'('+DataSetName+')')
    plt.legend(loc="lower right",prop={'size':PlotLegendSize})
    filename='OUTPUT_LOU/'+title+' TOP '+str(i)+' Features'
    plt.savefig(filename)
    if'Y' in AverageRead or 'y' in showResultConfig:    
        plt.show()
    plt.figure()

for i in mAUC:
    xlist=[]
    ylist=[]
    for j in mAUC[i]:
        x=j.tf
        y=j.auc
        xlist.append(x)
        ylist.append(y)
    plt.plot(xlist,ylist,label=i,
             linewidth=LineWidth)
print ("total process time"+str(processTime))

plt.xlim([0, featureRange+1])
plt.ylim([0.0, 1.05])
plt.xlabel('No. of features')
plt.ylabel('AUC')
plt.title(title+'_'+'('+DataSetName+')')
filename='OUTPUT_LOU/'+title+'_'+'('+DataSetName+')'
plt.legend(loc="lower right",prop={'size':PlotLegendSize})    
plt.savefig(filename)
if'Y' in AverageRead or 'y' in showResultConfig:
    plt.show()

