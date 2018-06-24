#!/usr/bin/env python
import os
import time
from functional import seq
import nltk
from nltk import word_tokenize
from word_forms.word_forms import get_word_forms
from cachetools import cached
from ordered_set import OrderedSet
import argparse


file_path = './the-eleventh-hour.txt'
# file_path = './1.txt'


raw_file = open(file_path, encoding="utf-8")
raw_text = raw_file.read()
tokens = word_tokenize(raw_text)


class Word:
    origin = ''  # the origin word in data
    location = ''  # the location of origin in data
    forms = ''  # the orgin'forms come from get_word_forms
    origin_repeat_time = 0  # the repeat time of orgin
    word_repest_time = 0  # the repeat time of word (orgin + form)

    def __init__(self, orgin):
        self.orgin = orgin


def normalize(tokens):
    return list(seq(tokens)
                .map(lambda w: w.lower())
                .filter(lambda token: not token in ",./;'[]<>?:\"{}!@#$%^&*()_+-=")
                .filter(lambda token: len(token) > 3)
                .filter(lambda token: not token.isnumeric())
                )


def reduce_form(words):
    words = list(OrderedSet(words))
    all_word = set()

    def is_exists(word):
        nonlocal all_word
        if word in all_word:
            return True
        all_word = all_word.union(*get_word_forms(word).values())
        return False

    return list(filter(lambda word: not is_exists(word), words))


def build_already_know_word(paths):
    words = set()
    for path in paths:
        with open(path, 'r') as f:
            for word in f.readlines():
                words.add(word.strip())
            pass
    return words


parser = argparse.ArgumentParser(description='filter the new word')
parser.add_argument("-i", "--ignore", nargs='+', required=False,
                    help="ignore words")
parser.add_argument("-w", "--word", required=True,
                    help="word path")
parser.add_argument("-o", "--output", required=False,
                    help="output path")


args = vars(parser.parse_args())
raw_text = open(args['word'],'r', encoding="utf-8").read()

know_words = build_already_know_word(args['ignore'])
all_word = set(reduce_form(normalize(word_tokenize(raw_text))))
all_word = all_word.difference(know_words)
if args['output']:
    with open(args['output'], 'w') as f:
        f.write(all_word)
        pass
else:
    for word in all_word:
        print(word)
print("capture {} new word".format(len(all_word)))
