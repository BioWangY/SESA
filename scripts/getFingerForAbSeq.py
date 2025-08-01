# -*- coding: utf-8 -*-

from collections import OrderedDict    
def readAaindexDict(csv_path):
    " read aaindex files and normalize them "
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

def getAAindexDict(aaindexf):
    
    #function: for each aaindex, obtain aaindex standard value of each amino acid
    #:param aaindex_f: aaindex file
    #:return all_aaindex_standard_value_dict: {aaindex_name : {res_name:aaindex_standard_value}}
    
    #res_li = ['ALA','ARG','ASN','ASP','CYS','GLN','GLU','GLY','HIS','ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL']
    aa_20 = 'ARNDCQEGHILKMFPSTWYV'
    res_li = list(aa_20)
    all_aaindex_standard_value_dict = OrderedDict()  # aaindex_name : {res_name:index_value}
    f = open(aaindexf, 'r')
    for line in f.readlines()[1:]:
        res_aaindex_value_dict = {}
        line = line.strip()
        line = line.split("\t")
        aaindexName = line[0]
        for i in range(20):
            res_aaindex_value_dict[res_li[i]] = float(line[i+1])
        all_aaindex_standard_value_dict[aaindexName] = res_aaindex_value_dict
    f.close()
    return all_aaindex_standard_value_dict

