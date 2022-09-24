import networkx as nx
from networkx.readwrite import json_graph
from random import choices
from collections import Counter
import json
import numpy as np
import scipy as sp
import argparse
import os
from scipy import sparse
import fnmatch
from params import params_dict
import time
timestr = time.strftime("%d.%m.%Y_%H.%M.%S_%z")


def main(opt):
    create_graph(opt['organism'])


def parse_graph(organism, removed_nodes=None):

    ppi_graph = nx.Graph()

    id_map         = {}
    id_map_int     = {}
    id_map_inv     = {}
    id_map_inv_int = {}
    id_name_dict   = {}

    files = fnmatch.filter(os.listdir('./'), 'BIOGRID-ORGANISM-{}*.tab3.txt'.format(params_dict[organism]['full_name']))
    if len(files) == 0:
        print("No data available for {}".format(params_dict[organism]['full_name']))
        print("Please run update.py in base directory")
        exit()

    with open(files[0]) as f:
        f.readline()
        i = 0
        for line in f:
            line = line.strip()
            line = line.split("\t")

            if line[1] == line[2]:
                continue

            if not line[1].isdigit() or not line[2].isdigit():
                continue
            
            if removed_nodes != None and (int(line[1]) in removed_nodes.values() or int(line[2]) in removed_nodes.values()):
                continue
            
            id_name_dict[line[1]] = line[7]
            id_name_dict[line[2]] = line[8]

            if int(line[1]) not in id_map_int and int(line[2]) not in id_map_int:
                ppi_graph.add_edge(i, i+1)

                id_map[line[1]] = i
                id_map_int[int(line[1])] = i
                id_map_inv[i] = line[1]
                id_map_inv_int[i] = int(line[1])
                ppi_graph.nodes[i]['id'] = i

                id_map[line[2]] = i+1
                id_map_int[int(line[2])] = i+1
                id_map_inv[i+1] = line[2]
                id_map_inv_int[i+1] = int(line[2])
                ppi_graph.nodes[i+1]['id'] = i+1

                i += 2

            elif int(line[1]) in id_map_int and int(line[2]) not in id_map_int:

                ppi_graph.add_edge(id_map_int[int(line[1])], i)

                id_map[line[2]] = i
                id_map_int[int(line[2])] = i
                id_map_inv[i] = line[2]
                id_map_inv_int[i] = int(line[2])

                ppi_graph.nodes[i]['id'] = i

                i += 1

            elif int(line[1]) not in id_map_int and int(line[2]) in id_map_int:

                ppi_graph.add_edge(i, id_map_int[int(line[2])])

                id_map[line[1]] = i
                id_map_int[int(line[1])] = i
                id_map_inv[i] = line[1]
                id_map_inv_int[i] = int(line[1])
                ppi_graph.nodes[i]['id'] = i

                i += 1

            else:
                ppi_graph.add_edge(id_map_int[int(line[1])], id_map_int[int(line[2])])
    
    return ppi_graph, id_map, id_map_int, id_map_inv, id_map_inv_int, id_name_dict

