import json
import sys
import os
import numpy as np

full_name = {'sc': 'Saccharomyces_cerevisiae', 'mm': 'Mus_musculus', 'hs': 'Homo_sapiens'}

name = sys.argv[1]
option = int(sys.argv[2])
organism = sys.argv[3]

id_name_dict = json.load('../data/{}-id_name_dict.json'.format(organism))


essential_dict = set()
with open('../data/deg_{}.dat'.format(organism)) as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[2])

location = name.split("/") 
path_str = "/".join(location[:-2])

if option == 1:
    path_str = path_str + "/csv_imp/"
elif option == 2:
    path_str = path_str + "/csv_imp_sl/"
elif option == 3:
    path_str = path_str + "/csv_imp_ge/"
elif option == 4:
    path_str = path_str + "/csv_imp_sl_ge/"

path_str = path_str + location[-1]

if os.path.isfile(name):
    sl = np.load('sc_eppugnn_sl-feats.npy')
    ge = np.load('sc_eppugnn_ge-feats.npy')
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
                        if option == 1:
                            pass
                        elif option == 2:
                            for i in range(sl.shape[1]):
                                out.write("SL_" + str(i) + ',')
                        elif option == 3:
                            for i in range(ge.shape[1]):
                                out.write("GE_" + str(i) + ',')
                        elif option == 4:
                            for i in range(sl.shape[1]):
                                out.write("SL_" + str(i) + ',')
                            for i in range(ge.shape[1]):
                                out.write("GE_" + str(i) + ',')
                        out.write('\n')
                        first_line = False
                    if option == 1:
                        out.write(','.join(line) + '\n')
                    elif option == 2:
                        # if sl[miter].sum() == 0:
                        #     miter += 1
                        #     continue
                        out.write(','.join(line) + ',')
                        for i in range(len(sl[miter])-1):
                            out.write(str(sl[miter][i]) + ',')
                        out.write(str(sl[miter][-1]) + '\n')
                    elif option == 3:
                        # if ge[miter].sum() == 0:
                        #     miter += 1
                        #     continue    
                        out.write(','.join(line) + ',')
                        for i in range(len(ge[miter])-1):
                            out.write(str(ge[miter][i]) + ',')
                        out.write(str(ge[miter][-1]) + '\n')
                    elif option == 4:
                        # if sl[miter].sum() == 0 and ge[miter].sum() == 0:
                        #     miter += 1
                        #     continue
                        out.write(','.join(line) + ',')
                        for i in sl[miter]:
                            out.write(str(i) + ',')
                        for i in range(len(ge[miter])-1):
                            out.write(str(ge[miter][i]) + ',')
                        out.write(str(ge[miter][-1]) + '\n')
                    
                    if id_name_dict[line[0]] in essential_dict:
                        ess_out.write('1\n')
                    else:
                        ess_out.write('0\n')
                    miter += 1
