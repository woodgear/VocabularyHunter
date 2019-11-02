from nltk.tokenize import sent_tokenize
from util import *
from nltk.tokenize.punkt import PunktSentenceTokenizer
from functional import seq
import json
from dicthelper import DictHelper
from db_model import *

from find_unknow_words import *


def save(user_id, article_data):
    article = article_data["article"]
    article = clear_article(article)
    url = article_data["url"]
    name = article_data["title"]
    md5 = md5(article)

    words = words(article)
    aricle_struct = cacl_article(article)
    model = DbModel()

    corpus_id = model.save_aritcle({"article": article, "name": name, "source": url, "type": "website-article",
                                    "md5": md5, "struct": json.dump(aricle_struct), "time": datetime.datetime.now()})
    model.save_word_invert_index(corpus_id, words)
    model.connect_user_and_corpus(user_id, corpus_id)
    pass


def words(aritcle):
    res = seq(word_span_tokenize(aritcle)).map(lambda w: (
        DictHelper().describe(w["word"]), w["span"])).filter(lambda w: w[0])

    for token in res:
        w = token[0]
        span = token[1]
        if w.exchange and w.exchange["0"]:
            assert aritcle[span[0]:span[1]].lower() == w.name
            yield {"span": span, "word": w.name, "lemma": w.exchange["0"]}
        else:
            assert aritcle[span[0]:span[1]] .lower() == w.name
            yield {"span": span, "word": w.name, "lemma": w.name}


def query_sentence(aritcle_id, span):
    aritcle = find_article_by_id(aritcle_id)
    aritcle_struct = aritcle["struct"]
    expand_left, expand_right = generate_expand_setence_range(
        article_struct, range)
    setence = pick_article(aritcle_id, range)
    return {"aritcle_id": aritcle_id, "sentence": sentence, "expand_left": expand_left, "expand_right": expand_right, "title": article["title"], "url": article["url"]}


def find_sentence_span_by_word_span(corpus_struct, span):
    # TODO need refactor
    """
    给定语料的结构与一个范围 找到最小树和expand_left expand right expand parent
    """

    def find_parent(corpus_struct, span):
        if span[0] < corpus_struct["start"] or span[1] > corpus_struct["end"]:
            return None
        if corpus_struct["child"] is None:
            span = (corpus_struct["start"], corpus_struct["end"])
            return -1, corpus_struct

        for index, c in enumerate(corpus_struct["child"]):
            if span[0] >= c["start"] and span[1] <= c["end"]:
                if "child" not in c:
                    sentence_span = (c["start"], c["end"])
                    print(span, sentence_span, index)
                    return index, corpus_struct
                else:
                    return find_parent(c, span)
        return None
        pass

    span_index, parent = find_parent(corpus_struct, span)
    if span_index == -1:
        return {"sentenct_span": sentenct_span, "expand_parent": None, "expand_left": None, "expand_right": None}

    sentenct_span = (parent["child"][span_index]["start"],
                     parent["child"][span_index]["end"])
    expand_parent = (parent["start"], parent["end"])
    expand_left_index = span_index-1
    expand_left = None
    if expand_left_index >= 0 and expand_left_index < len(parent["child"]):
        expand_left = (parent["child"][expand_left_index]["start"],
                       parent["child"][expand_left_index]["end"])

    expand_right_index = span_index+1
    expand_right = None
    if expand_right_index >= 0 and expand_right_index < len(parent["child"]):
        expand_right = (parent["child"][expand_right_index]["start"],
                        parent["child"][expand_right_index]["end"])

    return {"sentenct_span": sentenct_span, "expand_parent": expand_parent, "expand_right": expand_right, "expand_left": expand_left}
    pass


def query(user_id, word):
    """
    从用户的语料库中查询单词
    返回结构
    [{
        word:xx
        lemma:xxx,
        sentence:"xxxxxxxx",
        corpus_id:"xxxx",
        span:(xx,xxx)
        expand_left:(xx,xx)
        expand_right:(xx,xxx)
        name:xxx
        url:xxx
    }]
    """
    def find_sentence(invert_index):

        word = invert_index["word"]
        lemma = invert_index["lemma"]
        span = invert_index["span"]
        corpus_id = invert_index["corpus_id"]
        model = DbModel()

        corpus_meta = model.find_aritcle_meta(corpus_id)
        struct = corpus_meta["struct"]
        name = corpus_meta["name"]
        source = corpus_meta["source"]

        spans = find_sentence_span_by_word_span(struct, span)
        sentence_span = spans["sentence_span"]
        sentence = model.find_aritcle(corpus_id, sentence_span)
        return {"word": word, "lemma": lemma, "name": name, "url": source,  "corpus_id": corpus_id, "sentence": sentence, "span": sentence_span, "expand_right": spans["expand_right"], "expand_left": spans["expand_right"], "expand_left": spans["expand_right"]}

    lemma = DictHelper().find_lemma(word)
    model = DbModel()
    index = model.find_word_invert_index(user_id, lemma)
    return seq(index).map(lambda index: find_sentence(index))


def clear_article(data):
    seq_list = seq(data.splitlines()).map(
        lambda s: s.strip()).filter(lambda s: s)
    lis = list(seq_list)
    return "\n".join(lis)


def cacl_article(article):
    def find_line_index(article):
        start = 0
        end = len(article)
        while True:
            lineIndex = article.find('\n', start+1)
            if lineIndex == -1:
                yield start, end
                return
            yield start, lineIndex
            start = lineIndex+1
    pass
    res = []
    for start, end in find_line_index(article):
        sentence_range = cacl_paragraph(article[start:end], start)
        res.append({"start": start, "end": end,
                    "kind": "paragraph", "child": sentence_range})
    return {"start": 0, "end": len(article), "child": res, "kind": "article"}
    pass


def cacl_paragraph(paragraph, offset=0):
    res = []
    for start, end in PunktSentenceTokenizer().span_tokenize(paragraph):
        length = end - start
        res.append({"start": start+offset, "end": end+offset})
    return res
    pass
