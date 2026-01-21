# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import MultipleLocator


fr = open('unique_ab_info.txt','r')
lines = fr.readlines()
fr.close()

Lcdr_length = []

max_Lcdr_length = 0
max_Lcdr_name = ''
for line in lines:
    Lcdr = line.strip().split('\t')[3]
    Lcdr_length.append(len(Lcdr))
    
    if len(Lcdr) > max_Lcdr_length:
        max_Lcdr_length = len(Lcdr)
        max_Lcdr_name = line

Lcdr_length_count = []
for i in range(1,40):
    countl = Lcdr_length.count(i)
    Lcdr_length_count.append([i,countl])

xl = [x[0] for x in Lcdr_length_count]
yl = [x[1] for x in Lcdr_length_count]

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

font1 = {'family': 'Arial',
        'color':  'black',
        'weight': 'normal',
        'size': 18,
        }

plt.figure(figsize=(8, 6)) 
plt.bar(xl,yl,color="gray")
plt.xlabel('CDR length of VL',fontdict=font1)
plt.ylabel('Counting number',fontdict=font1)

plt.tick_params(labelsize=16,axis='x',labelcolor='black',size=3,width=1,tick2On=False,label2On=False,
                labelrotation=0,pad=1,tickdir='out',
                gridOn=False,grid_alpha=0.5,grid_color='gray',grid_linestyle='--')
plt.tick_params(labelsize=16,axis='y',labelcolor='black',size=3,width=1,tick2On=False,label2On=False,
                labelrotation=0,pad=1,tickdir='out',
                gridOn=False,grid_alpha=0.5,grid_color='gray',grid_linestyle='--')

plt.axvline(x=17.5, color='r', linestyle='--')
plt.axvline(x=22.5, color='r', linestyle='--')

x_major_locator=MultipleLocator(10)
y_major_locator=MultipleLocator(100)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.yaxis.set_major_locator(y_major_locator)

labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]

plt.savefig('Fig3a_LCDR.png',dpi=200)
plt.show()