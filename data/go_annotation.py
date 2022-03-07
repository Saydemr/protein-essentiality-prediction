import numpy as np
import json
import sys

converter = {'sc' : 'yeast', 'hs' : 'human'}
go_dict = {}

organism = sys.argv[1]
with open( converter[organism] + '_compartment_knowledge_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        if line[1] in go_dict:
            go_dict[line[1]] += 1
        else:
            go_dict[line[1]] = 1

print(len(go_dict))
print(go_dict['LEM3'])
