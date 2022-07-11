import json
import sys
import os
import numpy as np

sys.path.append("../data/")
from params import params_dict



name = sys.argv[1]
option = int(sys.argv[2])
organism = sys.argv[3]

def scale(*args):
    catted = np.concatenate((args), axis=1)
    from sklearn.preprocessing import StandardScaler
    catted = StandardScaler().fit_transform(catted)
    from sklearn.decomposition import PCA
    n_comp = min(params_dict[organism]['pca'],catted.shape[1])
    pca = PCA(n_components=n_comp)
    catted = pca.fit_transform(catted)
    return catted


essential_dict = set()
with open('../data/deg_{}.dat'.format(organism)) as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[0])

location = name.split("/") 
path_str = "/".join(location[:-2]) + "/csv_" + str(option) + "/"

feats = None
if option == 1:
    sl = np.load('{}-sl_feats.npy'.format(organism))
    feats = scale(sl)
elif option == 2:
    ge = np.load('{}-ge_feats.npy'.format(organism))
    feats = scale(ge)
elif option == 3:
    go = np.load('{}-go_feats.npy'.format(organism))
    feats = scale(go)    
elif option == 4:
    path_str += "/csv_imp_sl_ge_go/"
    sl = np.load('{}-sl_feats.npy'.format(organism))
    ge = np.load('{}-ge_feats.npy'.format(organism))
    go = np.load('{}-go_feats.npy'.format(organism))
    feats = scale(sl,ge,go)

path_str += location[-1]

id_name_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))
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
                        if option != 0:
                            for i in range(feats.shape[1]):
                                out.write(",Feature_" + str(i+1))
                        out.write('\n')
                        first_line = False
                    out.write(','.join(line))
                    if option == 0:
                        out.write('\n')
                    else:
                        out.write(',' + ','.join(map(str,feats[miter])) + '\n')
                
                    if id_name_dict[line[0].strip()] in essential_dict:
                        ess_out.write('1\n')
                    else:
                        ess_out.write('0\n')
                    miter += 1
