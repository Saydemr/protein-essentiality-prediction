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


def main(opt):
    create_graph(opt['organism'])


def create_graph(organism):
    """
    Create a networkx graph from the BIOGRID data
    """
    print("Organism: {}".format((params_dict[organism]['full_name']).replace('_', ' ')))
    print("Loading graph...")

    ppi_graph = nx.Graph()

    id_map = {}
    id_map_int = {}
    id_map_inv = {}
    id_map_inv_int = {}
    id_name_dict = {}

    files = fnmatch.filter(os.listdir('./'),
                           'BIOGRID-ORGANISM-{}*-4.4.*.tab3.txt'.format(params_dict[organism]['full_name']))
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

                #print(i, i+1)
                i += 2

            elif int(line[1]) in id_map_int and int(line[2]) not in id_map_int:

                ppi_graph.add_edge(id_map_int[int(line[1])], i)

                id_map[line[2]] = i
                id_map_int[int(line[2])] = i
                id_map_inv[i] = line[2]
                id_map_inv_int[i] = int(line[2])

                ppi_graph.nodes[i]['id'] = i
                #print(id_map_int[int(line[1])], i)

                i += 1

            elif int(line[1]) not in id_map_int and int(line[2]) in id_map_int:

                ppi_graph.add_edge(i, id_map_int[int(line[2])])

                id_map[line[1]] = i
                id_map_int[int(line[1])] = i
                id_map_inv[i] = line[1]
                id_map_inv_int[i] = int(line[1])
                ppi_graph.nodes[i]['id'] = i

                #print(i, id_map_int[int(line[2])])

                i += 1

            else:
                ppi_graph.add_edge(
                    id_map_int[int(line[1])], id_map_int[int(line[2])])

    np_adj_matrix = nx.to_numpy_matrix(ppi_graph)
    sp.sparse.save_npz('../grand_blend/{}_adj_matrix.npz'.format(organism),
                       sp.sparse.csr_matrix(np_adj_matrix))

    # 0 : training = train_removed false : test_removed true
    # 1 : test     = train_removed true  : test_removed false
    # 2 : validation = true true

    print("Graph info...")
    print("Number of nodes: ", ppi_graph.number_of_nodes())
    print("Number of connected components",
          nx.number_connected_components(ppi_graph))
    print("Number of edges: ", ppi_graph.number_of_edges())
    print()

    # # These lines are not needed for the current dataset
    # for component in list(nx.connected_components(ppi_graph)):
    #     if len(component) < 3:
    #         for node in component:
    #             ppi_graph.remove_node(node)

    print("Checking the graph if smth is modified.")
    print("Number of nodes: ", ppi_graph.number_of_nodes())
    print("Number of connected components",
          nx.number_connected_components(ppi_graph))
    print("Number of edges: ", ppi_graph.number_of_edges())
    print()

    with open("{}_ppi_graph.txt".format(organism), "w+") as f:
        for e in ppi_graph.edges():
            a, b = e
            f.write(str(id_map_inv_int[a]) + " " + str(id_map_inv_int[b]) + "\n")

    population = [0, 1, 2]
    weights = [0.8, 0.1, 0.1]
    distribution_samples = choices(population, weights, k=ppi_graph.number_of_nodes())

    print("Number of instances in training (0), test (1) and validation (2)\n", Counter(distribution_samples), sep='\n')
    print("Number of instances in training (0), test (1) and validation (2)\n", Counter(distribution_samples), sep='\n', file=open("{}_distribution_samples.txt".format(organism), "w+"))

    for i in range(ppi_graph.number_of_nodes()):
        if distribution_samples[i] == 0:
            ppi_graph.nodes[i]['test'] = False
            ppi_graph.nodes[i]['val'] = False
        elif distribution_samples[i] == 1:
            ppi_graph.nodes[i]['test'] = True
            ppi_graph.nodes[i]['val'] = False
        else:
            ppi_graph.nodes[i]['test'] = False
            ppi_graph.nodes[i]['val'] = True

        # print(i)
        # print(ppi_graph.nodes[id_map_inv[i]]['test'], ppi_graph.nodes[id_map_inv[i]]['val'], sep="\t", end="\n")

    print("Creating class-map")
    essential_dict = set()
    with open('deg_{}.dat'.format(organism)) as f:
        for line in f:
            line = line.strip().split('\t')
            essential_dict.add(line[0])

    class_map = {}
    # print(id_map)
    y_mat = np.zeros(ppi_graph.number_of_nodes(), dtype=np.int8)

    for i in id_map:
        my_key = id_map[i]
        my_str = id_name_dict[i]
        if my_str in essential_dict:
            class_map[my_key] = 1
            y_mat[my_key] = 1
        else:
            class_map[my_key] = 0

    
    np.save('../grand_blend/{}_y_mat.npy'.format(organism), y_mat)
    # print(class_map)

    print('Creating id-map')
    sage_id_map = {}
    for i in range(ppi_graph.number_of_nodes()):
        sage_id_map[str(i)] = i

    print("Writing graphs to JSON files...")

    json.dump(class_map, fp=open(
        "../GraphSAGE/{}-class_map.json".format(organism), "w+"))
    json.dump(json_graph.node_link_data(ppi_graph),
              fp=open("../GraphSAGE/{}-G.json".format(organism), "w+"))
    json.dump({str(v): int(k) for k, v in id_map.items()},
              fp=open("../GraphSAGE/{}-id_map_inv.json".format(organism), "w+"))
    json.dump({str(v): int(k) for k, v in id_map.items()},
              fp=open("./{}-id_map_inv.json".format(organism), "w+"))
    json.dump(sage_id_map, fp=open(
        "../GraphSAGE/{}-id_map.json".format(organism), "w+"))
    json.dump(id_map, fp=open(
        "../GraphSAGE/{}-id_map_dummy.json".format(organism), "w+"))
    json.dump(id_name_dict, fp=open(
        "./{}-id_name_dict.json".format(organism), "w+"))

    gene_expression(organism)
    subcellular_localization(organism)
    # go_annotation(organism)
    # rna_seq(organism)
    merge_features(organism)

