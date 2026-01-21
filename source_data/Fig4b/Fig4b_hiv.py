# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
from scipy.stats import spearmanr
import math
import matplotlib

th = 0.2

large_ls = []
for i in os.listdir('./pred_results_final_hiv/'):
    with open('./pred_results_final_hiv/'+i) as file:
        lines = file.readlines()
    lines = [x.strip().split('\t') for x in lines]
    lines = lines[1:]
    for j in lines:
        large_ls.append([float(j[1]),float(j[2])])

part1 = []
part2 = []

for i in large_ls:
    if not i[1] == 1:
    
        if i[0] < th or i[1] == 0:
            part1.append(i)
        else:
            part2.append(i)

data1 = [x[0] for x in part1]
data2 = [x[1] for x in part1]

data3 = [x[0] for x in part2]
data4 = [x[1] for x in part2]

plt.figure(figsize=(6,6))
matplotlib.rcParams['font.family'] = 'Arial'
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.weight'] = 'bold'

plt.scatter(data1, data2, s=0.5, color="gray")
plt.scatter(data3, data4, s=0.5, color="blue")
plt.xlabel('SESA Score',fontsize=14,weight='bold')
plt.ylabel('Epitope Overlapping Extent',fontsize=14,weight='bold')
plt.ylim(0,1.05)
plt.xlim(0,1.05)

plt.axvline(x=th, color='gray', linestyle='--', label=f'x={th}')

correlation = np.corrcoef(data3, data4)[0, 1]
print('Pearson correlation coefficien: ', correlation)
plt.text(0.5, 0.15, f'Pearson Corr: {correlation:.3f}', fontsize=14, color='black')

plt.plot(np.unique(data3), np.poly1d(np.polyfit(data3, data4, 1))(np.unique(data3)), color='gray', label=f'Pearson Trendline (corr={correlation:.3f})')

testframeposition = 0.6
x = [testframeposition, 1.0, 1.0, testframeposition, testframeposition]
y = [testframeposition, testframeposition, 1.0, 1.0, testframeposition]
plt.plot(x, y, color='darkred', linewidth=2)

rho, p_value = stats.spearmanr(data3, data4)
print("Spearman Correlation：", rho)
print("P value：", p_value)
plt.text(0.5, 0.1, f'Spearman Corr: {rho:.3f}', fontsize=14, color='black')
plt.text(0.5, 0.05, 'P value < 0.001', fontsize=14, color='black')
plt.text(0.7, 0.3, 'GP160', fontsize=20, color='black')
plt.savefig('Fig4b_hiv.png',dpi=200)
plt.show()
