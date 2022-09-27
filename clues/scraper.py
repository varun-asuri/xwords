#/usr/bin/env python3
import json
import pickle
import functools
import argparse
import requests

URL = "https://www.dictionary.com/browse/{0}?s=t"
dictionary = {}


def extract_word(resp, word):

    index = resp.find('<meta name="description" content="')
    data = resp[index:]
    data = data[:data.index("\n")]
    data = data[data.index("content=") + 22 + len(word):-12]
    return data


def get_words(args):
    words = open(args.filename, 'r').read().splitlines()
    cached_definitions = pickle.load(open('dictionary.pkl','rb'))
    #dummy line
    print(len([word for word in words if word.lower() in cached_definitions]))


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=get_words)
    parser.add_argument("filename", help="path to dictionary file")

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
