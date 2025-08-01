# -*- coding: utf-8 -*-

from collections import OrderedDict
import numpy as np
import joblib

def str_list2num_list(str_list):
    return [float(x) for x in str_list]

def predictAndRank(modelPath,epiFinFopath,abFinFoPath,proFopath):
    model = joblib.load(modelPath)     
    epiFinF = open(epiFinFopath)
    abFinF = open(abFinFoPath)
    proFo = open(proFopath,'w+')
    epiFpDic = OrderedDict()
    abFpDic = OrderedDict()
    
    for line1 in epiFinF.readlines():
        line1 = line1.strip().split('\t')
        epiname = line1[0]
        epi_fp = line1[1].split(',')
        epiFpDic[epiname] = epi_fp
    for line2 in abFinF.readlines():
        line2 = line2.strip().split('\t')
        paraname = line2[0]
        para_fp = line2[1].split(',')
        abFpDic[paraname] =para_fp 
    
    epi,epi_fp = list(epiFpDic.items())[0]
    ab_prob_dic = {}
    tmp_X1 = []
    abls = []
    for ab,para_fp in abFpDic.items():        
        epi_para_fp = str_list2num_list(epi_fp+para_fp)
        tmp_X1.append(epi_para_fp)
        abls.append(ab)
    tmp_X1 = np.array(tmp_X1)
    proba = model.predict_proba(tmp_X1)
    prob = [x[1] for x in proba]
    
    for i in range(len(abls)):
        ab_prob_dic[abls[i]] = prob[i]
    sort_ab_prob = sorted(ab_prob_dic.items(),key=lambda x:x[1],reverse=True)    
    
    rank = 0
    for ab_prob in sort_ab_prob:  
        ab,prob = ab_prob
        rank += 1
        prob = "%.3f"%float(prob)
        proFo.write(str(rank)+'\t'+ab+'\t'+prob+'\n')
    
    epiFinF.close()
    abFinF.close()    
    proFo.close()