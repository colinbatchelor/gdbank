# -*- coding: utf-8 -*-
import unittest

from GaelicTokeniser import Tokeniser

class Test(unittest.TestCase):
    def setUp(self):
        self.t = Tokeniser()

    def tearDown(self):
        self.t = None

    def test_basic(self):
        self.assertEqual(self.t.tokenise("tha mi a' dol"), ["tha","mi","a'","dol"])

if __name__ == '__main__':
    unittest.main()
