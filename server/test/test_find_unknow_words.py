import unittest
from find_unknow_words import *

aritcle1 = """Those who do not understand Unix are condemned to reinvent it, poorly.
– Henry Spencer, Usenet signature, November 1987
"""
class TestWord(unittest.TestCase):
    def test_case_word_tokenize(self):
        print(self.id())
        """
        Test word_tokenize which will spilt word from article
        """
        words1 = tokenize(aritcle1)
        print(words1)
        self.assertEqual(words1, ['those', 'understand', 'unix', 'condemned', 'reinvent',
                         'poorly', 'henry', 'spencer', 'usenet', 'signature', 'november'])
        self.assertEqual(tokenize("same word is same word"), ['same', 'word'])

    def test_find_different_word(self):
        unknow_word = find_unknow_word(['those', 'understand', 'unix', 'condemned', 'reinvent', 'poorly',
                                       'henry', 'spencer', 'usenet', 'signature', 'november'], ['those', 'understand', 'unix', 'november'])
        self.assertEqual(unknow_word, [
                         'condemned', 'reinvent', 'poorly', 'henry', 'spencer', 'usenet', 'signature'])

    def test_word_span_tokenize(self):
        res = list(raw_word_span_tokenize(aritcle1))
        res  = [s["span"] for s in res]

        self.assertEqual(res,[(0, 5), (6, 9), (10, 12), (13, 16), (17, 27), (28, 32), (33, 36), (37, 46), (47, 49), (50, 58), (59, 61), (61, 62), (63, 69), (69, 70), (71, 72), (73, 78), (79, 86), (86, 87), (88, 94), (95, 104), (104, 105), (106, 114), (115, 119)])
        pass

if __name__ == '__main__':
    unittest.main()
