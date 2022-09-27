#!/usr/bin/env python3

import os
import sys
import json
import pickle


def parse_args():
    if len(sys.argv) < 2:
        print("At least one dictionary file must be specified")
        sys.exit(1)
    return [open(arg) for arg in sys.argv[1:]]


def main():
    files = parse_args()
    dictionary = {}
    for file in files:
        dictionary = {**dictionary, **{x.lower():y for x,y in json.load(file).items()}}
    pickle.dump(dictionary, open('dictionary.pkl','wb'))


if __name__ == '__main__':
    main()