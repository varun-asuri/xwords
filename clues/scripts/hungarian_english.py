import pickle
import requests
from bs4 import BeautifulSoup

base_url = "https://glosbe.com/hu/en/{}"

words = pickle.load(open("pickles/hu-hu.pkl", "rb"))
words = list(words.keys())
data = {}
#words = words[0]
#print(words[0])
#words = ["nem"]

for num, word in words:
    url = base_url.format(word)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    meaning_elems = soup.find_all('div', class_='meaningContainer')
    job_elems = []
    for i, elem in enumerate(meaning_elems):
        if i > 3:
            break
        job_elems.append(elem.find_all('div', class_='phraseMeaning')[0])
    defs = {elem.text for elem in job_elems}
    if defs:
        data[word] = defs

print(len(data))

pickle.dump(data, open("pickles/full-hu-hu.pkl", "wb"))