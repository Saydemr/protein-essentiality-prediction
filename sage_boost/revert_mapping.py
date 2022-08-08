import numpy as np
import sys
import json
import os
sys.path.append("../data/")
from params import params_dict

organism = sys.argv[1]
models = ['graphsage_maxpool', 'graphsage_meanpool', 'n2v']

id_map       = json.load(open('../data/{}-id_map_inv.json'.format(organism)))
id_name_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))

essential_dict = set()
with open(params_dict[organism]['deg']) as f:
    for line in f:
        line = line.strip().split()
        essential_dict.add(line[0])

identity_dim = 32
epoch = 2
batch_size = 32
for option in range(5):
    for model in models:
        for learning_rate in [0.005 0.001 0.0001]:
            base_dir = './unsupervised/org{}_e{}_b{}_id{}_opt{}/unsup-example_data/{}_small_{}/'.format(organism,epoch,batch_size,identity_dim,option,model,learning_rate)
            path_txt = base_dir + 'val.txt'
            path_npy = base_dir + 'val.npy'
            
            print(path_txt)
            print(path_npy)
            if os.path.isfile(path_txt) and os.path.isfile(path_npy):
                with open(path_txt, 'r') as val_txt:
                    with open (base_dir + 'emb_out.csv', 'w+') as emb_csv:
                        emb_csv.write('Essentiality\n')
                        for line in val_txt:
                            line = line.strip().split()
                            gene_id = line[0]
                            gene_id_original = id_map[gene_id]
                            gene_name = id_name_dict[str(gene_id_original)]
                            if gene_name in essential_dict:
                                emb_csv.write('1\n')
                            else:
                                emb_csv.write('0\n')

                np_matrix = np.load(path_npy)
                with open(path_txt, 'r') as val_txt:
                    with open (base_dir 'emb.csv', 'w+') as emb_csv:
                        emb_csv.write('Protein_ID')
                        for i in range(np_matrix.shape[1]):
                            emb_csv.write(',Emb_' + str(i))
                        emb_csv.write('\n')
                        i = 0
                        for line in val_txt:
                            line = line.strip().split()
                            gene_id = line[0]
                            gene_id_original = id_map[gene_id]
                            emb_csv.write(str(gene_id_original) + ',')
                            emb_csv.write(','.join(map(str, np_matrix[i])) + '\n')
                            i += 1
