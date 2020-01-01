import unittest
from pathlib import Path
from db_model import * 
import shutil
import time
import datetime
import sys
import gc

sys.path.insert(0, os.path.abspath('./lib/ECDICT'))
from stardict import convert_dict



class TestDbModel(unittest.TestCase):
    def setUp(self):
        print("setUp")
        vhDict = "./mock_data/vol/vh-dict"
        vhUser = "./mock_data/vol/vh-user"
        os.system('rm -rf ./mock_data/vol')
        os.makedirs(vhDict)
        os.makedirs(vhUser)

        mock_dict_sqlite = f"{vhDict}/mock_dict.db"
        mock_dict_csv = "./mock_data/mock_dict.csv"

        convert_dict(mock_dict_sqlite,mock_dict_csv)   
        os.environ["STAR_DICT_SQLITE"] = mock_dict_sqlite
        os.environ["VH_USER_PATH"] = vhUser

        

    def tearDown(self):
        os.system('rm -rf ./mock_data/vol')
    
    def test_db(self):
        print(self.id())
        self.model = DbModel()

        # should get a empty list when it does not has word
        knowWords = self.model.get_all_know_word_by_id("mockId1")
        self.assertEqual(knowWords,[])
        unKnowWords = self.model.get_all_unknow_word_by_id("mockId1")
        self.assertEqual(unKnowWords,[])

        # should correctly insert word
        self.model.mark_know_word_by_id("mockId1",["apple","juice"])
        knowWords = self.model.get_all_know_word_by_id("mockId1")
        self.assertEqual(knowWords,["apple","juice"])

        self.model.mark_unknow_word_by_id("mockId1",["apple1","juice1"])
        unKnowWords = self.model.get_all_unknow_word_by_id("mockId1")
        self.assertEqual(unKnowWords,["apple1","juice1"])

        # should get a empty list when it does not has word
        knowWords = self.model.get_all_know_word_by_id("mockId2")
        self.assertEqual(knowWords,[])
        unKnowWords = self.model.get_all_unknow_word_by_id("mockId2")
        self.assertEqual(unKnowWords,[])
        # switch know unknow
        self.model.mark_know_word_by_id("mockId3",["apple","juice"])
        knowWords = self.model.get_all_know_word_by_id("mockId3")
        self.assertEqual(knowWords,["apple","juice"])

        self.model.mark_unknow_word_by_id("mockId3",["apple"])
        unKnowWords = self.model.get_all_unknow_word_by_id("mockId3")
        self.assertEqual(unKnowWords,["apple"])

        knowWords = self.model.get_all_know_word_by_id("mockId3")
        self.assertEqual(knowWords,["juice"])

        pass
    def test_save_article(self):
        print(self.id())
        self.model = DbModel()
        db = self.model._db()
        now = datetime.datetime(2019, 11, 1, 1, 4, 48)
        raw_article = "123456789"
        article =  {"article":raw_article,"name":"name","source":"https://xxx.com","type":"website-article",
        "struct":"{}",
        "md5":"md5","time":now}
        corpus_id = self.model.save_article(article)
        meta  = self.model.find_article_meta(corpus_id)
        print("meta",meta)
        self.assertEqual(meta,{'id': 1, 'md5': 'md5', 'type': 'website-article', 'struct': {},'time': now, 'source': 'https://xxx.com', 'name': 'name'})
        data = self.model.find_article(corpus_id,(1,2))
        self.assertEqual(data,raw_article[1:2])
        data = self.model.find_article(corpus_id,(0,7))
        self.assertEqual(data,raw_article[0:7])
        self.assertEqual(True,self.model.has_article({"md5":"md5"}))
        self.assertEqual(False,self.model.has_article({"md5":"mddxxx5"}))

        print(data)
        pass
    def test_save_word_invert_index(self):
        mock_word_invert = [{'span': (0, 4), 'word': 'apple', 'lemma': 'apple'}]

        raw_article = "apple is tree."
        article =  {"article":raw_article,"name":"name","source":"https://xxx.com","type":"website-article",
        "struct":"xxxxx",
        "md5":"md5","time":datetime.datetime.now()}
        self.model = DbModel()
        corpus_id_1 = self.model.save_article(article)
      
        self.model.connect_user_and_corpus("user_1",corpus_id_1)
        self.model.save_word_invert_index(corpus_id_1,mock_word_invert)
        res = list(self.model.find_word_invert_index("user_1","apple"))
        print("res ",res)
        self.assertEqual(res,[{'word': 'apple', 'lemma': 'apple', 'corpus_id': 1, 'span': [0, 4]}])

        res = list(self.model.find_word_invert_index("user_2","apple"))
        self.assertEqual(res,[])
        self.model.connect_user_and_corpus("user_2",corpus_id_1)
        res = list(self.model.find_word_invert_index("user_2","apple"))
        self.assertEqual(res,[{'word': 'apple', 'lemma': 'apple', 'corpus_id': 1, 'span': [0, 4]}])
        pass




if __name__ == '__main__':
    unittest.main()