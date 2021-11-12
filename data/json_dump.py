from os import link
import numpy as np

nodes = []
links = []

'''
with open("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt", 'r') as f:
    f.readline()
    with open("BIOGRID-ORGANISM-PPI-ONLY.txt", 'w+') as f1:
        for line in f:
            gene_id1 = line.split('\t')[3]
            gene_id2 = line.split('\t')[4]
            f1.write(gene_id1 + '\t' + gene_id2 + '\n')
'''


'''
with open("BIOGRID-ORGANISM-PPI-ONLY.txt", 'r') as f:
    with open ("BIOGRID-clean.txt",'w+') as f1:
        for line in f:
            gene_id1 = line.strip().split('\t')[0]
            gene_id2 = line.strip().split('\t')[1]
            if gene_id1 == gene_id2:
                continue
            f1.write(gene_id1 + '\t' + gene_id2 + '\n')

a = set()
with open ("BIOGRID-reverses.txt",'r') as f:
    for line in f:
        arr = line.strip().split('\t')
        #print(arr)

        a.add(int(arr[0]))
        a.add(int(arr[1]))


b = list(a)
c = sorted(b)
#print(c)
min_num = min(b)
max_num = max(b)
print(min_num, max_num)
print(len(c))

my_dict = {}
my_dict_r = {}
for i in range(len(c)):
    my_dict.update({c[i]:i})
    my_dict_r.update({i:c[i]})

#np.save('mapping.npy', my_dict)

beeg_matrix = np.zeros((len(a), len(a)))

with open ("BIOGRID-reverses.txt",'r') as f:
    for line in f:
        arr = line.strip().split('\t')
        #print(arr)
        beeg_matrix[my_dict[int(arr[0])]][my_dict[int(arr[1])]] = 1

with open("BIOGRID-clean.txt", 'w+') as f:
    for i in range(len(beeg_matrix)):
        for j in (range(i,len(beeg_matrix[i])))[::-1]:
            if beeg_matrix[i][j] == 1 or beeg_matrix[j][i] == 1:
                f.write(str(my_dict_r[i]) + '\t' + str(my_dict_r[j]) + '\n')

with open("BIOGRID-reverse.txt", 'w+') as f1:
    for [gene_id1, gene_id2] in b:
        f1.write(gene_id1 + '\t' + gene_id2 + '\n')
'''

num_nodes = set()
with open("BIOGRID-clean.txt", 'r') as f:
    for line in f:
        arr = line.strip().split('\t')
        num_nodes.add(int(arr[0]))
        num_nodes.add(int(arr[1]))
        link_dict = {"source": int(arr[0]), "target": int(arr[1])}
        links.append(link_dict)

item_count = len(num_nodes)

min_num = min(num_nodes)
max_num = max(num_nodes)
print(min_num, max_num)
print(len(num_nodes))

sorted_list = sorted(list(num_nodes))

my_dict = {}
my_dict_r = {}
for i in range(len(sorted_list)):
    my_dict.update({sorted_list[i]:i})
    my_dict_r.update({i:sorted_list[i]})

print(item_count)
eighty_percent = int(item_count * 0.8)
ten_percent    = int(item_count * 0.1)
rest           = item_count - eighty_percent - ten_percent

for i in range(0, eighty_percent):
    my_dict = {"test": False, "id": i, "val": False}
    nodes.append(my_dict)

for i in range(eighty_percent, eighty_percent + ten_percent):
    my_dict = {"test": True, "id": i, "val": False}
    nodes.append(my_dict)

for i in range(eighty_percent + ten_percent, item_count):
    my_dict = {"test": False, "id": i, "val": True}
    nodes.append(my_dict)

print(eighty_percent+ten_percent+rest)

print(len(nodes))
print(len(links))

#print(*links,sep='\n')
#print(*nodes,sep='\n')

# Combining data

the_dict = {"directed": False, "graph": {}, "nodes": nodes, "links": links, "multigraph": False}
print(the_dict, file=open("saccera-G.json", "w+"))

id_map = {}
for i in range(item_count):
    id_map.update({str(i):i})
print(id_map, file=open("saccera-id_map.json","w+"))