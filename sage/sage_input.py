# read embedding file from emb/ to numpy matrix. First column is the id, all others are the values in the matrix
# remove the first line of the embedding file
# read the first columns to a list
import numpy as np
import torch
import sys
import copy
sys.path.append("../data")
import eppugnn

org = 'sc'
dataset = eppugnn.Eppugnn(root='../data', name=org)
data = dataset.data

train_orig = data.x[data.train_mask]
train_labels_orig = data.y[data.train_mask]

rnd_state = np.random.RandomState(12345)
from imblearn.over_sampling import SVMSMOTE
ros = SVMSMOTE(random_state=rnd_state, sampling_strategy='minority')
train_data, train_labels = ros.fit_resample(train_orig, train_labels_orig)
train_data = torch.from_numpy(train_data)
train_labels = torch.from_numpy(train_labels)

assert torch.equal(train_data[:len(train_orig)], train_orig)
train_aug = train_data[len(train_orig):]

# find nodes with label 1 in train_orig
train_orig_1 = train_orig[train_labels_orig == 1]

counter = 0
init_edges = copy.deepcopy(data.edge_index.numpy())
for instance in train_aug:
    # get the most similar node in the original training set
    dists = torch.cdist(instance.unsqueeze(0), train_orig_1)
    closest_node = torch.argmin(dists, dim=1)
    closest_node = closest_node.item()
    # get the edges of the closest node
    row, col = init_edges
    closest_node_edges = np.where(row == closest_node)[0]
    closest_node_edges = [(row[i], col[i]) for i in closest_node_edges]
    # add the edges to the augmented node
    for e in closest_node_edges:
        data.edge_index = torch.cat((data.edge_index, torch.tensor(e).unsqueeze(1)), dim=1)

    counter += 1

val_data = data.x[data.val_mask]
val_labels = data.y[data.val_mask]

test_data = data.x[data.test_mask]
test_labels = data.y[data.test_mask]

import networkx as nx
ppi_graph = nx.from_edgelist(data.edge_index.T.numpy())


for node in list(ppi_graph.nodes):
    print(node)
