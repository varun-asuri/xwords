import sys
import os
import pickle

lang = sys.argv[1]
data = pickle.load(open("full-{}-{}.pkl".format(lang, lang), "rb"))
synonym_translation = {"en": "Synonyms: ", "es": "Sinónimos: ", "de": "Synonyme: ", "fr": "Synonymes"}
meanings = {}
print(len(data))
for key in data:
    obj = data[key]
    for worddata in obj:
        word = worddata['word']
        if word not in meanings: meanings[word] = []
        meaning = worddata['meaning']
        for wordtype in meaning:
            for meaning_obj in meaning[wordtype]:
                definition = meaning_obj['definition']
                synonyms = meaning_obj['synonyms']
                meanings[word].append(definition)
                if len(synonyms) >= 3:
                    meanings[word].append(synonym_translation[lang] + ", ".format(synonyms))

print(len(meanings))
pickle.dump(meanings, open("meanings-{}-{}.pkl".format(lang, lang), "wb+"))