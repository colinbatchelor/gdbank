# -*- coding: utf-8 -*-
import unittest
from acainn import Lemmatizer, Retagger, Subcat, Typer

# checks that all the labels actually match
class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.r = Retagger()
        self.s = Subcat()
        self.t = Typer()

    def tearDown(self):
        self.r = None
        self.s = None
        self.t = None

    def test_retagger(self):
        specialtags = set()
        tags = [value for key,value in self.r.retaggings.iteritems()]
        for key in self.r.specials.iterkeys():
            for item in self.r.specials[key]:
                specialtags.add(item)
        for tag in tags:
            self.assertTrue(tag in self.t.types.keys())

    def test_subcat(self):
        for key in self.s.mappings.iterkeys():
            for item in self.s.mappings[key]:
                self.assertTrue(item in self.t.types.keys(), item)

class TestTyper(unittest.TestCase):
    def setUp(self):
        self.t = Typer()

    def tearDown(self):
        self.t = None

    def test(self):
        self.assertEqual(self.t.type("tha", "V-p", "BIPP")[1], "s[dcl pres cons]/pp/n")
        self.assertEqual(self.t.type("bha", "V-s", "BIPP")[1], "s[dcl past cons]/pp/n")

class TestRetagger(unittest.TestCase):
    def setUp(self):
        self.r = Retagger()

    def tearDown(self):
        self.r = None

    def test(self):
        ag = self.r.retag("ag", "Sa")
        self.assertTrue("ASP" in ag)
        self.assertEqual(self.r.retag("a'", "Sa"), ["ASP"])
        agus = self.r.retag("agus", "Cc")
        self.assertTrue("CONJ" in agus)
        air = self.r.retag("air", "Sp")
        self.assertTrue("PP" in air)
        self.assertTrue("P" in air)
        self.assertEqual(self.r.retag("droch", "Ar"), ["DET"]) # not really
        comma = self.r.retag(",", "Fi")
        self.assertTrue("PUNC" in comma)
        fullstop = self.r.retag(".", "Fe")
        self.assertTrue("PUNC" in fullstop)
        self.assertEqual(self.r.retag("le", "Sp"), ["P"])
        self.assertEqual(self.r.retag("gun", "Qa"), ["GU"])
        self.assertEqual(self.r.retag("dìreach", "Rg"), ["ADV"])
        self.assertEqual(self.r.retag("Comhairle", "Ncsdf"), ["N"])
        self.assertEqual(self.r.retag("galain", "Ncsfn"), ["N"])
        self.assertEqual(self.r.retag("an", "Tdsf"), ["DET"])
        self.assertEqual(self.r.retag("na", "Tdsfg"), ["DETNMOD"])
        self.assertEqual(self.r.retag("[1]", "Xsc"), ["ADVPRE"])
        radh = self.r.retag("ràdh", "Nv")
        self.assertTrue("VPROP" in radh)
        rinn = self.r.retag("rinn", "V-s")
        self.assertTrue("TRANS" in rinn)
        tha = self.r.retag("tha", "V-p")
        self.assertTrue("BIPP" in tha)
        self.assertTrue("BIPROG" in tha)

