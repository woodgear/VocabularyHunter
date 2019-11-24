import sys
import os
sys.path.insert(0, os.path.abspath(f'{os.path.dirname(__file__)}/../lib/ECDICT'))
from stardict import  *
import util
import os

STAR_DICT_SQLITE = os.getenv(
    "STAR_DICT_SQLITE") or "./dict/ecdict/stardict.sqlite"


class WordPos:
    def __init__(self, pos_str):
        pos_dict = {p.split(":")[0]: p.split(":")[1]
                    for p in pos_str.split('/')}
        self.__dict__ = {**self.__dict__, **pos_dict}

    def to_json_serializable(self):
        return util.to_json_serializable(self.__dict__)


class WordExplain(dict):
    def __init__(self, name, data):
        if data["pos"]:
            self.pos = WordPos(data["pos"])
        else:
            self.pos = None
        self.name = name  # string
        self.phonetic = data["phonetic"]
        self.collins = data["collins"]
        self.oxford = data["oxford"]
        self.frq = data["frq"]
        self.definitions = data["definition"].splitlines()
        self.translations = data["translation"].splitlines()
        self.tags = data["tag"].split(' ')
        self.audio = data["audio"]
        self.exchange = data["exchange"]
        pass

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def to_json_serializable(self):
        return util.to_json_serializable(self.__dict__)


def parse_trans_type(exchange):
    if exchange == "":
        return None
    explain = exchange.split('/')
    data = {}
    for e in explain:
        tran_type, val = e.split(':')
        data[tran_type] = val
    return data


def init_star_dict():
    return StarDict(STAR_DICT_SQLITE)


class DictHelper:
    def __init__(self):
        self.sd = init_star_dict()
        pass

    def find_lemma(self,word):
        explain = self.sd.query(word)
        exchange = parse_trans_type(explain["exchange"])
        if exchange is not None and "0" in exchange:
            return exchange["0"]
        return None


    def describes(self, words):
        explains = [self.describe(w) for w in words]
        return [e for e in explains if e is not None]
        pass
    
    def describe(self, word):
        explain = self.sd.query(word)
        if explain is None:
            return None
        exchange = parse_trans_type(explain["exchange"])
        res = WordExplain(word, {**explain, **{"exchange": exchange}})
        return res
