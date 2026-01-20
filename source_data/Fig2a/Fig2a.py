# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Fig2a_data.csv')
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))
plt.gca().set_facecolor('#f0f0f0')
sns.kdeplot(data=df[df['real_label'] == 1]['prob'], linewidth=3,
            color='SteelBlue', shade=True, label='positive samples')
sns.kdeplot(data=df[df['real_label'] == 0]['prob'], linewidth=3,
            color='LightPink', shade=True, label='negative samples')
ps_socres = list(df[df['real_label'] == 1]['prob'])
ns_scores = list(df[df['real_label'] == 0]['prob'])
from scipy import stats
t_statistic, p_value = stats.ttest_ind(ps_socres, ns_scores)
print("T-statistic:", t_statistic)
print("P-value:", p_value)

plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.rcParams.update({'font.family': 'Arial'})
plt.axvline(0.155,color='gray',linestyle='dashed')
plt.text(0.17,6,'x = 0.155',fontsize=20)
plt.grid(False)
plt.xlim(0, 1)
plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
plt.tick_params(axis='x', direction='out', which='both', bottom=True, top=False)
plt.tick_params(axis='y', direction='out', which='both', left=True, right=False)
plt.xlabel('SESA Score', fontsize=20)
plt.ylabel('Density value', fontsize=20)
plt.title('Kernel Density Estimation Plot of SESA scores\non Independent Validation Data Set',
          fontsize=20,loc='center', pad = 5)
plt.legend(loc='upper right',fontsize=20)
plt.rcParams['axes.facecolor'] = 'lightgrey'
plt.savefig('./Fig2a.png',dpi=200)
plt.show()

