import sys
import json
import pickle
from Naked.toolshed.shell import muterun_js

lang = sys.argv[1]
words = pickle.load(open("pickles/{}-{}.pkl".format(lang, lang), "rb"))
words = list(words.keys())[:100]

cmd = ' '.join(['nodeDict.js', '1', lang] + words)
print(cmd)
print("Executing")
naked_object = muterun_js(cmd)
output = naked_object.stdout.decode("utf-8").strip().split("\n")[1].strip()
data = json.loads(output)
print(data.keys(), len(data.keys()))