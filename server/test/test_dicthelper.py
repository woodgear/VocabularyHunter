import unittest
from dicthelper import * 
from util import *
import json
class TestWord(unittest.TestCase):
    def test_construct_explain(self):
        print(self.id())
        db_e =  {'phonetic': "'æpl", 'definition': '', 'translation': '', 'pos': 'n:100', 'collins': 3, 'oxford': 1, 'tag': 'zk gk', 'bnc': 2446, 'frq': 2695, 'exchange': "", 'detail': None, 'audio': ''}
        explain  = WordExplain("apple",db_e)
        print(explain,to_json_serializable(explain))


if __name__ == '__main__':
    unittest.main()