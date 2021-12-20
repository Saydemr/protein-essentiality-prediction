

nhi2gene = {}
with open('GPL90-17389.txt', 'r') as f:
    for line in f:
        if line.startswith('#') or line.startswith('ID'):
            continue
        line = line.strip().split('\t')
        nhi2gene[line[0]] = line[1]

print(len(nhi2gene))

with open('GSE3431_series_matrix.txt', 'r') as f:
    with open('GSE3431_series_matrix_gene.txt', 'w+') as g:
        for line in f:
            line = line.strip()
            if line.startswith('!') or line.startswith('"ID_REF"'):
                continue
            line = line.split('\t')
            check = line[0].replace("\"","")

            if check in nhi2gene:
                if nhi2gene[check] == "":
                    continue
                g.write(nhi2gene[check] + '\t' + '\t'.join(line[1:]) + '\n')


with open('GSE3431_series_matrix_gene.txt', 'r+') as f:
    pass