def create_graph(organism):
    """
    Create a networkx graph from the BIOGRID data
    """
    print("Organism: {}".format((params_dict[organism]['full_name']).replace('_', ' ')))
    print("Loading graph...")

    ppi_graph, id_map, _, id_map_inv, id_map_inv_int, id_name_dict = parse_graph(organism)

    print("Graph info...")
    print("Number of nodes: ", ppi_graph.number_of_nodes())
    print("Number of connected components", nx.number_connected_components(ppi_graph))
    print("Number of edges: ", ppi_graph.number_of_edges())
    print()

    removed_index = {}
    for component in list(nx.connected_components(ppi_graph)):
        if len(component) < 10:
            for node in component:
                b = id_map_inv_int.pop(node)
                removed_index.update({node : b})
    
    if len(removed_index) > 0:
        ppi_graph, id_map, _, id_map_inv, id_map_inv_int, id_name_dict = parse_graph(organism, removed_index)
     
    print("Checking the graph if smth is modified.")
    print("Number of nodes: ", ppi_graph.number_of_nodes())
    print("Number of connected components", nx.number_connected_components(ppi_graph))
    print("Number of edges: ", ppi_graph.number_of_edges())
    print()

    np_adj_matrix = nx.to_numpy_matrix(ppi_graph)
    sp.sparse.save_npz('../grand_blend/{}_adj_matrix.npz'.format(organism), sp.sparse.csr_matrix(np_adj_matrix))

    with open("{}_ppi_graph.txt".format(organism), "w+") as f:
        for e in ppi_graph.edges():
            a, b = e
            f.write(str(id_map_inv_int[a]) + " " + str(id_map_inv_int[b]) + "\n")

    print("Creating class-map")
    essential_dict = set()
    with open('deg_{}.dat'.format(organism)) as f:
        for line in f:
            line = line.strip().split('\t')
            essential_dict.add(line[0])

    class_map = {}
    y_mat = np.zeros(ppi_graph.number_of_nodes(), dtype=np.int8)

    essential_count = 0
    for i in id_map:
        my_key = id_map[i]
        my_str = id_name_dict[i]
        if my_str in essential_dict:
            class_map[my_key] = 1
            y_mat[my_key] = 1
            essential_count += 1
        else:
            class_map[my_key] = 0


    population = [0, 1, 2]
    weights = [0.8, 0.1, 0.1]
    distribution_samples = choices(population, weights, k=ppi_graph.number_of_nodes())
    
    essential_train_count = 0
    essential_test_count  = 0
    essential_val_count = 0

    for i, node in enumerate(ppi_graph.nodes):
        if distribution_samples[i] == 0:
            ppi_graph.nodes[node]['test'] = False
            ppi_graph.nodes[node]['val'] = False
            if class_map[node] == 1:
                essential_train_count += 1

        elif distribution_samples[i] == 1:
            ppi_graph.nodes[node]['test'] = True
            ppi_graph.nodes[node]['val'] = False
            if class_map[node] == 1:
                essential_test_count += 1
        else:
            ppi_graph.nodes[node]['test'] = False
            ppi_graph.nodes[node]['val'] = True
            if class_map[node] == 1:
                essential_val_count += 1


    np.save('../grand_blend/{}_y_mat.npy'.format(organism), y_mat)

    print('Creating id-map')
    sage_id_map = {}
    max_deg = -1
    for index, node in enumerate(ppi_graph.nodes):
        sage_id_map[node] = int(index)
        if ppi_graph.degree(node) > max_deg:
            max_deg = ppi_graph.degree(node)


    print("Writing graphs to JSON files...")

    # json.dump(class_map, fp=open("../GraphSAGE/example_data/{}-class_map.json".format(organism), "w+"), indent=4)
    # json.dump(sage_id_map, fp=open("../GraphSAGE/example_data/{}-id_map.json".format(organism), "w+"), indent=4)
    # json.dump(json_graph.node_link_data(ppi_graph), fp=open("../GraphSAGE/example_data/{}-G.json".format(organism), "w+"), indent=4)
    
    json.dump(id_map_inv, fp=open("./{}-id_map_inv.json".format(organism), "w+"), indent=4)
    json.dump(sage_id_map, fp=open("./{}-id_map.json".format(organism), "w+"), indent=4)
    json.dump(id_name_dict, fp=open("./{}-id_name_dict.json".format(organism), "w+"), indent=4)
    
    name_index = {id_name_dict[str(id_map_inv[v])] : sage_id_map[v]  for v in id_map_inv.keys()}
    json.dump(name_index, fp=open("./{}-name_index.json".format(organism),"w+"), indent=4)
    


    print("Logging some numbers...")
    with open("{}_{}_log.txt".format(organism,timestr), "w+") as f:
        f.write("Number of nodes: {}\n".format(ppi_graph.number_of_nodes()))
        f.write("Number of edges: {}\n".format(ppi_graph.number_of_edges()))
        f.write("Number of connected components: {}\n".format(nx.number_connected_components(ppi_graph)))
        f.write("Number of essential genes: {}\n".format(essential_count))
        f.write("Number of essential genes in training set (GraphSAGE): {}\n".format(essential_train_count))
        f.write("Number of essential genes in validation set (GraphSAGE): {}\n".format(essential_val_count))
        f.write("Number of essential genes in test set (GraphSAGE): {}\n".format(essential_test_count))
        f.write("Number of instances in training (0), test (1) and validation (2)\n")
        f.write(str(Counter(distribution_samples)) + "\n")
        f.write("Max degree : {}\n".format(max_deg))
        f.flush()
        f.close()


    print("Creating the feature matrix...")
    gene_expression(organism)
    subcellular_localization(organism)
    go_annotation(organism)
    # rna_seq(organism)
    merge_features(organism)


