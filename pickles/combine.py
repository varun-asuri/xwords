import pickle
import sys

initial = sys.argv[1]
targets = sys.argv[2:]

combined = {}
for target in targets:
    data = pickle.load(open("full-{}-{}.pkl".format(initial, target), "rb"))
    for word in data:
        temp = word.lower()
        if temp not in combined: combined[temp] = {}
        combined[temp][target] = set(data[word])


missing = {i: 0 for i in targets}
errors = set()
for word in combined:
    if len(combined[word]) != len(sys.argv) - 2:
        errors.add(word)
        temp = targets - combined[word].keys()
        for t in temp:
            missing[t] += 1

print(len(errors))
print(missing)

for i, err in enumerate(errors):
    del combined[err]


# Check to make sure there's no erroring words left
errors = set()
for word in combined:
    if len(combined[word]) != len(sys.argv) - 2:
        errors.add(word)
print(len(errors))



pickle.dump(combined, open("full-{}.pkl".format(initial), "wb+"))