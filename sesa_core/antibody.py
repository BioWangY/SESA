# -*- coding: utf-8 -*-
import os, shutil, subprocess, zipfile, re, json
from collections import OrderedDict
from .utils import getPdbFile, readAaindexDict
from .antigen import _get_epitope_aaindex_fingerprint

def _parse_imgt_csv(number_fpath):
    parsed_data = []
    with open(number_fpath, 'r') as f:
        lines = f.readlines()
        if not lines: return parsed_data
        bianhao = lines[0].strip().split(',')[13:]
        for line in lines[1:]:
            line_parts = line.strip().split(',')
            name, seqLi = line_parts[0], line_parts[13:]
            bh_aa_dic = OrderedDict(zip(bianhao, seqLi))
            
            cdr1, cdr2, cdr3 = [], [], []
            for key, aa in bh_aa_dic.items():
                if aa == '-': continue
                bh = int(re.sub(r"\D", "", key))
                add = f"{key}|{aa}"
                if 27 <= bh <= 38: cdr1.append(add)
                elif 56 <= bh <= 65: cdr2.append(add)
                elif 105 <= bh <= 117: cdr3.append(add)
            parsed_data.append((name, cdr1, cdr2, cdr3))
    return parsed_data

def _get_ab_shell(len_H, len_L):
    if len_H <= 24:
        h_key = "H<=24"
    elif 25 <= len_H <= 35:
        h_key = "25<=H<=35"
    else:
        h_key = "36<=H"

    if len_L <= 17:
        l_key = "L<=17"
    elif 18 <= len_L <= 23:
        l_key = "18<=L<=23"
    else:
        l_key = "24<=L"

    dict_key = f"{h_key}_{l_key}"
    
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'ab_shells.json')
    with open(json_path, 'r') as f:
        shells_dict = json.load(f)

    return shells_dict[dict_key]

def _calc_seq_fingerprint(h_cdrs, l_cdrs, dict_list):
    ab_shell_li = _get_ab_shell(len(h_cdrs), len(l_cdrs))
    H_dic = {k: v for k, v in (item.split('|') for item in h_cdrs)}
    L_dic = {k: v for k, v in (item.split('|') for item in l_cdrs)}
    
    all_shell_aa_li = []
    for shell_H, shell_L in ab_shell_li:
        shell_aa = []
        for site in map(str, shell_H):
            if site in H_dic: shell_aa.append(H_dic[site])
        for site in map(str, shell_L):
            if site in L_dic: shell_aa.append(L_dic[site])
        all_shell_aa_li.append(shell_aa)
        
    allAAindex_shellValue = []
    for aaindex_dict in dict_list:
        for shell_aa in all_shell_aa_li:
            score = sum(aaindex_dict.get(aa, 0.) for aa in shell_aa)
            allAAindex_shellValue.append(f'{score:.4f}')
    return allAAindex_shellValue

def process_antibody(mode, output_fp_path, aaindex_csv, precalc_lib, temp_dir, ab_zip=None, heavy=None, light=None):
    if mode == 1:
        shutil.copy(precalc_lib, output_fp_path)
        
    elif mode == 2:
        ab_struct_dir = os.path.join(temp_dir, 'ab_structs')
        os.makedirs(ab_struct_dir, exist_ok=True)
        with zipfile.ZipFile(ab_zip, 'r') as zip_ref:
            zip_ref.extractall(ab_struct_dir)
            
        with open(output_fp_path, 'w') as f_out:
            for pdb_file in os.listdir(ab_struct_dir):
                if not pdb_file.endswith('.pdb'): continue
                cdr_path = os.path.join(ab_struct_dir, pdb_file)
                epitope = getPdbFile(cdr_path)
                fp_list = _get_epitope_aaindex_fingerprint(epitope, aaindex_csv)
                f_out.write(f"{pdb_file}\t{','.join(fp_list)}\n")
                
    elif mode == 3:
        h_out = os.path.join(temp_dir, 'heavy_imgt')
        l_out = os.path.join(temp_dir, 'light_imgt')
        
        subprocess.run(['ANARCI', '-i', heavy, '--scheme', 'imgt', '--restrict', 'heavy', '--outfile', h_out, '--csv', '--ncpu', '5'], check=True)
        subprocess.run(['ANARCI', '-i', light, '--scheme', 'imgt', '--restrict', 'light', '--outfile', l_out, '--csv', '--ncpu', '5'], check=True)
        
        h_data = _parse_imgt_csv(h_out + '_H.csv')
        l_data = _parse_imgt_csv(l_out + '_KL.csv')
        
        _, origin_Dict_list = readAaindexDict(aaindex_csv)
        l_dict = {item[0]: (item[1] + item[2] + item[3]) for item in l_data}
        
        with open(output_fp_path, 'w') as f_out:
            for name, h1, h2, h3 in h_data:
                if name in l_dict:
                    h_cdrs = h1 + h2 + h3
                    l_cdrs = l_dict[name]
                    fp_list = _calc_seq_fingerprint(h_cdrs, l_cdrs, origin_Dict_list)
                    f_out.write(f"{name}\t{','.join(fp_list)}\n")