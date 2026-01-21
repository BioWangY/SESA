# -*- coding: utf-8 -*-

fr1 = open('mut_test1_results_seq_main.txt').readlines()
fr2 = open('mut_test2_results_seq_main.txt').readlines()
fr3 = open('mut_test3_results_seq_main.txt').readlines()

fr1 = [float(x.strip().split('\t')[2]) for x in fr1][1:]
fr2 = [float(x.strip().split('\t')[2]) for x in fr2][1:]
fr3 = [float(x.strip().split('\t')[2]) for x in fr3][1:]

import matplotlib.pyplot as plt
import seaborn as sns

def plot_score_density(list1, list2, list3, label1, label2, label3, title):

    plt.rcParams["font.family"] = ["Arial"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=(14, 4))
    
    sns.kdeplot(list1, label=label1, color="#1f77b4", fill=True, alpha=0.5, linewidth=2)
    sns.kdeplot(list2, label=label2, color="#ff7f0e", fill=True, alpha=0.5, linewidth=2)
    sns.kdeplot(list3, label=label3, color="lightgreen", fill=True, alpha=0.5, linewidth=2)
    
    plt.axvline(x=0.259, linestyle='--', color='red', alpha=0.7, linewidth=1.5)
    
    plt.gca().tick_params(axis='x', labelsize=16)
    plt.gca().tick_params(axis='y', labelsize=16)
    
    plt.title(title, fontsize=18, pad=20)
    plt.xlabel("SESA Score", fontsize=18)  
    plt.ylabel("Density", fontsize=18)
    plt.legend(fontsize=18)   
    plt.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()  
    
    plt.savefig('Fig6j.png', dpi=300)
    plt.show()

# 测试示例
if __name__ == "__main__":
    
    # 调用函数绘制密度图
    plot_score_density(
        list1=fr1,
        list2=fr2,
        list3=fr3,
        label1="mut_1aa (n=50)",
        label2="mut_2aa (n=1,225)",
        label3="mut_3aa (n=19,600)",
        title="Antibody virtual mutation test"
    )