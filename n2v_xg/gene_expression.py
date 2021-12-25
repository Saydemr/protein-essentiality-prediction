import json
import numpy as np
import os
import sys


filename = sys.argv[1]

if os.path.isfile('sc_eppugnn_ge-feats.npy'):
    os.remove('sc_eppugnn_ge-feats.npy')

id_map_rev = {}
with open(filename, 'r') as f:
    i = 0
    f.readline()
    for line in f:
        line = line.strip().split(' ')
        id_map_rev[int(line[0])] = i
        i += 1

id_map = {v: k for k, v in id_map_rev.items()}
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