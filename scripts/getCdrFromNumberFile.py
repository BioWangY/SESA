# -*- coding: utf-8 -*-

######### IMGT H:27-38,56-65,105-117 ###############
import re
from collections import OrderedDict
def getHCdr(number_fpath,cdr_fpath):
    number_f = open(number_fpath)
    cdr_f = open(cdr_fpath,'w')
    line1 = number_f.readline().strip().split(',')
    bianhao = line1[13:]
    for line in number_f.readlines():
        line = line.strip().split(',')
        name = line[0]
        seqLi = line[13:]
        seq = ''.join(seqLi)
        seq = seq.replace('-','')
        bh_aa_dic = OrderedDict(zip(bianhao,seqLi))
        cdr1 = []
        cdr2 = []
        cdr3 = []
        for key,aa in bh_aa_dic.items():
            bh = re.sub("\D", "", key)
            if aa == '-':
                continue
            if 27<=int(bh)<=38:
                add = key+'|'+aa
                cdr1.append(add)
            if 56<=int(bh)<=65:
                add = key+'|'+aa
                cdr2.append(add)
            if 105<=int(bh)<=117:
                add = key+'|'+aa
                cdr3.append(add)
        cdrN = len(cdr1)+len(cdr2)+len(cdr3)
        cdr_f.write(name+'\t'+seq+'\t'+','.join(cdr1)+'\t'+','.join(cdr2)+'\t'+','.join(cdr3)+'\t'+str(cdrN)+'\n')
    number_f.close()
    cdr_f.close()

######### IMGT L:27-38,56-65,105-117 ###############
def getLCdr(number_fpath,cdr_fpath):
    number_f = open(number_fpath)
    cdr_f = open(cdr_fpath,'w')
    line1 = number_f.readline().strip().split(',')
    bianhao = line1[13:]
    for line in number_f.readlines():
        line = line.strip().split(',')
        name = line[0]
        seqLi = line[13:]
        seq = ''.join(seqLi)
        seq = seq.replace('-','')
        bh_aa_dic = OrderedDict(zip(bianhao,seqLi))
        cdr1 = []
        cdr2 = []
        cdr3 = []
        for key,aa in bh_aa_dic.items():
            bh = re.sub("\D", "", key)
            if aa == '-':
                continue
            if 27<=int(bh)<=38:
                add = key+'|'+aa
                cdr1.append(add)
            if 56<=int(bh)<=65:
                add = key+'|'+aa
                cdr2.append(add)
            if 105<=int(bh)<=117:
                add = key+'|'+aa
                cdr3.append(add)
        cdrN = len(cdr1)+len(cdr2)+len(cdr3)
        cdr_f.write(name+'\t'+seq+'\t'+','.join(cdr1)+'\t'+','.join(cdr2)+'\t'+','.join(cdr3)+'\t'+str(cdrN)+'\n')
    number_f.close()
    cdr_f.close()

def main(Hnumber_fpath,Lnumber_fpath,Hcdr_fpath,Lcdr_fpath):
    getHCdr(Hnumber_fpath,Hcdr_fpath)
    getLCdr(Lnumber_fpath,Lcdr_fpath)
 
