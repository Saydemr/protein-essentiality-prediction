import json
import numpy as np
import os
import sys

filename = sys.argv[1]
organism = sys.argv[2]

if os.path.isfile('{}-ge_feats.npy'.format(organism)):
    os.remove('{}-ge_feats.npy'.format(organism))

id_map_rev = {}
with open(filename, 'r') as f:
    i = 0
    f.readline()
    for line in f:
        line = line.strip().split(' ')
        id_map_rev[int(line[0])] = i
        i += 1

id_map = {v: k for k, v in id_map_rev.items()}
id_bioname_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))
name_index = {id_bioname_dict[str(id_map[v]).strip()] : v  for v in id_map.keys() }
ge_matrix = np.zeros((len(id_map), np.load('../data/{}-ge_feats.npy'.shape[1])))

with open('GSE3431_series_matrix_gene.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[0]
        ge_vector = line[1:]
        if name not in name_index.keys():
            continue
        
        index = int(name_index[name])
        ge_matrix[index] = ge_vector

np.save('{}-ge_feats.npy', ge_matrix)
