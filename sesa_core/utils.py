# -*- coding: utf-8 -*-
import os
from math import sqrt

class Atom:
    def __init__(self, atom_id, atom_type, resi_id=None, coord=[0., 0., 0.]):
        self.id = atom_id
        self.type = atom_type
        self.resi = resi_id
        self.coord = coord
        self.x, self.y, self.z = self.coord

class Residue:
    aa_dict = {
        'GLY': 'G', 'SER': 'S', 'ALA': 'A', 'THR': 'T', 'VAL': 'V',
        'ILE': 'I', 'LEU': 'L', 'TYR': 'Y', 'PHE': 'F', 'HIS': 'H',
        'PRO': 'P', 'ASP': 'D', 'MET': 'M', 'GLU': 'E', 'TRP': 'W',
        'LYS': 'K', 'CYS': 'C', 'ARG': 'R', 'ASN': 'N', 'GLN': 'Q', 'UNK': 'U'}
    
    def __init__(self, resi_id, aa_type=None, chain=None, coord=[0., 0., 0.]):
        self.id = resi_id
        self.aa_type = self.aa_dict.get(aa_type, 'U')
        self.chain = chain
        self.coord = coord
        self.atom_list = []
        
    def addAtom(self, atom):
        self.atom_list.append(atom)
        
    def calResiCoord(self):
        if not self.atom_list: return
        x = sum(a.x for a in self.atom_list) / len(self.atom_list)
        y = sum(a.y for a in self.atom_list) / len(self.atom_list)
        z = sum(a.z for a in self.atom_list) / len(self.atom_list)
        self.coord = [x, y, z]

    def getCoord(self): return self.coord
    def getAatype(self): return self.aa_type

class Epitope:
    aa_20 = 'ARNDCQEGHILKMFPSTWYV'
    
    def __init__(self, coord=[0, 0, 0]):
        self.coord = coord
        self.resi_list = []
        
    def addResi(self, resi):
        self.resi_list.append(resi)
        
    def calEpitopeCoord(self):
        if not self.resi_list: return
        x, y, z = 0, 0, 0
        for resi in self.resi_list:
            resi.x, resi.y, resi.z = resi.getCoord()
            x += resi.x; y += resi.y; z += resi.z
        n = len(self.resi_list)
        self.coord = [x/n, y/n, z/n]
        
    def dist(self, other_coord):
        x0, y0, z0 = self.coord
        x1, y1, z1 = other_coord.getCoord()
        return sqrt((x0 - x1)**2 + (y0 - y1)**2 + (z0 - z1)**2)
    
    def getAaindexWithinShell(self, shell_range, aaindex_dict, Ave=0):
        if not self.resi_list: return 0
        aaindex_sum, aa_count = 0., 0.
        min_range, max_range = min(shell_range), max(shell_range)
        for resi in self.resi_list:
            if min_range < self.dist(resi) <= max_range:
                aa_count += 1
                aa_type = resi.getAatype()
                if aa_type in self.aa_20:
                    aaindex_sum += aaindex_dict.get(aa_type, 0)
        return aaindex_sum if Ave == 0 else (aaindex_sum / aa_count if aa_count > 0 else aaindex_sum)

def readAaindexDict(csv_path):
    aa_20 = 'ARNDCQEGHILKMFPSTWYV'
    origin_Dict_list, Dict_names = [], []
    with open(csv_path, 'r') as f:
        Dict = {}
        for line in f:
            if line.startswith('#'):
                parts = line.strip().split(',')
                aaindex = parts[0][1:]
                line = next(f)
                idname = line.strip().split(',')[0]
                Dict_names.append(aaindex + '_' + idname)
                Dict = {}
            else:
                aaindex_list = [float(val) for val in line.strip().split(',')]
                for i in range(20):
                    Dict[aa_20[i]] = aaindex_list[i]
                origin_Dict_list.append(Dict.copy())
    return Dict_names, origin_Dict_list

def getPdbFile(pdbpath):
    epitope = Epitope()
    pre_resi_id = ""
    residue = None
    with open(pdbpath, 'r') as fobj:
        for line in fobj:
            if not line.startswith('ATOM'): continue
            resi_id = line[22:30].strip()
            aa_type = line[17:20].strip()
            atom_id = line[7:11].strip()
            atom_type = line[13:16].strip()
            atom_coord = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
            
            if resi_id == pre_resi_id and residue:
                residue.addAtom(Atom(atom_id, atom_type, resi_id, atom_coord))
            else:
                if residue:
                    residue.calResiCoord()
                    epitope.addResi(residue)
                residue = Residue(resi_id, aa_type)
                residue.addAtom(Atom(atom_id, atom_type, resi_id, atom_coord))
                pre_resi_id = resi_id
        if residue:
            residue.calResiCoord()
            epitope.addResi(residue)
    epitope.calEpitopeCoord()
    return epitope