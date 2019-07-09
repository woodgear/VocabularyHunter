import unittest
from find_unknow_words import * 
class TestWord(unittest.TestCase):
    def test_case_word_tokenize(self):
        print(self.id())
        """
        Test word_tokenize which will spilt word from article
        """
        words1 = tokens(
"""Those who do not understand Unix are condemned to reinvent it, poorly.
– Henry Spencer, Usenet signature, November 1987
""")
        self.assertEqual(words1,['those', 'understand', 'unix', 'condemned', 'reinvent', 'poorly', 'henry', 'spencer', 'usenet', 'signature', 'november'])
        self.assertEqual(tokens("same word is same word"),['same','word'])
    def test_find_different_word(self):
        unknow_word = find_unknow_word(['those', 'understand', 'unix', 'condemned', 'reinvent', 'poorly', 'henry', 'spencer', 'usenet', 'signature', 'november'],['those','understand','unix','november'])
        self.assertEqual(unknow_word,['condemned','reinvent','poorly','henry','spencer','usenet','signature'])

if __name__ == '__main__':
    unittest.main()