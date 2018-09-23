import unittest

from checker import Checker

class Test(unittest.TestCase):
    def setUp(self):
        self.c = Checker()

    def tearDown(self):
        self.c = None

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
        for t in checked:
            print(t)
       
if __name__ == '__main__':
    unittest.main()
