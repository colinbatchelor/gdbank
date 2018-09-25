import unittest

from checker import Checker

class Test(unittest.TestCase):
    def setUp(self):
        self.c = Checker()

    def tearDown(self):
        self.c = None

    def check(self, goodtokens, badtokens, code):
        self.assertFalse(code in [t[2] for t in self.c._check(goodtokens)])
        self.assertTrue(code in [t[2] for t in self.c._check(badtokens)])
        
    def test_singilte(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        bad_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rudan","Ncpmn")]
        self.check(good_iomadh, bad_iomadh, "SINGILTE")

    def test_barrachd(self):
        good_tokens = [("barrachd", "Ncsfn"), ("fiosrachaidh", "Ncsmg")]
        bad_tokens = [("barrachd", "Ncsfn"), ("fiosrachadh", "Ncsmn")]
        self.check(good_tokens, bad_tokens, "GINIDEACH/SINGILTE")
        good_tokens = [("tuilleadh", "Ncsfn"), ("fiosrachaidh", "Ncsmg")]
        bad_tokens = [("tuilleadh", "Ncsfn"), ("fiosrachadh", "Ncsmn")]
        self.check(good_tokens, bad_tokens, "GINIDEACH/SINGILTE")
        
    def test_Ar(self):
        badtokens = [("deagh", "Ar"), ("foghlam", "Ncsmn")]
        goodtokens = [("deagh", "Ar"), ("fhoghlam", "Ncsmn")]
        self.check(goodtokens, badtokens, "LENITE")
        
    def test_hyphens(self):
        text = '''Sann,Wp-i-x
ris,Sp
a',Tdsm
ghinealach,Ncsmd
againne,Pr1p--e
an diugh,Rt
a,Q-r
tha,V-p
e,Pp3sm
an,Sp
urra,Ncsmd
a,Ug
dhearbhadh,Nv
có,Uq
de'n,Spa-s
dithis,Ncsfn
a,Q-r
tha,V-p
ceàrr,Ap
:,Fi
's,Wp-i
neònach,Ap
mur,Cs
e,Pp3sm
seo,Pd
an,Tdsm
cothrom,Ncsmn
mu dheireadh,Aq
a,Q-r
gheibh,V-f
sinn,Pp1p
.,Fe'''
        pairs = text.splitlines()
        tokens = [(pair.split(',')[0],pair.split(',')[1]) for pair in pairs]
        checked = self.c._check(tokens)
        self.assertEqual(checked[5], ('an diugh', 'Rt', 'GOC-HYPHEN', 'hyphen needed'))
        
if __name__ == '__main__':
    unittest.main()
