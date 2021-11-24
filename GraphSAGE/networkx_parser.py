from os import sep
import networkx as nx
from networkx.readwrite import json_graph
from random import choices
from collections import Counter
import json
import numpy as np

print("Don't use the script anymore")
#exit()
print("Loading graph...")
ppi_graph = nx.Graph() 
'''
id_map = {}
id_map_inv = {}
id_map_int = {}
with open("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt") as f:
    f.readline()
    i = 0
    for line in f:
        line = line.strip()
        line = line.split("\t")
        if line[3] == line[4]:
            continue

        ppi_graph.add_edge(int(line[3]), int(line[4]))
        
        if line[3] not in id_map:
            id_map[line[3]] = i
            id_map[int(line[3])] = i
            id_map_inv[i] = int(line[3])
            i += 1
        if line[4] not in id_map:
            id_map[line[4]] = i
            id_map[int(line[4])] = i
            id_map_inv[i] = int(line[4])
            i += 1

'''

id_map = {}
id_map_int = {}
id_map_inv = {}
id_map_inv_int = {}

with open("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt") as f:
    f.readline()
    i = 0
    for line in f:
        line = line.strip()
        line = line.split("\t")
        if line[3] == line[4]:
            continue

        if int(line[3]) not in id_map_int and int(line[4]) not in id_map_int:
            ppi_graph.add_edge(i,i+1)

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
            i+=2

        elif int(line[3]) in id_map_int and int(line[4]) not in id_map_int:
            
            ppi_graph.add_edge(id_map_int[int(line[3])],i)

            id_map[line[4]] = i
            id_map_int[int(line[4])] = i
            id_map_inv[i] = line[4]
            id_map_inv_int[i] = int(line[4])

            ppi_graph.nodes[i]['id'] = i
            #print(id_map_int[int(line[3])], i)
            i+=1

            
        elif int(line[3]) not in id_map_int and int(line[4]) in id_map_int:
            
            ppi_graph.add_edge(i,id_map_int[int(line[4])])

            id_map[line[3]] = i
            id_map_int[int(line[3])] = i
            id_map_inv[i] = line[3]
            id_map_inv_int[i] = int(line[3])
            ppi_graph.nodes[i]['id'] = i
            
            #print(i, id_map_int[int(line[4])])
            i+=1

        else:
            ppi_graph.add_edge(id_map_int[int(line[3])],id_map_int[int(line[4])])


# 0 : training = train_removed false : test_removed true
# 1 : test     = train_removed true  : test_removed false
# 2 : validation = true true


print("Graph info...")
print("Number of nodes: ", ppi_graph.number_of_nodes())
print("Number of connected components", nx.number_connected_components(ppi_graph))
print("Number of edges: ", ppi_graph.number_of_edges())
print()

population = [0, 1, 2]
weights    = [0.8, 0.1, 0.1]
distribution_samples = choices(population, weights, k=ppi_graph.number_of_nodes())
print("Number of instances in training (0), test (1) and validation (2)\n",Counter(distribution_samples),sep='\n')
for i in range(ppi_graph.number_of_nodes()):
    if distribution_samples[i] == 0:
        ppi_graph.nodes[i]['test'] = False 
        ppi_graph.nodes[i]['val']  = False 
    elif distribution_samples[i] == 1:
        ppi_graph.nodes[i]['test'] = True
        ppi_graph.nodes[i]['val']  = False
    else:
        ppi_graph.nodes[i]['test'] = False
        ppi_graph.nodes[i]['val']  = True

    #print(i)
    #print(ppi_graph.nodes[id_map_inv[i]]['test'], ppi_graph.nodes[id_map_inv[i]]['val'], sep="\t", end="\n")

print("Checking the graph if smth is modified.")
print("Number of nodes: ", ppi_graph.number_of_nodes())
print("Number of connected components", nx.number_connected_components(ppi_graph))
print("Number of edges: ", ppi_graph.number_of_edges())
print()

print("Creating class-map")
id_name_dict ={}
with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        if line[3] == line[4]:
            continue
        id_name_dict[line[3]] = line[7]
        id_name_dict[line[4]] = line[8]

essential_dict = set()
with open('deg_sc.dat') as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[2])


class_map = {}
#print(id_map)
for i in id_map:
    my_str = id_name_dict[i]
    if my_str in essential_dict:
        class_map[i] = 1
    else:
        class_map[i] = 0

#print(class_map)

print('Creating id-map')
id_mappppp = {}
for i in range(ppi_graph.number_of_nodes()):
    id_mappppp[str(i)] = i

print("Writing graph to JSON file...")
json.dump(class_map, fp=open("eppugnn-class_map.json", "w+"))
json.dump(json_graph.node_link_data(ppi_graph), fp=open("eppugnn-G.json", "w+"))
json.dump({str(v): int(k) for k, v in id_map.items()}, fp=open("eppugnn-id_map_inv.json", "w+"))
json.dump(id_mappppp, fp=open("eppugnn-id_map.json", "w+"))
json.dump(id_map, fp=open("eppugnn-id_map_dummy.json", "w+"))
