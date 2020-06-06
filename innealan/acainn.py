import os
import pandas as pd
import re
import csv

class Lemmatizer:
    def __init__(self):
        self.irregulars = [
            ('bi', ['tha', 'bha', 'robh', 'eil', 'bheil', 'bith', 'bhith',
                    "bh'", "bhà", "thà", "th'", 'bhios', 'bidh', 'biodh',
                    'bhiodh', "'eil", "bhithinn", "bhitheadh", "bitheamaid",
                    "thathas", "thathar", "robhar"]),
            ('arsa', ["ars'", "ar", "ars", "as"]),
            ('abair', ['ràdh', 'thuirt', 'their', 'theirear']),
            ('beir', ['breith', 'bhreith', 'rug', 'beiridh']),
            ('cluinn', ['cluinntinn', 'chluinntinn', 'cuala', "cual'",
                        'chuala', 'cluinnidh']),
            ('rach', ['chaidh', 'dol', 'dhol', 'thèid', 'tèid', "deach"]),
            ('dèan', ['rinn', 'dèanamh', 'dhèanamh', 'nì']),
            ('faic', ['chunnaic', 'chunna', 'faicinn', 'fhaicinn', 'chì',
                      'chithear', 'chitheadh', 'fhaca', 'faca']),
            ('faigh', ['faighinn', 'fhaighinn', 'fhuair', 'gheibh',
                       'gheibhear']),
            ('ruig', ['ruigsinn', 'ràinig', 'ruigidh']),
            ('toir', ['toirt', 'thoirt', 'thug', 'bheir', 'bheirear', 'tug']),
            ('thig', ['tighinn', 'thighinn', 'thàinig', 'thig', 'tig',
                      'tàinig', 'dàinig'])]
        self.prepositions = {
            'aig':["aga(m|t|inn|ibh)|aige|aice|aca"],
            'air':["or[mt]|oir(re|bh|nn)|orra"],
            'airson':["'?son"],
            'an':["'?s?a[mn]", "sa", "'?na", "anns?_a[nm]", "innte", "a's"],
            'as':["às", "as.*", "ais.*"],
            'bho':["(bh)?o", "(bh)?ua(m|t)"],
            'eadar':["ea.*"],
            'fo':["fo.*"],
            'gu':["gu_ruige"],
            'de':["dh(en?|iom|[ei]th|inn|iu?bh)"],
            'do':["dh(omh|i|ut|uinn|an?|[au]ib[h'])(-?s['a]?)?"],
            'le':["le.*"],
            'ri':["ri(um|ut|s)", "ru.*"],
            'ro':["ro.*"],
            'thar':["tha.*"]
        }
        self.pronouns = {
            "mi": ["mise"], "thu": ["tu", "tusa", "thusa"],
            "e": ["esan"], "i": ["ise"],
            "sinn": ["sinne"], "sibh": ["sibhse"], "iad": ["iadsan"]
            }
        dir = os.path.dirname(__file__)
        vn_path = os.path.join(dir, 'resources', 'vns.csv')
        self.vns = []
        with open(vn_path) as f:
            reader = csv.reader(f)
            for row in reader:
                self.vns.append((row[0], row[1].split(";")))

    def can_follow_de(self, s):
        return s in ["cho","am","an","a'", "na","mar","bha", "tha"]

    def lenited(self, s):
        unlenitable = re.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]", s)
        return bool(unlenitable) | (s[1] == 'h')

    def lenited_pd(self, s):
        unlenitable = s.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]")
        return unlenitable | (s[1] == 'h')

    def chalenited_pd(self, s):
        unlenitable = s.match(r"[AEIOUaeiouLlNnRrDTSdts]")
        return unlenitable | (s[1] == 'h')

    def ndlenited_pd(self, s):
        unlenitable = s.match(r"[AEIOUaeiouDdTtNnRrSs]")
        return unlenitable | (s[1] == 'h')

    def delenite(self, s):
        if len(s) < 2: return s
        return s[0] + s[2:] if s[1] == 'h' else s

    def lemmatize_preposition(self, s):
        s = s.replace(' ','_')
        if not re.match("^'?san$", s): s = re.sub('-?san$','',s)
        for key in self.prepositions:
            for pattern in self.prepositions[key]:
                if re.match("^("+pattern+")$", s): return key
        return s

    def lemmatize_pronoun(self, s):
        for key in self.pronouns:
            if s in self.pronouns[key]:
                return key
        return s

    def lemmatize_vn(self, s):
        for vn in self.vns:
            if self.delenite(s) in vn[1]:
                return vn[0]
        replacements = [
            ('sinn', ''), ('tail', ''), ('ail', ''), ('eil', ''), ('eal', ''),
            ('aich', ''), ('ich', ''), ('tainn', ''), ('tinn', ''),
            ('eamh', ''), ('amh', ''),
            ('eamhainn', ''), ('mhainn', ''), ('inn', ''),
            ('eachadh', 'ich'), ('achadh', 'aich'), ('airt', 'air'),
            ('gladh', 'gail'), ('eadh', ''), ('adh', ''), ('e', ''),
            ('eachd', 'ich'), ('achd', 'aich')
        ]
        for replacement in replacements:
            if s.endswith(replacement[0]):
                return self.delenite(s.replace(replacement[0], replacement[1]))
        return self.delenite(s)

    def lemmatize_adjective(self, s):
        s = self.delenite(s)
        if s.endswith("ir"): return re.sub("ir$", "r", s)
        return s

    def remove_apostrophe(self, s):
        result = re.sub("'$", "", s)
        stem = re.sub("[bcdfghlmnprst]+'$", "", s)
        if re.match(".*[aouàòù]$", stem):
            return "%sa" % result
        else:
            return "%se" % result

    def lemmatize_n(self, s, pos):
        demonyms = {
            "Albannaich":"Albannach", "Basgaich":"Basgach",
            "Beàrnaraich":"Beàrnarach", "Beàrnaraich":"Beàrnaraich",
            "Breatannaich":"Breatannach",
            "Caimbeulaich":"Caimbeulach",
            "Deamaich":"Deamach",
            "Èireannaich":"Èireannach",
            "Gàidheil": "Gàidheal",
            "Gaidheil": "Gaidheal", "Nàiseantaich":"Nàiseantach",
            "Sasannaich": "Sasannach", "Tearaich":"Tearach",
            "Uibhistich": "Uibhisteach"}
        specials = {
            "aodainn":"aodann", "ainmeannan":"ainm",
            "bailtean":"baile", "bàtaichean": "bàta", "beanntan":"beinn",
            "beathaichean":"beathach",
            "bilean":"bile",
            "bliadhnaichean":"bliadhna",
            "buidheannan":"buidheann", "buill":"ball",
            "busaichean":"bus",
            "choin":"cù",
            "còirichean":"còir",
            "daoine":"duine", "drugaichean":"druga",
            "ealain":"ealan", "eich":"each", "eileanan":"eilean",
            "facail":"facal",
            "faclan":"facal",
            "fiaclan":"fiacal",
            "fir":"fear", "fuinn":"fonn",
            "gillean":"gille",
            "làithean":"làtha", "linntean":"linn",
            "notaichean":"not",
            "obraichean":"obair",
            "òran":"òran",
            "paraistean":"paraiste",
            "planaichean":"plana",
            "puirt":"port",
            "rannan":"rann",
            "seòmraichean":"seòmra",
            "seòrsachan":"seòrsa", "seòrsaichean":"seòrsa",
            "sgìrean":"sgìre", "sgoiltean":"sgoil",
            "sparran":"spàrr",
            "teaghlaichean":"teaghlach"
        }
        obliques = {
            "'ille":"gille",
            "athar":"athair", "bidhe":"biadh", "bùird":"bòrd",
            "cinn":"ceann", "cnuic":"cnoc",
            "coin":"cù",
            "cois":"cas",
            "èisg":"iasg",
            "mic":"mac", "Mic":"mac",
            "obrach":"obair",
            "seòid":"seud", "taighe":"taigh", "tighe":"tigh",
            "uamha":"uamh"
        }
        s = self.delenite(s)
        s = re.sub('-?san$', '', s)
        if s.endswith("'"): s = self.remove_apostrophe(s)
        if pos == "Nv":
            return self.lemmatize_vn(self.delenite(s))
        if pos.startswith("Ncp"):
            if s in demonyms:
                return demonyms[s]
            if s in specials:
                return specials[s]
            if s.endswith('aich'):
                return s.replace('aich','ach')
            if s.endswith('aidhean'):
                return s.replace('aidhean', 'adh')
            if s.endswith("ichean"):
                return s.replace("ichean", "iche")
            if s.endswith("ean"):
                return re.sub('ean$', '', s)
            elif s.endswith("eannan"):
                return re.sub("annan$", "", s)
            elif s.endswith("nnan"):
                return s.replace('nnan', '')
            elif s.endswith("an") and s != "ealan":
                return re.sub('an$', '', s)
        if pos.endswith("d") or pos.endswith("g") or pos.endswith("v"):
            if s in specials:
                return specials[s]
            if re.match(".*eige?$", s):
                return re.sub("eige?$", "eag", s)
            if s.endswith("aich"):
                return re.sub("aich$", "ach", s)
            if re.match(".*[bcdfghlmnprst]ich$", s):
                return re.sub("ich$", "each", s)
            if re.match(".*[au]is$",s) and 'm' in pos:
                return re.sub("is$", "s", s)
            if 'f' in pos and s.endswith('e'):
                return re.sub("e$", "", s)
        if s in obliques:
            return obliques[s]
        return s

    def lemmatize_comparative(self, s):
        specials = {
            "àille":"àlainn", "aotruime":"aotrom",
            "bige":"beag", "duirche":"dorcha",
            "fhasa":"furasta",
            "fhaide":"fada", "fhaid'":"fada",
            "fhaisge":"faisg", "fhaisg'":"faisg",
            "fheàrr":"math", "fhearr":"math", "fhèarr":"math",
            "fheàirrde":"math",
            "iomchaidhe":"iomchaidh",
            "ìsle":"ìosal",
            "leatha":"leathann",
            "mheasaile":"measail",
            "mhò":"mòr","mhuth'":"mòr",
            "miona":"mion", "miosa":"dona", "mhisde":"dona",
            "lugha":"beag",
            "righinne":"righinn",
            "righne":"righinn",
            "shine":"sean", "sine":"sean",
            "truime":"trom"
        }
        if s in specials:
            return specials[s]
        elif re.match(".*i[cl]e$",s):
            return re.sub("(i[cl])e$", r"\1", s)
        else:
            return re.sub("(.*[aeiouàòù])i([bcdfghmnpqrst]+)[e']?$", r"\1\2", self.delenite(s))

    def lemmatize(self, surface, pos):
        """Lemmatize surface based on pos, which is XPOS."""
        s = surface.replace('\xe2\x80\x99', "'").replace('\xe2\x80\x98', "'").replace("’", "'")
        s = re.sub("^(h-|t-|n-|[Dd]h')", "", s)
        if pos != "Nt" and not pos.startswith("Nn"):
            s = s.lower()
        if pos == "Apc" or pos == "Aps":
            return self.lemmatize_comparative(s)
        if pos.startswith("Aq") or pos.startswith("Ar"):
            return self.lemmatize_adjective(s)
        # do in this order because of "as"
        if pos.startswith("W") or pos == "Csw":
            return "is"
        if pos.startswith("Td"):
            return "an"
        if pos == ("Nt"):
            return "Alba" if s == "Albann" else self.delenite(s)
        if s.startswith("luchd"):
            return s.replace("luchd", "neach")
        if pos.startswith("Sp") or pos.startswith("Pr"):
            return self.lemmatize_preposition(s)
        if pos.startswith("Pp"):
            return self.lemmatize_pronoun(s)
        if pos.startswith("Sa") and s.endswith("'"):
            return "ag"
        if pos.startswith("V"):
            for irregular in self.irregulars:
                if s in irregular[1]:
                    return irregular[0]
        if pos.startswith("N"):
            return self.lemmatize_n(s, pos)
        if pos.startswith("Vm-1p"):
            return s.replace("eamaid", "") if s.endswith("eamaid") else s.replace("amaid", "")
        # singular imperative; easiest to deal with
        if pos == "Vm-2s" or pos == "Vm":
            return s
        if pos == "Vm-2p": # plural imperative
            return s.replace("aibh", "") if s.endswith("aibh") else s.replace("ibh", "")
        if pos == "V-f":
            return s.replace("aidh", "") if s.endswith("aidh") else s.replace("idh","")
        if pos.endswith("r"): # relative form
            if s.endswith("eas"):
                return s.replace("eas","")
            elif s.endswith("as"):
                return s.replace("as","")
            elif pos == "Ar":
                return self.delenite(s)
        elif pos.startswith("V-s0"):
            return self.delenite(s.replace("eadh", "")) if s.endswith("eadh") else self.delenite(s.replace("adh", ""))
        elif pos.startswith("V-p0") or pos.startswith("V-f0"):
            return self.delenite(s.replace("ear", "")) if s.endswith("ear") else self.delenite(s.replace("ar", ""))
        elif pos.startswith("V-s"): # past tense
            return self.delenite(s)
        # conditional or third person imperative
        elif pos.startswith("V-h") or pos.startswith("Vm-3"):
            return self.delenite(s).replace("eadh", "") if s.endswith("eadh") else self.delenite(s).replace("adh", "")
        elif pos.endswith("d"): # dependent form
            return self.delenite(s)
        if pos.startswith("A"):
            return self.delenite(s)
        return s

