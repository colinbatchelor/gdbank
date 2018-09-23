import unittest

from simpletokeniser import Tokeniser
from GaelicTokeniser import FullTokeniser

class Test(unittest.TestCase):
    def setUp(self):
        self.t = Tokeniser()
        self.f = FullTokeniser()

    def tearDown(self):
        self.t = None
        self.f = None

    def test_longer(self):
        self.assertEqual(self.f.tokenise("Bha cuimhn' aige air Uilleam o'n a bha e 'n Glaschu: duine mór socair, sàmhach."), ["Bha", "cuimhn'", "aige", "air", "Uilleam", "o'n", "a", "bha", "e", "'n", "Glaschu", ":", "duine", "mór", "socair", ",", "sàmhach", "."])

    def test_placenames(self):
        names = ['Coille Chaoil', 'Gleann Dail', 'Ruaidh Mhònaidh', 'Roinn Eòrpa', 'Port Rìgh', 'Phort Rìgh', 'Loch Aillse', 'Rubha Gharbh', 'Tràigh Ghil', 'Chaolas Mhór', 'Eilean Sgitheanach', 'Fairy Bridge', 'Dùn Bheagain', 'Dùn Èideann', 'Eilean Tiridhe', 'Gleann Ois', 'Inbhir Nis', 'Srath Chluaidh']
        for name in names:
            self.assertEqual(self.f.tokenise(name), [name])

    def test_normalise_quotes(self):
        self.assertEqual(self.f.normalise_quotes("'"), r"'")
        self.assertEqual(self.f.normalise_quotes('’'), r"'")

    def test_bigrams(self):
        self.assertEqual(self.f.tokenise("an raoir"), ["an raoir"])
        self.assertEqual(self.f.tokenise("mun a' BhBC"), ["mun a'", "BhBC"])
        self.assertEqual(self.f.tokenise('Gu dé'), ["Gu dé"])
        self.assertEqual(self.f.tokenise('mu thràth'), ["mu thràth"])
        self.assertEqual(self.f.tokenise('ma tha'), ["ma tha"])
        self.assertEqual(self.f.tokenise('an dràsda'), ["an dràsda"])
        self.assertEqual(self.f.tokenise('an dràsta'), ["an dràsta"])
        self.assertEqual(self.f.tokenise('bhon an'), ["bhon an"])
        self.assertEqual(self.f.tokenise("bhon a' cholbh"), ["bhon a'", "cholbh"])
        self.assertEqual(self.f.tokenise("Nuair a b' e"), ["Nuair", "a b'", "e"])
        
    def test_moregrams(self):
        self.assertEqual(self.f.tokenise("ma dh' fhaoidhte"), ["ma dh'fhaoidhte"])
        self.assertEqual(self.f.tokenise("ma dh' fhaoite"), ["ma dh'fhaoite"])
        self.assertEqual(self.f.tokenise("math dh' fhaoidte"), ["math dh'fhaoidte"])
        self.assertEqual(self.f.tokenise("Caledonian Mac a' Bhruthainn"), ["Caledonian Mac a' Bhruthainn"])
        self.assertEqual(self.f.tokenise("Caledonian Mac a' Bhruthainn a bhith ga ruith"), ["Caledonian Mac a' Bhruthainn", "a", "bhith", "ga", "ruith"])
        # something funny going on here
        #self.assertEqual(self.f.tokenise("Caledonian Mac a’ Bhruthainn a bhith ga ruith"), ["Caledonian Mac a’ Bhruthainn", "a", "bhith", "ga", "ruith"])
        
    def test_punctuation(self):
        mrmcivor = '''"Tha plana eile a' dol airson coimhead ris a' Ghearraidh Chruaidh air fad", thuirt Mgr MacÌomhair.'''
        tokens = self.f.tokenise(mrmcivor)
        self.assertEqual('"', tokens[0])
        self.assertEqual('"', tokens[14])
        self.assertEqual(',', tokens[15])
        self.assertEqual('.', tokens[19])
        self.assertEqual(self.f.tokenise("(oir chan eil carbad aige)"), ["(", "oir", "chan", "eil", "carbad", "aige", ")"])
        self.assertEqual(self.f.tokenise('''"Cha robh gnothach aige thighinn an seo idir," ars esan le feirg.'''), ['"', "Cha", "robh", "gnothach", "aige", "thighinn", "an seo", "idir", ",", '"', "ars", "esan", "le", "feirg", "."])
        self.assertEqual(self.f.tokenise('''(Chan e 'n fhìrinn, a th' aig an seo oir tha grunn ghillean air a' bhaile nach eil pòsd.)'''), ["(", "Chan", "e", "'n", "fhìrinn", ",", "a", "th'", "aig", "an seo", "oir", "tha", "grunn", "ghillean", "air", "a'", "bhaile", "nach", "eil", "pòsd", ".",")"])
        
    def test_hyphens(self):
        self.assertEqual(self.f.tokenise("dhaibh-san"), ["dhaibh-san"])
        self.assertEqual(self.f.tokenise("aobhar-sa"), ["aobhar-sa"])
        self.assertEqual(self.f.tokenise("sibh-se"), ["sibh-se"])
        self.assertEqual(self.f.tokenise('h-uile'), ['h-uile'])
        self.assertEqual(self.f.tokenise('a h-uile'), ['a h-uile'])
        self.assertEqual(self.f.tokenise('na h-Oilthigh'), ["na", "h-", "Oilthigh"])
        self.assertEqual(self.f.tokenise('h-ana-miannaibh'), ['h-', 'ana-miannaibh'])
        self.assertEqual(self.f.tokenise('t-astar'), ['t-', 'astar'])
        self.assertEqual(self.f.tokenise('a-steach'), ['a-steach'])
        # this one breaks interestingly
        # source: http://www.bbc.co.uk/naidheachdan/41523721
        #self.assertEqual(self.t.tokenise("m' aois-se"), ["m'", "aois", "-", "se"])
        self.assertEqual(self.f.tokenise('l\xe0n-\xf9ine'), ['l\xe0n-\xf9ine'])
        self.assertEqual(self.f.tokenise('ar n-eileanan ri teachd'), ['ar', 'n-', 'eileanan', 'ri', 'teachd'])

    def test_money(self):
        # guidelines are silent on the decimal point. Corpus says five tokens.
        # tokeniser originally peeled off the last character as a separate token
        # regardless.
        self.assertEqual(self.f.tokenise("£4.2m"), ["£", "4.2m"])

    def test_fhein(self):
        # making sure fhèin hyphenated to a pronoun is three tokens
        self.assertEqual(self.f.tokenise("e-fhèin"), ["e","-","fhèin"])
        self.assertEqual(self.f.tokenise("sinn-fhìn"), ["sinn","-","fhìn"])
        
    def test_dh(self):
        self.assertEqual(self.f.tokenise("dh’fhàs"), ["dh’", "fhàs"])
        self.assertEqual(self.f.tokenise("dh'fhàs"), ["dh'", "fhàs"])
        self.assertEqual(self.f.tokenise("dh'fhaodas"), ["dh'", "fhaodas"])
        self.assertEqual(self.f.tokenise('dh’obair-riaghaltais'), [ "dh’", "obair-riaghaltais" ])

    def singletons_leading_smart_quote(self):
        # don't seem to work at present
        exceptions = [ "‘nar", "‘San", "‘sa", "‘S", "‘ac", "‘ga", "‘gan" ]

    def test_multiple_punctuation(self):
        # chiefly here because of checks at bigram stage in original
        # also remember to pass tokens
        self.assertEqual(self.f._punctuation(["tus'"]), ["tus'"])
        self.assertEqual(self.f._punctuation([".)"]), [".",")"])
        self.assertEqual(self.f._punctuation(["),"]), [")",","])
        self.assertEqual(self.f._punctuation([")."]), [")","."])
        self.assertEqual(self.f._punctuation([");"]), [")",";"])
         #self.assertEqual(self.f._punctuation(["’.”"]), ["’",".","”"])
        self.assertEqual(self.f._punctuation(['mo','chat!)']), ["mo", "chat", "!", ")"]) 
        self.assertEqual(self.f._punctuation(["a","chanas","mi.”"]), ["a", "chanas", "mi",".","”"])
        self.assertEqual(self.f._punctuation(["a","chanas", "mi,”"]), ["a", "chanas", "mi",",","”"])
        self.assertEqual(self.f._punctuation(["às.”"]), ["às",".","”"])
        self.assertEqual(self.f._punctuation(["sa,”"]), ["sa",",","”"])

    def test_trailing_apostrophes(self):
        # don't seem to work at present in original
        self.assertEqual(self.t.tokenise("a bh innt',"), ["a", "bh", "innt'", ","])
        self.assertEqual(self.t.tokenise("creids'"), ["creids'"])
        self.assertEqual(self.t.tokenise("toilicht'"), ["toilicht'"])

    def test_areir(self):
        self.assertEqual(self.f.tokenise('a-réir'), ['a','-','réir'])

    def test_demonstratives(self):
        self.assertEqual(self.f.tokenise("a' shineach"), ["a' shineach"])
        self.assertEqual(self.f.tokenise("a shineach"), ["a shineach"])
        self.assertEqual(self.f.tokenise("ann a sheo"), ["ann a sheo"])
        self.assertEqual(self.f.tokenise("ann a shin"), ["ann a shin"])
        self.assertEqual(self.f.tokenise("ann a shineach"), ["ann a shineach"])
        self.assertEqual(self.f.tokenise("ann a shiudach"), ["ann a shiudach"])
        self.assertEqual(self.f.tokenise("ann a' shiudach"), ["ann a' shiudach"])
        self.assertEqual(self.f.tokenise("ann an seo"), ["ann an seo"])
        self.assertEqual(self.f.tokenise("ann an siud"), ["ann an siud"])
        self.assertEqual(self.f.tokenise("ann an"), ["ann an"])
        self.assertEqual(self.f.tokenise("ann am"), ["ann am"])

    def test_multipunc(self):
        self.assertEqual(self.f.tokenise("!)"), ["!",")"])

    def test_internal_apostrophes(self):
        self.assertEqual(self.f.tokenise("Mu’n"), ["Mu’n"])
        self.assertEqual(self.f.tokenise("a's"), ["a's"])
        self.assertEqual(self.f.tokenise("a’s"), ["a’s"])
        self.assertEqual(self.f.tokenise("le'r"), ["le","'r"])
        
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
