import json

'''class_map = None
with open('ppi-class_map.json', 'r') as f:
    class_map = json.load(f)


print(len(class_map["1"]))
print(len(class_map["2"]))

for i in range(len(class_map)):
    print(len(class_map[str(i)]))'''

g_map = None
with open('toy-ppi-G.json', 'r') as f:
    g_map = json.load(f)

print(g_map["nodes"][1]["label"])