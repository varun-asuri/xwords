from translate import Translator
import pickle
import time

start = time.time()
translator = Translator(from_lang="Spanish", to_lang="English")
for i in range(100):
    translator.translate("Como estas?")



"""
data = pickle.load(open("pickles/full-es-es.pkl", "rb"))
translator = Translator(from_lang="Spanish", to_lang="English")
new_data = {}
print(len(data))
for i, word in enumerate(data):
    if i % 100 == 0:
        print(i)
    definitions = data[word]
    translated_defs = set()
    for definition in definitions:
        translated = translator.translate(definition)
        translated_defs.add(translated)
    new_data[word] = translated_defs
pickle.dump(new_data, open("full-es-en", "wb"))
"""