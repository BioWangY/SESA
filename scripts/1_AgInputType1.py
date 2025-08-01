# -*- coding: utf-8 -*-

import shutil,sys

AgPdbFilePath = sys.argv[1]
jobid = sys.argv[2]

shutil.copy(AgPdbFilePath,'../user_data/'+jobid+'/input_files/ag_pdb_file/epitope.pdb')


























