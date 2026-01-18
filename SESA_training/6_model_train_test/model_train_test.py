# -*- coding: utf-8 -*-
'''
This code is used for model construction and model validation.
'''

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn import metrics
import random
import time

A = time.time()
random.seed(326)

############## Step 1: Expand positive samples
# traindata_path = '../3_get_key_and_met_train/aaindex_training_data_pos_neg.txt'
# data = np.loadtxt(traindata_path, delimiter = ',')
# choice_pos_sample = []
# X = data
# training_pos_complex_number = 2165
# pos_sample = X[:training_pos_complex_number,:]
# neg_sample = X[training_pos_complex_number:,:]
# for i in range(training_pos_complex_number*10):
#     idx = random.randint(0,training_pos_complex_number-1)
#     choice_pos_sample.append(pos_sample[idx])
# all_sample = np.vstack((choice_pos_sample,neg_sample))
# print(all_sample.shape)
# np.savetxt('./expanded_training_data_pos_neg.csv', all_sample, fmt = '%.4f', delimiter = ',')


############## Step 2: Import data
f2=open('../5_get_key_and_met_test/aaindex_testing_data_pos_neg.txt')
test=pd.read_csv(f2,header=None)
f3=open('./expanded_training_data_pos_neg.csv')
train2=pd.read_csv(f3,header=None)

key_list = []
key_list_f = open('../5_get_key_and_met_test/aaindex_testing_data_pos_neg_key.txt')
for line in key_list_f.readlines():
    line = line.strip()
    key_list.append(line)
key_list_f.close()

x = train2[train2.columns[:-1]]
y = train2[train2.columns[-1]]

test_x = test[test.columns[:-1]]
test_y = test[test.columns[-1]]

## Step 3: Parameter Optimization
# Here, we traverse and tune n_estimators, max_depths, min_samples_splits, and min_samples_leafs.
# The optimal parameters are used for model construction in the next step.

## Step 4: model construction
rf = RandomForestClassifier(n_estimators=2000,max_depth=60,
                            min_samples_split=5,min_samples_leaf=1,
                            bootstrap=True,max_features='sqrt',random_state=1)
rf.fit(x,y)
model_path = './test.model'
joblib.dump(rf,model_path)

## Step 5: model validation
prob = rf.predict_proba(test_x)
label = rf.predict(test_x)
test_auc = metrics.roc_auc_score(test_y,prob[:,1])
print(test_auc)