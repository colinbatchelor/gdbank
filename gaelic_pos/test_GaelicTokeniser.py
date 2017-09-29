# -*- coding: utf-8 -*-
import unittest

from GaelicTokeniser import Tokeniser

class Test(unittest.TestCase):
    def setUp(self):
        self.t = Tokeniser()

    def tearDown(self):
        self.t = None

    def test_hyphens(self):
        self.assertEqual(self.t.tokenise('h-uile'), ['h-uile'])
        # the code tries to keep h-ana-miannaibh together but breaks it elsewhere

    def test_singletons(self):
        # these all have leading apostrophes and should remain as a single unit
        exceptions = ["'ac", '`ac', "'gam", "`gam", "'gad", "`gad", "'ga", "`ga", "'gar", "`gar", "'gur",
                           "`gur", "'gan", "`gan", "'m", "`m", "'n", "`n", "'nam", "`nam", "'nad", "`nad", "'na", "`na",
                           "'nar", "`nar", "‘nar", "'nur", "`nur", "'nan", "`nan", "'san", "'San", "‘San", "`san",
                           "‘sa", "`sa", "‘S", "'S", "`S", "‘ac", "‘ga", "`ga", "‘gan", "`gan"]
        # have omitted [?] as it may be fixed downstream, but worth bearing in mind
        for exception in exceptions:
            self.assertEqual(self.t.tokenise(exception), [ self.t.normalise_quotes(exception) ])

    def test_basic(self):
        self.assertEqual(self.t.tokenise("tha mi a' dol"), ["tha","mi","a'","dol"])

if __name__ == '__main__':
    unittest.main()
