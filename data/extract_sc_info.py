
gene_names = set()
useful_info = []

with open("deg_annotation_e.txt", 'r') as f:
    for line in f:
        info = line.split('\t')
        if len(info) < 8:
            continue
        if info[7] == "Saccharomyces cerevisiae" and info[2] not in gene_names:
            print(info[7], info[2])
            gene_names.add(info[2])



with open("BIOGRID-ALL-4.4.202.mitab.txt", 'r') as f: 
    f.readline()
    for line in f:
        gene_name = line.split('\t')[2].split('|')[1].split(':')[1]
        if gene_name in gene_names:
            with open("information.txt", 'a+') as f:
                f.write(line)
