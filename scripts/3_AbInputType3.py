# -*- coding: utf-8 -*-

import sys,os
import getCdrFromNumberFile
import getFingerForAbSeq
import shutil

HeavyChainFasta = sys.argv[1]
LightChainFasta = sys.argv[2]
jobid = sys.argv[3]

os.system('ANARCI -i '+HeavyChainFasta+' --scheme imgt --restrict heavy --outfile ../user_data/'+jobid+'/input_files/ab_seq_file_path/heavy_imgt_result --csv --ncpu 5')
os.system('ANARCI -i '+LightChainFasta+' --scheme imgt --restrict light --outfile ../user_data/'+jobid+'/input_files/ab_seq_file_path/light_imgt_result --csv --ncpu 5')

# shutil.move('./heavy_imgt_result_H.csv','../user_data/'+jobid+'/input_files/ab_seq_file_path/heavy_imgt_result_H.csv')
# shutil.move('./light_imgt_result_KL.csv','../user_data/'+jobid+'/input_files/ab_seq_file_path/light_imgt_result_KL.csv')

Hnumber_fpath = '../user_data/'+jobid+'/input_files/ab_seq_file_path/heavy_imgt_result_H.csv'
Hcdr_fpath = '../user_data/'+jobid+'/calculate_files/ab_number_H_cdr.txt'
Lnumber_fpath = '../user_data/'+jobid+'/input_files/ab_seq_file_path/light_imgt_result_KL.csv'
Lcdr_fpath = '../user_data/'+jobid+'/calculate_files/ab_number_L_cdr.txt'
getCdrFromNumberFile.main(Hnumber_fpath,Lnumber_fpath,Hcdr_fpath,Lcdr_fpath)

abFinFoPath = '../user_data/'+jobid+'/calculate_files/CDRFingerPrint.txt'
aaindexf = '../bin/usedAAindex.csv'
getFingerForAbSeq.main(aaindexf,Hcdr_fpath,Lcdr_fpath,abFinFoPath)