import unittest

from gaelic_pos import GaelicTokeniser
from gaelic_pos import postagger
from checker import Checker

class Test(unittest.TestCase):
    def setUp(self):
        self.t = GaelicTokeniser.Tokeniser()
        self.p = postagger.PosTagger()
        self.c = Checker()

    def tearDown(self):
        self.t = None
        self.f = None
        self.c = None

    def test_integration(self):
        text = "Bha cuimhn' aige air Uilleam o'n a bha e 'n Glaschu: duine mór socair, sàmhach."
        tokens = self.t.tokenise(text)
        result = self.p.tagfile_default(tokens)
        expected = [('Bha', 'V-s'), ("cuimhn'", 'Ncsfn'), ('aige', 'Pr3sm'), ('air', 'Sp'), ('Uilleam', 'Nn-md'), ("o'n", 'Q--s'), ('a', 'Q-r'), ('bha', 'V-s'), ('e', 'Pp3sm'), ("'n", 'Sp'), ('Glaschu', 'Nt'), (':', 'Fi'), ('duine', 'Ncsmn'), ('mór', 'Rg'), ('socair', 'Ncsfn'), (',', 'Fi'), ('sàmhach', 'Ap'), ('.', 'Fe')]
        self.assertEqual(result,expected)
        checked = self.c._check(result)
        for check in checked:
            print(check)
        codes = [t[2] for t in checked]
        self.assertTrue('GOC' in codes)

if __name__ == '__main__':
    unittest.main()

