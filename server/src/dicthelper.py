import sys
import os
sys.path.insert(0, os.path.abspath(f'{os.path.dirname(__file__)}/../ECDICT'))
from stardict import  *
import util
STAR_DICT_SQLITE = "./ECDICT/stardict.sqlite"
class WordPos:
    def __init__(self,pos_str):
        pos_dict = {p.split(":")[0]:p.split(":")[1] for p in pos_str.split('/')}
        self.__dict__ = {**self.__dict__,**pos_dict}
    def to_json_serializable(self):
        return util.to_json_serializable(self.__dict__)

class WordExplain:
    def __init__(self,name,data):
        self.name = name # string
        self.pos = WordPos(data["pos"])
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
    def to_json_serializable(self):
        return util.to_json_serializable(self.__dict__)


def parse_trans_type(exchange):
    explain = exchange.split('/')
    data = {}
    for e in explain:
        tran_type,val = e.split(':')
        data[tran_type]=val
    return data

def init_star_dict():
    return StarDict(STAR_DICT_SQLITE)

class DictHelper:
    def __init__(self):
        self.sd = init_star_dict()
        pass
    def describes(self,words):
        explains = [self.describe(w) for w in words]
        return explains
        pass
    def describe(self,word):
        explain = self.sd.query(word)
        exchange = parse_trans_type(explain["exchange"])
        if "l" in exchange:
            detail_exchange = parse_trans_type(self.sd.query(exchange['0'])["exchange"])
            exchange = {**exchange,**detail_exchange}
        else:
            exchange = {**exchange,**{"0":word,"l":"0"}}
        res = WordExplain(word,{**explain,**{"exchange":exchange}})
        return res
