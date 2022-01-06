import numpy as np
from sklearn import decomposition as dc 
import json
from sklearn.decomposition import PCA
locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

id_map = json.load(open('sc_eppugnn-id_map_inv.json'))
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

print(np.sum(sl_matrix, axis=0))

print(sl_matrix.shape)
np.save('sc_eppugnn_sl-feats.npy', sl_matrix)