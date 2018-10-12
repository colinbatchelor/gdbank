import numpy as np
import unittest

from dataframes import Frame
from checker import Checker

class Test(unittest.TestCase):
    def setUp(self):
        self.f = Frame()
        self.c = Checker()

    def tearDown(self):
        self.f = None

    def testBasic(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.f.make(good_iomadh)
        self.assertEqual(3, len(result))

    def testMo(self):
        good = [("dhùin","V-s"),("mi","Pp1s"),("mo","Dp1s"),("shùilean","Ncpfn"),("san","Spa-s"),("deireadh","Ncsmd")]
        result = self.c._check(good)
        bad = [("dhùin","V-s"),("mi","Pp1s"),("mo","Dp1s"),("sùilean","Ncpfn"),("san","Spa-s"),("deireadh","Ncsmd")]
        r2 = self.c._check(bad)
        print(r2)
        
    def testFeats(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.f.feats(self.f.make(good_iomadh))
        self.assertEqual(np.dtype(bool), np.dtype(result._lenited))
        br = [("barrachd", "Ncsmn"), ("fiosrachaidh", "Ncsmg")]
        r2 = self.f.feats(self.f.make(br))
        self.assertEqual(np.dtype(bool), np.dtype(r2._genitive))
        self.assertListEqual([False, True], r2._genitive.tolist())
        self.assertListEqual([False, True], r2._genitivesing.tolist())
        self.assertListEqual([True, True], r2._sing.tolist())

    def testCheckerDfs(self):
        self.assertEqual(np.dtype(object), np.dtype(self.c.lenitesp_1._p_1))
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.f.feats(self.f.make(good_iomadh))
        merged = result.merge(self.c.lenitesp_1, on = ("_p_1","_lenited"), how="left")
        print(merged)

if __name__ == '__main__':
    unittest.main()

