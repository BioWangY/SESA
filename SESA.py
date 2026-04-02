# -*- coding: utf-8 -*-

import argparse
import os
import tempfile
import sys

from sesa_core.antigen import process_antigen
from sesa_core.antibody import process_antibody
from sesa_core.predictor import predict_and_rank

def main():
    parser = argparse.ArgumentParser(description="SESA: Screening Epitope-Specific Antibodies.")
    
    parser.add_argument("-ag", "--antigen", required=True, help="Path to your antigen.pdb file")
    parser.add_argument("-c", "--chain", required=True, help="Epitope chain name (e.g., 'A')")
    parser.add_argument("-s", "--sites", required=True, help="Comma-separated epitope residues (e.g., '119,120')")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2, 3], required=True, 
                        help="Mode 1: Built-in lib | Mode 2: User CDR pdb zip | Mode 3: User Fab fasta")
    parser.add_argument("-o", "--output", required=True, help="Path to save the final prediction result (e.g., ./result.tsv)")
    
    parser.add_argument("--host", default="Unspecified", choices=['Homo', 'Mus', 'Unspecified'], 
                        help="Immune host (default: Unspecified)")
    parser.add_argument("--ab_zip", help="Path to CDR structure .zip (Required for Mode 2)")
    parser.add_argument("--heavy", help="Path to Heavy Chain Fasta (Required for Mode 3)")
    parser.add_argument("--light", help="Path to Light Chain Fasta (Required for Mode 3)")
    
    args = parser.parse_args()

    if args.mode == 2 and not args.ab_zip:
        parser.error("Mode 2 requires --ab_zip argument.")
    if args.mode == 3 and not (args.heavy and args.light):
        parser.error("Mode 3 requires both --heavy and --light arguments.")

    print(f"--- Starting SESA Pipeline (Mode: {args.mode}) ---")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.mode in [1, 2]:
        model_name = {
            'Homo': 'model_abstructure_homo.model',
            'Mus': 'model_abstructure_mus.model',
            'Unspecified': 'model_abstructure_main.model'
        }[args.host]
    else:
        model_name = {
            'Homo': 'model_abseq_homo.model',
            'Mus': 'model_abseq_mus.model',
            'Unspecified': 'model_abseq_main.model'
        }[args.host]
    
    selected_model = os.path.join(base_dir, 'models', model_name)
    aaindex_csv = os.path.join(base_dir, 'sesa_core', 'data', 'usedAAindex.csv')
    precalc_lib = os.path.join(base_dir, 'sesa_core', 'data', 'structure_cdr_lib_AAindex.txt')

    if not os.path.exists(selected_model):
        print(f"[Error] Model file not found: {selected_model}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        epi_fp_path = os.path.join(temp_dir, 'EpitopeFingerPrint.txt')
        cdr_fp_path = os.path.join(temp_dir, 'CDRFingerPrint.txt')

        print("Processing Antigen and calculating Epitope Fingerprints...")
        process_antigen(args.antigen, args.chain, args.sites, epi_fp_path, aaindex_csv, temp_dir)

        print("Processing Antibodies and calculating CDR Fingerprints...")
        process_antibody(args.mode, cdr_fp_path, aaindex_csv, precalc_lib, temp_dir, 
                         ab_zip=args.ab_zip, heavy=args.heavy, light=args.light)

        print(f"Generating predictions using '{model_name}'...")

        out_dir = os.path.dirname(os.path.abspath(args.output))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        
        predict_and_rank(selected_model, epi_fp_path, cdr_fp_path, args.output)
        
    print(f"Done! Results successfully saved to: {os.path.abspath(args.output)}")

if __name__ == '__main__':
    main()