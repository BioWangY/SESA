# -*- coding: utf-8 -*-

import shutil
import sys

jobid = sys.argv[1]

shutil.copy("../bin/structure_cdr_lib_AAindex.txt",'../user_data/'+jobid+'/calculate_files/CDRFingerPrint.txt')





