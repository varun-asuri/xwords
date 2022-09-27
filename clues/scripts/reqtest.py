import faster_than_requests as faster_requests
import requests
import pickle
import time
import unidecode

words = pickle.load(open("../es-es.pkl", "rb"))
words = list(words.keys())[:100]

baseurl = "https://api.dictionaryapi.dev/api/v1/entries/es/"

def test1():
    start = time.time()
    dct = {}
    for i, word in enumerate(words):
        word = unidecode.unidecode(word)
        url = baseurl + word
        print(i, url)
        data = faster_requests.get2json(url)
        print("Saving word: ", word)
        dct[word] = data
    print(time.time() - start, len(dct))


def test2():
    start = time.time()
    dct = {}
    for i, word in enumerate(words):
        url = baseurl + word
        print(i, url)
        data = requests.get(url).json()
        dct[word] = data
    print(time.time() - start, len(dct))


def test3():
    start = time.time()
    urls = []
    for i, word in enumerate(words):
        word = unidecode.unidecode(word)
        url = baseurl + word
        urls.append(url)
    print(urls)
    faster_requests.get2ndjson(urls, "saved.ndjson")
    print(time.time() - start)



#test1()
#test2()
test3()