def get_ab_shell(len_H,len_L):
    
    if len_H<=24 and len_L<=17:
        shell1 = [[], []]
        shell2 = [['107'], []]
        shell3 = [['38', '108', '115'], []]
        shell4 = [['37', '105', '106'], ['107']]
        shell5 = [['56', '57', '58', '116'], ['29', '56', '108', '109', '114', '115', '116']]
        shell6 = [['36', '64', '117'], ['38', '105', '106']]
        shell7 = [['28', '29', '30', '35', '59', '62', '65'], ['28', '37', '57', '117']]
        shell8 = [['63'], ['27', '65']]
        shell9 = [['27'], []]
        shell10 = [[], []]
    elif len_H<=24 and 18<=len_L<=23:
        shell1 = [[], []]
        shell2 = [['108'], ['107', '108', '109']]
        shell3 = [['38', '107', '114'], []]
        shell4 = [['115'], ['106', '110', '114']]
        shell5 = [['37', '105', '106', '116'], ['38', '113', '115', '116']]
        shell6 = [['36', '56', '57'], ['56', '105', '117']]
        shell7 = [['58', '64', '65', '117'], ['36', '37']]
        shell8 = [['28', '30', '35', '59', '62', '63'], ['29', '30', '35', '57']]
        shell9 = [['29'], ['28', '31', '65']]
        shell10 = [['27'], ['27']]
    elif len_H<=24 and 24<=len_L:
        shell1 = [[], []]
        shell2 = [[], []]
        shell3 = [['107', '115'], ['107']]
        shell4 = [['38'], ['38', '116']]
        shell5 = [['37', '105', '106', '116'], ['56', '105', '106', '108', '109', '114']]
        shell6 = [[], ['31', '115']]
        shell7 = [['28', '36', '56', '57', '58', '117'], ['29', '33', '34', '36', '37', '117']]
        shell8 = [['29', '30', '35', '59', '64', '65'], ['28', '30', '32', '57']]
        shell9 = [['27', '62', '63'], ['27', '35', '65']]
        shell10 = [[], []]
    elif 25<=len_H<=35 and len_L<=17:
        shell1 = [[], []]
        shell2 = [['107', '113'], []]
        shell3 = [['114'], ['107']]
        shell4 = [['38', '108', '109', '112A', '115'], []]
        shell5 = [['37', '105', '106', '110', '112', '116'], ['105', '116']]
        shell6 = [['56', '57', '117'], ['56', '106', '108', '109', '114', '115']]
        shell7 = [['36', '58', '64', '65', '111'], ['37', '38', '117']]
        shell8 = [['28', '29', '30', '35', '59', '62', '63'], ['29', '57']]
        shell9 = [[], ['65']]
        shell10 = [['27'], ['27', '28']]
    elif 25<=len_H<=35 and 18<=len_L<=23:
        shell1 = [[], []]
        shell2 = [['108', '109', '110', '113'], []]
        shell3 = [['107', '114', '115'], []]
        shell4 = [['38', '111', '112'], ['107', '116']]
        shell5 = [['57', '105', '106', '116'], ['38', '105', '115']]
        shell6 = [['37', '56', '117'], ['37', '106', '108', '114', '117']]
        shell7 = [['36', '58', '64', '65'], ['56']]
        shell8 = [['28', '29', '30', '35', '59', '63'], ['29', '30', '36', '57']]
        shell9 = [['27'], ['65']]
        shell10 = [[], ['27', '28']]
    elif 25<=len_H<=35 and 24<=len_L:
        shell1 = [[], []]
        shell2 = [['109', '112', '113'], []]
        shell3 = [['110', '114'], ['107']]
        shell4 = [['38', '107', '108', '115'], ['116']]
        shell5 = [['106'], ['38', '105', '108', '109', '114']]
        shell6 = [['36', '37', '57', '105', '116'], ['31', '56', '106', '115']]
        shell7 = [['56', '64', '117'], ['29', '34', '36', '37', '117']]
        shell8 = [['30', '35', '58', '65'], ['30', '33', '57']]
        shell9 = [['29', '59', '62', '63'], ['27', '28', '32', '35', '65']]
        shell10 = [['27', '28'], []]
    elif 36<=len_H and len_L<=17:
        shell1 = [[], []]
        shell2 = [['111A'], []]
        shell3 = [['38', '107'], []]
        shell4 = [['109', '111C', '113', '114'], ['107', '114']]
        shell5 = [['37', '56', '57', '106', '108', '110', '111B', '112B', '112A', '112', '115'], ['108', '115', '116']]
        shell6 = [['36', '58', '62', '64', '105', '111', '111D', '112E', '116'], ['105', '106', '109', '113']]
        shell7 = [['30', '35', '59', '63', '65', '112C'], ['27', '38', '56', '117']]
        shell8 = [['28', '29', '112D', '117'], ['28', '57']]
        shell9 = [[], ['65']]
        shell10 = [['27'], []]
    elif 36<=len_H and 18<=len_L<=23:
        shell1 = [[], []]
        shell2 = [['112A', '112', '113'], []]
        shell3 = [['110'], []]
        shell4 = [['109', '111', '112B', '114'], ['107']]
        shell5 = [['38', '107', '108', '111A', '112C'], ['38', '105', '114']]
        shell6 = [['64', '111B', '115'], ['56', '106', '109', '115', '116']]
        shell7 = [['56', '57', '106', '111C', '116'], ['36', '37', '57', '108', '113']]
        shell8 = [['37', '63', '65', '105', '111D', '111F', '112E', '112D', '117'], ['29', '112', '117']]
        shell9 = [['36', '58', '59'], ['28', '65', '110']]
        shell10 = [['30', '35', '111E', '112G', '112F'], ['27']]
    elif 36<=len_H and 24<=len_L:
        shell1 = [[], []]
        shell2 = [['112A', '112', '113'], []]
        shell3 = [['112C', '112B', '114'], []]
        shell4 = [['38', '107'], ['107']]
        shell5 = [['37', '106', '108', '109', '111', '112E', '112D', '115'], ['38', '56', '109', '116']]
        shell6 = [['35', '36', '57', '111A', '111B', '111D', '116'], ['36', '105', '106', '108', '114']]
        shell7 = [['56', '64', '105', '110', '117'], ['31', '37', '115', '117']]
        shell8 = [['30', '58', '59', '63', '65', '111C'], ['29', '30', '33', '34', '35', '57']]
        shell9 = [[], ['28', '32', '65']]
        shell10 = [['29'], ['27']]
    
    site_li = [shell1,shell2,shell3,shell4,shell5,shell6,shell7,shell8,shell9,shell10]
    return site_li

