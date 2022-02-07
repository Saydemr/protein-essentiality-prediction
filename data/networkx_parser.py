from os import sep
import string
import networkx as nx
from networkx.readwrite import json_graph
from random import choices
from collections import Counter
import json
import numpy as np
import scipy as sp
from scipy import sparse
import argparse
import os
import fnmatch

full_name = {'sc': 'Saccharomyces_cerevisiae',
             'mm': 'Mus_musculus', 'hs': 'Homo_sapiens'}


def main(opt):
    if not opt == 'all':
        create_graph(opt['organism'])
    else:
        create_graph('sc')
        create_graph('mm')
        create_graph('hs')


def create_graph(organism):
    """
    Create a networkx graph from the BIOGRID data
    """
    print("Organism: {}".format(full_name[organism].replace('_', ' ')))
    print("Loading graph...")

    ppi_graph = nx.Graph()

    id_map = {}
    id_map_int = {}
    id_map_inv = {}
    id_map_inv_int = {}
    id_name_dict = {}

    files = fnmatch.filter(os.listdir('./'),
                           'BIOGRID-ORGANISM-{}*-4.4.*.tab3.txt'.format(full_name[organism]))
    if len(files) == 0:
        print("No data available for {}".format(full_name[organism]))
        print("Please run update.py in base directory")
        exit()

    with open(files[0]) as f:
        f.readline()
        i = 0
        for line in f:
            line = line.strip()
            line = line.split("\t")
            if line[3] == line[4]:
                continue

            id_name_dict[line[3]] = line[7]
            id_name_dict[line[4]] = line[8]

            if int(line[3]) not in id_map_int and int(line[4]) not in id_map_int:
                ppi_graph.add_edge(i, i+1)

                id_map[line[3]] = i
                id_map_int[int(line[3])] = i
                id_map_inv[i] = line[3]
                id_map_inv_int[i] = int(line[3])
                ppi_graph.nodes[i]['id'] = i

                id_map[line[4]] = i+1
                id_map_int[int(line[4])] = i+1
                id_map_inv[i+1] = line[4]
                id_map_inv_int[i+1] = int(line[4])
                ppi_graph.nodes[i+1]['id'] = i+1

                #print(i, i+1)
                i += 2

            elif int(line[3]) in id_map_int and int(line[4]) not in id_map_int:

                ppi_graph.add_edge(id_map_int[int(line[3])], i)

                id_map[line[4]] = i
                id_map_int[int(line[4])] = i
                id_map_inv[i] = line[4]
                id_map_inv_int[i] = int(line[4])

                ppi_graph.nodes[i]['id'] = i
                #print(id_map_int[int(line[3])], i)

                i += 1

            elif int(line[3]) not in id_map_int and int(line[4]) in id_map_int:

                ppi_graph.add_edge(i, id_map_int[int(line[4])])

                id_map[line[3]] = i
                id_map_int[int(line[3])] = i
                id_map_inv[i] = line[3]
                id_map_inv_int[i] = int(line[3])
                ppi_graph.nodes[i]['id'] = i

                #print(i, id_map_int[int(line[4])])

                i += 1

            else:
                ppi_graph.add_edge(
                    id_map_int[int(line[3])], id_map_int[int(line[4])])

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

    # These lines are not needed for the current dataset
    for component in list(nx.connected_components(ppi_graph)):
        if len(component) < 3:
            for node in component:
                ppi_graph.remove_node(node)

    print("Checking the graph if smth is modified.")
    print("Number of nodes: ", ppi_graph.number_of_nodes())
    print("Number of connected components",
          nx.number_connected_components(ppi_graph))
    print("Number of edges: ", ppi_graph.number_of_edges())
    print()

    with open("{}_ppi_graph.txt".format(organism), "w+") as f:
        for e in ppi_graph.edges():
            a, b = e
            f.write(str(id_map_inv_int[a]) + " " +
                    str(id_map_inv_int[b]) + "\n")

    population = [0, 1, 2]
    weights = [0.8, 0.1, 0.1]
    distribution_samples = choices(
        population, weights, k=ppi_graph.number_of_nodes())

    print("Number of instances in training (0), test (1) and validation (2)\n",
          Counter(distribution_samples), sep='\n')
    print("Number of instances in training (0), test (1) and validation (2)\n", Counter(
        distribution_samples), sep='\n', file=open("{}_distribution_samples.txt".format(organism), "w+"))

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
        #print(ppi_graph.nodes[id_map_inv[i]]['test'], ppi_graph.nodes[id_map_inv[i]]['val'], sep="\t", end="\n")

    print("Creating class-map")
    essential_dict = set()
    with open('deg_{}.dat'.format(organism)) as f:
        for line in f:
            line = line.strip().split('\t')
            essential_dict.add(line[2])

    class_map = {}
    # print(id_map)
    y_mat = np.zeros((ppi_graph.number_of_nodes(), 1), dtype=np.int8)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--organism', type=str,
                        help='Organism name : sc hs mm all')
    args = parser.parse_args()
    opt = vars(args)

    main(opt)
