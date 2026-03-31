# -*- coding: utf-8 -*-
import os
from .utils import getPdbFile, readAaindexDict

def _get_epitope_aaindex_fingerprint(epitope, csv_path):
    RADIUS, STEP_LENGTH = 20, 2
    epitope_fp_list = []
    shell_ranges = [(x, x + STEP_LENGTH) for x in range(0, RADIUS, STEP_LENGTH)]
    Dict_names, Dict_list = readAaindexDict(csv_path)
    
    for aaindex_dict in Dict_list:
        for shell_range in shell_ranges:
            aaindex_sum = epitope.getAaindexWithinShell(shell_range, aaindex_dict, Ave=0)
            epitope_fp_list.append(f'{aaindex_sum:.4f}')
    return epitope_fp_list

def process_antigen(antigen_path, chain, sites_str, output_fp_path, aaindex_csv, temp_dir):
    episite = sites_str.split(',')
    temp_epitope_pdb = os.path.join(temp_dir, 'temp_epitope.pdb')
    
    with open(antigen_path, 'r') as f_in, open(temp_epitope_pdb, 'w') as f_out:
        for line in f_in:
            if line.startswith('ATOM') and line[21] == chain:
                resi = line[22:26].strip()
                if resi in episite:
                    f_out.write(line)
                    
    epitope = getPdbFile(temp_epitope_pdb)
    epitope_fp_list = _get_epitope_aaindex_fingerprint(epitope, aaindex_csv)
    
    agfname = os.path.basename(antigen_path)
    with open(output_fp_path, 'w') as f:
        f.write(f"{agfname}\t{','.join(epitope_fp_list)}\n")