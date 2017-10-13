import numpy as np
import matplotlib.pyplot as plt


def drawBar(Matrix):
    Matrix=map(list, zip(*Matrix))
    print Matrix
    # data to plot
    n_groups = 5
    means_frank = (90, 55, 40, 65)
    means_guido = (85, 62, 54, 20)
     
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    print index
    bar_width = 0.15
    opacity = 0.8
     
#     plt.bar(index, Matrix[0], bar_width,
#                      alpha=opacity,
#                      color='b',
#                      label='At Least 5')
#      
#     plt.bar(index + bar_width, Matrix[1], bar_width,
#                      alpha=opacity,
#                      color='g',
#                      label='At Least 4')
    gap=0
    label=["Union","At Least 2","At Least 3","At Least 4","At Least 5"]
    idx=0
    for ls in Matrix:
        plt.bar(index+gap,ls,bar_width,alpha=opacity,label=label[idx])
        gap+=bar_width
        idx+=1
   
    
     
    plt.xlabel('Person')
    plt.ylabel('Scores')
    plt.title('Scores by person')
    plt.xticks(index + bar_width, ('Class 0', 'Class 1', 'Class 2', 'Class 3',"MicroAverage"))
    plt.legend(loc="upper right",prop={'size':8})
    plt.yticks([0,0.2,0.4,0.6,0.8,1.0])
    plt.ylim([0.0, 1.39])
    plt.tight_layout()
    plt.show()



lists=[[0.8,0.9,0.9,1,1],[0.4,0.6,0.7,0.8,1],[0.4,0.6,0.7,0.8,1],[0.4,0.6,0.7,0.8,1],[0.4,0.6,0.7,0.8,1]]
drawBar(lists)
showPlot()