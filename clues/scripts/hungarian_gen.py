import sys
import time
import json
import pickle
import unidecode
#import faster_than_requests as requests
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup

NUM_PROCS = 1
def run(words, id, lang):
    base_url = "https://glosbe.com/hu/en/{}"
    start = time.time()
    dct = {}
    failed = 0
    print(len(words))
    file = open("all-{}-{}/{}.txt".format(lang, lang, id), "r")
    lines = [line.strip() for line in file]
    already_there = set()
    for line in lines:
        temp = json.loads(line)
        for key in temp:
            already_there.add(key)
    for i, word in enumerate(words):
        if id == 0 and i % 10 == 0:
            print(i * NUM_PROCS, len(dct))
            if failed:
                print("{}%".format(str(100 * (i - failed) / i)), failed)
        if word in already_there:
            continue
        if len(dct) > 10:
            file = open("all-{}-{}/{}.txt".format(lang, lang, id), "a+")
            file.write(json.dumps(dct) + "\n")
            file.close()
            dct = {}
        try:
            page = requests.get(base_url.format(word))
            if page.status_code != 200:
                print("Error:", page)
#            print(page.headers)
#            print(page.content, page.text)
            soup = BeautifulSoup(page.content, 'html.parser')
            meaning_elems = soup.find_all('div', class_='meaningContainer')
#            print(meaning_elems)
            job_elems = []
            for i, elem in enumerate(meaning_elems):
                if i > 3:
                    break
                job_elems.append(elem.find_all('div', class_='phraseMeaning')[0])
#            print(job_elems)
            defs = {elem.text for elem in job_elems}
#            print(defs)
            if defs:
                dct[word] = list(defs)
#            else:
#                print("No definitions: {}".format(word))
        except Exception as e:
#            print("REE IT FAILED")
            print("Failed request for {}: {}".format(word, str(e)))
            failed += 1
            continue
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
    lang = sys.argv[1]
    words = pickle.load(open("pickles/{}-{}.pkl".format(lang, lang), "rb"))
    words = list(words.keys())
    chunks = get_chunks(words, len(words) // NUM_PROCS + 1)
    processes = []
    run(chunks[0], 0, lang)
#    for id in range(NUM_PROCS):
#        proc = Process(target=run, args=(chunks[id], id, lang))
#        proc.start()
#        processes.append(proc)
#    for proc in processes:
#        proc.join()

    print("Done!: {}".format(str(time.time() - start)))