import json
import numpy as np
import os

nhi2gene = {}
with open('GPL90-17389.txt', 'r') as f:
    for line in f:
        if line.startswith('#') or line.startswith('ID'):
            continue
        line = line.strip().split('\t')
        nhi2gene[line[0]] = line[1]

with open('GSE3431_series_matrix.txt', 'r') as f:
    with open('GSE3431_series_matrix_gene.txt', 'w+') as g:
        for line in f:
            line = line.strip()
            if line.startswith('!') or line.startswith('"ID_REF"'):
                continue
            line = line.split('\t')
            check = line[0].replace("\"","")

            if check in nhi2gene:
                if nhi2gene[check] == "":
                    continue
                g.write(nhi2gene[check] + '\t' + '\t'.join(line[1:]) + '\n')


id_map = json.load(open('sc_eppugnn-id_map_inv.json'))
id_bioname_dict = {}

with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_bioname_dict[line[3]] = line[5]
        id_bioname_dict[line[4]] = line[6]

ge_matrix = np.zeros((len(id_map), 36))
name_index = {id_bioname_dict[str(id_map[v])] : v  for v in id_map.keys() }

with open('GSE3431_series_matrix_gene.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[0]
        ge_vector = line[1:]
        if name not in name_index.keys():
            continue
        
        index = int(name_index[name])
        ge_matrix[index] = ge_vector

np.save('sc_eppugnn_ge-feats.npy', ge_matrix)
os.remove('GSE3431_series_matrix_gene.txt')