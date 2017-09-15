# coding: utf-8

# ipython notebook requires this
# %matplotlib inline

# python console requires this
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import venn



A=[1,2,3,4,5]
B=[2,3,4,5,6]
C=[3,4,5,6,7]
D=[7,8,9]
E=[1,2,4,6,7]

label1=venn.get_labels([A,B,C,D,E],fill=['number'])
label2=venn.get_labels([A,B,C,D,E],fill=['number','logic'])
print label1
print label2
fig, ax = venn.venn5(label2, names=['list 1', 'list 2', 'list 3', 'list 4', 'list 5'])
fig.savefig('venn5.png', bbox_inches='tight')

plt.close()

