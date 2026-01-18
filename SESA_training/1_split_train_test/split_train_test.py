'''
This code is used for randomly splitting the training set and the test set. We limited the 
sampling size according to the data scale to ensure that the proportions of complexes from 
different antigen families in the training and test sets remain balanced.
'''

import random
from random import sample

random.seed(326)

fr = open('info_final_need.txt','r')
lines = fr.readlines()
fr.close()

fw1 = open('Training_set_pos_ls.txt','w+')
fw2 = open('Independent_test_set_pos_ls.txt','w+')

IVA_set = []
HIV_set = []
SARS2_set = []
Other_set = []

for i in lines:
    agtype = i.strip().split('\t')[2]
    if agtype == 'IVA':
        IVA_set.append(i)
    elif agtype == 'HIV':
        HIV_set.append(i)
    elif agtype == 'SARS2':
        SARS2_set.append(i)
    elif agtype == 'Other':
        Other_set.append(i)
    
IVA_train_set = sample(IVA_set,136)
IVA_independent_test_set = []
for j in IVA_set:
    if not j in IVA_train_set:
        IVA_independent_test_set.append(j)

HIV_train_set = sample(HIV_set,276)
HIV_independent_test_set = []
for j in HIV_set:
    if not j in HIV_train_set:
        HIV_independent_test_set.append(j)

SARS2_train_set = sample(SARS2_set,360)
SARS2_independent_test_set = []
for j in SARS2_set:
    if not j in SARS2_train_set:
        SARS2_independent_test_set.append(j)

Other_train_set = sample(Other_set,1393)
Other_independent_test_set = []
for j in Other_set:
    if not j in Other_train_set:
        Other_independent_test_set.append(j)

train_set = IVA_train_set+HIV_train_set+SARS2_train_set+Other_train_set
independent_test_set = IVA_independent_test_set+HIV_independent_test_set+\
                       SARS2_independent_test_set+Other_independent_test_set

train_set.sort()
independent_test_set.sort()

for x in train_set:
    fw1.write(x)
for y in independent_test_set:
    fw2.write(y)

fw1.close()
fw2.close()