def gene_expression(organism):
    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))
    nhi2gene = {}
    expression_file = params_dict[organism]['ge']
    expression_size = 0

    non_zero_count = 0
    if organism == 'sc' or organism == 'mm':
        with open(params_dict[organism]['map'], 'r') as f:
            for line in f:
                if line.startswith('#') or line.startswith('ID'):
                    continue
                line = line.split('\t')

                if "///" in line[10]:
                    genes = line[10].strip().split("///")
                    genes = [x.strip() for x in genes]
                    if any(gene in id_bioname_dict for gene in genes):
                        for gene in genes:
                            if gene in id_bioname_dict:
                                nhi2gene[line[0]] = gene
                    else:
                        nhi2gene[line[0]] = genes[0]    
                else:
                    nhi2gene[line[0]] = line[10]

        with open(expression_file, 'r') as f:
            with open(expression_file.replace(".txt", "_gene.txt"), 'w+') as g:
                for line in f:
                    line = line.rstrip()
                    if line.startswith('!') or line.startswith('"ID_REF"'):
                        continue
                    line = line.split('\t')
                    check = line[0].replace("\"","")

                    if check in nhi2gene:
                        if nhi2gene[check] == "":
                            continue
                        g.write(nhi2gene[check] + '\t' + '\t'.join(line[1:]) + '\n')
                        expression_size = len(line) - 1

    elif organism == 'hs':
        with open(expression_file, 'r') as f:
            with open(expression_file.replace(".txt", "_gene.txt"), 'w+') as g:
                f.readline()
                for line in f:
                    line = line.rstrip()
                    line = line.split('\t')
                    
                    if line[0] in id_bioname_dict.values():
                        g.write(line[0] + '\t' + '\t'.join(line[1:]) + '\n')
                        expression_size = len(line) - 1

    
    ge_matrix  = np.zeros((len(id_bioname_dict), expression_size), dtype=np.float32)
    name_index = json.load(open("./{}-name_index.json".format(organism)))


    with open(expression_file.replace(".txt", "_gene.txt"), 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            name = line[0]
            ge_vector = line[1:]

            if name not in name_index.keys():
                continue

            index = int(name_index[name])
            ge_matrix[index] = ge_vector
            non_zero_count += 1

    with open("{}_{}_log.txt".format(organism,timestr), "a+") as f:
        f.write("Number of genes that has gene expressions matrix: {}\n".format(non_zero_count))
        f.flush()
        f.close()
    
    from sklearn.preprocessing import StandardScaler
    ge_matrix = StandardScaler().fit_transform(ge_matrix)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=min(params_dict[organism]['pca'], ge_matrix.shape[1]))
    ge_matrix = pca.fit_transform(ge_matrix)

    np.save('{}-ge_feats.npy'.format(organism), ge_matrix)
    # np.save('../GraphSAGE/example_data/{}-ge_feats.npy'.format(organism), ge_matrix)

def subcellular_localization(organism):
    locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

    name_index = json.load(open("./{}-name_index.json".format(organism)))
    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))
    

    sl_matrix = np.zeros((len(id_bioname_dict), 11), dtype=np.int8)
    with open(params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            name = line[1]
            sl_feature = line[3]
            if name not in name_index.keys() or sl_feature not in locations:
                continue
            index = int(name_index[name])
            sl_matrix[index, locations.index(sl_feature)] = 1

    sl_non_zero_count = 0
    for line in sl_matrix:
        if sum(line) != 0:
            sl_non_zero_count += 1
    
    with open("{}_{}_log.txt".format(organism,timestr), "a+") as f:
        f.write("Number of genes that has subcellular localization vector: {}\n".format(sl_non_zero_count))
        f.flush()
        f.close()

    np.save('{}-sl_feats.npy'.format(organism), sl_matrix)
    # np.save('../GraphSAGE/example_data/{}-sl_feats.npy'.format(organism), sl_matrix)

def go_annotation(organism):
    annotations = set()
    with open(params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            annotations.add(line[2])

    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))
    name_index = json.load(open("./{}-name_index.json".format(organism)))    
    annotations     = list(annotations)
    go_matrix = np.zeros((len(id_bioname_dict), len(annotations)), dtype=np.int8)

    with open(params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            gene = line[1]
            annotation = line[2]
            if gene in id_bioname_dict.values():
                go_matrix[int(name_index[gene]), annotations.index(annotation)] = 1

    go_non_zero_count = 0
    for line in go_matrix:
        if sum(line) != 0:
            go_non_zero_count += 1
    
    with open("{}_{}_log.txt".format(organism,timestr), "a+") as f:
        f.write("Number of genes that has go annotation vector: {}\n".format(go_non_zero_count))
        f.flush()
        f.close()



    from sklearn.preprocessing import StandardScaler
    go_matrix = StandardScaler().fit_transform(go_matrix)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=min(params_dict[organism]['pca'], go_matrix.shape[1]))
    go_matrix = pca.fit_transform(go_matrix)

    np.save('{}-go_feats.npy'.format(organism), go_matrix)
    # np.save('../GraphSAGE/example_data/{}-go_feats.npy'.format(organism), go_matrix)


def rna_seq(organism):
    # TODO
    pass


def merge_features(organism):
    b = np.load('{}-ge_feats.npy'.format(organism), allow_pickle=True, fix_imports=True, encoding='latin1')
    a = np.load('{}-sl_feats.npy'.format(organism), allow_pickle=True, fix_imports=True, encoding='latin1')
    d = np.load('{}-go_feats.npy'.format(organism), allow_pickle=True, fix_imports=True, encoding='latin1')

    c = np.concatenate((a, b, d), axis=1)

    from sklearn.preprocessing import StandardScaler
    c = StandardScaler().fit_transform(c)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=min(params_dict[organism]['pca'], c.shape[1]))
    c = pca.fit_transform(c)
    
    np.save('{}-feats.npy'.format(organism), c)
    # np.save('../GraphSAGE/example_data/{}-all-feats.npy'.format(organism), c)
    sp.sparse.save_npz('../grand_blend/{}-feats.npz'.format(organism), sparse.csr_matrix(c))

    with open("{}_{}_log.txt".format(organism,timestr), "a+") as f:
        f.write("Shape of the feature matrix: {}\n".format(c.shape))
        f.flush()
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--organism', type=str, help='Organism name : sc hs', default='sc')
    args = parser.parse_args()
    opt = vars(args)

    main(opt)
