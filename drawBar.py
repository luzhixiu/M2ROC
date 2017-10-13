# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
 
# data to plot
n_groups = 5
means_frank = [0.97, 0.96, 0.97, 0.97,0.97]


# create plot
plt.figure(figsize=(10,10))
# fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.3
opacity = 0.8
lables=['At Least Five', 'At Least Four', 'At Least Three','At Least Two','Union']
colors=['b','r','y','purple','g']

# rects1 = plt.bar(index, means_frank, bar_width,
#                  alpha=opacity,
#                  color=colors,
#                  label=lables)
for i in range(n_groups):
    plt.bar(i, means_frank[i], bar_width,
                 alpha=opacity,
                 color=colors[i],
                 label=lables[i])


plt.xlabel('')
plt.ylabel('AUC')

plt.ylim([0.0, 1.19])
from matplotlib.font_manager import FontProperties


plt.legend(loc="upper right",prop={'size':8})     


# plt.tight_layout()
def showPlot():
    plt.show()
    
showPlot()