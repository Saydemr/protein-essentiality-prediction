import json
import sys
import os
import numpy as np
sys.path.append("../data/")
from params import params_dict

def scale(*args):
    catted = np.concatenate((args), axis=1)
    print(catted)
    from sklearn.preprocessing import StandardScaler
    catted = StandardScaler().fit_transform(catted)
    return catted

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

if option == 0:
    path_str += "/csv_imp/"
elif option == 1:
    path_str += "/csv_imp_sl/"
elif option == 2:
    path_str += "/csv_imp_ge/"
elif option == 3:
    path_str += "/csv_imp_go/"
elif option == 4:
    path_str += "/csv_imp_sl_ge_go/"

path_str = path_str + location[-1]

if option != 0:
    sl = np.load('{}-sl_feats.npy'.format(organism))
    ge = np.load('{}-ge_feats.npy'.format(organism))
    go = np.load('{}-go_feats.npy'.format(organism))
    if option == 1:
        sl = scale(sl)
    elif option == 2:
        ge = scale(ge)
    elif option == 3:
        go = scale(go)
    elif option == 4:
        scaled = scale(sl,ge,go)
        sl,ge,go = np.split(scaled, [sl.shape[1], sl.shape[1] + ge.shape[1]], axis=1)

if os.path.isfile(name):
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
                        out.write("Protein_ID")
                        for i in range(1,len(line)):
                            out.write(",Emb_" + str(i))
                        if option == 0:
                            pass
                        elif option == 1:
                            for i in range(sl.shape[1]):
                                out.write(",SL_" + str(i))
                        elif option == 2:
                            for i in range(ge.shape[1]):
                                out.write(",GE_" + str(i))
                        elif option == 3:
                            for i in range(go.shape[1]):
                                out.write(",GO_" + str(i))
                        elif option == 4:
                            for i in range(sl.shape[1]):
                                out.write(",SL_" + str(i))
                            for i in range(ge.shape[1]):
                                out.write(",GE_" + str(i))
                            for i in range(go.shape[1]):
                                out.write(",GO_" + str(i))   
                        out.write('\n')
                        first_line = False
                    
                    out.write(','.join(line))
                    if option == 0:
                        out.write('\n')
                    elif option == 1:
                        out.write(',' + ','.join(map(str,sl[miter])) + '\n')
                    elif option == 2:
                        out.write(',' + ','.join(map(str,ge[miter])) + '\n')
                    elif option == 3:
                        out.write(',' + ','.join(map(str,go[miter])) + '\n')
                    elif option == 4:
                        out.write(',' + ','.join(map(str,sl[miter])))
                        out.write(',' + ','.join(map(str,ge[miter])))
                        out.write(',' + ','.join(map(str,go[miter])) + '\n')
                    
                
                    if id_name_dict[line[0].strip()] in essential_dict:
                        ess_out.write('1\n')
                    else:
                        ess_out.write('0\n')
                    miter += 1
