import networkx as nx
from collections import Counter
import json
import numpy as np
import scipy as sp
from scipy import sparse
import argparse
import os
import fnmatch
from params import params_dict
import time
timestr = time.strftime("%d.%m.%Y_%H.%M.%S_%z")

def main(opt):
    if opt['organism'] == "all":
        for org in ["sc", "mm", "dm", "hs"]:
            create_graph(org)
    else:
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

    json.dump(id_map_inv, fp=open("./{}-id_map_inv.json".format(organism), "w+"), indent=4)
    json.dump(sage_id_map, fp=open("./{}-id_map.json".format(organism), "w+"), indent=4)
    json.dump(id_name_dict, fp=open("./{}-id_name_dict.json".format(organism), "w+"), indent=4)
    
    name_index = {id_name_dict[str(id_map_inv[v])] : sage_id_map[v]  for v in id_map_inv.keys()}
    json.dump(name_index, fp=open("./{}-name_index.json".format(organism),"w+"), indent=4)

    print("Creating the feature matrix...")
    _, ge_names = gene_expression(organism)
    _, sl_names = subcellular_localization(organism)
    _, go_names = go_annotation(organism)
    # rna_seq(organism)
    data = merge_features(organism)
    
    # cast data to sparse matrix
    data = sparse.csr_matrix(data)

    # find the row indices that have all zeros
    zero_row_indices = np.where(~data.any(axis=1))[0]

    # find the node ids that correspond to the zero rows
    zero_node_ids = [id_map_inv_int[i] for i in zero_row_indices]

    # parse the graph again, this time removing the zero rows
    # ppi_graph, id_map, _, id_map_inv, id_map_inv_int, id_name_dict = parse_graph(organism, zero_node_ids)


    # id map inv int  e.g. 0 : 7266
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


    np_adj_matrix = nx.to_numpy_matrix(ppi_graph)

    with open("{}_ppi_graph.txt".format(organism), "w+") as f:
        for e in ppi_graph.edges():
            a, b = e
            f.write(str(id_map_inv_int[a]) + " " + str(id_map_inv_int[b]) + "\n")


    essential_dict = set()
    with open('deg_{}.dat'.format(organism)) as f:
        for line in f:
            line = line.strip().split('\t')
            essential_dict.add(line[0])

    labels = np.zeros(ppi_graph.number_of_nodes(), dtype=np.int8)

    essential_count = 0
    for i in id_map:
        my_key = id_map[i]
        my_str = id_name_dict[i]
        if my_str in essential_dict:
            labels[my_key] = 1
            essential_count += 1

    np.save('./{}-labels.npy'.format(organism), labels, allow_pickle=False)

    sage_id_map = {}
    max_deg = -1
    for index, node in enumerate(ppi_graph.nodes):
        sage_id_map[node] = int(index)
        if ppi_graph.degree(node) > max_deg:
            max_deg = ppi_graph.degree(node)

    node_names = np.asarray([k for k in id_name_dict.values()])

    print("Logging some numbers...")
    with open("{}_{}_log.txt".format(organism,timestr), "w+") as f:
        f.write("Number of nodes: {}\n".format(ppi_graph.number_of_nodes()))
        f.write("Number of edges: {}\n".format(ppi_graph.number_of_edges()))
        f.write("Number of connected components: {}\n".format(nx.number_connected_components(ppi_graph)))
        f.write("Number of essential genes: {}\n".format(essential_count))
        f.write("Max degree : {}\n".format(max_deg))
        f.flush()
        f.close()

    attr_names = np.concatenate((sl_names,ge_names,go_names))

    from pde_input_handler import SparseGraph, save_sparse_graph_to_npz
    mydataset = SparseGraph(adj_matrix=sp.sparse.csr_matrix(np_adj_matrix), attr_matrix=data, labels=labels, node_names=node_names, attr_names=attr_names)
    save_sparse_graph_to_npz("./{}-data.npz".format(organism), mydataset)

def gene_expression(organism):
    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))
    nhi2gene = {}
    expression_file = params_dict[organism]['ge']
    expression_size = 0

    non_zero_count = 0
    if organism == 'sc' or organism == 'mm' or organism == 'dm':
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
    
    np.save('{}-ge_feats.npy'.format(organism), ge_matrix, allow_pickle=False)
    # np.save('../GraphSAGE/example_data/{}-ge_feats.npy'.format(organism), ge_matrix)
    return ge_matrix, ["ge_" + str(i) for i in range(ge_matrix.shape[1])]

def subcellular_localization(organism):
    locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic', 'Golgi', 'Plasma', 'Endosome', 'Extracellular', 'Mitochondrion'] 

    name_index = json.load(open("./{}-name_index.json".format(organism)))
    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))

    sl_matrix = np.zeros((len(id_bioname_dict), 11), dtype=np.int8)
    with open(params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            name = line[1]
            sl_feature = line[3]
            if name not in name_index.keys() or not any([location in sl_feature for location in locations]):
                continue

            index = int(name_index[name])
            sl_index = [location in sl_feature for location in locations].index(True)
            sl_matrix[index, sl_index] += 1

    sl_non_zero_count = 0
    for line in sl_matrix:
        if sum(line) != 0:
            sl_non_zero_count += 1
    
    with open("{}_{}_log.txt".format(organism,timestr), "a+") as f:
        f.write("Number of genes that has subcellular localization vector: {}\n".format(sl_non_zero_count))
        f.flush()
        f.close()

    np.save('{}-sl_feats.npy'.format(organism), sl_matrix, allow_pickle=False)
    return sl_matrix, ["sl_" + location for location in locations]

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
                go_matrix[int(name_index[gene]), annotations.index(annotation)] += 1

    go_non_zero_count = 0
    for line in go_matrix:
        if sum(line) != 0:
            go_non_zero_count += 1
    
    with open("{}_{}_log.txt".format(organism,timestr), "a+") as f:
        f.write("Number of genes that has go annotation vector: {}\n".format(go_non_zero_count))
        f.flush()
        f.close()


    np.save('{}-go_feats.npy'.format(organism), go_matrix, allow_pickle=False)
    return go_matrix, ["go_" + annotation for annotation in annotations]

def merge_features(organism):
    sl = np.load('{}-sl_feats.npy'.format(organism))
    ge = np.load('{}-ge_feats.npy'.format(organism))
    if organism == "mm":
        ge = ge.astype(np.int32)
    go = np.load('{}-go_feats.npy'.format(organism))
    data = np.concatenate((sl,ge,go), axis=1)

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--organism', type=str, help='Organism name: sc hs mm dm all', default='sc')
    args = parser.parse_args()
    opt = vars(args)

    main(opt)
