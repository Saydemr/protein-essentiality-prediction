
gene_names = set()
useful_info = []

with open("biogrid_DEG_scerevisiae.txt", 'r') as f:
    for line in f:
        info = line.split('\t')
        if info[2] not in gene_names:
            gene_name = line.split('\t')[2].split('|')[1].split(':')[1]
            gene_names.add(gene_name)



with open("gene_essentiality.txt", 'r') as f: 
    f.readline()
    for line in f:
        gene_name1 = line.split('\t')[3]
        if gene_name1 in gene_names:
            essentiality = line.split('\t')[4]
            es_bool = line.split('\t')[5]
            with open("scerevisiae_essentiality.txt", 'a+') as f:
                f.write(gene_name1 + '\t' + essentiality + '\t' + es_bool + '\n')
