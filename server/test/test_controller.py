import os
import sys
import unittest
sys.path.insert(0, os.path.abspath('./lib/ECDICT'))
from stardict import convert_dict

from controler import *


class Test(unittest.TestCase):
    def setUp(self):
        print("setUp")
        vhDict = "./mock_data/vol/vh-dict"
        vhUser = "./mock_data/vol/vh-user"
        
        os.makedirs(vhDict)
        os.makedirs(vhUser)

        mock_dict_sqlite = f"{vhDict}/mock_dict.db"
        mock_dict_csv = "./mock_data/mock_dict.csv"

        convert_dict(mock_dict_sqlite,mock_dict_csv)   
        os.environ["STAR_DICT_SQLITE"] = mock_dict_sqlite
        os.environ["VH_USER_PATH"] = vhUser

        

    def tearDown(self):
        os.system('rm -rf ./mock_data/vol')

    def test_describe(self):
        input = {
            "words": ["apple", "tree"],
            "explains": [
                {
                    "name": "apple",
                },
                {
                    "name": "tree",
                },
            ],
            "know_words": [],
            "unknow_words": []
        }
        expect_output = [
            {
                "name": "apple",
                "explain": {
                    "name": "apple",
                },
                "know_type":None
            },
            {
                "name": "tree",
                "explain": {
                    "name": "tree",
                },
                "know_type":None
            }
        ]
        output = Controller()._describes(**input)
        self.assertEqual(output, expect_output)

        input = {
            "words": ["apple", "tree"],
            "explains": [
                {
                    "name": "apple",
                },
                {
                    "name": "tree",
                },
            ],
            "know_words": ["apple"],
            "unknow_words": ["tree"]
        }
        expect_output = [
            {
                "name": "apple",
                "explain": {
                    "name": "apple",
                },
                "know_type":"know"
            },
            {
                "name": "tree",
                "explain": {
                    "name": "tree",
                },
                "know_type":"unknow"
            }
        ]

        output = Controller()._describes(**input)
        self.assertEqual(output, expect_output)
        