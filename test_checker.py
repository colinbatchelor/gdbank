import unittest
from gd_tools.acainn import Morphology
from checker import Checker
import numpy as np

class Test(unittest.TestCase):
    def setUp(self):
        self.c = Checker()
        self.l = Morphology()

    def tearDown(self):
        self.c = None
        self.l = None
        
    def check(self, goodtokens, badtokens, code):
        goodresult = self.c._check(goodtokens)
        goodlist = [list(filter(None, t.split(','))) for t in goodresult.code.tolist()]
        flat_good = [item for sublist in goodlist for item in sublist]

        badresult = self.c._check(badtokens)
        badlist = [list(filter(None, t.split(','))) for t in badresult.code.tolist()]
        flat_bad = [item for sublist in badlist for item in sublist]

        self.assertFalse(code in flat_good)
        self.assertTrue(code in flat_bad)

    # this is for cases where we have a list of single tokens
    def check_every(self, goodtokens, badtokens, code):
        goodresult = [''.join(t.split(',')) for t in self.c._check(goodtokens).code.tolist()]
        for i,result_code in enumerate(goodresult):
            self.assertNotEqual(result_code, code, msg = goodtokens[i])
        badresult = [''.join(t.split(',')) for t in self.c._check(badtokens).code.tolist()]
        for i,result_code in enumerate(badresult):
            self.assertEqual(result_code, code, msg = badtokens[i])

    def test_lenition(self):
        self.assertTrue(self.l.lenited("stad"))
        goodtokens = [("ma","Cs"), ("thomhaiseas","V-f--r")]
        badtokens = [("ma","Cs"), ("tomhaiseas","V-f--r")]
        self.check(goodtokens, badtokens, "45iealpha")
        goodtokens = [("a", "Q-r"), ("chòrdas","V-f--r")]
        badtokens = [("a", "Q-r"), ("còrdas","V-f--r")]
        self.check(goodtokens, badtokens, "45iealpha")
        goodtokens = [("do", "Q--s"), ("chòrd","V-s")]
        badtokens = [("do", "Q--s"), ("còrd","V-s")]
        self.check(goodtokens, badtokens, "45iebeta")
        goodtokens = [("an", "Tdsf"), ("dithis", "Ncsfn"), ("bheag", "Aq-sfn")]
        badtokens = [("an", "Tdsf"), ("dithis", "Ncsfn"), ("beag", "Aq-smn")]
        self.check(goodtokens, badtokens, "144ii")
        goodtokens = [("dithis", "Ncsfn"), ("bhalach", "Ncsmg")]
        badtokens = [("dithis", "Ncsfn"), ("balach", "Ncsmn")]
        self.check(goodtokens, badtokens, "144iii")
        
        goodtokens = [("Thug","V-s"), ("stad","V-s"), ("Bhiodh","V-h"), ("ruigeadh","V-h")]
        badtokens = [("Tug","V-s"), ("faodadh", "V-h"), ("dèanadh","V-h")]
        self.check_every(goodtokens, badtokens, "44iiia")

    def test_speciallenition(self):
        goodtokens = [("cha", "Qn"), ("ghabh", "V-f--d")]
        badtokens = [("cha", "Qn"), ("gabh", "V-f--d")]
        self.check(goodtokens, badtokens, "45iegamma")

    def test_flenition(self):
        goodtokens = [("An","Qq"), ("fhàs","V-f--d")]
        badtokens = [("Am","Qq"), ("fàs","V-f--d")]
        self.check(goodtokens, badtokens, "45iia")
        # the test for this is not f-lenition but d-lenition. More complicated.
        #goodtokens = [("Chan","Qn"), ("fhuirich","V-s--d")]
        #badtokens = [("Cha","Qn"), ("do","Q--s"), ("dh'", "Uo"), ("fhuirich", "V-s--d")]

    def test_nolenition(self):
        goodtokens = [("tug","V-s--d"), ("stad","V-s--d"), ("biodh","V-h--d"), ("ruigeadh","V-h--d")]
        badtokens = [("thug","V-s--d"), ("fhaodadh", "V-h--d"), ("dhèanadh","V-h--d")]
        self.check_every(goodtokens, badtokens, "44iiia-")
        
    def test_genitivenames(self):
        good_f = [("Brìde","Nn-fg")]
        bad_f = [("Bhrìde","Nn-fg")]
        self.check(good_f, bad_f, "45iabeta-")
        self.assertFalse("LENITE" in [t[2] for t in self.c._check ([("Aonghais","Nn-mg")])])
        good_m = [("Dhòmhnaill","Nn-mg")]
        bad_m = [("Dòmhnaill","Nn-mg")]
        self.check(good_m, bad_m, "45iabeta")
        
    def test_singilte(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        bad_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rudan","Ncpmn")]
        self.check(good_iomadh, bad_iomadh, "173")

    def test_barrachd(self):
        good_tokens = [("barrachd", "Ncsfn"), ("fiosrachaidh", "Ncsmg")]
        bad_tokens = [("barrachd", "Ncsfn"), ("fiosrachadh", "Ncsmn")]
        self.check(good_tokens, bad_tokens, "170")
        good_tokens = [("tuilleadh", "Ncsfn"), ("fiosrachaidh", "Ncsmg")]
        bad_tokens = [("tuilleadh", "Ncsfn"), ("fiosrachadh", "Ncsmn")]
        self.check(good_tokens, bad_tokens, "176")
        
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
        checked = [list(filter(None, t.split(','))) for t in self.c._check(tokens).code.tolist()]
        self.assertEqual(checked[5], ['GOC-HYPHEN'])

    def test_basic(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.c._make_df(good_iomadh)
        self.assertEqual(3, len(result))

    def test_mo(self):
        good = [("dhùin","V-s"),("mi","Pp1s"),("mo","Dp1s"),("shùilean","Ncpfn"),("san","Spa-s"),("deireadh","Ncsmd")]
        result = self.c._check(good)
        bad = [("dhùin","V-s"),("mi","Pp1s"),("mo","Dp1s"),("sùilean","Ncpfn"),("san","Spa-s"),("deireadh","Ncsmd")]
        r2 = self.c._check(bad)
        
    def test_feats(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.c._feats(self.c._make_df(good_iomadh))
        self.assertEqual(np.dtype(bool), np.dtype(result._lenited))
        br = [("barrachd", "Ncsmn"), ("fiosrachaidh", "Ncsmg")]
        r2 = self.c._feats(self.c._make_df(br))
        self.assertEqual(np.dtype(bool), np.dtype(r2._genitive))
        self.assertListEqual([False, True], r2._genitive.tolist())
        self.assertListEqual([False, True], r2._genitivesing.tolist())
        self.assertListEqual([True, True], r2._sing.tolist())

    def test_checkerDfs(self):
        self.assertEqual(np.dtype(object), np.dtype(self.c.lenitesp_1._p_1))
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.c._feats(self.c._make_df(good_iomadh))
        merged = result.merge(self.c.lenitesp_1, on = ("_p_1","_lenited"), how="left")
        
if __name__ == '__main__':
    unittest.main()
