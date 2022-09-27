import os
import sys
import json
import pickle

lang1, lang2 = sys.argv[1], sys.argv[2]
data = {}
base = "all2-{}-{}/".format(lang1, lang2)
filenames = os.listdir(base)
for filename in filenames:
    file = open(base + filename)
    lines = [line.strip() for line in file]
    for line in lines:
        temp = json.loads(line)
        for key in temp:
            if key not in data: data[key] = []
            data[key].extend(temp[key])

for key in data:
    data[key] = {data[key][i][1] for i in range(len(data[key]))}


print(len(data))
keys = list(data.keys())
print(keys[0], data[keys[0]])
print(keys[1], data[keys[1]])

pickle.dump(data, open("full-{}-{}.pkl".format(lang1, lang2), "wb"))