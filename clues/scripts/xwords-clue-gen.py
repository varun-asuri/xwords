#you need to be in a directory that has language pkl files to work.  An example is de-de.pkl
import sys, requests, pickle, os
language = sys.argv[1]
outfilename = language+"-"+language+"-1.pkl"
newdict = pickle.load(open(outfilename, "rb")) if os.path.isfile(outfilename) else {}
baseurl = "https://api.dictionaryapi.dev/api/v1/entries/"
langDict = pickle.load(open(language+"-"+language+".pkl", "rb"))
#print(requests.get('https://api.dictionaryapi.dev/api/v1/entries/de/alkdjf').json())
counter = 0
for word in langDict:
    if word in newdict:
        continue
    wordinfo = requests.get(baseurl+language+"/"+word).json()
    if 'title' in wordinfo:
        continue
    counter += 1
    meanings = wordinfo[0]['meaning']
    newdict[word] = meanings[list(meanings.keys())[0]][0]['definition']
    if counter % 100 == 0:
        pickle.dump(newdict, open(outfilename, "wb"))
pickle.dump(newdict, open(outfilename, "wb"))
