print(__doc__)

import numpy as np
from numpy import*
from scipy import interp
import copy
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.cross_validation import KFold
import matplotlib as mpl
## Run classifier with cross-validation and plot ROC curves
random_state = np.random.RandomState(0)
classifier = svm.SVC(kernel='linear', probability=True,random_state=random_state)
methodName='SVM'

#classifier =GaussianNB()
#methodName='Naive Bayes'

#classifier = RandomForestClassifier(n_estimators=100)
#methodName='Random Forest' 

mpl.rcParams['axes.color_cycle'] = ['red', 'orange','yellow','green','cyan','blue','purple','black']


#iris = datasets.load_iris()
#X = iris.data
#Y=iris.target

data=genfromtxt('./Relief.csv',delimiter=',')
target=data[:,84:85]
dataLength=data.shape[1]
target=data[:,(dataLength-1):dataLength]  
target=np.squeeze(target)
X=data
Y=target


#n_classes = y.shape[1]
#y = label_binarize(y, classes=[0, 1, 2])
#kf = KFold(X.shape[0], n_folds=5)
n_classes=np.unique(Y).shape
print n_classes
FPR=dict()
TPR=dict()
ROC_AUC=dict()
PROBAS=[]
YTEST=[]
MEANTPR=[]
ALLFPR=[]

for n in range(0,n_classes[0]):
#    iris = datasets.load_iris()
#    X = iris.data
#    Y=iris.target
    #add noise to better test the performance
    data=genfromtxt('./Relief.csv',delimiter=',')
    target=data[:,84:85]
    X=data
    target=np.squeeze(target)
    Y=target

    random_state = np.random.RandomState(0)
    n_samples, n_features = X.shape
#    X = np.c_[X, random_state.randn(n_samples, 20* n_features)]    
#    print n    
    y = copy.copy(Y)
    for k in range(0,len(y)):
        if y[k]==n:
            y[k]=1
        else:
            y[k]=0
#    print y            

    fpr = dict()
    tpr = dict()
    roc_auc = dict()    
    cv = StratifiedKFold(y, n_folds=3)
    

   
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []
    
    for i, (train, test) in enumerate(cv):
        Ytest=y[test]
        for m in range(0,len(Ytest)):
            YTEST.append(Ytest[m])
        
        probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
        PRO=probas_[:, 1]
        
#        print '========================================================='
        for k in range(0,len(PRO)):
            PROBAS.append(PRO[k])
        
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
#        YTEST.append(y[test])        
#        PROBAS.append(probas_)
        for i in range(0,len(fpr)):
            ALLFPR.append(fpr[i])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
    #    plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
    mean_tpr /= len(cv)
    for x in range(0,len(mean_tpr)):
        MEANTPR.append(mean_tpr[x])
    
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr,
             label='Mean ROC class %d(area = %0.2f)' % (n,mean_auc),lw=2) 
#             plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))

#print YTEST#y_score
FPR["micro"], TPR["micro"], _ = roc_curve(YTEST, PROBAS)
ROC_AUC["micro"] = auc(FPR["micro"], TPR["micro"])
plt.plot(FPR["micro"], TPR["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(ROC_AUC["micro"]),
         linewidth=2)
       



##=================MACRO AVERAGE(not fully tested) 
#MEANTPR=np.array(MEANTPR)
#print len(all_fpr)
#print len(mean_tpr)
#MeanTPR=[]
#mean_tpr=list(mean_tpr)
#while(len(mean_tpr)>len(all_fpr)):
#    mean_tpr.pop()
#
#ROC_AUC["macro"] = auc(all_fpr, mean_tpr)
#plt.plot(all_fpr, mean_tpr,
#         label='macro-average ROC curve (area = {0:0.2f})'
#               ''.format(ROC_AUC["macro"]),
#         linewidth=2)
##=========================================================        
         
         
plt.plot([0, 1], [0, 1], 'k--',label='Perfectly calibrated')    
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title(methodName)
plt.legend(loc="lower right")           
plt.show()


