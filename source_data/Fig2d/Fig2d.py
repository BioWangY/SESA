# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv('Fig2d_data.csv')

plt.figure(figsize=(10, 8))
sns.barplot(x='del',data=data,y='score')

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 20

plt.xlabel('Deletion Ratio of Epitope Amino Acids',fontdict={'family':'Arial', 'size':20})
plt.ylabel('ROC-AUC Values',fontdict={'family':'Arial', 'size':20})
plt.ylim(0, 1)
plt.title('Performance Testing on Incomplete Epitopes',
          loc='center',pad=7,
          fontdict={'family':'Arial', 'size':20})
plt.xticks(fontproperties = 'Arial', size = 20)
plt.yticks(fontproperties = 'Arial', size = 20)
plt.rcParams['axes.facecolor'] = '#F2F2F2'

plt.savefig('Fig2d.png',dpi=200)
plt.show()

