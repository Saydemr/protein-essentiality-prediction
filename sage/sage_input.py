# read embedding file from emb/ to numpy matrix. First column is the id, all others are the values in the matrix
# remove the first line of the embedding file
# read the first columns to a list
import numpy as np
import torch
import sys
import copy
import json
sys.path.append("../data")
import eppugnn

for org in ['dm', 'mm', 'hs', 'sc']:
    dataset = eppugnn.Eppugnn(root='../data', name=org)
    data = dataset.data

    train_orig = data.x[data.train_mask]
    train_labels_orig = data.y[data.train_mask]

    # Normalize train
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    train_orig = scaler.fit_transform(train_orig)

    # PCA train
    from sklearn.decomposition import PCA
    pca = PCA(n_components=64)
    train_orig = pca.fit_transform(train_orig)
    train_orig = torch.from_numpy(train_orig)
    
    val_data = data.x[data.val_mask]
    test_data = data.x[data.test_mask]

    # Normalize and PCA
    val_data = scaler.transform(val_data)
    val_data = pca.transform(val_data)
    test_data = scaler.transform(test_data)
    test_data = pca.transform(test_data)
    val_data = torch.from_numpy(val_data)
    test_data = torch.from_numpy(test_data)

    rnd_state = np.random.RandomState(12345)
    from imblearn.over_sampling import SMOTE
    ros = SMOTE(random_state=rnd_state, sampling_strategy='minority')
    train_data, train_labels = ros.fit_resample(train_orig, train_labels_orig)
    train_data = torch.from_numpy(train_data)
    train_labels = torch.from_numpy(train_labels)

    assert torch.equal(train_data[:len(train_orig)], train_orig)
    train_aug = train_data[len(train_orig):]
    train_orig_ones = train_orig[train_labels_orig == 1]

    init_edges = copy.deepcopy(data.edge_index.numpy())
    for idx, instance in enumerate(train_aug):        
        # find the closest positive node in the training set
        closest_node = torch.argmin(torch.cdist(instance.unsqueeze(0), train_orig_ones), dim=1).item()
        closest_node = torch.argmin(torch.cdist(train_orig_ones[closest_node].unsqueeze(0), train_orig), dim=1).item()

        # get the edges of the closest node
        row, col = init_edges
        closest_node_edges = np.where(row == closest_node)[0]
        closest_node_edges = [(row[i], col[i]) for i in closest_node_edges]

        # add edges to the new node
        for source, target in closest_node_edges:
            data.edge_index = torch.cat((data.edge_index, torch.tensor([[data.x.shape[0] + idx], [target]])), dim=1)

        data.edge_index = torch.cat((data.edge_index, torch.tensor([[closest_node], [data.x.shape[0] + idx]])), dim=1)


    train_mask = torch.cat((data.train_mask, torch.ones(len(train_aug), dtype=torch.bool)))
    val_mask = torch.cat((data.val_mask, torch.zeros(len(train_aug), dtype=torch.bool)))
    test_mask = torch.cat((data.test_mask, torch.zeros(len(train_aug), dtype=torch.bool)))


    import networkx as nx
    from networkx.readwrite import json_graph
    ppi_graph = nx.Graph()
    for x,y in data.edge_index.T.numpy():
        ppi_graph.add_edge(int(x),int(y))

    for i in range(ppi_graph.number_of_nodes()):
        if train_mask[i]:
            ppi_graph.nodes[i]['test'] = False
            ppi_graph.nodes[i]['val'] = False
        elif val_mask[i]:
            ppi_graph.nodes[i]['test'] = False
            ppi_graph.nodes[i]['val'] = True
        else:
            ppi_graph.nodes[i]['test'] = True
            ppi_graph.nodes[i]['val'] = False

    class_map = {}
    labels = np.concatenate((data.y, np.ones(len(train_aug))))
    for idx, label in enumerate(labels):
        class_map.update({str(idx) : int(label)})

    sage_id = {}
    for i in range(ppi_graph.number_of_nodes()):
        sage_id.update({str(i) : int(i)})


    json.dump(json_graph.node_link_data(ppi_graph), open('{}-G.json'.format(org), 'w+'), indent=4)
    json.dump(sage_id,                              open('{}-id_map.json'.format(org), 'w+'), indent=4)
    json.dump(class_map,                            open('{}-class_map.json'.format(org), 'w+'), indent=4)
    np.save('{}-feats.npy'.format(org), np.concatenate((train_orig, val_data, test_data, train_aug), axis=0))

    print("Done for {}".format(org))