class CCGRetagger:
    def __init__(self):
        self.sub = Subcat()
        self.retaggings = {}
        with open('resources/retaggings.txt') as f:
            for line in f:
                if not line.startswith("#"):
                    tokens = line.split('\t')
                    self.retaggings[tokens[0]] = tokens[1].strip()
        self.specials = {
            'Mgr':['FIRSTNAME'], "Mghr":['FIRSTNAME'],
            'Dh’':['ADVPRE'], "Dh'":['ADVPRE'],
            'dragh':['NPROP'], 'dùil':['NPROP'],
            'Ach':['CONJ','SCONJ', 'ADVPRE'],
            'ach':['CONJ','SCONJ', 'ADVPRE'],
            'Agus':['CONJ', 'SCONJ', 'ADVPRE'],
            'agus':['CONJ', 'SCONJ', 'ADVPRE'],
            ',':['APPOS', 'NMOD', 'PUNC'],
            '-':['APPOS', 'NMOD', 'PUNC'],
            'dèidh':['N', 'NDEIDH'],
            'air':['ASPAIR', 'ASP', 'P', 'PP'],
            'ag':['ASP'],
            'rùnaire':['NAME'],
            'riaghladair':['NAME'],
            'dè':['INTERRDE'], 'i':['PRONOUN']
        }

    def retag_article(self, surface, pos):
        return ['DET'] if not pos.endswith('g') else ['DETNMOD']

    def retag_verb(self, surface, pos):
        return self.sub.subcat_tuple(surface, pos)

    def retag(self, surface, rawpos):
        # assume it was meant all along
        pos = rawpos.replace('*','')
        if surface.lower() in self.specials:
            return self.specials[surface.lower()]
        # separate mechanism for verbs
        if pos.startswith('Nv') or pos.startswith('V') or pos.startswith('W'):
            return self.retag_verb(surface, pos)
        # and articles
        if pos.upper().startswith('T'):
            return self.retag_article(surface, pos)
        if pos in self.retaggings:
            return [self.retaggings[pos]]
        # for cases where we are not using all of the features
        return [self.retaggings[pos[0:2]]]

