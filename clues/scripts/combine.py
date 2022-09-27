import json
import sys
import os
import pickle

lang = sys.argv[1]
base = "all-{}-{}/".format(lang, lang)
files = os.listdir(base)
data = {}
for filename in files:
    file = open(base + filename, "r")
    lines = [line.strip() for line in file]
    for line in lines:
        dct = json.loads(line)
        for key in dct:
            data[key] = json.loads(dct[key])

pickle.dump(data, open("full-{}-{}.pkl".format(lang, lang), "wb+"))