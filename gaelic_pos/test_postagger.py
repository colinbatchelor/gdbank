import unittest

from postagger import PosTagger

class Test(unittest.TestCase):
    def setUp(self):
        self.tagger = PosTagger()

    def tearDown(self):
        self.tagger = None

    def test_basic(self):
        self.assertEqual(self.tagger._retag(["tha", "mi", "a'", "dol", "dhachaigh"], ["V-p", "Pp1s", "Sp", "Nv", "Rs"]), [("tha","V-p"),("mi","Pp1s"),("a'","Sp"),("dol","Nv"),("dhachaigh","Rs")])
        
if __name__ == '__main__':
    unittest.main()
