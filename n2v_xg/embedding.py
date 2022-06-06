import json
import sys
import os
import numpy as np
sys.path.append("../data/")
from params import params_dict


name = sys.argv[1]
option = int(sys.argv[2])
organism = sys.argv[3]

id_name_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))


essential_dict = set()
with open('../data/deg_{}.dat'.format(organism)) as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[0])

location = name.split("/") 
path_str = "/".join(location[:-2])
path_str = path_str + "/csv_imp/"
path_str = path_str + location[-1]

if os.path.isfile(name):
    sl = np.load('{}-sl_feats.npy'.format(organism))
    ge = np.load('{}-ge_feats.npy'.format(organism))
    go = np.load('{}-go_feats.npy'.format(organism))
    with open(name) as emb:
        with open(path_str + '.csv', "w+") as out:
            with open(path_str +'_out.csv','w+') as ess_out:
                emb.readline()
                ess_out.write('Essentiality\n')
                first_line = True
                miter = 0
                for line in emb:
                    line = line.strip().split(' ')
                    if first_line:
                        out.write("Protein_ID,")
                        for i in range(1,len(line)):
                            out.write("Emb_" + str(i) + ',')
                        for i in range(sl.shape[1]):
                            out.write("SL_" + str(i) + ',')
                        for i in range(ge.shape[1]):
                            out.write("GE_" + str(i) + ',')
                        for i in range(go.shape[1]-1):
                            out.write("GO_" + str(i) + ',')
                        out.write("GO_" + str(go.shape[1]-1) + '\n')
                        first_line = False
                    
                    out.write(','.join(line) + ',')
                    for i in sl[miter]:
                        out.write(str(i) + ',')
                    for i in ge[miter]:
                        out.write(str(i) + ',')
                    for i in range(len(go[miter])-1):
                        out.write(str(go[miter][i]) + ',')
                    out.write(str(go[miter][-1]) + '\n')
                
                    if id_name_dict[line[0]] in essential_dict:
                        ess_out.write('1\n')
                    else:
                        ess_out.write('0\n')
                    miter += 1
