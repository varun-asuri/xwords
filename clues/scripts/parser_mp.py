import sys
import time
import json
import pickle
import unidecode
from multiprocessing import Process
from Naked.toolshed.shell import muterun_js

def get_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    chunks = []
    for i in range(0, len(lst), n):
        chunks.append(lst[i:min(i+n, len(lst))])
    return chunks


def run(words, id, lang):
    start = time.time()
    dct = {}
    chunk_size = 100
    chunks = get_chunks(words, chunk_size)
    for i, chunk in enumerate(chunks):
        cmd = ' '.join(['nodeDict.js', lang] + chunk)
        naked_object = muterun_js(cmd)
        output = naked_object.stdout.decode("utf-8").strip().split("\n")[1].strip()
#        data = json.loads(output)

#        for key in data:
#            if key not in dct: dct[key] = []
#            dct[key].extend(data[key])

        if id == 0:
            print(i * 20 * chunk_size)
        file = open("all-{}-{}/{}.txt".format(lang, lang, id), "a+")
#        file.write(json.dumps(dct) + "\n")
        file.write(json.dumps(output) + "\n")
        file.close()
        dct = {}

    file = open("all-{}-{}/{}.txt".format(lang, lang, id), "a+")
    file.write(json.dumps(dct) + "\n")
    file.close()


if __name__ == '__main__':
    start = time.time()
    NUM_PROCS = 20
    lang = sys.argv[1]
    words = pickle.load(open("{}-{}.pkl".format(lang, lang), "rb"))
    words = list(words.keys())
    chunks = get_chunks(words, len(words) // NUM_PROCS + 1)
    processes = []
    for id in range(NUM_PROCS):
        proc = Process(target=run, args=(chunks[id], id, lang))
        proc.start()
        processes.append(proc)
    for proc in processes:
        proc.join()

    print("Done!: {}".format(str(time.time() - start)))