def gene_expression(organism):
    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))
    nhi2gene = {}
    expression_file = params_dict[organism]['ge']
    expression_size = 0

    if organism == 'sc':
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

    ge_matrix  = np.zeros((len(id_bioname_dict), expression_size))
    id_map     = json.load(open("./{}-id_map_inv.json".format(organism)))
    name_index = {id_bioname_dict[str(id_map[v]).strip()] : v  for v in id_map.keys()}


    with open(expression_file.replace(".txt", "_gene.txt"), 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            name = line[0]
            ge_vector = line[1:]

            if name not in name_index.keys():
                continue

            index = int(name_index[name])
            ge_matrix[index] = ge_vector

    np.save('{}-ge_feats.npy'.format(organism), ge_matrix)
    
def subcellular_localization(organism):
    locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

    id_map = json.load(open('{}-id_map_inv.json'.format(organism)))
    id_bioname_dict = json.load(open("./{}-id_name_dict.json".format(organism)))
    name_index = {id_bioname_dict[str(id_map[v]).strip()] : v  for v in id_map.keys()}

    sl_matrix = np.zeros((len(id_map), 11))
    with open(params_dict[organism]['go'], 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            name = line[1]
            sl_feature = line[3]
            if name not in name_index.keys() or sl_feature not in locations:
                continue
            index = int(name_index[name])
            sl_matrix[index, locations.index(sl_feature)] = 1


    np.save('{}-sl_feats.npy'.format(organism), sl_matrix)

def go_annotation(organism):
    # TODO
    pass


def rna_seq(organism):
    # TODO
    pass


def merge_features(organism):
    b = np.load('{}-ge_feats.npy'.format(organism), allow_pickle=True, fix_imports=True, encoding='latin1')
    a = np.load('{}-sl_feats.npy'.format(organism), allow_pickle=True, fix_imports=True, encoding='latin1')

    c = np.concatenate((a, b), axis=1)

    print(c.shape)
    np.save('{}-feats.npy'.format(organism), c)
    sp.sparse.save_npz('../grand_blend/{}-feats.npz'.format(organism), sparse.csr_matrix(c))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--organism', type=str, help='Organism name : sc hs')
    args = parser.parse_args()
    opt = vars(args)

    main(opt)
