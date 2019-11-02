import unittest
from pathlib import Path
from db_model import * 
import shutil
import time
import datetime

import gc
FOLDER_PATH = "test-db"


class TestDbModel(unittest.TestCase):
    def setUp(self):
        print(self.id(),"setUp")
        test_folder = Path(FOLDER_PATH)
        if test_folder.exists():
            print("setUp rmtree")
            shutil.rmtree(test_folder)
            print("setUp over")
        test_folder.mkdir()
        pass

    def tearDown(self):
        print(self.id(),"tearDown")
        del self.model
        test_folder = Path(FOLDER_PATH)
        if test_folder.exists():
            shutil.rmtree(test_folder)
        pass
    
    def test_db(self):
        print(self.id())
        self.model = DbModel(folder_path=FOLDER_PATH)

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
        self.model = DbModel(folder_path=FOLDER_PATH)
        db = self.model._db()
        now = datetime.datetime(2019, 11, 1, 1, 4, 48)
        raw_article = "123456789"
        aritcle =  {"aritcle":raw_article,"name":"name","source":"https://xxx.com","type":"website-article",
        "struct":"xxxxx",
        "md5":"md5","time":now}
        corpus_id = self.model.save_aritcle(aritcle)
        meta  = self.model.find_aritcle_meta(corpus_id)
        self.assertEqual(meta,{'id': 1, 'md5': 'md5', 'type': 'website-article', 'struct': 'xxxxx','time': now, 'source': 'https://xxx.com', 'name': 'name'})
        data = self.model.find_aritcle(corpus_id,(1,2))
        self.assertEqual(data,raw_article[1:2])
        data = self.model.find_aritcle(corpus_id,(0,7))
        self.assertEqual(data,raw_article[0:7])
        self.assertEqual(True,self.model.has_article({"md5":"md5"}))
        self.assertEqual(False,self.model.has_article({"md5":"mddxxx5"}))

        print(data)
        pass
    def test_save_word_invert_index(self):
        mock_word_invert = [{'span': (0, 4), 'word': 'apple', 'lemma': 'apple'}]

        raw_article = "apple is tree."
        aritcle =  {"aritcle":raw_article,"name":"name","source":"https://xxx.com","type":"website-article",
        "struct":"xxxxx",
        "md5":"md5","time":datetime.datetime.now()}
        self.model = DbModel(folder_path=FOLDER_PATH)
        corpus_id_1 = self.model.save_aritcle(aritcle)
      
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