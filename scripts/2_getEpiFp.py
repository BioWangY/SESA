# -*- coding: utf-8 -*-
from math import sqrt
import os, gc
import sys

def usage():
    print("To get fingerprint of epitope pdb file.\n")

class Atom:
    def __init__(self, atom_id, atom_type, resi_id = None, coord = [0., 0., 0.]):
        self.id = atom_id
        self.type = atom_type
        self.resi = resi_id
        self.coord = coord
        self.x, self.y, self.z = self.coord
    def __str__(self):
        return "atom %d: %s" % (self.id, str(self.coord))
    __repr__ = __str__

class Residue:
    atom_list = []
    aa_dict = {
    'GLY': 'G', 'SER': 'S', 'ALA': 'A', 'THR': 'T', 'VAL': 'V',\
    'ILE': 'I', 'LEU': 'L', 'TYR': 'Y', 'PHE': 'F', 'HIS': 'H',\
    'PRO': 'P', 'ASP': 'D', 'MET': 'M', 'GLU': 'E', 'TRP': 'W',\
    'LYS': 'K', 'CYS': 'C', 'ARG': 'R', 'ASN': 'N', 'GLN': 'Q','UNK':'U'}
    def __init__(self, resi_id, aa_type = None, chain = None, coord = [0., 0., 0.]):
        self.id = resi_id
        self.aa_type = self.aa_dict[aa_type]
        self.chain = chain
        self.coord = coord
    def addAtom(self, atom):
        self.atom_list.append(atom)
    def calResiCoord(self):
        atom_num = 0.
        x, y, z = 0, 0, 0
        for atom in self.atom_list:
            atom_num += 1
            x += atom.x
            y += atom.y
            z += atom.z
        x /= atom_num
        y /= atom_num
        z /= atom_num
        self.coord = [x, y, z]
    def getCoord(self):
        return self.coord
    def getAatype(self):
        return self.aa_type
    def clear(self):
        self.atom_list = []
    def __str__(self):
        return "residue %s %s: %s" % (self.id, self.aa_type, str(self.coord))
    __repr__ = __str__

class Epitope:
    """can be class for epitope or paratope"""
    aa_20 = 'ARNDCQEGHILKMFPSTWYV'
    resi_list = []
    def __init__(self,  coord = [0, 0, 0]):
        #self.id = pdb_id + '_' + abag_type
        self.coord = coord
    def addResi(self, resi):
        self.resi_list.append(resi)
    def calEpitopeCoord(self):
        resi_num = 0.
        x, y, z = 0, 0, 0
        for resi in self.resi_list:
            resi_num += 1
            resi.x, resi.y, resi.z = resi.getCoord()
            x += resi.x
            y += resi.y
            z += resi.z
        x /= resi_num
        y /= resi_num
        z /= resi_num
        self.coord = [x, y, z]        
    def getCoord(self):
        return self.coord
    def dist(self, other_coord):
        """get distance with any object (atom, residue...) having a coord"""
        x0, y0, z0 = self.coord
        x1, y1, z1 = other_coord.getCoord()
        return sqrt((x0 - x1)**2 + (y0 - y1)**2 + (z0 - z1)**2)
    
    def getAaindexWithinShell(self, shell_range, aaindex_dict, Ave = 0):
        if self.resi_list == []:
            return 0
        aaindex_sum = 0.
        aa_count = 0.
        for resi in self.resi_list:
            min_range = min(shell_range)
            max_range = max(shell_range)
            if min_range < self.dist(resi) <= max_range: 
                aa_count += 1
                aa_type = resi.getAatype()
                if aa_type in self.aa_20:
                    aaindex_sum += aaindex_dict[aa_type]
        if Ave == 0:
            return aaindex_sum
        else:
            if aa_count == 0:
                return aaindex_sum
            return aaindex_sum/aa_count
    def getAatypeWithinShell(self, shell_range, need_aa_type):
        """get a kind of aa type number within a given shell range"""
        if self.resi_list == []:
                return 0
        need_aa_type_num = 0.
        for resi in self.resi_list:
            min_range = min(shell_range)
            max_range = max(shell_range)
            if min_range < self.dist(resi) <= max_range: 
                aa_type = resi.getAatype()
                if aa_type == need_aa_type:
                    need_aa_type_num += 1
        return need_aa_type_num
    def clear(self):
        self.resi_list = []
    def getResiList(self):
        resi_ids = []
        for resi in self.resi_list:
            resi_ids.append(resi.id)
        return resi_ids
            