class TestSubcat(unittest.TestCase):
    def setUp(self):
        self.s = Subcat()

    def tearDown(self):
        self.s = None

    def test_lemmata(self):
        self.assertEqual(self.s.subcat("bi"), ['BIPROG', 'BIPP'])
        self.assertEqual(self.s.subcat("is"), ['TRANS'])
        self.assertEqual(self.s.subcat("abair"), ['TRANS', 'VPROP'])
        self.assertEqual(self.s.subcat("arsa"), ['QUOTE'])
        cluinn = self.s.subcat("cluinn")
        self.assertTrue('TRANS' in cluinn)
        self.assertTrue('VPROPQ' in cluinn)
        self.assertTrue('VBHO' in cluinn)
        dean = self.s.subcat("dèan")
        self.assertTrue('TRANS' in dean)
        self.assertTrue('VAIR' in dean)
        faic = self.s.subcat("faic")
        self.assertEqual(faic, ['TRANS'])
        faigh = self.s.subcat("faigh")
        self.assertTrue('TRANS' in faigh)
        rach = self.s.subcat("rach")
        self.assertTrue('INTRANS' in rach)
        self.assertTrue('RACH' in rach)
        thig = self.s.subcat("thig")
        self.assertTrue('INTRANS' in thig)
        buail = self.s.subcat("buail")
        self.assertTrue('TRANS' in buail)
        bruidhinn = self.s.subcat("bruidhinn")
        self.assertTrue('VRI' in bruidhinn)
        coimhead = self.s.subcat("coimhead")
        self.assertTrue('VAIR' in coimhead)
        self.assertTrue('VRI' in coimhead)
        coinnich = self.s.subcat("coinnich")
        self.assertTrue('VRI' in coinnich)
        cuir = self.s.subcat("cuir")
        self.assertTrue('VAIR' in cuir)
        self.assertTrue('VRI' in cuir)
        cum = self.s.subcat("cùm")
        self.assertTrue('VAIR' in cum)
        self.assertTrue('VPROPQ' in cum)
        fag = self.s.subcat("fàg")
        self.assertFalse('INTRANS' in fag)
        falbh = self.s.subcat("falbh")
        self.assertFalse('TRANS' in falbh)
        faod = self.s.subcat("faod")
        self.assertTrue('FAODFEUM' in faod)
        fas = self.s.subcat("fàs")
        self.assertTrue('INTRANS' in fas)
        self.assertTrue('VADJ' in fas)
        feuch = self.s.subcat("feuch")
        self.assertTrue('VRI' in feuch)
        self.assertTrue('VPROP' in feuch)
        self.assertTrue('VPROPQ' in feuch)
        feum = self.s.subcat("feum")
        self.assertTrue('FAODFEUM' in feum)
        fuirich = self.s.subcat("fuirich")
        self.assertTrue('VAIR' in fuirich)
        gabh = self.s.subcat("gabh")
        self.assertTrue('VAIR' in gabh)
        self.assertTrue('VRI' in gabh)
        gluais = self.s.subcat("gluais")
        self.assertFalse('INTRANS' in gluais)
        iarr = self.s.subcat("iarr")
        self.assertTrue('VAIR' in iarr)
        inns = self.s.subcat("inns")
        self.assertTrue('VPROPQ' in inns)
        leig = self.s.subcat("leig")
        self.assertTrue('VLE' in leig)
        self.assertTrue('VDE' in leig)
        obraich = self.s.subcat("obraich")
        self.assertTrue('INTRANS' in obraich)
        ruig = self.s.subcat("ruig")
        self.assertTrue('VAIR' in ruig)
        ruith = self.s.subcat("ruith")
        self.assertFalse('TRANS' in ruith)
        seall = self.s.subcat("seall")
        self.assertTrue('VAIR' in seall)
        smaoinich = self.s.subcat("smaoinich")
        self.assertTrue('VPROP' in smaoinich)
        self.assertTrue('VMU' in smaoinich)
        tachair = self.s.subcat("tachair")
        self.assertTrue('IMPERS' in tachair)
        self.assertTrue('VAIR' in tachair)
        toisich = self.s.subcat("tòisich")
        self.assertTrue('BIPROG', toisich)
        tionndaidh = self.s.subcat("tionndaidh")
        self.assertTrue('VGU' in tionndaidh)

