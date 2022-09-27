import sys
import time
import json
import pickle
from mtranslate import translate
#import unidecode
#from multiprocessing import Process
#from multiprocessing import Pool


def run_word(from_lang, to_lang, defs):
    translated = []
    for defi in set(defs):
#        time.sleep(1)
        trans = translate(defi, to_lang, from_lang)
        translated.append((defi, trans))
    return translated


def run(args):
    words, id, initial_lang, target_lang, definitions = args
    file = open("all2-{}-{}/{}.txt".format(initial_lang, target_lang, id), "r")
    lines = [line.strip() for line in file]
    already_there = set()
    for line in lines:
        temp = json.loads(line)
        for key in temp:
            already_there.add(key)
    print(len(already_there))
    dct = {}
    failed = 0
    for i, word in enumerate(words):
        if id == 0 and i % 10 == 0:
            print(i * 1)
            if failed:
                print("{}%".format(str(100 * (i - failed) / i)), failed)
        if word in already_there:
            continue
        if len(dct) > 10:
            file = open("all2-{}-{}/{}.txt".format(initial_lang, target_lang, id), "a+")
            file.write(json.dumps(dct) + "\n")
            file.close()
            dct = {}
#            break
        translated = run_word(initial_lang, target_lang, definitions[word])
        if not translated:
            print("Confusion 1000")
            return
        dct[word] = translated
    file = open("all2-{}-{}/{}.txt".format(initial_lang, target_lang, id), "a+")
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
    NUM_PROCS = 1
    initial_lang = sys.argv[1]
    target_lang = sys.argv[2]
    data = pickle.load(open("../../pickles/full-{}-{}.pkl".format(initial_lang, initial_lang), "rb"))
    words = list(data.keys())
    chunks = get_chunks(words, len(words) // NUM_PROCS + 1)
    processes = []
    args = [(chunks[i], i, initial_lang, target_lang, data) for i in range(NUM_PROCS)]
    run(args[0])

    print("Done!: {}".format(str(time.time() - start)))