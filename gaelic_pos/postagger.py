#from nltk.tag import brill
import os
import pickle
import re

class PosTagger():
    def __init__(self):
        self.datadir = os.path.join(os.getcwd(), "Data")
        self.modeldir = os.path.join(os.getcwd(), "Model")
        self.defaultFN = os.path.join(self.modeldir, "DefaultModel_310516.pkl")  # trained on 117,381 manually-tagged tokens
        self.simplifiedFN = os.path.join(self.modeldir, "SimplifiedModel_010616.pkl")  # trained on 117,381 manually-tagged tokens
        self.englishLexicon = []
        with open(os.path.join(self.datadir, "EnglishLexiconFinal11062015.csv")) as f:  # list of English words
            for line in f:
                self.englishLexicon.append(line.strip())

    def _load_defaultmodel(self):
        with open(self.defaultFN, "rb") as dModel:
            model = pickle.load(dModel)
        return model

    def _load_simplifiedmodel(self):
        with open(self.simplifiedFN, "rb") as sModel:
            model = pickle.load(sModel)
        return model

    def _retag(self, algT, algV):
        Sp = ["Spp3sm", "Spp3sf", "Spp3p", "Spp1s", "Spa-s", "Spa-p", "Spa", "Sp"]  # removed 'Spv' (verbal part) from list

        for x, b in enumerate(algV):
            Nouncasesd = re.findall(r"(\bN+.*d\b)", str(b))
            Nouncasesn = re.findall(r"(\bN+.*n\b)", str(b))
            Nouncasesg = re.findall(r"(\bN+.*g\b)", str(b))

            temp = []
            temp2 = []

            temp.append(''.join(algV[x - 1]))
            temp.append(''.join(algV[x - 2]))
            temp.append(''.join(algV[x - 3]))

            tp = (set(temp) & set(Sp))

            if (Nouncasesd and not tp):
                nc = ''.join(Nouncasesd)
                cc = re.findall(r"\S", str(nc))
                cca = cc[:len(cc) - 1]
                cca.extend('n')
                algV[y] = ''.join(cca)

            if (Nouncasesg and not tp):
                ng = ''.join(Nouncasesg)
                cc = re.findall(r"\S", str(ng))
                cca = cc[:len(cc) - 1]
                cca.extend('d')
                algV[y] = ''.join(cca)

            if ''.join(b) == 'Sp' and 'Ug' in algV[:3]:
                algV[y] = 'Sa'

        for y, token in enumerate(algT):
            tag = algV[y]
            for d in self.englishLexicon:
                if str(d).lower() == token and token not in ['air', 'shine', 'gun', 'sin', 'far', 'fear', 'a', 'can', 'coin'] and tag != 'Xfe':
                    algV[y] = 'Xfe'

            Verbcases = ''.join(re.findall(r"(\bV+.*\b)", str(b)))
            Wcases = ''.join(re.findall(r"(\bW+.*\b)", str(b)))
            if str(token) in ['Sann', 'sann', "'sann"]:
                algV[y] = 'Wp-i-x'
                        
            if tag == 'Sap3sf' and ''.join(algT[y + 1][:2])[1] == "h":
                algV[y] = 'Sap3sm'

            if tag == 'Sap3sm' and ''.join(algT[y + 1][:2])[1] != "h":
                algV[y] = 'Sap3sf'

            if tag == 'Sap3sm' and ''.join(algT[y + 1][:1]) == 'h-':
                algV[y] = 'Sap3sf'

            if token == "an" and ''.join(algT[y + 1]) == 'sàs':
                algV[y] = 'Sp'
                algV[y + 1] = 'Ncsmd'

            if token in ["nam", "nan"] and ''.join(algV[y + 1]) == Verbcases:
                algV[y] = 'Q-s'

            if token == 'a' and ''.join(algV[y + 1]) == Verbcases:
                algV[y] = 'Q-r'

            if token == 'na' and ''.join(algV[y - 1]) == "Sp":
                algV[y] = 'Tdpm'

            if token == 'am' and ''.join(algV[y]) != "Tdsm":
                algV[y] = 'Tdsm'

            if token in ["gum", "gun", "gu"] and ''.join(algV[x + 1]) in [Verbcases, Wcases]:
                algV[y] = 'Qa'

            if tag == 'Dp3sf' and ''.join(algT[y + 1][:2]) in ['ph', 'bh', 'ch', 'th', 'dh', 'mh', 'sh', 'fh']:
                algV[y] = 'Dp3sm'

            unlenited = ['pa','pe','pi','po','pu','pl','pm','pn',
                         'ba','be','bi','bo','bu','bl','bm','bn',
                         'ca','ce','ci','co','cu','cl','cm','cn',
                         'ga','ge','gi','go','gu','gl','gm','gn',
                         'ta','te','ti','to','tu','tl','tm','tn',
                         'da','de','di','do','du','dl','dm','dn',
                         'ma','me','mi','mo','mu','ml','mm','mn',
                         'sa','se','si','so','su','sl','sm','sn',
                         'fa','fe','fi','fo','fu','fl','fm','fn']
                
            if tag == 'Dp3sm' and ''.join(algT[y + 1][:2]) in unlenited:
                algV[y] = 'Dp3sf'

            if tag == 'Dp3sm' and ''.join(algT[y + 1][:1]) == 'h-':
                algV[y] = 'Dp3sf'

            if tag == 'Spp3sf' and ''.join(algT[y + 1][:2]) in ['ph', 'bh', 'ch', 'th', 'dh', 'mh', 'sh', 'fh']:
                algV[y] = 'Spp3sm'

            if tag == 'Spp3sm' and ''.join(algT[y + 1][:2]) in unlenited:
                algV[y] = 'Spp3sf'

            if tag == 'Spp3sm' and ''.join(algT[y + 1][:1]) == 'h-':
                algV[y] = 'Spp3sf'
            digits = ['0','1','2','3','4','5','6','7','8','9']

            if tag != 'Mn' and ''.join(algT[y][:1]) in digits and ''.join(algT[y][len(algT[y]) - 1:]) in digits:
                algV[y] = 'Mn'

            if tag != 'Mn' and ''.join(algT[y][:1]) in digits and ''.join(algT[y][len(algT[y]) - 2:]) in ['an']:
                algV[y] = 'Mn'

            if tag != 'Mo' and ''.join(algT[y][:1]) in digits and ''.join(algT[y][len(algT[y]) - 2:]) in ['mh']:
                algV[y] = 'Mo'

            if tag != 'Fb' and ''.join(algT[y]) == '—':
                algV[y] = 'Fb'

        taggerFile = list(zip(algT, algV))
        return taggerFile
    
    def tagfile_default(self, tokens):
        """Uses default, morphologically detailed tag set (246 tags)"""
        algT = []
        algV = []
        defmodel = self._load_defaultmodel()
        BrillTag = defmodel.tag(tokens)
        for (c, d) in BrillTag:  # algorithm output
            algT.append(c)
            algV.append(d)
        return self._retag(algT, algV)
            
