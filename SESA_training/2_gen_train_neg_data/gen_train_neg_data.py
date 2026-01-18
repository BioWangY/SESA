# -*- coding: utf-8 -*-
"""

This code is used to generate negative data and invokes the antigen similarity alignment tool CE-Blast.
For a given epitope, the CE-Blast epitope similarity between the epitope of its negative antibody and
the target epitope shall be less than 0.7.

Qiu T, Yang Y, Qiu J, Huang Y, Xu T, Xiao H, Wu D, Zhang Q, Zhou C, Zhang X, Tang K, Xu J, Cao Z.
CE-BLAST makes it possible to compute antigenic similarity for newly emerging pathogens.
Nat Commun. 2018 May 2;9(1):1772. doi: 10.1038/s41467-018-04171-2. PMID: 29720583; PMCID: PMC5932059.

Since the CE-Blast code is written based on Python 2, this script should also be executed in a Python 2 environment.

"""
import random
from random import choice
import os
from CEBLAST import get_sim_score as sscore

random.seed(326)

def sim_score(pdb1,pdb2):
    score1, score2, score3,div=sscore.get_similarity_score(pdb1, pdb2)
    sim_score = div
    return sim_score

fr = open('../1_split_train_test/Training_set_pos_ls.txt','r')
lines = fr.readlines()
fr.close()

fw1 = open('./Training_set_pos_part.txt','w+')
for i in lines:
    pair_id = i.strip().split('\t')[0]
    fw1.write(pair_id+'_ab'+'\t'+pair_id+'_ag'+'\t'+'POS'+'\n')
fw1.close()

fw2 = open('./Training_set_neg_part.txt','w+')
ag_pdb_path = '../0_get_fingerprint_files/ag_pdb_imgt/'

for i in lines:
    neg_ls = []
    i_pair_id = i.strip().split('\t')[0]
    i_sp = i.strip().split('\t')[2]
    
    while len(neg_ls) != 10:
        test = choice(lines)
        test_pair_id = test.strip().split('\t')[0]
        test_sp = test.strip().split('\t')[2]
        
        if not test == i:
            if (i_sp == test_sp == 'Other') or (i_sp != test_sp):
                i_test_sim_score = sim_score(ag_pdb_path+i_pair_id+'_ag.pdb',ag_pdb_path+test_pair_id+'_ag.pdb')
                if i_test_sim_score < 0.7:
                    neg_ls.append(test_pair_id)
    
    for j in neg_ls:
        word = j+'_ab'+'\t'+i_pair_id+'_ag'+'\t'+'NEG'+'\n'
        fw2.write(word)
        print j+'_ab'+'\t'+i_pair_id+'_ag'+'\t'+'NEG'
fw2.close()