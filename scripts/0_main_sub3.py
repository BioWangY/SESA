#!/usr/bin/python3
# -*- coding: utf-8 -*-

import predictAndRank
import os
import sys

### The submitted parameters ###
jobid = sys.argv[1]         # jobid
SubAgPdbName = sys.argv[2]  # your/path/to/antigen.pdb
EpitopeChain = sys.argv[3]  # name of the antigen chain (0-9，a-z，A-Z)
EpitopeSite = sys.argv[4]   # epitope resi, e.g. 119,120,122,200,202,203,419,421,422,423,434,437
ImmuneHost = sys.argv[5]    # immune host，choose from: 'Homo','Mus', and 'Unspecified'
HeavyChainFastaName = sys.argv[6]  # your/path/to/abheavychains.fasta
LightChainFastaName = sys.argv[7]  # your/path/to/ablightchains.fasta

### Use this script to query the user-defined antibody CDR sequence library. ###
SubAgPdbPath = '../user_data/'+jobid+'/input_files/ag_pdb_file/'+SubAgPdbName  
AgInput2_ls = [SubAgPdbPath,EpitopeChain,EpitopeSite]
AbInput3_ls = ['../user_data/'+jobid+'/input_files/ab_seq_file_path/'+HeavyChainFastaName,
               '../user_data/'+jobid+'/input_files/ab_seq_file_path/'+LightChainFastaName]

### step1: Input antigen information to obtain epitope fingerprints. ###
os.system('python ./1_AgInputType2.py '+AgInput2_ls[0]+' '+AgInput2_ls[1]+' '+AgInput2_ls[2]+' '+jobid)
os.system('python ./2_getEpiFp.py '+jobid)

### step2: Input antibody information to obtain cdr fingerprints. ###
ModelType = 'sequence'
os.system('python ./3_AbInputType3.py '+AbInput3_ls[0]+' '+AbInput3_ls[1]+' '+jobid)

### step3: choose immune host ###
if ImmuneHost == 'Homo':
    modelPath = '../models/model_abstructure_homo.model'
elif ImmuneHost == 'Mus':
    modelPath = '../models/model_abstructure_mus.model'
else:
    modelPath = '../models/model_abstructure_main.model'

### step4: pred and rank ###
proFopath = '../user_data/'+jobid+'/output_files/pred_result.txt'
epiFinFopath = '../user_data/'+jobid+'/calculate_files/EpitopeFingerPrint.txt'
cdrFinFopath = '../user_data/'+jobid+'/calculate_files/CDRFingerPrint.txt'
predictAndRank.predictAndRank(modelPath,epiFinFopath,cdrFinFopath,proFopath)