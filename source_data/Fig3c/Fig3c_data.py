# -*- coding: utf-8 -*-

fr = open('result_hiv_gp120_interval_simscore.txt')
lines = fr.readlines()
fr.close()

lines = [x.strip().split('\t') for x in lines]
need_list = sorted(lines, key=lambda x: x[1], reverse=True)
need_list = [[x[0],float("%.3f"%float(x[1])),x[2],float("%.3f"%float(x[3]))] for x in need_list]
need_list = [x for x in need_list if x[1]>0.5][:-3]

data = []
count = 0 
for i in need_list:
    if 0.5 < i[1] <= 0.6:
        data.append([i[3],"0.5~0.6"])
        count += 1
    elif 0.6 < i[1] <= 0.7:
        data.append([i[3],"0.6~0.7"])
    elif 0.7 < i[1] <= 0.8:
        data.append([i[3],"0.7~0.8"])
    elif 0.8 < i[1] <= 0.9:
        data.append([i[3],"0.8~0.9"])
    elif 0.9 <=i[1] <= 1.0:
        data.append([i[3],"0.9~1.0"])

fw = open('plotdata.txt','w+')
fw.write('CDR Similarity to the native antibody\tSESA Score Interval\n')
for i in data:
    fw.write(str(i[0])+'\t'+i[1]+'\n')
fw.close()


