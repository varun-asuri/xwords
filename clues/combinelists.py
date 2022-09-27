import glob, os

exclude = ['dctFrench.txt', 'dctMasterEng.txt']
path = 'crossword_dictionaries/'
words = set()
for filename in os.listdir(path):
    if filename not in exclude: 
        print(filename)
        words.update(open(path + filename, "r").read().strip().split('\n'))

print('{} words total'.format(len(words)))

f = open("crossword_dictionaries/dctMasterEng.txt", "w")
for w in words: 
    if w.isalpha() and len(w) > 2:
        print(w.lower().replace('-', '').replace(' ', '').replace("'", ''), file = f)
f.close()