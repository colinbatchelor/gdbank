import unittest

from GaelicTokeniser import Tokeniser
from postagger import PosTagger

class Test(unittest.TestCase):
    def setUp(self):
        self.t = Tokeniser()
        self.p = PosTagger()

    def tearDown(self):
        self.t = None
        self.f = None

    def test_integration(self):
        text = "Bha cuimhn' aige air Uilleam o'n a bha e 'n Glaschu: duine mór socair, sàmhach."
        tokens = self.t.tokenise(text)
        result = self.p.tagfile_default(tokens)
        expected = [('Bha', 'V-s'), ("cuimhn'", 'Ncsfn'), ('aige', 'Pr3sm'), ('air', 'Sp'), ('Uilleam', 'Nn-md'), ("o'n", 'Q--s'), ('a', 'Q-r'), ('bha', 'V-s'), ('e', 'Pp3sm'), ("'n", 'Sp'), ('Glaschu', 'Nt'), (':', 'Fi'), ('duine', 'Ncsmn'), ('mór', 'Rg'), ('socair', 'Ncsfn'), (',', 'Fi'), ('sàmhach', 'Ap'), ('.', 'Fe')]
        self.assertEqual(result,expected)

if __name__ == '__main__':
    unittest.main()

