import numpy as np
import json
import sys
import os
from ..data.params import params_dict


filename = sys.argv[1]
organism = sys.argv[2]

locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

if os.path.isfile('{}-sl_feats.npy'.format(organism)):
    os.remove('{}-sl_feats.npy'.format(organism))

id_map_rev = {}
with open(filename, 'r') as f:
    i = 0
    f.readline()
    for line in f:
        line = line.strip().split(' ')
        id_map_rev[int(line[0])] = i
        i += 1

id_map       = {v: k for k, v in id_map_rev.items()}
id_name_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))
name_index   = {id_name_dict[str(id_map[v]).strip()] : v  for v in id_map.keys() }

sl_matrix = np.zeros((len(id_map), 11))

with open(params_dict[organism]['go'], 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[1]
        sl_feature = line[3]
        if name not in name_index.keys() or sl_feature not in locations:
            continue
        index = int(name_index[name])
        sl_matrix[index, locations.index(sl_feature)] = 1

np.save('{}-sl_feats.npy'.format(organism), sl_matrix)
