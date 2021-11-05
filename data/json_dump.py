

links = []

with open("biogrid_DEG_scerevisiae.txt", 'r') as f:
    for line in f: 
        gene_name1 = line.split('\t')[2].split('|')[1].split(':')[1]
        gene_name2 = line.split('/t')[3].split('|')[1].split(':')[1]
        my_dict = {"source": gene_name1, "target": gene_name2}
        links.append(my_dict)

        