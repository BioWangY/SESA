# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 14:25:58 2024

@author: 92839
"""

fr = open('testdata_pdbid_index_rank_precent_score.txt','r')
lines = fr.readlines()
fr.close()

lines = [x.strip().split('\t') for x in lines]
lines = [[x[0],int(x[1]),int(x[2]),float(x[3]),float(x[4])] for x in lines]

rank_100 = []
for i in lines:
    rank_100.append(int(i[3])+1)

A = list([x+1 for x in range(100)])
A_count = [rank_100.count(x) for x in A]
A_add_count = []
A_add_ratio = []
add_count = 0
for i in A_count:
    add_count += i
    add_ratio = float("%.3f"%float(add_count/1444))
    A_add_count.append(add_count)
    A_add_ratio.append(add_ratio)
A_ratio = [float("%.3f"%float(x/1444)) for x in A_count]

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({'font.size': 20})

A = A
B = A_ratio
C = A_add_ratio
D = [str(x)+'%' for x in A]

plt.figure(figsize=(14, 6))

plt.bar(D[0], B[0], color='SteelBlue', alpha=1)
plt.bar(D[1:], B[1:], color='LightPink', alpha=1)

plt.plot(D, C, 'ro', markersize=3,alpha=1)
plt.plot(D, C, 'k-', linewidth=0.5, linestyle='dashed')

plt.xlim(-1,100)
plt.xticks(['1%','20%','40%','60%','80%','100%'])
plt.xlabel('RANK% of cognate antibody for each epitope')
plt.ylabel('Proportion of epitopes in each RANK%')
plt.rcParams['axes.facecolor'] = '#F2F2F2'

plt.savefig('Fig2e',dpi=300)
plt.show()