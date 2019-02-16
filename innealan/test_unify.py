import unittest
import unify

class TestFeatures(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unify(self):
        nom = unify.unify(("an","Tdsm"), ("sàbhaladh","Ncsmn"))
        gen = unify.unify(("nan","Tdpmg"),("rabhaidhean","Ncpmg"))
        self.assertEqual("Nom", nom["Case"])
        self.assertEqual("Gen", gen["Case"])

if __name__ == '__main__':
    unittest.main()

