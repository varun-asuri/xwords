from multiprocessing import Process, Manager
#you need to be in a directory that has language pkl files to work.  An example is de-de.pkl
import sys, requests, pickle, os

def run(baseurl, language, word, newdict, counter, outfilename):
    #print(newdict)
    wordinfo = requests.get(baseurl+language+"/"+word).json()
    if 'title' in wordinfo:
        return
    counter.value += 1
    meanings = wordinfo[0]['meaning']
#    print("Got meaning of: " + word)
#    print(meanings)
    newdict[word] = {meanings[meaning][0]['definition'] for meaning in meanings}
    if counter.value % 200 == 0:
        print(counter.value)
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
#    words = words[:150]
    print(len(words))
#    print(words)
#    print(len(words))
    processes = []
    manager = Manager()
    newdict = manager.dict()
    counter = manager.Value('i', 0)
    for i, word in enumerate(words):
        proc = Process(target=run, args=(baseurl, language, word, newdict, counter, outfilename))
        proc.start()
        processes.append(proc)
        if i % 300 == 0:
            for proc in processes:
                proc.join()
            processes = []
#        proc.join()

    print("Created all processes, now joining them")
    for proc in processes:
        proc.join()

    pickle.dump(dict(newdict), open(outfilename, "wb"))

#pickle.dump(newdict, open(outfilename, "wb"))
