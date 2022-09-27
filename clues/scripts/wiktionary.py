import requests
import pickle
from bs4 import BeautifulSoup

#https://hu.wiktionary.org/w/api.php?action=parse&page=nem&format=json
def get_definitions(lang, word):
    url = "https://{}.wiktionary.org/w/api.php?action=parse&page={}&format=json".format(lang, word)
    page = requests.get(url)
#    print(word)
    page_json = page.json()
    if 'parse' not in page_json:
        return []
    html = page_json['parse']['text']['*']
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_="mw-parser-output")
    hungarian = False
    ols = []
    for child in div.findChildren():
        if child.name == "h2":
            if child.findChild() and child.findChild().get("id") == "Magyar":
                hungarian = True
            else:
                hungarian = False
        if hungarian:
            if child.name == "ol":
                ols.append(child)
#    print(len(ols))
    if not ols:
        print("No definitions found for word: {}".format(word))
        return []
    lis = []
    for ol in ols:
        lis.extend(ol.findAll("li"))
#    print(len(lis))
    for li in lis:
        for child in li.findChildren():
            if child.name == "dl":
                child.extract()
    defs = [li.text for li in lis]
    print(len(defs))
    return defs

#defs = get_definitions("hu", "a")
words = pickle.load(open("pickles/hu-hu.pkl", "rb"))
data = {}
for i, word in enumerate(words):
    if i % 10 == 0:
        print(i)
    data[word] = get_definitions("hu", word)
    if len(data) > 10:
        file = open("all2-hu-hu/{}.txt".format("id"), "a+")