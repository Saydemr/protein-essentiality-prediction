import json
import numpy as np
import os
import sys
sys.path.append("../data/")
from params import params_dict

filename = sys.argv[1]
organism = sys.argv[2]
option   = int(sys.argv[3])

if os.path.isfile('{}-sl_feats.npy'.format(organism)):
    os.remove('{}-sl_feats.npy'.format(organism))

if os.path.isfile('{}-go_feats.npy'.format(organism)):
    os.remove('{}-go_feats.npy'.format(organism))

if os.path.isfile('{}-ge_feats.npy'.format(organism)):
    os.remove('{}-ge_feats.npy'.format(organism))

n2v_to_biogrid = {}
with open(filename, 'r') as f:
    i = 0
    f.readline()
    for line in f:
        line = line.strip().split(' ')
        n2v_to_biogrid[i] = int(line[0])
        i += 1

id_bioname_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))
name_index = {id_bioname_dict[str(n2v_to_biogrid[v]).strip()] : v  for v in n2v_to_biogrid.keys() }

if option == 3 or option == 4:
    annotations = set()
    with open("../data/" + params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            annotations.add(line[2])

    annotations = list(annotations)
    go_matrix = np.zeros((len(n2v_to_biogrid), len(annotations)), dtype=np.float32)

    with open("../data/" + params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            gene = line[1]
            annotation = line[2]
            if gene in id_bioname_dict.values():
                go_matrix[int(name_index[gene]), annotations.index(annotation)] = 1

    np.save('{}-go_feats.npy'.format(organism), go_matrix)

if option == 1 or option == 4:
    locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 
    sl_matrix = np.zeros((len(n2v_to_biogrid), 11), dtype=np.float32)

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


if option == 2 or option == 4:
    ge_matrix = np.zeros((len(n2v_to_biogrid), np.load('../data/{}-ge_feats.npy'.format(organism)).shape[1]), dtype=np.float32)

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
