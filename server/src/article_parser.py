from nltk.tokenize import sent_tokenize
from util import *
from nltk.tokenize.punkt import PunktSentenceTokenizer
from functional import seq
import json


def save(user_id, article):
    words = words(article)
    words = seq(words).map(
        lambda w: {"word": w["word"], range: w["range"], "word_root": find_word_root(w["word"])})
    id = build_aritcle(article)
    build_word_inver_index(id, words)
    connect_user_and_article(user_id, id)
    pass


def query_sentence(user_id, aritcle_id, range):
    aritcle = find_article_by_id(aritcle_id)
    aritcle_struct = aritcle["struct"]
    expand_left, expand_right = generate_expand_setence_range(
        article_struct, range)
    setence = pick_article(aritcle_id, range)
    return {"aritcle_id": aritcle_id, "sentence": sentence, "expand_left": expand_left, "expand_right": expand_right, "title": article["title"], "url": article["url"]}


def query(user_id, word):
    def find_sentence(article, word_invert_index):
        word_range = json.load(word_invert_index[article["id"]]["position"])
        sentence_range = find_sentence_range(
            json.load(article["struct"]), word_range)
        aritcle_id = article["id"]
        article_struct = article["struct"]

        expand_left, expand_right = generate_expand_setence_range(
            article_struct, word_range)
        sentence = pick_article(article["id"], sentence_range)
        return {"aritcle_id": article["id"], "sentence": sentence, "expand_left": expand_left, "expand_right": expand_right, "title": article["title"], "url": article["url"]}
        pass

    word_root = find_word_root(word)
    articles = find_article_by_word_root(user_id, word_root)
    word_invert_index = find_word_invert_index(user_id, word_root)
    res = list(seq(articles).map(
        lambda a: find_sentence(a, word_invert_index)))
    return res
    pass


def clear_article(data):
    seq_list = seq(data.splitlines()).map(
        lambda s: s.strip()).filter(lambda s: s)
    lis = list(seq_list)
    return "\n".join(lis)


def cacl_article(article):
    article = clear_article(article)

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
    for start, end in list(find_line_index(article))[0:10]:
        sentence_range = cacl_paragraph(article[start:end], start)
        res.append({"start": start, "end": end,
                    "kind": "paragraph", "child": sentence_range})
    return {"start": 0, "end": len(article), "child": res, "kind": "article", "raw": article}
    pass


def cacl_paragraph(paragraph, offset=0):
    res = []
    for start, end in PunktSentenceTokenizer().span_tokenize(paragraph):
        length = end - start
        res.append({"start": start+offset, "end": end+offset})
    return res
    pass
