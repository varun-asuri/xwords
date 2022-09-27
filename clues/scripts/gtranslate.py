import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import _find_element
from selenium.webdriver.common.keys import Keys

base = "https://translate.google.com/#view=home&op=translate&sl={}&tl={}&text={}"
from_lang = sys.argv[1]
to_lang = sys.argv[2]


class text_to_change(object):
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        actual_text = _find_element(driver, self.locator).text
        return actual_text != self.text and actual_text != self.text + "..." and actual_text != ""


def run_word(driver, string, prev):
    url_string = string.strip().replace(" ", "%20")
    url = base.format(from_lang, to_lang, url_string)

    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(url)
#    print(driver.current_url)
#    print(prev)

    WebDriverWait(driver, 10).until(
        text_to_change((By.CLASS_NAME, "tlid-translation"), prev)
    )
#    WebDriverWait(driver, 10).until(
#        text_to_change((By.CLASS_NAME, "tlid-translation"), prev)
#    )

    element = driver.find_element_by_class_name("tlid-translation")
    print(element.text)
    return element.text

#    items = driver.execute_script("""return document.querySelector('.tlid-translation').children""")
#    return ''.join([item.text for item in items])
#    html = driver.page_source
    #html = requests.get(url).content
#    soup = BeautifulSoup(html, 'lxml')
#    a = soup.find('span', class_="tlid-translation")
#    return a.text


start = time.time()
driver = webdriver.PhantomJS()
#for i in range(30):
#    run_word(driver, "word")
#    run_word(driver, "word")
string1 = "Se utiliza para enlazar dos palabras, grupos de palabras u oraciones que están al mismo nivel y tienen la misma función, e indica que los elementos que se enlazan se suceden alternativamente; se antepone a cada una de las alternativas."
string2 = "Resplandor vivo y moment\u00e1neo producido por un choque entre nubes tormentosas cargadas de electricidad est\u00e1tica."
val = run_word(driver, string1, "")
#print(val)
val = run_word(driver, string2, val)
#print(val)

print(time.time() - start)