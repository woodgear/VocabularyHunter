import unittest

from controler import *


class Test(unittest.TestCase):
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
        