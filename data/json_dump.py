
from os import unlink

nodes = []
links = []

with open("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt", 'r') as f:
    f.readline()
    for line in f: 
        gene_id1 = line.split('\t')[3]
        gene_id2 = line.split('\t')[4]
        my_dict = {"source": gene_id1, "target": gene_id2}
        links.append(my_dict)


helper_list = []
unique = []
item_count = 0
with open("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt", 'r') as f:
    f.readline()
    for line in f: 
        gene_id1 = line.split('\t')[3]
        gene_id2 = line.split('\t')[4]
        if gene_id1 not in unique:
            helper_list.append([gene_id1, item_count])
            unique.append(gene_id1)
            item_count += 1
        if gene_id2 not in unique:
            helper_list.append([gene_id2, item_count])
            unique.append(gene_id2)
            item_count += 1


eighty_percent = int(item_count * 0.8)
ten_percent    = int(item_count * 0.1)
rest           = item_count - eighty_percent - ten_percent

for i in range(0, eighty_percent):
    my_dict = {"test": False, "id": int(helper_list[i]), "val": False}
    nodes.append(my_dict)

for i in range(eighty_percent, eighty_percent + ten_percent):
    my_dict = {"test": True, "id": int(helper_list[i]), "val": False}
    nodes.append(my_dict)

for i in range(eighty_percent + ten_percent, item_count):
    my_dict = {"test": False, "id": int(helper_list[i]), "val": True}
    nodes.append(my_dict)

print(nodes)