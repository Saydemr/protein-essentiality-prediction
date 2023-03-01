import eppugnn as EP

for org in ["sc", "dm", "mm", "hs"]:
    dataset = EP.Eppugnn(root="./", name=org, custom_split=(0.6, 0.2))
