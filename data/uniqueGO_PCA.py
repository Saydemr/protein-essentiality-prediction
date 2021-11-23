import numpy as np
from sklearn import decomposition as dc 

gos =set()
genes = set()
with open('yeast_compartment_integrated_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        gos.add(line[2])
print("go annotations are ready")

with open('yeast_compartment_integrated_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        genes.add(line[1])

print("genes are ready")

print(len(gos))
print(len(genes))


gen_map = {}
gen_map_rev = {}
b = list(gos)
c = list(genes)

for i in range(len(c)):
    gen_map.update({i:c[i]})
    gen_map_rev.update({c[i]:i})


beeeg_matrix = np.zeros((len(genes), len(gos)))
print("matrix is created")

with open('yeast_compartment_integrated_full.tsv', 'r') as f:
    prev = ''
    for line in f:
        line = line.strip().split('\t')
        beeeg_matrix[c.index(line[1])][b.index(line[2])] = 1
print("matrix is ready")
np.save('beeeg_matrix.npy', beeeg_matrix)
np.save('genes.npy', genes)
np.save('gos.npy', gos)

'''print(beeeg_matrix[1])
print(len(beeeg_matrix[1]))
print(len(beeeg_matrix))


pca = dc.PCA(.95)
pca.fit(beeeg_matrix)
print(pca.explained_variance_ratio_)
print(len(pca.explained_variance_ratio_))
print(mean(pca.explained_variance_ratio_) * len(pca.explained_variance_ratio_))
print(pca.singular_values_)'''

