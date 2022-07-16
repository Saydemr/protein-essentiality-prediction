import numpy as np
for i in range(5):
    avgs = np.zeros(10)
    count = 0
    with open("sc_results_" + str(i) + ".csv") as f:
        f.readline()
        for line in f:
            line = line.strip().split(",")
            count += 1
            for index, item in enumerate(line):
                if index < 7:
                    continue
                else:
                    avgs[index-7] += float(item)
    avgs = list(avgs)

    for i in range(len(avgs)):
        avgs[i] = avgs[i] / count
    print(avgs)    
