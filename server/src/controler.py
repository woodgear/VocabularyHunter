from find_unknow_words import *
from db_model import *
from dicthelper import DictHelper
# 如何去除link


class Controller:
    def __init__(self):
        self.model = DbModel()
        pass

    def mark_know_word(self, id, words):
        self.model.mark_know_word_by_id(id, words)
        pass

    def mark_unknow_word(self, id, words):
        self.model.mark_unknow_word_by_id(id, words)
        pass

    def get_all_know_word(self, id):
        return self.model.get_all_know_word_by_id(id)
        pass

    def get_all_unknow_word(self, id):
        return self.model.get_all_unknow_word_by_id(id)
        pass

    def find_unknow_words_by_article(self, id, article):
        know_words = self.model.get_all_know_word_by_id(id)
        unknow = find_unknow_word(tokens(article), know_words)
        return unknow
        pass

    def describes(self, id, words):
        print("describes")
        explains = DictHelper().describes(words)
        know_words = self.model.get_all_know_word_by_id(id)
        unknow_words = self.model.get_all_unknow_word_by_id(id)
        return self._describes(words, explains, know_words, unknow_words)
        pass

    def _describes(self, words, explains, know_words, unknow_words):
        def get_know_type(w, k, uk):
            if w in k:
                return "know"
            if w in uk:
                return "unknow"
            return None
            pass
        know_words_set = set(know_words)
        unknow_words_set = set(unknow_words)
        know_type_map = {w: get_know_type(
            w, know_words_set, unknow_words_set) for w in words}
        print("_describes")
        [print(e.name) for e in explains]
        return [{"name": e.name, "explain": e, "know_type": know_type_map[e.name]} for e in explains]
        pass
