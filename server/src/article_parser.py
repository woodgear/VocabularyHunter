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
    # id = build_aritcle({"article":article,"name":name,"source":url,"type":"website-article","md5":md5})
    # # build_word_inver_index(id, words)
    # connect_user_and_article(user_id, id)
    pass

# def build_aritcle(article):
#     struct = cacl_article(article["article"])
#     aritcle["struct"] = struct
#     model = DbModel()
#     model.save_article(article)



def words(aritcle):
    res = seq(word_span_tokenize(aritcle)).map(lambda w: (DictHelper().describe(w["word"]), w["span"])).filter(lambda w: w[0])

    for token in res:
        w = token[0]
        span = token[1]
        if w.exchange and w.exchange["0"]:
            assert aritcle[span[0]:span[1]].lower() == w.name
            yield {"span":span,"word":w.name,"lemma":w.exchange["0"]}
        else:
            assert aritcle[span[0]:span[1]] .lower()==w.name
            yield {"span":span,"word":w.name,"lemma":w.name}

# res = list(words(cacl_article(read_to_string("./mock_data/content.data"))["raw"]))
# for w in res:
#     if w["word"] != w["lemma"]:
#         print(w)


# def query_sentence(user_id, aritcle_id, range):
#     aritcle = find_article_by_id(aritcle_id)
#     aritcle_struct = aritcle["struct"]
#     expand_left, expand_right = generate_expand_setence_range(
#         article_struct, range)
#     setence = pick_article(aritcle_id, range)
#     return {"aritcle_id": aritcle_id, "sentence": sentence, "expand_left": expand_left, "expand_right": expand_right, "title": article["title"], "url": article["url"]}


# def query(user_id, word):
#     def find_sentence(article, word_invert_index):
#         word_range = json.load(word_invert_index[article["id"]]["position"])
#         sentence_range = find_sentence_range(
#             json.load(article["struct"]), word_range)
#         aritcle_id = article["id"]
#         article_struct = article["struct"]

#         expand_left, expand_right = generate_expand_setence_range(
#             article_struct, word_range)
#         sentence = pick_article(article["id"], sentence_range)
#         return {"aritcle_id": article["id"], "sentence": sentence, "expand_left": expand_left, "expand_right": expand_right, "title": article["title"], "url": article["url"]}
#         pass

#     lemma = find_lemma(word)
#     articles = find_article_by_lemma(user_id, lemma)
#     word_invert_index = find_word_invert_index(user_id, lemma)
#     res = list(seq(articles).map(
#         lambda a: find_sentence(a, word_invert_index)))
#     return res
#     pass


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

