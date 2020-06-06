import unittest
from acainn import CCGRetagger, CCGTyper, Features, Lemmatizer, Subcat

# checks that all the labels actually match
class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.r = CCGRetagger()
        self.s = Subcat()
        self.t = CCGTyper()

    def tearDown(self):
        self.r = None
        self.s = None
        self.t = None

    def test_retagger(self):
        specialtags = set()
        for key in self.r.retaggings:
            tag = self.r.retaggings[key]
            self.assertTrue(tag in self.t.types.keys())

    def test_subcat(self):
        for key in self.s.mappings:
            for item in self.s.mappings[key]:
                self.assertTrue(item in self.t.types.keys(), item)

class TestFeatures(unittest.TestCase):
    def setUp(self):
        self.f = Features()

    def tearDown(self):
        self.f = None

    def test_feats_adj(self):
        self.assertEqual({}, self.f.feats_adj('Ap'))
        self.assertEqual({'Degree':['Cmp,Sup']}, self.f.feats_adj('Apc'))

    def test_feats_det(self):
        self.assertEqual({'Gender':['Masc'],'Number':['Sing']},
                         self.f.feats_det('Tdsm'))
        self.assertEqual({'Gender':['Fem'],'Number':['Sing']},
                         self.f.feats_det('Tdsf'))
        self.assertEqual({'Gender':['Masc'],'Number':['Plur']},
                         self.f.feats_det('Tdpm'))
        self.assertEqual({'Case':['Gen'],'Gender':['Fem'], 'Number':['Plur']},
                         self.f.feats_det('Tdpfg'))

    def test_feats_noun(self):
        self.assertEqual({'Case':['Nom'],'Gender':['Masc'],'Number':['Sing']},
                         self.f.feats_noun('Ncsmn'))
        self.assertEqual({'Case':['Dat'],'Gender':['Fem'],'Number':['Plur']},
                         self.f.feats_noun('Ncpfd'))
        self.assertEqual({'Case':['Gen'],'Gender':['Fem'],'Number':['Plur']},
                         self.f.feats_noun('Ncpfg'))

class TestCCGTyper(unittest.TestCase):
    def setUp(self):
        self.t = CCGTyper()

    def tearDown(self):
        self.t = None

    def test(self):
        self.assertEqual(self.t.type("tha", "V-p", "BIPP")[1],
                         "s[dcl pres cons]/pp/n")
        self.assertEqual(self.t.type("bha", "V-s", "BIPP")[1],
                         "s[dcl past cons]/pp/n")

