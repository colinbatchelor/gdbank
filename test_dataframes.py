import unittest

from dataframes import Frame

class Test(unittest.TestCase):
    def setUp(self):
        self.f = Frame()

    def tearDown(self):
        self.f = None

    def testBasic(self):
        good_iomadh = [("'S", "Wp-i"), ("iomadh","Ar"), ("rud","Ncsmn")]
        result = self.f.make(good_iomadh)
        self.assertEqual(3, len(result))
        print(result.dtypes)

if __name__ == '__main__':
    unittest.main()

