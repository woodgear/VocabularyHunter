import unittest
import util
from article_parser import *
data = """ So, I took this challenge myself and came out the other end with a pretty limited NES emulator, which I call Lochnes. It’s not very good at actually emulating most games, but I’m pretty happy with the guts of the thing and I learned a lot a long the way. I figured it might be worthwhile to share my approach, which might help or inspire others on their own emulation venture!"""


class Test(unittest.TestCase):
    def test_paragraph(self):
        res = cacl_paragraph(data)
        print(res)
        self.assertEqual(res, [{'start': 0, 'end': 118}, {
                         'start': 119, 'end': 255}, {'start': 256, 'end': 377}])
        pass

    def test_clear_article(self):
        input = "\n\ra\n\nb\n\nv\n\r"
        self.assertEqual(clear_article(input), "a\nb\nv")

    def test_cacl_article(self):
        res = clear_article(data)
        res = cacl_article(res)
        expect_res = {"start": 0, "end": 376, "child":   [{'start': 0, 'end': 376, 'kind': 'paragraph', 'child': [
            {'start': 0, 'end': 117}, {'start': 118, 'end': 254}, {'start': 255, 'end': 376}]}], "kind": "article"}
        self.assertEqual((res["start"], res["end"]), (0, 376))
        self.assertEqual(res, expect_res)
        pass

    def test_words(self):
        # data = "So, I took this challenge myself and came out the other end with a pretty limited NES emulator, which I call Lochnes."
        res = clear_article(data)
        res = words(res)
        for w in res:
            # print(w)
            pass
        pass

    def test_find_sentence_span_by_word_span(self):
        struct = {
            "start": 0,
            "end": 376,
            "kind": "article",
            "child":   [
                {
                    'start': 0,
                    'end': 376,
                    'kind': 'paragraph',
                    'child': [
                        {'start': 0, 'end': 117},
                        {'start': 118, 'end': 254},
                        {'start': 255, 'end': 376}
                    ]
                }
            ]
        }

        res = find_sentence_span_by_word_span(struct, (257, 264))

        self.assertEqual(res,{"sentenct_span": (255, 376),
                          "expand_parent":(0,376),"expand_left": (118, 254), "expand_right": None})
    
        res = find_sentence_span_by_word_span(struct, (119, 202))
        self.assertEqual(res,{'sentenct_span': (118, 254), 'expand_parent': (0, 376), 'expand_right': (255, 376), 'expand_left': (0, 117)})

        res = find_sentence_span_by_word_span(struct, (118, 254))
        self.assertEqual(res,{'sentenct_span': (118, 254), 'expand_parent': (0, 376), 'expand_right': (255, 376), 'expand_left': (0, 117)})

        pass
