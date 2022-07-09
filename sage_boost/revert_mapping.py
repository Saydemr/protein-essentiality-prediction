import numpy as np
import sys
import json
import os
sys.path.append("../data/")
from params import params_dict

organism = sys.argv[1]
models = ['gcn', 'graphsage_maxpool', 'graphsage_mean', 'graphsage_meanpool', 'graphsage_seq', 'n2v']

id_map = json.load(open('{}-id_map_inv.json'.format(organism)))
id_name_dict = json.load(open('{}-id_name_dict.json'.format(organism)))

essential_dict = set()
with open(params_dict[organism]['deg']) as f:
    for line in f:
        line = line.strip().split()
        essential_dict.add(line[0])

for ii in range(5):
    for model in models:
        path_txt = './runs/{}_'.format(organism) + str(ii) + '_/unsup-example_data/' + model + '_small_0.000010/val.txt'
        path_npy = './runs/{}_'.format(organism) + str(ii) + '_/unsup-example_data/' + model + '_small_0.000010/val.npy'
        
        print(path_txt)
        print(path_npy)
        if os.path.isfile(path_txt) and os.path.isfile(path_npy):
            with open(path_txt, 'r') as val_txt:
                with open ('./runs/{}_'.format(organism) + str(ii) + '_/unsup-example_data/' + model + '_small_0.000010/emb_out.csv', 'w+') as emb_csv:
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
                with open ('./runs/{}_'.format(organism) + str(ii) + '_/unsup-example_data/' + model + '_small_0.000010/emb.csv', 'w+') as emb_csv:
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
