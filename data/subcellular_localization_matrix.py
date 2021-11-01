'''
This script reads the gene names from scerevisiae_essentiality.txt and yeast_compartment_integrated_full.tsv
and finds the intersection of the genes in the two files. Then, it reads all GO annotation to find the set of
all annotations used. After that, it creates a matrix where the rows are the genes and the columns are the GO
annotations. The values in the matrix represent if that gene has the specific annotation or not.
'''

gene_names = set()
sc_names_two = set()

with open("scerevisiae_essentiality.txt", 'r') as f:
    for line in f:
        info = line.split('\t')
        gene_names.add(info[0])


with open("yeast_compartment_integrated_full.tsv", 'r') as f:
    for line in f:
        arr = line.split('\t')
        sc_names_two.add(arr[1])

related = gene_names.intersection(sc_names_two)
related_list = list(related)

go_annotations = set()
with open("yeast_compartment_integrated_full.tsv", 'r') as f:
    for line in f:
        arr = line.split('\t')
        if arr[1] in related:
            go_annotations.add(arr[2])

print(len(go_annotations))

annonation_vector = list(go_annotations)

data = [[0 for x in range(len(annonation_vector))] for y in range(len(related))]

with open("yeast_compartment_integrated_full.tsv", 'r') as f:
    for line in f:
        arr = line.split('\t')
        if arr[1] in related:
            data[related_list.index(arr[1])][annonation_vector.index(arr[2])] = 1

print(data)