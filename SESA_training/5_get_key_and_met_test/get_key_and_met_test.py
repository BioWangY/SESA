# -*- coding: utf-8 -*-
"""
This code is used to generate the fingerprint matrix for the testing set data.
"""

fr1 = open('../4_gen_test_neg_data/Test_set_pos_part.txt','r').readlines()
fr2 = open('../4_gen_test_neg_data/Test_set_neg_part.txt','r').readlines()
fw = open('aaindex_testing_data_pos_neg_key.txt','w+')

for i in fr1:
    word = i.strip().split('\t')[1]+'>'+i.strip().split('\t')[0]+'\n'
    fw.write(word)
for i in fr2:
    word = i.strip().split('\t')[1]+'>'+i.strip().split('\t')[0]+'\n'
    fw.write(word)

fw.close()

agAAindex = open('../0_get_fingerprint_files/agAAindex.txt','r').readlines()
agAAindex_dict = {}
for i in agAAindex:
    a = i.strip().split('\t')[0][:-4]
    b = i.strip().split('\t')[1]
    agAAindex_dict[a] = b

cdrAAindex = open('../0_get_fingerprint_files/cdrAAindex.txt','r').readlines()
cdrAAindex_dict = {}
for i in cdrAAindex:
    a = i.strip().split('\t')[0][:-4]
    b = i.strip().split('\t')[1]
    cdrAAindex_dict[a] = b

keyfile = open('./aaindex_testing_data_pos_neg_key.txt','r').readlines()
keyfile_ls = [x.strip() for x in keyfile]

fw_fp = open('./aaindex_testing_data_pos_neg.txt','w+')
for m in range(len(keyfile_ls)):
    if m <= 1443:
        ag = keyfile_ls[m].split('>')[0]
        ab = keyfile_ls[m].split('>')[1]
        word = agAAindex_dict[ag]+','+cdrAAindex_dict[ab]+','+'1'+'\n'
        fw_fp.write(word)
    else:
        ag = keyfile_ls[m].split('>')[0]
        ab = keyfile_ls[m].split('>')[1]
        word = agAAindex_dict[ag]+','+cdrAAindex_dict[ab]+','+'0'+'\n'
        fw_fp.write(word)
fw_fp.close()