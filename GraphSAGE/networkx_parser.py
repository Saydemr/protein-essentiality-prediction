from os import sep
import networkx as nx
from networkx.readwrite import json_graph
from random import choices
from collections import Counter
import json

print("Loading graph...")
ppi_graph = nx.Graph() 

id_map = {}
id_map_inv = {}
with open("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt") as f:
    f.readline()
    i = 0
    for line in f:
        line = line.strip()
        line = line.split("\t")
        ppi_graph.add_edge(int(line[3]), int(line[4]))
        
        if line[3] not in id_map:
            id_map[line[3]] = i
            id_map_inv[i] = int(line[3])
            i += 1
        if line[4] not in id_map:
            id_map[line[4]] = i
            id_map_inv[i] = int(line[4])
            i += 1

# 0 : training
# 1 : test
# 2 : validation

population = [0, 1, 2]
weights    = [0.8, 0.1, 0.1]
distribution_samples = choices(population, weights, k=ppi_graph.number_of_nodes())
print(Counter(distribution_samples))
for i in range(ppi_graph.number_of_nodes()):
    if distribution_samples[i] == 0:
        ppi_graph.nodes[id_map_inv[i]]['test'] = False 
        ppi_graph.nodes[id_map_inv[i]]['val']  = False 
    elif distribution_samples[i] == 1:
        ppi_graph.nodes[id_map_inv[i]]['test'] = True
        ppi_graph.nodes[id_map_inv[i]]['val']  = False
    else:
        ppi_graph.nodes[id_map_inv[i]]['test'] = False
        ppi_graph.nodes[id_map_inv[i]]['val']  = True

    #print(i)
    #print(ppi_graph.nodes[id_map_inv[i]]['test'], ppi_graph.nodes[id_map_inv[i]]['val'], sep="\t", end="\n")


print("Number of nodes: ", ppi_graph.number_of_nodes())
print("Number of connected components", nx.number_connected_components(ppi_graph))
print("Number of edges: ", ppi_graph.number_of_edges())
print("Writing graph to JSON file...")
json.dump(json_graph.node_link_data(ppi_graph), fp=open("ppi-G.json", "w+")) 
json.dump(id_map, fp=open("ppi-id_map.json", "w+"))
