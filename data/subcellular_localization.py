import numpy as np
from sklearn import decomposition as dc 
import json

locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

id_map = json.load(open('eppugnn-id_map_inv.json'))
id_name_dict ={}

with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_name_dict[line[3]] = line[7]
        id_name_dict[line[4]] = line[8]

name_id_dict = {v:k for k,v in id_name_dict.items()}

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
        sl_matrix[index, 0] = int(name_id_dict[name])


np.save('eppugnn-feats.npy', sl_matrix)
