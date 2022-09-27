from multiprocessing import Process, Manager
#you need to be in a directory that has language pkl files to work.  An example is de-de.pkl
import sys, requests, pickle, os

def run(baseurl, language, word, newdict, counter, outfilename):
    wordinfo = requests.get(baseurl+language+"/"+word).json()
    if 'title' in wordinfo:
        return
    counter.value += 1
    if not isinstance(wordinfo, list) or not wordinfo:
        return
    word_data = wordinfo[0]
    if 'meaning' not in word_data:
        return
    meanings = word_data['meaning']
    word_meanings = set()
    for word_type in meanings:
        meaning = meanings[word_type][0]
        assert('definition' in meaning and 'synonyms' in meaning)
        definition = meaning['definition']
        synonyms = meaning['synonyms']
        word_meanings.add(definition)
        if len(synonyms) > 3:
            word_meanings.add("Synonyms: " + ', '.join())
#    print(word_meanings)
#    newdict[word] = "HI"
#    print(newdict)
    newdict[word] = word_meanings
    if counter.value % 200 == 0:
        print(counter.value, len(dict(newdict)))
        pickle.dump(dict(newdict), open(outfilename, "wb"))


if __name__ == '__main__':
    language = sys.argv[1]
    outfilename = language+"-"+language+"-1.pkl"
    newdict = pickle.load(open(outfilename, "rb")) if os.path.isfile(outfilename) else {}
    baseurl = "https://api.dictionaryapi.dev/api/v1/entries/"
    langDict = pickle.load(open(language+"-"+language+".pkl", "rb"))
    counter = 0
    print("The process has started")

    words = [word for word in langDict if word not in newdict]
    words = words[:10]
    assert(len(words) == 10)
    print(len(words))
#    print(words)
#    print(len(words))
    processes = []
    manager = Manager()
    newdict = manager.dict()
    counter = manager.Value('i', 0)
    for i, word in enumerate(words):
        print(i)
        proc = Process(target=run, args=(baseurl, language, word, newdict, counter, outfilename))
#        run(baseurl, language, word, newdict, counter, outfilename)
        proc.start()
        processes.append(proc)
        if i % 300 == 0:
            for proc in processes:
                proc.join()
            processes = []
        proc.join()

    print("Created all processes, now joining them")
    for proc in processes:
        proc.join()

    print(len(dict(newdict)))
    pickle.dump(dict(newdict), open(outfilename, "wb"))

#pickle.dump(newdict, open(outfilename, "wb"))