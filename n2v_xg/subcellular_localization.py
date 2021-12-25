import numpy as np
from sklearn import decomposition as dc 
import json
import sys
import os

locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

if os.path.isfile('sc_eppugnn_sl-feats.npy'):
    os.remove('sc_eppugnn_sl-feats.npy')

filename = sys.argv[1]

id_map_rev = {}
with open(filename, 'r') as f:
    i = 0
    f.readline()
    for line in f:
        line = line.strip().split(' ')
        id_map_rev[int(line[0])] = i
        i += 1

id_map = {v: k for k, v in id_map_rev.items()}
id_name_dict ={}

with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_name_dict[line[3]] = line[7]
        id_name_dict[line[4]] = line[8]

name_index = {id_name_dict[str(id_map[v])] : v  for v in id_map.keys() }

sl_matrix = np.zeros((len(id_map), 11), dtype=np.int64)

with open('yeast_compartment_knowledge_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[1]
        sl_feature = line[3]
        if name not in name_index.keys() or sl_feature not in locations:
            continue
        index = int(name_index[name])
        sl_matrix[index, locations.index(sl_feature)] = 1

np.save('sc_eppugnn_sl-feats.npy', sl_matrix)