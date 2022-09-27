import requests
from bs4 import BeautifulSoup

def get_definitions(word):
    page = requests.get("https://www.lexico.com/en/definition/{}".format(word))
    soup = BeautifulSoup(page.content, 'lxml')
    sections = soup.findAll("section", class_="gramb")
    defs = []
    for section in sections:
        header = section.findChild("h3").findChild("span").text
        def_section = section.findChild("p")
    #    def_section = section.findChild("div", class_="trg")
        for child in def_section.findChildren("span", class_="ind"):
            defs.append(child.text)
    return defs

print(get_definitions("mystery"))

#print(sections)
#print(len(sections))