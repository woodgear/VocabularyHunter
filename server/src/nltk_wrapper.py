# all the thing that relatived to nltk

import os
import sys
import time
from functional import seq
from orderedset import OrderedSet
import nltk
from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize

from nltk.tokenize import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.data import load
from typing import *

import re


def init_treebank_wordtokenizer():
    _treebank_word_tokenizer = TreebankWordTokenizer()
    improved_open_quote_regex = re.compile(u'([«“‘„]|[`]+)', re.U)
    improved_open_single_quote_regex = re.compile(
        r"(?i)(\')(?!re|ve|ll|m|t|s|d)(\w)\b", re.U)
    improved_close_quote_regex = re.compile(u'([»”’])', re.U)
    improved_punct_regex = re.compile(
        r'([^\.])(\.)([\]\)}>"\'' u'»”’ ' r']*)\s*$', re.U)
    _treebank_word_tokenizer.STARTING_QUOTES.insert(
        0, (improved_open_quote_regex, r' \1 '))
    _treebank_word_tokenizer.STARTING_QUOTES.append(
        (improved_open_single_quote_regex, r'\1 \2'))
    _treebank_word_tokenizer.ENDING_QUOTES.insert(
        0, (improved_close_quote_regex, r' \1 '))
    _treebank_word_tokenizer.PUNCTUATION.insert(
        0, (improved_punct_regex, r'\1 \2 \3 '))
    return _treebank_word_tokenizer
    pass


_treebank_word_tokenizer = init_treebank_wordtokenizer()


def span_tokenize(sentence:str)->List[Tuple[int,int]]:
    return _treebank_word_tokenizer.span_tokenize(sentence)
    pass


def remove_duplicate(data_list):
    return list(OrderedSet(data_list))


def sentence_span_tokenize(article):
    tokenizer = load('tokenizers/punkt/{0}.pickle'.format("english"))
    return tokenizer.span_tokenize(article)
    pass


def raw_word_span_tokenize(article):
    sentences = sentence_span_tokenize(article)
    for sentence_span in sentences:
        sentence = article[sentence_span[0]:sentence_span[1]]
        for word_span in span_tokenize(sentence):
            word_span_start = word_span[0]+sentence_span[0]
            word_span_end = word_span[1]+sentence_span[0]
            word = article[word_span_start:word_span_end]

            yield {"span": (word_span_start, word_span_end), "word":word }
    return
    pass


def word_span_tokenize(article):
    def lower_token(token):
        token["word"] = token["word"].lower()
        return token
    tokens = raw_word_span_tokenize(article)
    return (seq(tokens)
        .map(lower_token)
        .filter(lambda token: not token["word"] in ",./;'[]<>?:\"{}!@#$%^&*()_+-=")
        .filter(lambda token: len(token["word"]) > 3)
        .filter(lambda token: not token["word"].isnumeric()))


def tokenize(article):
    tokens = word_span_tokenize(article)
    tokens = [t["word"] for t in tokens]
    return remove_duplicate(tokens)

def find_unknow_word(words, know_words):
    return list(OrderedSet(words).difference(OrderedSet(know_words)))


def build_already_know_word(paths):
    words = set()
    for path in paths:
        with open(path, 'r') as f:
            for word in f.readlines():
                words.add(word.strip())
            pass
    return words
