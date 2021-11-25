import numpy as np
from sklearn import decomposition as dc 
import json
import math

id_map = json.load(open('eppugnn-id_map_inv.json'))
id_name_dict ={}
with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_name_dict[line[3]] = line[7]
        id_name_dict[line[4]] = line[8]

name_id_dict = {v:k for k,v in id_name_dict.items()}


gos =set()
genes_compartment = set()

with open('yeast_compartment_knowledge_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        gos.add(line[2])
print("go annotations are ready")
print("Compartment go annotations", len(gos))

with open('yeast_compartment_knowledge_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        genes_compartment.add(line[1])

print("genes_compartment are ready")
print("Compartment genes ", len(genes_compartment))

genes = set()
with open ('BIOGRID-ORGANISM-Saccharomyces_cerevisiae.txt') as f:
    for line in f:
        line = line.strip().split('\t')
        genes.add(line[7])
        genes.add(line[8])

j = 0
for i in genes_compartment:
    if i in genes:
        j += 1
print("j : ",j)

gen_map = {}
gen_map_rev = {}
b = list(gos)
c = list(genes_compartment)

for i in range(len(c)):
    gen_map.update({i:c[i]})
    gen_map_rev.update({c[i]:i})

print(gen_map[1])
print(gen_map_rev[gen_map[1]])

beeeg_matrix = np.zeros((len(genes_compartment), len(gos)))
print("matrix is created")

with open('yeast_compartment_knowledge_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        beeeg_matrix[c.index(line[1])][b.index(line[2])] = 1
#print("matrix is ready")
#np.save('beeeg_matrix.npy', beeeg_matrix)
#np.save('genes_compartment.npy', genes_compartment)
#np.save('gos.npy', gos)

feats = np.zeros(shape=(len(id_map), len(gos)))
#print(feats.shape)
for i in id_map:
    name = id_name_dict[str(id_map[str(i)])]
    if name in genes_compartment:
        if name in genes:
            '''print(i)
            print(beeeg_matrix[gen_map_rev[name]])
            print(gen_map_rev[name])
            print(beeeg_matrix[gen_map_rev[name]].shape)
            '''
            feats[int(i)] = beeeg_matrix[int(gen_map_rev[name])]


np.save('eppugnn-feats.npy',feats)

exit()
print("feats is ready")
print(feats[0])
print()
print(feats[1])


pca = dc.PCA(n_components=64)
pca.fit(feats)
print("exp variance ratio", pca.explained_variance_ratio_)
print("exp variance ratio (len) ",len(pca.explained_variance_ratio_))
print("hesaplama   " ,np.mean(pca.explained_variance_ratio_) * len(pca.explained_variance_ratio_))
print("sing values " , pca.singular_values_)
print()
print(pca.components_[0])

print(len(pca.components_[0]))