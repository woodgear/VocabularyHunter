from find_unknow_words import * 
from db_model import * 
class Controller:
    def __init__(self):
        self.model = DbModel()
        pass
    def mark_know_word(self,id,words):
        self.model.mark_know_word_by_id(id,words)
        pass
    def mark_unknow_word(self,id,words):
        self.model.mark_unknow_word_by_id(id,words)
        pass
    def get_all_know_word(self,id):
        return self.model.get_all_know_word_by_id(id)
        pass
    def get_all_unknow_word(self,id):
        return self.model.get_all_unknow_word_by_id(id)
        pass
    def find_unknow_words_by_article(self,id,article):
        know_words = self.model.get_all_know_word_by_id(id)
        unknow = find_unknow_word(tokens(article),know_words)
        return unknow
        pass
    

