# -*- coding: utf-8 -*-

import sys

jobid = sys.argv[4]
mypath = '../user_data/'+jobid+'/input_files/ag_pdb_file/'

AgPdbFilePath = sys.argv[1]
### Split Ag chain ###
ChainID = sys.argv[2]
fpdbraw = open(AgPdbFilePath,'r')
fpdbraw_lines = fpdbraw.readlines()
fpdbraw.close()

fpdbspilt = open(mypath+'antigen.pdb','w+')
for line in fpdbraw_lines:
    if line.startswith('ATOM') and line[21] == ChainID:
        fpdbspilt.write(line)
fpdbspilt.close()

### Split epitope ###
fantigen = open(mypath+'antigen.pdb','r')
fantigen_lines = fantigen.readlines()
fantigen.close()

episite = sys.argv[3]
episite = episite.split(',')

fepitope = open(mypath+'epitope.pdb','w+')

for line in fantigen_lines:
    resi = line[22:26].strip()
    if resi in episite:
        fepitope.write(line)
fepitope.close()


























