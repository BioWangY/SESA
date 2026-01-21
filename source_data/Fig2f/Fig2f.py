# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 14:25:58 2024

@author: 92839
"""

fr1 = open("testdata_annotated.txt")
fr1_lines = fr1.readlines()
fr1.close()

antigen_pairdID_dict = {}
antigen_pairdID_dict['virus'] = []
antigen_pairdID_dict['mammal'] = []
antigen_pairdID_dict['cancer'] = []
antigen_pairdID_dict['cancerother'] = []
antigen_pairdID_dict['selfimmu'] = []
antigen_pairdID_dict['mammalother'] = []
antigen_pairdID_dict['other'] = []

fr1_lines = [x.strip().split('\t') for x in fr1_lines]
fr1_lines = fr1_lines[1:]
for i in fr1_lines:
    pairdID = i[0]
    antigen = i[5].lower()
    class1 = i[8].lower()
    class2 = i[9].lower()
    
    if class1 == 'virus':
        antigen_pairdID_dict['virus'].append(pairdID)
        if not antigen in antigen_pairdID_dict:
            antigen_pairdID_dict[antigen] = [pairdID]
        else:
            antigen_pairdID_dict[antigen].append(pairdID)
    
    elif class1 == 'mammal':
        antigen_pairdID_dict['mammal'].append(pairdID)
        
        if class2 == 'cancer':
            antigen_pairdID_dict['cancer'].append(pairdID)
            
            if not antigen == 'other':
                if not antigen in antigen_pairdID_dict:
                    antigen_pairdID_dict[antigen] = [pairdID]
                else:
                    antigen_pairdID_dict[antigen].append(pairdID)
            else:
                antigen_pairdID_dict['cancerother'].append(pairdID)
        
        elif class2 == 'selfimmu':
            antigen_pairdID_dict['selfimmu'].append(pairdID)
        
        else:
            antigen_pairdID_dict['mammalother'].append(pairdID)
    
    else:
        antigen_pairdID_dict['other'].append(pairdID)

fr = open('testdata_pdbid_index_rank_precent_score.txt','r')
lines = fr.readlines()
fr.close()

lines = [x.strip().split('\t') for x in lines]
lines = [[x[0],int(x[1]),int(x[2]),float(x[3]),float(x[4])] for x in lines]

top_rank_ls = [1,5,10,15,20,25,30]
top_rank_dict = {}
for i in top_rank_ls:
    top_rank_dict[i] = []

for i in lines:
    if i[2] <= 1:
        top_rank_dict[1].append(i[0])
    elif 1 < i[2] <= 5:
        top_rank_dict[5].append(i[0])
    elif 5 < i[2] <= 10:
        top_rank_dict[10].append(i[0])
    elif 10 < i[2] <= 15:
        top_rank_dict[15].append(i[0])
    elif 15 < i[2] <= 20:
        top_rank_dict[20].append(i[0])
    elif 20 < i[2] <= 25:
        top_rank_dict[25].append(i[0])
    elif 25 < i[2] <= 30:
        top_rank_dict[30].append(i[0])

ratio_ls = []
ratio_class_ls = []
add_ratio_ls = []
add_count = 0

add_ratio_virus_ls = []
add_virus_count = 0

add_ratio_cancer_ls = []
add_cancer_count = 0

nums = []

for i in top_rank_ls:
    add_count += len(top_rank_dict[i])
    ratio = len(top_rank_dict[i])/1444
    ratio = float("%.3f"%float(ratio))
    ratio_ls.append(ratio)
    
    add_ratio = add_count/1444
    add_ratio = float("%.3f"%float(add_ratio))
    add_ratio_ls.append(add_ratio)
    
    virus_num = 0
    cancer_num = 0
    all_num = 0
    
    for j in top_rank_dict[i]:
        
        all_num += 1
        
        if j in antigen_pairdID_dict['virus']:
            virus_num += 1
            add_virus_count += 1
            
            
        elif j in antigen_pairdID_dict['cancer']:
            cancer_num += 1
            add_cancer_count += 1
    
    add_ratio_virus = add_virus_count/716
    add_ratio_virus = float("%.3f"%float(add_ratio_virus))
    add_ratio_virus_ls.append(add_ratio_virus)
    
    add_ratio_cancer = add_cancer_count/245
    add_ratio_cancer = float("%.3f"%float(add_ratio_cancer))
    add_ratio_cancer_ls.append(add_ratio_cancer)
            
    print(i,all_num,virus_num,cancer_num)

    ratio_class_ls.append([float("%.3f"%float(all_num/1444)),float("%.3f"%float(virus_num/716)),float("%.3f"%float(cancer_num/245))])

import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体为Arial
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.dpi'] = 100

A = ["Top 1",'Top 2~5','Top 6~10','Top 11~15','Top 16~20','Top 21~25','Top 26~30']
B = ratio_ls

bars = ratio_class_ls

txtbars = [["{:.1f}%".format(y * 100) for y in x] for x in bars]


plt.figure(figsize=(14,8))

colors = ['#A6A9C8', '#F0B67F', '#D6E3F8']

num_groups = len(bars)
num_bars = len(bars[0])

bar_width = 0.8 / num_bars

index = np.arange(num_groups)

for i in range(num_bars):
    positions = index + i * bar_width
    heights = [bar[i] for bar in bars]
    plt.bar(positions, heights, width=bar_width, color=colors[i], label=f'Bar {i + 1}')
    
    # 在每个条形图的顶端标注数值
    for j, pos in enumerate(positions):
        if j == 0:
            continue
        else:
            plt.text(pos, heights[j], str(txtbars[j][i]), ha='center', va='bottom', size = 11, font = 'Arial')

plt.xticks(index + bar_width * (num_bars - 1) / 2, A)

x_index = np.arange(len(A))

C = add_ratio_ls
D = ["{:.1f}%".format(x * 100) for x in C]
plt.plot(A, C, 'o', color = '#A6A9C8', markersize=10, alpha=1)
plt.plot(A, C, color='black', linewidth=2, linestyle='dashed')
# 使用 plt.text 标注数值
for i in range(len(A)):
    plt.text(A[i], C[i]+0.01, D[i], ha='center', va='bottom', size = 12, font = 'Arial')

C = add_ratio_virus_ls
D = ["{:.1f}%".format(x * 100) for x in C]
plt.plot(x_index + bar_width, C, 'o', color = '#F0B67F', markersize=10, alpha=1)
plt.plot(x_index + bar_width, C, color='black', linewidth=2, linestyle='dashed')
# 使用 plt.text 标注数值
for i in range(len(A)):
    plt.text(x_index[i] + bar_width, C[i]+0.01, D[i], ha='center', va='bottom', size = 12, font = 'Arial')
    
C = add_ratio_cancer_ls
D = ["{:.1f}%".format(x * 100) for x in C]
plt.plot(x_index + 2 * bar_width, C, 'o', color = '#D6E3F8', markersize=10, alpha=1)
plt.plot(x_index + 2 * bar_width, C, color='black', linewidth=2, linestyle='dashed')
# 使用 plt.text 标注数值
for i in range(len(A)):
    plt.text(x_index[i] + 2 * bar_width, C[i]+0.01, D[i], ha='center', va='bottom', size = 12, font = 'Arial')

plt.xlabel('Ranking positions of cognate antibody for each epitope')
plt.ylabel('Proportion of epitopes in each rank')

plt.rcParams['axes.facecolor'] = '#F2F2F2'

plt.savefig('Fig2f.png', dpi = 200)
plt.show()

