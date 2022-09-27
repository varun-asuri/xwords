import sys
import time
import json
import pickle
import unidecode
import faster_than_requests as requests
from multiprocessing import Process

def run(words, id, lang):
    baseurl = "https://api.dictionaryapi.dev/api/v1/entries/{}/".format(lang)
    start = time.time()
    dct = {}
    for i, word in enumerate(words):
        if id == 0 and i % 10 == 0:
            print(i * 20)
        if len(dct) > 10:
            file = open("all-{}-{}/{}.txt".format(lang, lang, id), "a+")
            file.write(json.dumps(dct) + "\n")
            file.close()
            dct = {}
        word = unidecode.unidecode(word)
        url = baseurl + word
#        print(url)
        try:
            data = requests.get2json(url)
            dct[word] = data
        except:
            continue
#            print("Failed request for {}".format(word))
    file = open("all-{}-{}/{}.txt".format(lang, lang, id), "a+")
    file.write(json.dumps(dct) + "\n")
    file.close()


def get_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    chunks = []
    for i in range(0, len(lst), n):
        chunks.append(lst[i:min(i+n, len(lst))])
    return chunks

if __name__ == '__main__':
    start = time.time()
    NUM_PROCS = 20
    lang = sys.argv[1]
    words = pickle.load(open("{}-{}.pkl".format(lang, lang), "rb"))
    words = list(words.keys())[:400]
    chunks = get_chunks(words, len(words) // NUM_PROCS + 1)
    processes = []
    for id in range(NUM_PROCS):
        proc = Process(target=run, args=(chunks[id], id, lang))
        proc.start()
        processes.append(proc)
    for proc in processes:
        proc.join()

    print("Done!: {}".format(str(time.time() - start)))