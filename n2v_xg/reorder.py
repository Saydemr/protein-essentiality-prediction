import json
import numpy as np
import os
import sys
sys.path.append("../data/")
from params import params_dict

filename = sys.argv[1]
organism = sys.argv[2]

if os.path.isfile('{}-sl_feats.npy'.format(organism)):
    os.remove('{}-sl_feats.npy'.format(organism))

if os.path.isfile('{}-go_feats.npy'.format(organism)):
    os.remove('{}-go_feats.npy'.format(organism))

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


annotations = set()
with open("../data/" + params_dict[organism]['go'], 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        annotations.add(line[2])

annotations = list(annotations)
go_matrix = np.zeros((len(id_map), len(annotations)))

with open("../data/" + params_dict[organism]['go'], 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        gene = line[1]
        annotation = line[2]
        if gene in id_bioname_dict.values():
            go_matrix[int(name_index[gene]), annotations.index(annotation)] = 1

from sklearn.preprocessing import StandardScaler
go_matrix = StandardScaler().fit_transform(go_matrix)

from sklearn.decomposition import PCA
pca = PCA(params_dict[organism]['pca'])
go_matrix = pca.fit_transform(go_matrix)

np.save('{}-go_feats.npy'.format(organism), go_matrix)


locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 
sl_matrix = np.zeros((len(id_map), 11))

with open("../data/" + params_dict[organism]['go'], 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[1]
        sl_feature = line[3]
        if name not in name_index.keys() or sl_feature not in locations:
            continue
        index = int(name_index[name])
        sl_matrix[index, locations.index(sl_feature)] = 1

np.save('{}-sl_feats.npy'.format(organism), sl_matrix)

ge_matrix = np.zeros((len(id_map), np.load('../data/{}-ge_feats.npy'.format(organism)).shape[1]))

with open("../data/" + params_dict[organism]['ge'], 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[0]
        ge_vector = line[1:]
        if name not in name_index.keys():
            continue
        
        index = int(name_index[name])
        ge_matrix[index] = ge_vector

np.save('{}-ge_feats.npy'.format(organism), ge_matrix)
