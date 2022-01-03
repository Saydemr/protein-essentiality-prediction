import numpy as np
import scipy as sp
from scipy import sparse
from sklearn.decomposition import PCA


b = np.load('sc_eppugnn_ge-feats.npy',allow_pickle=True,fix_imports=True,encoding='latin1')
a = np.load('sc_eppugnn_sl-feats.npy',allow_pickle=True,fix_imports=True,encoding='latin1')

c = np.concatenate((a, b), axis=1)

print(c.shape)
pca = PCA(n_components=0.99)
pca.fit(c)

# print(pca.components_)
# print(pca.explained_variance_ratio_)
print(np.sum(pca.explained_variance_ratio_))
print(len(pca.explained_variance_ratio_))
# transform data
ge_sl_matrix_clear = pca.transform(c)
print(ge_sl_matrix_clear.shape)

np.save('sc_eppugnn_sl_ge-feats.npy', ge_sl_matrix_clear)
sp.sparse.save_npz('../grand_blend/sc_eppugnn_sl_ge-feats.npz', sparse.csr_matrix(ge_sl_matrix_clear))