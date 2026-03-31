# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import joblib

def predict_and_rank(model_path, epi_fp_path, ab_fp_path, output_path):
    model = joblib.load(model_path)
    
    with open(epi_fp_path, 'r') as f:
        line = f.readline().strip().split('\t')
        epi_fp = np.fromstring(line[1], sep=',', dtype=float)

    ab_df = pd.read_csv(ab_fp_path, sep='\t', header=None, names=['ab_name', 'ab_fp'])
    ab_fps = np.array([np.fromstring(fp, sep=',', dtype=float) for fp in ab_df['ab_fp']])
    
    epi_fps_repeated = np.tile(epi_fp, (ab_fps.shape[0], 1))
    X_input = np.hstack((epi_fps_repeated, ab_fps))
    
    probabilities = model.predict_proba(X_input)[:, 1]
    
    result_df = pd.DataFrame({
        'Rank': 0,
        'Antibody': ab_df['ab_name'],
        'Score': np.round(probabilities, 3)
    })
    
    result_df = result_df.sort_values(by='Score', ascending=False).reset_index(drop=True)
    result_df['Rank'] = result_df.index + 1
    
    result_df.to_csv(output_path, sep='\t', header=True, index=False)