class TestCCGRetagger(unittest.TestCase):
    def setUp(self):
        self.r = CCGRetagger()

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

    def comparative(self, comparative, lemma):
        self.assertEqual(self.l.lemmatize(comparative, "Apc"), lemma)

    def second_comparative(self, comparative, lemma):
        self.assertEqual(self.l.lemmatize(comparative, "Aps"), lemma)

    def test_adjectives(self):
        self.assertEqual(self.l.lemmatize("Mhòir", "Aq-smg"), "mòr")

    def test_comparatives(self):
        self.comparative("àille", "àlainn")
        self.comparative("àirde", "àrd")
        self.comparative("aotruime", "aotrom")
        self.comparative("bige", "beag")
        self.comparative("caime", "cam")
        self.comparative("comasaiche", "comasach")
        self.comparative("cudromaiche", "cudromach")
        self.comparative("dealasaich", "dealasach")
        self.comparative("dhorcha", "dorcha")
        self.comparative("dlùithe", "dlùth")
        self.comparative("duirche", "dorcha")
        self.comparative("fhaide", "fada")
        self.comparative("fhaid'", "fada")
        self.comparative("fhaisge", "faisg")
        self.comparative("fhaisg'", "faisg")
        self.comparative("fhasa", "furasta")
        self.comparative("fhèarr", "math")
        self.comparative("fhearr", "math")
        self.comparative("fheàrr", "math")
        self.comparative("fuaire", "fuar")
        self.comparative("iomchaidhe", "iomchaidh")
        self.comparative("ìsle", "ìosal")
        self.comparative("leatha", "leathann")
        self.comparative("luaithe", "luath")
        self.comparative("lugha", "beag")
        self.comparative("mheasaile", "measail")
        self.comparative("mhò", "mòr")
        self.comparative("mhuth'", "mòr")
        self.comparative("miona", "mion")
        self.comparative("miosa", "dona")
        self.comparative("òige", "òg")
        self.comparative("nitheile", "nitheil")
        self.comparative("righne", "righinn")
        self.comparative("righinne", "righinn")
        self.comparative("shaoire", "saor")
        self.comparative("shine", "sean")
        self.comparative("sine", "sean")
        self.comparative("tràithe", "tràth")
        self.comparative("trice", "tric")
        self.second_comparative("fheàirrde", "math")
        self.second_comparative("mhisde", "dona")

    def test_nouns(self):
        self.assertEqual(self.l.lemmatize("athar", "Ncsmg"), "athair")
        self.assertEqual(self.l.lemmatize("bhalaich", "Ncsmv"), "balach")
        self.assertEqual(self.l.lemmatize("bàt’", "Ncsmn"), "bàta")
        self.assertEqual(self.l.lemmatize("bheachd-san", "Ncsmd"), "beachd")
        self.assertEqual(self.l.lemmatize("bhliadhn'", "Ncsfn"), "bliadhna")
        self.assertEqual(self.l.lemmatize("bhliadhna", "Ncsfn"), "bliadhna")
        self.assertEqual(self.l.lemmatize("bhòrd", "Ncsmd"), "bòrd")
        self.assertEqual(self.l.lemmatize("bhùird", "Ncsmg"), "bòrd")
        self.assertEqual(self.l.lemmatize("bhruaich", "Ncsfd"), "bruach")
        self.assertEqual(self.l.lemmatize("chinn", "Ncsmg"), "ceann")
        self.assertEqual(self.l.lemmatize("chnuic", "Ncsmg"), "cnoc")
        self.assertEqual(self.l.lemmatize("choin", "Ncsmd"), "cù")
        self.assertEqual(self.l.lemmatize("chois", "Ncsfd"), "cas")
        self.assertEqual(self.l.lemmatize("chor", "Ncsmn"), "cor")
        self.assertEqual(self.l.lemmatize("doruis", "Ncsmg"), "dorus")
        self.assertEqual(self.l.lemmatize("èisg", "Ncsmg"), "iasg")
        self.assertEqual(self.l.lemmatize("fhacal", "Ncsmd"), "facal")
        self.assertEqual(self.l.lemmatize("fhèithe", "Ncsfg"), "fèith")
        self.assertEqual(self.l.lemmatize("gill'", "Ncsfn"), "gille")
        self.assertEqual(self.l.lemmatize("h-ainm", "Ncsmd"), "ainm")
        self.assertEqual(self.l.lemmatize("'ill'", "Ncsmv"), "gille")
        self.assertEqual(self.l.lemmatize("'ille", "Ncsmv"), "gille")
        self.assertEqual(self.l.lemmatize("mhàthair", "Ncsfv"), "màthair")
        self.assertEqual(self.l.lemmatize("Mic", "Nn"), "mac")
        self.assertEqual(self.l.lemmatize("mhic", "Ncsmg"), "mac")
        self.assertEqual(self.l.lemmatize("mhòintich", "Ncsfd"), "mòinteach")
        self.assertEqual(self.l.lemmatize("mhuir", "Ncsmd"), "muir")
        self.assertEqual(self.l.lemmatize("dh’oidhcheannan", "Ncpfd"),
                         "oidhche")
        self.assertEqual(self.l.lemmatize("peantairean", "Ncpmn"), "peantair")
        self.assertEqual(self.l.lemmatize("sanas", "Ncsmn"), "sanas")
        self.assertEqual(self.l.lemmatize("sanais", "Ncsfn"), "sanais")
        self.assertEqual(self.l.lemmatize("seilich", "Ncsmg"), "seileach")
        self.assertEqual(self.l.lemmatize("sheòid", "Ncsmv"), "seud")
        self.assertEqual(self.l.lemmatize("taighe", "Ncsmg"), "taigh")
        self.assertEqual(self.l.lemmatize("t-samhradh", "Ncsmd"), "samhradh")
        self.assertEqual(self.l.lemmatize("t-sead", "Ncsmd"), "sead")
        self.assertEqual(self.l.lemmatize("uamha", "Ncsfd"), "uamh")
        self.assertEqual(self.l.lemmatize("uinneig", "Ncsfd"), "uinneag")

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
        self.assertEqual(self.l.lemmatize("thug", "V-s"), "toir")
        self.assertEqual(self.l.lemmatize("tug", "V-s--d"), "toir")
        self.assertEqual(self.l.lemmatize("bheir", "V-f"), "toir")
        self.assertEqual(self.l.lemmatize("thoirt", "Nv"), "toir")
        self.assertEqual(self.l.lemmatize("toirt", "Nv"), "toir")

    def test_pronouns(self):
        self.assertEqual(self.l.lemmatize("fhèin","Px"), "fèin")

    def test_particles(self):
        self.assertEqual(self.l.lemmatize("d’", "Q--s"), "do")

    def test_prefixes(self):
        self.assertEqual(self.l.lemmatize("h-Alba", "Nt"), "Alba")
        self.assertEqual(self.l.lemmatize("dh’aon", "Mc"), "aon")
        self.assertEqual(self.l.lemmatize("n-eachdraidh", "Ncsfd"),
                         "eachdraidh")
        self.assertEqual(self.l.lemmatize("t-seòrsa", "Ncsmd"), "seòrsa")

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

    def preposition(self, preposition, root):
        self.assertEqual(self.l.lemmatize_preposition(preposition), root)

    def test_prepositions(self):
        self.preposition("a'd", 'aig')
        self.preposition('oirre','air')
        self.preposition('airson','airson')
        self.preposition('anns','an')
        self.preposition('uam','bho')
        self.preposition('am','an')
        self.preposition('anns an','an')
        self.preposition('agam','aig')
        self.preposition('dhi','do')
        self.preposition('dhuinn','do')
        self.preposition('dhaibh','do')
        self.preposition('dhe', 'de')
        self.preposition('dhen','de')
        self.preposition('dhiom','de')
        self.preposition('dheth','de')
        self.preposition('dhith','de')
        self.preposition('dhinn','de')
        self.preposition('dhibh','de')
        self.preposition('dhiubh','de')
        self.preposition('dhomhsa', 'do')
        self.preposition("dhomh-s'", "do")
        self.preposition('dhut', 'do')
        self.preposition('fon','fo')
        self.preposition('fodha','fo')
        self.preposition('foidhpe','fo')
        self.preposition('rium','ri')
        self.preposition('ris','ri')
        self.preposition('ruinn','ri')
        self.preposition('ruibh','ri')
        self.preposition('ron','ro')
        self.preposition('tharad','thar')
        self.preposition('thairis','thar')
        self.preposition('leam','le')
        self.preposition('leis','le')
        self.preposition('leibh','le')
        self.preposition('leotha','le')
        self.preposition('eatorra','eadar')
        self.preposition('innte','an')
        self.preposition('asam','as')
        self.preposition('aiste','as')

    def nv(self, vn, root):
        self.assertEqual(self.l.lemmatize_vn(vn), root)

    def test_nvs(self):
        self.nv('aithris', 'aithris')
        self.nv('amas', 'amais')
        self.nv('amharc', 'amhairc')
        self.nv('agairt', 'agair')
        self.nv("àrdachadh", "àrdaich")
        self.nv('at','at')
        self.nv('bagairt', 'bagair')
        self.nv('baisteadh', 'baist')
        self.nv("beantainn","bean")
        self.nv('beucaich', 'beuc')
        self.nv('beucail', 'beuc')
        self.nv('bhith', 'bi')
        self.nv('blasad', 'blais')
        self.nv('blasadh', 'blais')
        self.nv('bleith', 'bleith')
        self.nv("bleoghan", "bleoghain")
        self.nv('breith', 'beir')
        self.nv('brìodal', 'brìodail')
        self.nv('briseadh', 'bris')
        self.nv('bristeadh', 'bris')
        self.nv('bruich', 'bruich')
        self.nv("bruidhinn", "bruidhinn")
        self.nv('bruthadh', 'brùth')
        self.nv('bualadh', 'buail')
        self.nv('bùirich', 'bùir')
        self.nv('buntainn', 'buin')
        self.nv('cadal', 'caidil')
        self.nv('cantail', 'can')
        self.nv("cantainn", "can")
        self.nv('call', 'caill')
        self.nv("caoidh", "caoidh")
        self.nv("cinntinn", "cinn")
        self.nv("cagar", "cagair")
        self.nv("cagarsaich", "cagair")
        self.nv("cagartaich", "cagair")
        self.nv('caitheamh', 'caith')
        self.nv('canail', 'can')
        self.nv("càradh", "càirich")
        self.nv("casgairt", "casgair")
        self.nv("casgradh", "casgair")
        self.nv("ceangal", "ceangail")
        self.nv('ceannach', 'ceannaich')
        self.nv("ceiltinn", "ceil")
        self.nv('ciallachadh', 'ciallaich')
        self.nv("cinntinn", "cinn")
        self.nv("coimhead", "coimhead")
        self.nv('coinneachadh', 'coinnich')
        self.nv('coiseachd', 'coisich')
        self.nv("cosnadh", "coisinn")
        self.nv("cur", "cuir")
        self.nv("chur", "cuir")
        self.nv('cluich', 'cluich')
        self.nv("cluiche", "cluich")
        self.nv("cluinntinn", "cluinn")
        self.nv("creidsinn", "creid")
        self.nv('cuideachadh', 'cuidich')
        self.nv("cumail", "cùm")
        self.nv('dèanamh', 'dèan')
        self.nv("dearmad", "dearmad")
        self.nv("dìobairt", "dìobair")
        self.nv("dìon", "dìon")
        self.nv("dìreadh", "dìrich")
        self.nv('dòrtadh', 'dòirt')
        self.nv("dol", "rach")
        self.nv('dùnadh', 'dùin')
        self.nv('dùsgadh', 'dùisg')
        self.nv("èigheachd", "èigh")
        self.nv("èirigh", "èirich")
        self.nv("èisteachd", "èist")
        self.nv("fàgail", "fàg")
        self.nv('faicinn', 'faic')
        self.nv("faicsinn","faic")
        self.nv('faighinn', 'faigh')
        self.nv('faighneachd', 'faighnich')
        self.nv('faireachadh', 'fairich')
        self.nv("faireachdainn", "fairich")
        self.nv("fàsgadh", "fàisg")
        self.nv("falbh", "falbh")
        self.nv('fanmhainn', 'fan')
        self.nv('fantail', 'fan')
        self.nv("fantainn", "fan")
        self.nv("faotainn", "faod")
        self.nv('feitheamh', 'feith')
        self.nv("fàs", "fàs")
        self.nv("feuchainn", "feuch")
        self.nv("feumachdainn", "feum")
        self.nv("fhalbh", "falbh")
        self.nv("fògairt", "fògair")
        self.nv('fògradh', 'fògair')
        self.nv('fosgladh', 'fosgail')
        self.nv("freagairt", "freagair")
        self.nv('freagradh', 'freagair')
        self.nv('fuaigheal', 'fuaigh')
        self.nv('fuine', 'fuin')
        self.nv("fuireach", "fuirich")
        self.nv('fulang', 'fuiling')
        self.nv("gabhail", "gabh")
        self.nv("gàireachdaich", "gàir")
        self.nv("gàireachdainn", "gàir")
        self.nv("gairm", "gairm")
        self.nv("gealltainn", "geall")
        self.nv('gearan', 'gearain')
        self.nv('geàrradh','geàrr')
        self.nv('gineamhainn', 'gin')
        self.nv("gintinn", "gin")
        self.nv('glaodhaich', 'glaodh')
        self.nv('gleadhraich', 'gleadhar')
        self.nv("gluasad", "gluais")
        self.nv("goid", "goid")
        self.nv('greasadh', 'greas')
        self.nv("greastainn", "greas")
        self.nv('guidhe', 'guidh')
        self.nv('gul', 'guil')
        self.nv("iarraidh", "iarr")
        self.nv('iasgach', 'iasgaich')
        self.nv('imeachd', 'imich')
        self.nv("innse", "inns")
        self.nv("iomain", "iomain")
        self.nv("iomairt", "iomair")
        self.nv('iomramh', 'iomair')
        self.nv("ionndrainn", "ionndrainn")
        self.nv("ithe", "ith")
        self.nv("labhairt", "labhair")
        self.nv('lagachadh', 'lagaich')
        self.nv("laighe", "laigh")
        self.nv('leagail', 'leag')
        self.nv('leanmhainn', 'lean')
        self.nv('leantail', 'lean')
        self.nv("leantainn", "lean")
        self.nv("leigeil", "leig")
        self.nv("leigheas", "leighis")
        self.nv("leughadh", "leugh")
        self.nv("leum", "leum")
        self.nv("lìonadh", "lìon")
        self.nv('losgadh', 'loisg')
        self.nv('luasgadh', 'luaisg')
        self.nv("maireachdainn", "mair")
        self.nv("mairsinn", "mair")
        self.nv('marcachd', 'marcaich')
        self.nv("mealtainn", "meal")
        self.nv("meas", "meas")
        self.nv("moladh", "mol")
        self.nv('mothachadh', 'mothaich')
        self.nv('nasgadh', 'naisg')
        self.nv('nighe', 'nigh')
        self.nv("obair", "obraich")
        self.nv('obrachadh', 'obraich')
        self.nv("òl", "òl")
        self.nv('pasgadh', 'paisg')
        self.nv("pòsadh", "pòs")
        self.nv("ràdh", "abair")
        self.nv("rànaich", "ràn")
        self.nv("rànail", "ràn")
        self.nv('rannsachadh', 'rannsaich')
        self.nv("reic", "reic")
        self.nv("ruigheachd", "ruig")
        self.nv("ruighinn", "ruig")
        self.nv("ruigsinn", "ruig")
        self.nv("ruith", "ruith")
        self.nv("saltairt", "saltair")
        self.nv("saoilsinn", "saoil")
        self.nv("sealltainn", "seall")
        self.nv('seasamh', 'seas')
        self.nv("seinn", "seinn")
        self.nv("sgrìobhadh", "sgrìobh")
        self.nv("sgur", "sguir")
        self.nv("sìoladh", "sìolaidh")
        self.nv("siubhal", "siubhail")
        self.nv("smaoineachadh", "smaoinich")
        self.nv('smuaineachadh', 'smuainich')
        self.nv("snàmh", "snàmh")
        self.nv("snìomh", "snìomh")
        self.nv('srannail', 'srann')
        self.nv("sreap", "sreap")
        self.nv('suidhe', 'suidh')
        self.nv("tabhairt", "tabhair")
        self.nv("tachairt", "tachair")
        self.nv("tadhal", "tadhail")
        self.nv("tagairt", "tagair")
        self.nv('tagradh', 'tagair')
        self.nv("tairgsinn", "tairg")
        self.nv("tarraing", "tarraing")
        self.nv("teagasg", "teagaisg")
        self.nv('teasairginn', 'teasairg')
        self.nv("tighinn", "thig")
        self.nv('tilgeil', 'tilg')
        self.nv("tilleadh", "till")
        self.nv('tiodhlacadh', 'tiodhlaic')
        self.nv("tional", "tionail")
        self.nv('togail', 'tog')
        self.nv("togairt", "togair")
        self.nv('togradh', 'togair')
        self.nv("toirt", "toir")
        self.nv("tòiseachadh", "tòisich")
        self.nv("tionndadh", "tionndaidh")
        self.nv("triall", "triall")
        self.nv("trod", "trod")
        self.nv("trusadh", "trus")
        self.nv("tuigsinn", "tuig")
        self.nv("tuiteam", "tuit")

if __name__ == '__main__':
    unittest.main()
