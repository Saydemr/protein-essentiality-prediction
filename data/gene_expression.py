
with open('GSE3431_series_matrix.txt', 'r') as f:
    for line in f:
        if line.startswith('!'):
            continue
        
        line = line.strip().split('\t')
        gene = line[0].removeprefix("\"").removesuffix("\"")
        #gene_biogrid_id = 