from operator import itemgetter
lines = []
a = set()
b = set()
with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt', 'r') as f:
    f.readline()
    #with open('node2vec_inp_ppi_yeast.txt', 'w') as f1:
    for line in f:
        line = line.split('\t')
        a.add(line[3] + '\t' + line[4])
        lines.append( [line[3], line[4]])
print(len(a))

print('\n\n\n\n\n\n\n\n')
aa = sorted(lines, key=lambda x: x[1])
print(*aa[:10], sep='\n')