# -*- coding: utf-8 -*-

import sys,os

jobid = sys.argv[4]
mypath = '../user_data/'+jobid+'/input_files/ag_pdb_file/'

### Download pdb ###
try:
    PDBID = sys.argv[1]
    url = 'https://files.rcsb.org/download/' + PDBID + '.pdb'
    from urllib import request
    request.urlretrieve(url, mypath+PDBID+'.pdb')
except:
    try:
        PDBID = sys.argv[1]
        url = 'https://files.rcsb.org/download/' + PDBID + '.pdb'
        import requests
        with open(mypath+PDBID+'.pdb', 'wb') as code:
            code.write(requests.get(url).content)
    except:
        try:
            PDBID = sys.argv[1]
            url = 'https://files.rcsb.org/download/' + PDBID + '.pdb'
            import urllib3
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            with open(mypath+PDBID+'.pdb', 'wb') as code:
                code.write(r.data)
        except Exception as e:
            import time
            t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            t = str(t) + '-' + str(time.time()).split('.')[1][:3]
            f = open('../user_data/errors/download error '+t, 'w+')
            f.write(str(Exception)+'\n')
            f.write(str(e)+'\n')
            f.close()
            f = open('../user_data/errors/download error '+t, 'r')
            line1 = f.readline()
            line2 = f.readline()
            if line2.find('Permission denied') != -1:
                f.close()
                os.system('rm ../user_data/errors/download error '+t)
            else:
                f.close()

### Split Ag chain ###
ChainID = sys.argv[2]
fpdbraw = open(mypath+PDBID+'.pdb','r')
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


