class Subcat:
    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.mappings = {}
        self.mappings['default'] = ['TRANS', 'INTRANS']
        subcats = []
        with open('resources/subcat.txt') as f:
            for line in f:
                if not line.startswith('#'):
                    if re.match('^[0-9]', line):
                        tokens = line.split()
                        subcats = [t.strip() for t in tokens[1:]]
                    else:
                        self.mappings[line.strip()] = subcats

    def subcat_tuple(self, surface, pos):
        return self.subcat(self.lemmatizer.lemmatize(surface, pos))

    def subcat(self, lemma):
        if lemma in self.mappings.keys():
            return self.mappings[lemma]
        else:
            return self.mappings["default"]

class Features:
    def __init__(self):
        self.cases = {'n':'Nom', 'd':'Dat', 'g':'Gen', 'v':'Voc'}
        self.genders = {'m':'Masc', 'f':'Fem'}
        self.numbers = {'s':'Sing', 'p':'Plur', 'd':'Dual'}
        self.tenses = {"p":"Pres", "s":"Past", "f":"Fut"}
        self.parttypes_u = {"a":"Ad", "c":"Comp", "g":"Inf", "v":"Voc",
                            "p":"Pat", "o":"Num"}
        self.parttypes_q = {"Qn":"Cmpl", "Q-r":"Vb", "Qnr":"Vb", "Qq":"Vb",
                            "Qnm":"Vb"}
        self.polartypes_q = {"Qn":"Neg", "Qnr":"Neg", "Qnm":"Neg"}
        self.prontypes_q = {"Q-r":"Rel", "Qnr":"Rel", "Qq":"Int"}
        self.moodtypes_q = {"q":"Int"}

    def feats(self, xpos: str) -> dict:
        if xpos.startswith("A"):
            return self.feats_adj(xpos)
        if xpos.startswith("N"):
            return self.feats_noun(xpos)
        if xpos.startswith("T"):
            return self.feats_det(xpos)

    def feats_adj(self, xpos: str) -> dict:
        if xpos == "Apc": return {"Degree":["Cmp,Sup"]}
        result = {}
        if not xpos.startswith('Aq-'): return result
        result["Number"] = [self.numbers[xpos[3]]]
        if len(xpos) == 4:
            return result
        result["Gender"] = [self.genders[xpos[4]]]
        if len(xpos) == 5:
            return result
        result["Case"] = [self.cases[xpos[5]]]
        return result

    def feats_det(self, xpos: str) -> dict:
        result = {}
        number = [self.numbers[xpos[2]]]
        result["Number"] = number
        if len(xpos) == 3:
            return result
        result["Gender"] = [self.genders[xpos[3]]]
        if len(xpos) == 4:
            return result
        case = [self.cases[xpos[4]]]
        result["Case"] = case
        if xpos[3] == "-": return {"Case":case, "Number":number}
        return result

    def feats_noun(self, xpos: str) -> dict:
        result = {}
        result["Case"] = [self.cases[xpos[4]]]
        if xpos[3] == "-": return result
        result["Gender"] = [self.genders[xpos[3]]]
        if xpos.startswith('Nn'): return result
        result["Number"] = [self.numbers[xpos[2]]]
        return result

    def feats_nv(self, prev_xpos: str, xpos: str) -> dict:
        result = {}
        if prev_xpos.startswith("Sa") or prev_xpos.startswith("Sp"):
            result["VerbForm"] = ["Vnoun"]
        elif prev_xpos == "Ug" or prev_xpos.startswith("Dp"):
            result["VerbForm"] = ["Inf"]
        else:
            result["VerbForm"] = ["Vnoun"]
        return result

    def feats_part(self, xpos: str) -> dict:
        result = {}
        if xpos[1] in self.parttypes_u:
            result["PartType"] = [self.parttypes_u[xpos[1]]]
        if xpos[1] in self.moodtypes_q:
            result["Mood"] = [self.moodtypes_q[xpos[1]]]
        if xpos in self.parttypes_q:
            result["PartType"] = [self.parttypes_q[xpos]]
            if xpos in self.polartypes_q:
                result["Polarity"] = [self.polartypes_q[xpos]]
            if xpos in self.prontypes_q:
                result["PronType"] = [self.prontypes_q[xpos]]
        if xpos == "Q--s":
            result["Tense"] = ["Past"]
        if xpos == "Qnm":
            result["Mood"] = ["Imp"]
        return result

    def feats_pron(self, xpos: str) -> dict:
        result = {}
        result["Person"] = [xpos[2]]
        result["Number"] = [self.numbers[xpos[3]]]
        if len(xpos) > 4 and xpos[4] in self.genders:
            result["Gender"] = [self.genders[xpos[4]]]
        if xpos.endswith('e'):
            result["PronType"] = ['Emp']
        return result

    def feats_verb(self, xpos: str) -> dict:
        result = {}
        if '0' in xpos:
            result["Person"] = ["0"]
        elif '1' in xpos:
            result["Person"] = ["1"]
        elif '2' in xpos:
            result["Person"] = ["2"]
        if len(xpos) == 2: # this may well be a mistagging
            result["Mood"] = ["Imp"]
            return result
        if xpos[2] in self.tenses:
            result["Tense"] = [self.tenses[xpos[2]]]
        if xpos[2] == "h":
            result["Mood"] = ["Cnd"]
        if xpos[1] == "m":
            result["Mood"] = ["Imp"]
        return result

