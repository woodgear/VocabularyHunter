import unittest
import util
from article_parser import *
data = """ So, I took this challenge myself and came out the other end with a pretty limited NES emulator, which I call Lochnes. It’s not very good at actually emulating most games, but I’m pretty happy with the guts of the thing and I learned a lot a long the way. I figured it might be worthwhile to share my approach, which might help or inspire others on their own emulation venture!"""


class Test(unittest.TestCase):
    def test_paragraph(self):
        res = cacl_paragraph(data)
        self.assertEqual(res, [{'start': 0, 'end': 118}, {
                         'start': 119, 'end': 255}, {'start': 256, 'end': 377}])
        pass

    def test_clear_article(self):
        input = "\n\ra\n\nb\n\nv\n\r"
        self.assertEqual(clear_article(input), "a\nb\nv")

    def test_cacl_article(self):
        res = cacl_article(data)
        expect_res = [{'start': 0, 'end': 376, 'kind': 'paragraph', 'child': [
            {'start': 0, 'end': 117}, {'start': 118, 'end': 254}, {'start': 255, 'end': 376}]}]
        # print(res)
        for p_range in res["child"]:
            for s_range in p_range["child"]:
                # print(res["raw"][s_range["start"]:s_range["end"]])
                pass
        print(res)
        self.assertEqual((res["start"], res["end"]), (0, 376))
        self.assertEqual(res["child"], expect_res)
        pass
