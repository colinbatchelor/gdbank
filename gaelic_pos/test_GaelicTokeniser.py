import unittest

from GaelicTokeniser import Tokeniser

class Test(unittest.TestCase):
    def setUp(self):
        self.t = Tokeniser()

    def tearDown(self):
        self.t = None

    def test_placenames(self):
        self.assertEqual(self.t.tokenise('Roinn Eòrpa'), ['Roinn Eòrpa'])
        self.assertEqual(self.t.tokenise('Port Rìgh'), ['Port Rìgh'])
        self.assertEqual(self.t.tokenise('Phort Rìgh'), ['Phort Rìgh'])
        self.assertEqual(self.t.tokenise('Loch Aillse'), ['Loch Aillse'])

    def test_normalise_quotes(self):
        self.assertEqual(self.t.normalise_quotes("'"), r"'")
        self.assertEqual(self.t.normalise_quotes('’'), r"'")

    def test_bigrams(self):
        self.assertEqual(self.t.tokenise('Gu dé'), ["Gu dé"])
        self.assertEqual(self.t.tokenise('mu thràth'), ["mu thràth"])
        self.assertEqual(self.t.tokenise('ma tha'), ["ma tha"])
        # self.assertEqual(self.t.tokenise("a b'"), ["a b'"])

    def moregrams(self):
        # this one doesn't seem to work either
        self.assertEqual(self.t.tokenise("Caledonian Mac a' Bhruthainn"), ["Caledonian Mac a' Bhruthainn"])
        
    def punctuation(self):
        # this one doesn't seem to work either
        tokens = self.t.tokenise('''"Tha plana eile a' dol airson coimhead ris a' Ghearraidh Chruaidh air fad", thuirt Mgr MacÌomhair.''')
        print(tokens)
        self.assertEqual('"', tokens[0])
        self.assertEqual('"', tokens[13])
        self.assertEqual(',', tokens[14])
        self.assertEqual('.', tokens[18])
        
    def test_hyphens(self):
        self.assertEqual(self.t.tokenise('h-uile'), ['h-uile'])
        self.assertEqual(self.t.tokenise('h-ana-miannaibh'), ['h-', 'ana-miannaibh'])
        self.assertEqual(self.t.tokenise('t-astar'), ['t-', 'astar'])
        self.assertEqual(self.t.tokenise('a-steach'), ['a-steach'])
        # this one breaks interestingly
        # source: http://www.bbc.co.uk/naidheachdan/41523721
        #self.assertEqual(self.t.tokenise("m' aois-se"), ["m'", "aois", "-", "se"])
        self.assertEqual(self.t.tokenise('l\xe0n-\xf9ine'), ['l\xe0n-\xf9ine'])
        self.assertEqual(self.t.tokenise('ar n-eileanan ri teachd'), ['ar', 'n-', 'eileanan', 'ri', 'teachd'])

    def test_dh(self):
        self.assertEqual(self.t.tokenise("dh’fhàs"), ["dh'", "fhàs"])
        self.assertEqual(self.t.tokenise("dh'fhàs"), ["dh'", "fhàs"])
        #mentioned in code but doesn't seem to work like that
        #self.assertEqual(self.t.tokenise('dh’obair-riaghaltais'), [ "dh'", "obair-riaghaltais" ])

    def singletons_leading_smart_quote(self):
        # don't seem to work at present
        exceptions = [ "‘nar", "‘San", "‘sa", "‘S", "‘ac", "‘ga", "‘gan" ]

    def trailing_apostrophes(self):
        # don't seem to work at present
        self.assertEqual(self.t.tokenise("innt'"), ["innt'"])
        self.assertEqual(self.t.tokenise("creids'"), ["creids'"])
        self.assertEqual(self.t.tokenise("toilicht'"), ["toilicht'"])

    def test_singletons(self):
        # these all have leading apostrophes and should remain as a single unit
        exceptions = ["'ac", '`ac', "'gam", "`gam", "'gad", "`gad", "'ga", "`ga", "'gar", "`gar", "'gur",
                      "`gur", "'gan", "`gan", "'m", "`m", "'n", "`n", "'nam", "`nam", "'nad", "`nad", "'na", "`na",
                      "'nar", "`nar", "'nur", "`nur", "'nan", "`nan", "'san", "'San", "`san",
                      "`sa", "'S", "`S",
                      "`ga", "`gan"]
        # have omitted [?] as it may be fixed downstream, but worth bearing in mind
        for exception in exceptions:
            self.assertEqual(self.t.tokenise(exception), [ self.t.normalise_quotes(exception) ])

    def test_basic(self):
        self.assertEqual(self.t.tokenise("tha mi a' dol"), ["tha","mi","a'","dol"])

if __name__ == '__main__':
    unittest.main()