def readAaindexDict(csv_path):
    """ read aaindex files and normalize them """
    aa_20 = 'ARNDCQEGHILKMFPSTWYV'
    origin_Dict_list = []
    Dict_names = []
    dict_num = -1
    f = open(csv_path)
    while 1:
        line = f.readline()
        if not line:
            break
        if line.startswith('#'):
            aaindex = line.strip().split(',')[0][1:]
            line = f.readline()
            idname = line.strip().split(',')[0]
            Dict_names.append(aaindex + '_' + idname)
            dict_num += 1
            Dict = {}
        else:
            aaindex_list = [float(val) for val in line.strip().split(',')]
            for i in range(20):
                Dict[aa_20[i]] = aaindex_list[i]
            origin_Dict_list.append(Dict.copy())
    f.close()
    return Dict_names, origin_Dict_list

def getPdbFile(pdbpath):
    fobj = open(pdbpath)
    #filename = os.path.basename(pdbpath)
    #pdb_id, agab_type = filename.split('_')
    epitope = Epitope()
    epitope.clear()
    pre_resi_id = ""
    iter_num = 0
    while 1:
        line = fobj.readline()
        
        if not line:
            residue.calResiCoord()  #notice!
            epitope.addResi(residue)
            break
        if not line.startswith('ATOM'):
            continue
        resi_id = line[22:30].strip()
        aa_type = line[17:20].strip()        
        atom_id = line[7:11].strip() 
        atom_type = line[13:16].strip()
        atom_coord = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
        if resi_id == pre_resi_id:
            atom = Atom(atom_id, atom_type, resi_id, atom_coord)
            residue.addAtom(atom)
        else:
            if iter_num != 0:
                residue.calResiCoord()
                epitope.addResi(residue)
            residue = Residue(resi_id, aa_type)
            residue.clear()
            atom = Atom(atom_id, atom_type, resi_id, atom_coord)
            residue.addAtom(atom)
            pre_resi_id = resi_id
            iter_num += 1
    fobj.close()
    epitope.calEpitopeCoord()
    return epitope

def getEpitopeAaindexFingerprint(epitope, csv_path, Ave = 0):
    RADIUS = 20
    STEP_LENGTH = 2
    epitope_fp_list = []
    shell_ranges = [(x, x + STEP_LENGTH) for x in range(0, RADIUS, STEP_LENGTH)]
    Dict_names, Dict_list = readAaindexDict(csv_path)
    for idx in range(len(Dict_names)):
        aaindex_dict = Dict_list[idx]
        for shell_range in shell_ranges:
            aaindex_sum = epitope.getAaindexWithinShell(shell_range, aaindex_dict, Ave)
            epitope_fp_list.append('%.4f' % aaindex_sum)
    return epitope_fp_list

def main(aaindexf,epitope_pdb_path,epitopeFingerFopath):
    epitopeFingerFo = open(epitopeFingerFopath,'a+')
    agfname = os.path.basename(epitope_pdb_path)
    epitope = getPdbFile(epitope_pdb_path)
    epitope_fp_list = getEpitopeAaindexFingerprint(epitope, aaindexf, Ave = 0)
    epitopeFingerFo.write(agfname+'\t'+','.join(epitope_fp_list) + '\n')
    del epitope
    gc.collect()               
    epitopeFingerFo.close()    

jobid = sys.argv[1]
aaindexf = '../bin/usedAAindex.csv'
epitope_pdb_path = '../user_data/'+jobid+'/input_files/ag_pdb_file/epitope.pdb'
epitopeFingerFopath = '../user_data/'+jobid+'/calculate_files/EpitopeFingerPrint.txt'
main(aaindexf,epitope_pdb_path,epitopeFingerFopath)

    
    