def getFingerprintForOneSeq(HCDRs,LCDRs,Dict_list):
    ### HCDRs:list,['31|S','32|Y',...]
    h_len = len(HCDRs)
    l_len = len(LCDRs)
    ab_shell_li = get_ab_shell(h_len,l_len)
    
    H_id_aa_dic = {}
    for id_aa in HCDRs:
        _id,aa = id_aa.split('|')
        H_id_aa_dic[_id]=[aa]
            
    L_id_aa_dic = {}
    for id_aa in LCDRs:
        _id,aa = id_aa.split('|')
        L_id_aa_dic[_id]=[aa]
       
    all_shell_aa_li = [] #10个列表，存储每层的氨基酸
    for shell in ab_shell_li:
        shell_H = shell[0]
        shell_L = shell[1]
        
        tmp_site_H = []
        for site in shell_H:                
            tmp_site_H.append(site)
        tmp_site_H = [str(site) for site in tmp_site_H]
        
        tmp_site_L = []        
        for site in shell_L:
            tmp_site_L.append(site)     
        tmp_site_L = [str(site) for site in tmp_site_L]
        
        shell_aa_li = []
        for site in tmp_site_H:
            if site in H_id_aa_dic.keys():
                aa_li = H_id_aa_dic[site]
                shell_aa_li.extend(aa_li)
        for site in tmp_site_L:
            if site in L_id_aa_dic.keys():
                aa_li = L_id_aa_dic[site]
                shell_aa_li.extend(aa_li)
        all_shell_aa_li.append(shell_aa_li)
    
    allAAindex_shellValue = []
    aa_20 = 'ARNDCQEGHILKMFPSTWYV'
    res_li = list(aa_20)
    for idx in range(len(Dict_list)):
        aaindex_value_dict = Dict_list[idx]
        aaindex_li = []
        for shell_aa_li in all_shell_aa_li:
            aaindex_sum = 0.        
            for aa in shell_aa_li:
                if aa in res_li:                    
                    aaindex_sum += aaindex_value_dict[aa]
            aaindex_li.append('%.4f' % aaindex_sum)
        allAAindex_shellValue.extend(aaindex_li)
    return allAAindex_shellValue

def main(aaindexf,Hcdr_fpath,Lcdr_fpath,abFinFoPath):
    Dict_names, origin_Dict_list = readAaindexDict(aaindexf)
    h_cdr_f = open(Hcdr_fpath)
    l_cdr_f = open(Lcdr_fpath)
    finger_f = open(abFinFoPath,'w+')
    H_name_cdrLi_dic = OrderedDict()
    L_name_cdrLi_dic = OrderedDict()
    for line1 in h_cdr_f.readlines():
        line1 = line1.strip().split('\t')
        h_name,h_seq,h_cdr1,h_cdr2,h_cdr3,h_num = line1
        name = h_name
        h_cdrLi = h_cdr1.split(',')+h_cdr2.split(',')+h_cdr3.split(',')
        while '' in h_cdrLi:
            h_cdrLi.remove('')
        H_name_cdrLi_dic[name] = h_cdrLi
    for line2 in l_cdr_f.readlines():
        line2 = line2.strip().split('\t')
        l_name,l_seq,l_cdr1,l_cdr2,l_cdr3,l_num = line2
        name = l_name
        l_cdrLi = l_cdr1.split(',')+l_cdr2.split(',')+l_cdr3.split(',')
        while '' in l_cdrLi:
            l_cdrLi.remove('')
        L_name_cdrLi_dic[name] = l_cdrLi
    for name in H_name_cdrLi_dic.keys():
        h_cdrLi = H_name_cdrLi_dic[name]
        l_cdrLi = L_name_cdrLi_dic[name]  
        allAAindex_shellValue = getFingerprintForOneSeq(h_cdrLi,l_cdrLi,origin_Dict_list)
        finger_f.write(name+'\t'+','.join(allAAindex_shellValue)+'\n')
    finger_f.close()

