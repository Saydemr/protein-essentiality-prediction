import sys
import json

organism = sys.argv[0]
id_name_dict = json.load(open('../data/{}-id_name_dict.json'.format(organism)))

essential_dict = set()
with open('deg_{}.dat'.format(organism)) as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[0])


class_map = {}
with open ('ppiemb.txt') as emb:
    with open('ppiemb_essentiality.txt','w+') as out:
        emb.readline()
        for line in emb:
            line = line.strip().split(' ')
            if id_name_dict[line[0]] in essential_dict:
                out.write('1\n')
            else:
                out.write('0\n')
