import numpy as np
import sys
import json

models = ['gcn', 'graphsage_maxpool', 'graphsage_mean', 'graphsage_meanpool', 'graphsage_seq', 'n2v']

if len(sys.argv) < 2:
    print('Usage: python revert_mapping.py <model>')
    sys.exit(0)

identifier = sys.argv[1]
f = open('eppugnn-id_map_inv.json')
id_map = json.load(f)

id_name_dict ={}
with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        if line[3] == line[4]:
            continue
        id_name_dict[line[3]] = line[7]
        id_name_dict[line[4]] = line[8]

essential_dict = set()
with open('deg_sc.dat') as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[2])

for model in models:
    with open('./' + model + '_' + identifier + '/' + 'val.txt', 'r') as val_txt:
        with open ('./' + model + '_' + identifier + '/' + 'emb_out.csv', 'w+') as emb_csv:
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

    np_matrix = np.load('./' + model + '_' + identifier + '/' + 'val.npy')
    with open('./' + model + '_' + identifier + '/' + 'val.txt', 'r') as val_txt:
        with open ('./' + model + '_' + identifier + '/' + 'emb.csv', 'w+') as emb_csv:
            emb_csv.write('Protein_ID,')
            for i in range(np_matrix.shape[1]-1):
                emb_csv.write('Emb_' + str(i) + ',')
            emb_csv.write( 'Emb_' + str(np_matrix.shape[1]) + '\n')
            i = 0
            for line in val_txt:
                line = line.strip().split()
                gene_id = line[0]
                gene_id_original = id_map[gene_id]
                emb_csv.write(str(gene_id_original) + ',')
                emb_csv.write(','.join(map(str, np_matrix[i])) + '\n')
                i += 1