class TestLemmatizer(unittest.TestCase):
    def setUp(self):
        self.l = Lemmatizer()

    def tearDown(self):
        self.l = None

    def test_bi(self):
        self.assertEqual(self.l.lemmatize("tha", "V-p"), "bi")
        self.assertEqual(self.l.lemmatize("thà", "V-p"), "bi")
        self.assertEqual(self.l.lemmatize("Tha", "V-p"), "bi")
        self.assertEqual(self.l.lemmatize("th'", "V-p"), "bi")
        self.assertEqual(self.l.lemmatize("bha", "V-s"), "bi")
        self.assertEqual(self.l.lemmatize("bh'", "V-s"), "bi")
        self.assertEqual(self.l.lemmatize("eil", "V-p--d"), "bi")
        self.assertEqual(self.l.lemmatize("robh", "V-s--d"), "bi")
        self.assertEqual(self.l.lemmatize("bhith", "Nv"), "bi")
        self.assertEqual(self.l.lemmatize("bhiodh", "V-h"), "bi")
        self.assertEqual(self.l.lemmatize("bhi", "V-f--d"), "bi")
        self.assertEqual(self.l.lemmatize("bi", "V-f--d"), "bi")
        self.assertEqual(self.l.lemmatize("bhios", "V-f--r"), "bi")
        self.assertEqual(self.l.lemmatize("bidh", "V-f"), "bi")
        self.assertEqual(self.l.lemmatize("biodh", "V-h--d"), "bi")

    def test_copula(self):
        self.assertEqual(self.l.lemmatize("an", "Wpdqa"), "is")
        self.assertEqual(self.l.lemmatize("B'", "Ws"), "is")
        self.assertEqual(self.l.lemmatize("b'", "Ws"), "is")
        self.assertEqual(self.l.lemmatize("bu", "Ws"), "is")
        self.assertEqual(self.l.lemmatize("cha", "Wp-in"), "is")
        self.assertEqual(self.l.lemmatize("chan", "Wp-in"), "is")
        self.assertEqual(self.l.lemmatize("gur", "Wpdia"), "is")
        self.assertEqual(self.l.lemmatize("'S", "Wp-i"), "is")
        self.assertEqual(self.l.lemmatize("'s", "Wp-i"), "is")
        self.assertEqual(self.l.lemmatize("is", "Wp-i"), "is")
        self.assertEqual(self.l.lemmatize("nach", "Wpdqn"), "is")
        self.assertEqual(self.l.lemmatize("'se", "Wp-i-3"), "is")
        self.assertEqual(self.l.lemmatize("as", "Wpr"), "is")

    def test_irregulars(self):
        self.assertEqual(self.l.lemmatize("Thuirt", "V-s"), "abair")
        self.assertEqual(self.l.lemmatize("thuirt", "V-s"), "abair")
        self.assertEqual(self.l.lemmatize("ràdh", "Nv"), "abair")
        self.assertEqual(self.l.lemmatize("ars\xe2\x80\x99", "V-s"), "arsa")
        self.assertEqual(self.l.lemmatize("ars'", "V-s"), "arsa")
        self.assertEqual(self.l.lemmatize("as", "V-s"), "arsa")
        self.assertEqual(self.l.lemmatize("chuala", "V-s"), "cluinn")
        self.assertEqual(self.l.lemmatize("dèanamh", "Nv"), "dèan")
        self.assertEqual(self.l.lemmatize("dhèanamh", "Nv"), "dèan")
        self.assertEqual(self.l.lemmatize("nì", "V-f"), "dèan")
        self.assertEqual(self.l.lemmatize("Rinn", "V-s"), "dèan")
        self.assertEqual(self.l.lemmatize("rinn", "V-s"), "dèan")
        self.assertEqual(self.l.lemmatize("chunnaic", "V-s"), "faic")
        self.assertEqual(self.l.lemmatize("faicinn", "Nv"), "faic")
        self.assertEqual(self.l.lemmatize("fhaicinn", "Nv"), "faic")
        self.assertEqual(self.l.lemmatize("faigheadh", "V-h--d"), "faigh")
        self.assertEqual(self.l.lemmatize("faighinn", "Nv"), "faigh")
        self.assertEqual(self.l.lemmatize("fhuair", "V-s"), "faigh")
        self.assertEqual(self.l.lemmatize("gheibh", "V-f"), "faigh")
        self.assertEqual(self.l.lemmatize("Chaidh", "V-s"), "rach")
        self.assertEqual(self.l.lemmatize("chaidh", "V-s"), "rach")
        self.assertEqual(self.l.lemmatize("deach", "V-s--d"), "rach")
        self.assertEqual(self.l.lemmatize("dhol", "Nv"), "rach")
        self.assertEqual(self.l.lemmatize("dol", "Nv"), "rach")
        self.assertEqual(self.l.lemmatize("Thèid", "V-f"), "rach")
        self.assertEqual(self.l.lemmatize("thèid", "V-f"), "rach")
        self.assertEqual(self.l.lemmatize("tèid", "V-f--d"), "rach")
        self.assertEqual(self.l.lemmatize("thàinig", "V-s"), "thig")
        self.assertEqual(self.l.lemmatize("tighinn", "Nv"), "thig")
        self.assertEqual(self.l.lemmatize("thug", "V-s"), "thoir")
        self.assertEqual(self.l.lemmatize("tug", "V-s--d"), "thoir")
        self.assertEqual(self.l.lemmatize("bheir", "V-f"), "thoir")
        self.assertEqual(self.l.lemmatize("thoirt", "Nv"), "thoir")
        self.assertEqual(self.l.lemmatize("toirt", "Nv"), "thoir")

    def test_regulars(self):
        self.assertEqual(self.l.lemmatize("bhuail", "V-s"), "buail")
        self.assertEqual(self.l.lemmatize("choinnich", "V-s"), "coinnich")
        self.assertEqual(self.l.lemmatize("chuir", "V-s"), "cuir")
        self.assertEqual(self.l.lemmatize("fhàg", "V-s"), "fàg")
        self.assertEqual(self.l.lemmatize("faodaidh", "V-f"), "faod")
        self.assertEqual(self.l.lemmatize("feuch", "Vm-2s"), "feuch")
        self.assertEqual(self.l.lemmatize("fheuch", "V-s"), "feuch")
        self.assertEqual(self.l.lemmatize("feumaidh", "V-f"), "feum")
        self.assertEqual(self.l.lemmatize("ghabh", "V-s"), "gabh")
        self.assertEqual(self.l.lemmatize("ràinig", "V-s"), "ruig")
        self.assertEqual(self.l.lemmatize("thachair", "V-s"), "tachair")
        self.assertEqual(self.l.lemmatize("thòisich", "V-s"), "tòisich")

    def nv(self, vn, root):
        self.assertEqual(self.l.lemmatize_vn(vn), root)

    def test_nvs(self):
        self.assertEqual(self.l.lemmatize_vn('àicheadh'), "àicheidh")
        self.assertEqual(self.l.lemmatize_vn('amas'), 'amais')
        self.assertEqual(self.l.lemmatize_vn('amharc'), 'amhairc')
        self.assertEqual(self.l.lemmatize_vn('agairt'), 'agair')
        self.assertEqual(self.l.lemmatize_vn('bagairt'), 'bagair')
        self.assertEqual(self.l.lemmatize_vn('baisteadh'), 'baist')
        self.assertEqual(self.l.lemmatize_vn('blasad'), 'blais')
        self.assertEqual(self.l.lemmatize_vn('blasadh'), 'blais')
        self.assertEqual(self.l.lemmatize_vn('brìodal'), 'brìodail')
        self.assertEqual(self.l.lemmatize_vn('briseadh'), 'bris')
        self.assertEqual(self.l.lemmatize_vn('bristeadh'), 'bris')
        self.assertEqual(self.l.lemmatize_vn('bruich'), 'bruich')
        self.assertEqual(self.l.lemmatize("bruidhinn", "Nv"), "bruidhinn")
        self.assertEqual(self.l.lemmatize_vn('bruthadh'), 'brùth')
        self.assertEqual(self.l.lemmatize_vn('buntainn'), 'buin')
        self.nv("cinntinn", "cinn")
        self.nv("cagar", "cagair")
        self.nv("cagarsaich", "cagair")
        self.nv("cagartaich", "cagair")
        self.nv("casgairt", "casgair")
        self.nv("casgradh", "casgair")
        self.assertEqual(self.l.lemmatize("coimhead", "Nv"), "coimhead")
        self.assertEqual(self.l.lemmatize("cur", "Nv"), "cuir")
        self.assertEqual(self.l.lemmatize("chur", "Nv"), "cuir")
        self.nv("cluiche", "cluich")
        self.assertEqual(self.l.lemmatize("creidsinn", "Nv"), "creid")
        self.assertEqual(self.l.lemmatize("cumail", "Nv"), "cùm")
        self.assertEqual(self.l.lemmatize("falbh", "Nv"), "falbh")
        self.assertEqual(self.l.lemmatize("fàs", "Nv"), "fàs")
        self.assertEqual(self.l.lemmatize("feuchainn", "Nv"), "feuch")
        self.assertEqual(self.l.lemmatize("fhalbh", "Nv"), "falbh")
        self.assertEqual(self.l.lemmatize("fuireach", "Nv"), "fuirich")
        self.assertEqual(self.l.lemmatize("gabhail", "Nv"), "gabh")
        self.assertEqual(self.l.lemmatize("gluasad", "Nv"), "gluais")
        self.assertEqual(self.l.lemmatize("iarraidh", "Nv"), "iarr")
        self.assertEqual(self.l.lemmatize("innse", "Nv"), "inns")
        self.assertEqual(self.l.lemmatize("leigeil", "Nv"), "leig")
        self.assertEqual(self.l.lemmatize("obair", "Nv"), "obraich")
        self.assertEqual(self.l.lemmatize("ruith", "Nv"), "ruith")
        self.assertEqual(self.l.lemmatize("sealltainn", "Nv"), "seall")
        self.assertEqual(self.l.lemmatize("smaoineachadh", "Nv"), "smaoinich")
        self.assertEqual(self.l.lemmatize("tachairt", "Nv"), "tachair")
        self.assertEqual(self.l.lemmatize_vn("tòiseachadh"), "tòisich")
        self.assertEqual(self.l.lemmatize_vn("tionndadh"), "tionndaidh")

if __name__ == '__main__':
    unittest.main()
