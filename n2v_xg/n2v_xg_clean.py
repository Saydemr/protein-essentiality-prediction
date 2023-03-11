# read embedding file from emb/ to numpy matrix. First column is the id, all others are the values in the matrix
# remove the first line of the embedding file
# read the first columns to a list
import numpy as np
import json
from scipy.sparse import csr_matrix
import torch

org = 'mm'
emb_file = 'emb/{}_emb.txt'.format(org)
matrix = None
ids = []
with open(emb_file) as f:
    lines = f.readlines()
    lines = lines[1:]
    ids = [line.split()[0] for line in lines]

    # read the rest of the columns to a numpy matrix
    matrix = np.array([line.strip().split()[1:] for line in lines], dtype=np.float32)


# get the features from ../data/$org-data.npz
data = np.load('../data/{}-data.npz'.format(org))
features = csr_matrix((data['attr_data'], data['attr_indices'], data['attr_indptr']),
                                        shape=data['attr_shape']).toarray()
labels = data['labels']
inv = json.load(open('../data/{}-id_map_inv.json'.format(org)))
indeces = {str(v) : int(k) for k, v in inv.items()}

# reorder the matrix
new_matrix = np.zeros(matrix.shape, dtype=np.float32)
for i in range(len(ids)):
    new_matrix[i] = matrix[indeces[ids[i]]]

# concatanate the features to the emb matrix
new_matrix = np.concatenate((new_matrix, features), axis=1)

# load splits
split = np.load('../splits/eppugnn_splits_{}_0.6_0.2_0.npz'.format(org))
train = torch.tensor(split['train_mask']).to(torch.bool)
val   = torch.tensor(split['val_mask']).to(torch.bool)
test  = torch.tensor(split['test_mask']).to(torch.bool)

# normalize the matrix based on training
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(new_matrix[train])
new_matrix = scaler.transform(new_matrix)

# dim reduction
from sklearn.decomposition import PCA
pca = PCA(n_components=64)
pca.fit(new_matrix[train])
new_matrix = pca.transform(new_matrix)

# Do oversampling on the train data
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=12345, sampling_strategy='minority')

train_data   = new_matrix[train]
train_labels = labels[train]
train_data, train_labels = smote.fit_resample(train_data, train_labels)

# Do XGBoost with predetermined split
import xgboost as xgb
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, roc_auc_score

dtrain = xgb.DMatrix(train_data, label=train_labels)
dval = xgb.DMatrix(new_matrix[val], label=labels[val])
dtest = xgb.DMatrix(new_matrix[test], label=labels[test])


param = {'max_depth': 10, 'eta': 0.1, 'num_class': 2, 'objective': 'multi:softmax'}
param['nthread'] = 4
param['eval_metric'] = 'merror'
evallist = [(dval, 'eval')]
num_round = 500

import time
start = time.time()
bst = xgb.train(param, dtrain=dtrain,evals=evallist, num_boost_round=num_round, early_stopping_rounds=5)
preds = bst.predict(dtest)
print('Accuracy: {}'.format(accuracy_score(labels[test], preds)))
print('F1: {}'.format(f1_score(labels[test], preds)))
print('AUC: {}'.format(roc_auc_score(labels[test], preds)))
print('Precision: {}'.format(precision_score(labels[test], preds)))
print('Recall: {}'.format(recall_score(labels[test], preds)))
print('Time: {}'.format(time.time() - start))
# print(classification_report(labels[test], preds[test]))
# print(confusion_matrix(labels[test], preds[test]))
