import unittest
from pathlib import Path
from db_model import * 
import shutil
import time
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



if __name__ == '__main__':
    unittest.main()