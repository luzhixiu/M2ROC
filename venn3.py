from matplotlib import pyplot as plt
import numpy as np
from matplotlib_venn import venn3, venn3_circles


set1 = set(['A', 'B', 'C', 'D'])
set2 = set(['B', 'C', 'D', 'E'])
set3 = set(['C', 'D',' E', 'F', 'G'])
set4=set(['A'])

venn([set1, set2, set3,set4], ('Set1', 'Set2', 'Set3','Set4'))
plt.show()