class CCGTyper:
    def __init__(self):
        self.types = {}
        with open('resources/types.txt') as f:
            for line in f:
                if not line.startswith("#"):
                    tokens = line.split('\t')
                    self.types[tokens[0]] = tokens[1].strip()

    def type_verb(self, surface, pos, tag):
        clausetypes = {"p":"dcl","s":"dcl","f":"dcl","r":"rel","d":"dep"}
        clausetype = clausetypes[pos[-1]] if pos[-1] in clausetypes else "small" if pos == "Nv" else "imp"
        tense = "pres" if "p" in pos else "past" if "s" in pos else "fut" if "f" in pos else "hab" if "h" in pos else None
        phon = "vowel" if re.match("^[aeiouàèìòù]", surface) or surface.startswith("f") else "cons"
        features = (clausetype if tense is None else f"{clausetype} {tense}") + f" {phon}"
        newtag = tag + features.upper().replace(' ','')
        type = self.types[tag] % features
        if pos.startswith("Vm") or '0' in pos:
            newtag = newtag + "IMPERS"
        else:
            type = type + "/n"
        return (newtag, type)

    def type(self, surface, pos, tag):
        if pos.startswith("V") or pos.startswith("W") or pos == "Nv":
            return self.type_verb(surface, pos, tag)
        else:
            return (tag, self.types[tag])
