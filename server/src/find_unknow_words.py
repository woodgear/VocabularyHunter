import os
import sys
import time
from functional import seq
from orderedset import OrderedSet
import nltk
from nltk import word_tokenize
import util

def remove_duplicate(data_list):
    return list(OrderedSet(data_list))

def tokens(aritcle):
    return remove_duplicate(filter_invalid_word(word_tokenize(aritcle)))

def filter_invalid_word(tokens):
    return list(seq(tokens)
                .map(lambda w: w.lower())
                .filter(lambda token: not token in ",./;'[]<>?:\"{}!@#$%^&*()_+-=")
                .filter(lambda token: len(token) > 3)
                .filter(lambda token: not token.isnumeric())
                )

def find_unknow_word(words,know_words):
    return list(OrderedSet(words).difference(OrderedSet(know_words)))

def build_already_know_word(paths):
    words = set()
    for path in paths:
        with open(path, 'r') as f:
            for word in f.readlines():
                words.add(word.strip())
            pass
    return words

if __name__ == '__main__':
    article = util.read_to_string(sys.argv[1])
    words = util.read_to_string(sys.argv[2])
    unknow = find_unknow_word(tokens(article),tokens(words))
    print(unknow)