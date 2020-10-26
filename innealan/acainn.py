import os
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
            ('rach', ['chaidh', 'dol', 'dhol', 'thèid', 'tèid', "deach",
                      "deachaidh"]),
            ('dèan', ['rinn', 'dèanamh', 'dhèanamh', 'nì']),
            ('faic', ['chunnaic', 'chunna', 'faicinn', 'fhaicinn', 'chì',
                      'chithear', 'chitheadh', 'fhaca', 'faca']),
            ('faigh', ['faighinn', 'fhaighinn', 'fhuair', 'gheibh',
                       'gheibhear']),
            ('ruig', ['ruigsinn', 'ràinig', 'ruigidh']),
            ('tadhail', ['thadhladh']),
            ('toir', ['toirt', 'thoirt', 'thug', 'bheir', 'bheirear', 'tug']),
            ('thig', ['tighinn', 'thighinn', 'thàinig', 'thig', 'tig',
                      'tàinig', 'dàinig'])]
        self.prepositions = {
            'ag':["a'", "'"],
            'aig':["aga(m|d|inn|ibh)|aige|aice|aca|a'[dm]"],
            'air':["or[mt]|oir(re|bh|nn)|orra"],
            'airson':["'?son"],
            'an': ["'?s?a[mn]", "'?sa", "'?na", "anns?(_a[nm])?", "annam",
                   "innte", "a's", "'nam", "anns"],
            'as':["às", "as.*", "ais.*", "á"],
            'bho':["(bh)?o", "(bh)?ua(m|t)"],
            'eadar':["ea.*"],
            'fo':["fo.*"],
            'gu': ["chun", "gu_ruige", "(th)?ui[cg]e", "(th)?uga(m|d|inn|ibh)",
                   "(th)?uca"],
            'de':["dh?(en?|iom|[ei]th|inn|iu?bh)"],
            'do':["dh(à|am|[oò]mh|i|ui?t|u'|uinn|an?|[au]ib[h'])(-?s['a]?)?e?"],
            'le':["le.*"],
            'ri':["ri(um|ut(ha)?|s)", "ru.*", "r'"],
            'ro':["ro.*"],
            'thar':["tha.*"]
        }
        self.possessives = {
            "Dp1s": "mo", "Dp2s": "do", "Dp3s": "a",
            "Dp1p": "ar", "Dp2p": "ur", "Dp3p": "an"
        } 
        self.pronouns = {
            "mi": ["mise"], "thu": ["tu", "tusa", "thusa"],
            "e": ["esan"], "i": ["ise"],
            "sinn": ["sinne"], "sibh": ["sibhse"], "iad": ["iadsan"],
            "fèin": ["fhìn"]
            }
        folder = os.path.dirname(__file__)
        vn_path = os.path.join(folder, 'resources', 'vns.csv')
        self.vns = []
        with open(vn_path) as file:
            reader = csv.reader(file)
            for row in reader:
                self.vns.append((row[0], row[1].split(";")))
        lemmata_path = os.path.join(folder, 'resources', 'lemmata.csv')
        self.lemmata = {}
        with open(lemmata_path) as file:
            reader = csv.reader(filter(lambda row: row[0] != '#', file))
            for row in reader:
                self.lemmata[row[0]] = row[1]

    def can_follow_de(self, surface: str) -> bool:
        """this is dè the interrogative"""
        return surface in ["cho", "am", "an", "a'", "na", "mar", "bha", "tha"]

    def lenited(self, surface: str) -> bool:
        unlenitable = re.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]", surface)
        return bool(unlenitable) | (surface[1] == 'h')

    def lenited_pd(self, surface: str) -> bool:
        unlenitable = surface.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]")
        return unlenitable | (surface[1] == 'h')

    def chalenited_pd(self, surface: str) -> bool:
        """There are different rules for lenition after cha."""
        unlenitable = surface.match(r"[AEIOUaeiouLlNnRrDTSdts]")
        return unlenitable | (surface[1] == 'h')

    def ndlenited_pd(self, surface: str) -> bool:
        unlenitable = surface.match(r"[AEIOUaeiouDdTtNnRrSs]")
        return unlenitable | (surface[1] == 'h')

    def delenite(self, surface: str) -> str:
        if len(surface) < 3:
            return surface
        return surface[0] + surface[2:] if surface[1] == 'h' else surface

    def deslenderize(self, surface: str) -> str:
        if re.match('.*ei.$', surface):
            return re.sub("(.*)ei(.)", r"\1ea\2", surface)
        return re.sub("(.*[aiouàòù])i([bcdfghmnpqrst]+)[e']?$", r"\1\2", surface)

    def lemmatize_adjective(self, surface: str) -> str:
        surface = self.delenite(surface)
        if surface.endswith("òir"):
            return re.sub("òir$", "òr", surface)
        return surface

    def lemmatize_comparative(self, surface: str) -> str:
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
            "mhò":"mòr","mhuth'":"mòr", "motha":"math",
            "miona":"mion", "miosa":"dona", "mhisde":"dona",
            "lugha":"beag",
            "righinne":"righinn",
            "righne":"righinn",
            "shine":"sean", "sine":"sean",
            "truime":"trom"
        }
        if surface in specials:
            return specials[surface]
        if re.match(".*i[cl]e$",surface):
            return re.sub("(i[cl])e$", r"\1", surface)
        return self.delenite(self.deslenderize(surface))

    def lemmatize_noun(self, s: str, xpos: str) -> str:
        if s not in ["Shaw", "Christie"]:
            s = self.delenite(s)
        if s not in ["dusan", "mìosan", "pìosan"]:
            s = re.sub('-?san$', '', s)
        oblique = re.match('.*[vdg]$', xpos)
        if s.endswith("'") and s!= "a'":
            s = self.remove_apostrophe(s)
        if xpos == "Nv":
            return self.lemmatize_vn(s)
        if xpos == "Nt":
            return "Alba" if s == "Albann" else s
        if s.startswith("luchd"):
            return s.replace("luchd", "neach")
        if xpos.startswith("Nn"):
            if s == "a'":
                return "an"
            s = s.replace("Mic", "Mac")
            if s in self.lemmata:
                return self.lemmata[s]
            if oblique and s not in ["Iain", "Keir", "Magaidh"]:
                return self.deslenderize(s)
            return s
        if xpos.startswith("Ncp"):
            if s in self.lemmata:
                return self.lemmata[s]
            if s.endswith("eachan"):
                return re.sub("achan$", "", s)
            if s.endswith("achan"):
                return re.sub("chan$","",s)
            if s.endswith('aich'):
                return s.replace('aich','ach')
            if s.endswith('aidhean'):
                return s.replace('aidhean', 'adh')
            if s.endswith("aichean"):
                return s.replace("aichean", "ach")
            if s.endswith("ichean"):
                return s.replace("ichean", "iche")
            if s.endswith("ean"):
                return re.sub('ean$', '', s)
            if s.endswith("eannan"):
                return re.sub("annan$", "", s)
            if s.endswith("nnan"):
                return s.replace('nnan', '')
            if s.endswith("an") and s != "ealan":
                return re.sub('an$', '', s)
        if oblique:
            if s in self.lemmata:
                return self.lemmata[s]
            if re.match(".*eige?$", s):
                return re.sub("eige?$", "eag", s)
            if s.endswith("aich") and 'm' in xpos:
                return re.sub("aich$", "ach", s)
            if s.endswith("aidh") and 'm' in xpos:
                return re.sub("aidh$", "adh", s)
            if re.match(".*[bcdfghlmnprst]ich$", s):
                return re.sub("ich$", "each", s)
            if re.match(".*[au]is$",s) and 'm' in xpos:
                return re.sub("is$", "s", s)
            if 'f' in xpos and s.endswith('the'):
                return re.sub("e$", "", s)
        if s in self.lemmata:
            return self.lemmata[s]
        return s

    def lemmatize_possessive(self, surface: str, xpos: str) -> str:
        return self.possessives[xpos[0:4]]
    
    def lemmatize_preposition(self, surface: str) -> str:
        surface = surface.replace(' ','_')
        surface = re.sub('^h-', '', surface)
        if not re.match("^'?san?$", surface):
            surface = re.sub('-?san?$','',surface)
        for key in self.prepositions:
            for pattern in self.prepositions[key]:
                if re.match("^("+pattern+")$", surface):
                    return key
        return surface if surface.startswith('bh') else self.delenite(surface)

    def lemmatize_pronoun(self, surface: str) -> str:
        for key in self.pronouns:
            if surface in self.pronouns[key]:
                return key
        if surface.startswith("fh") or surface.startswith("ch"):
            return self.delenite(surface)
        return surface

    def lemmatize_verb(self, s: str, xpos: str) -> str:
        for irregular in self.irregulars:
            if s in irregular[1]:
                return irregular[0]
        if xpos.startswith("Vm-1p"):
            return re.sub('e?amaid$', '', s)
        # singular imperative; easiest to deal with
        if xpos in ["Vm-2s", "Vm"]:
            return s
        if xpos == "Vm-2p": # plural imperative
            return re.sub('a?ibh$', '', s)
        if xpos == "V-f":
            return re.sub('a?idh$', '', s)
        if xpos.endswith("r"): # relative form
            if s.endswith("eas"):
                return s.replace("eas","")
            if s.endswith("as"):
                return s.replace("as","")
        if xpos.startswith("V-s0"):
            return self.delenite(re.sub('e?adh$', '', s))
        if xpos.startswith("V-p0") or xpos.startswith("V-f0"):
            return self.delenite(re.sub('e?ar$', '', s))
        if xpos.startswith("V-s"): # past tense
            return self.delenite(s)
        # conditional or third person imperative
        if xpos.startswith("V-h") or xpos.startswith("Vm-3"):
            return self.delenite(re.sub('e?adh$', '', s))
        if xpos.endswith("d"): # dependent form
            return self.delenite(s)
        return self.delenite(s)

    def lemmatize_vn(self, surface: str) -> str:
        for verbal_noun in self.vns:
            if self.delenite(surface) in verbal_noun[1]:
                return verbal_noun[0]
        replacements = [
            ('sinn', ''), ('tail', ''), ('ail', ''), ('eil', ''), ('eal', ''),
            ('aich', ''), ('ich', ''), ('tainn', ''), ('tinn', ''),
            ('eamh', ''), ('amh', ''),
            ('eamhainn', ''), ('mhainn', ''), ('inn', ''), ('eachdainn', 'ich'),
            ('eachadh', 'ich'), ('achadh', 'aich'), ('airt', 'air'),
            ('gladh', 'gail'), ('eadh', ''), ('-adh', ''), ('adh', ''),
            ('e', ''), ('eachd', 'ich'), ('achd', 'aich')
        ]
        for replacement in replacements:
            if surface.endswith(replacement[0]):
                return self.delenite(surface.replace(replacement[0], replacement[1]))
        return self.delenite(surface)

    def remove_apostrophe(self, surface: str) -> str:
        result = re.sub("'$", "", surface)
        stem = re.sub("[bcdfghlmnprst]+'$", "", surface)
        if re.match(".*[aouàòù]$", stem):
            return "%sa" % result
        return "%se" % result

    def lemmatize(self, surface: str, xpos: str) -> str:
        """Lemmatize surface based on xpos."""
        s = surface.replace('\xe2\x80\x99', "'").replace('\xe2\x80\x98', "'")
        s = re.sub("[’‘]", "'", s)
        s = re.sub("^(h-|t-|n-|[Dd]h')", "", s)
        if xpos == "Q--s":
            return "do"
        if not (xpos in ["Nt", "Up", "Y"]) and not xpos.startswith("Nn"):
            s = s.lower()
        if xpos.startswith("R") or xpos == "I":
            if s not in ["bhuel", "chaoidh", "cho", "fhathast", "mhmm",
                               "thall", "thairis", "thì"]:
                return self.delenite(s)
        if xpos in ["Apc", "Aps"]:
            return self.lemmatize_comparative(s)
        if xpos.startswith("Aq") or xpos.startswith("Ar"):
            return self.lemmatize_adjective(s)
        # do in this order because of "as"
        if xpos.startswith("W") or xpos == "Csw":
            return "is"
        if xpos.startswith("Td"):
            return "an"
        if xpos.startswith("Sa") or xpos.startswith("Sp") or xpos.startswith("Pr"):
            return self.lemmatize_preposition(s)
        if xpos.startswith("Pp") or xpos == "Px":
            return self.lemmatize_pronoun(s)
        if xpos.startswith("V"):
            return self.lemmatize_verb(s, xpos)
        if xpos.startswith("N"):
            return self.lemmatize_noun(s, xpos)
        if xpos.startswith("A"):
            return self.delenite(s)
        if xpos.startswith("Dp"):
            return self.lemmatize_possessive(s, xpos)
        return s

class CCGRetagger:
    def __init__(self):
        self.sub = Subcat()
        self.retaggings = {}
        with open('resources/retaggings.txt') as file:
            for line in file:
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

    def retag_article(self, pos):
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
            return self.retag_article(pos)
        if pos in self.retaggings:
            return [self.retaggings[pos]]
        # for cases where we are not using all of the features
        return [self.retaggings[pos[0:2]]]

class Subcat:
    """Assigns subcategories based on lemmata."""
    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.mappings = {}
        self.mappings['default'] = ['TRANS', 'INTRANS']
        subcats = []
        with open('resources/subcat.txt') as file:
            for line in file:
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
        return self.mappings["default"]

class Features:
    """Assigns UD features based on ARCOSG POS tags."""
    def __init__(self):
        self.cases = {'n':'Nom', 'd':'Dat', 'g':'Gen', 'v':'Voc'}
        self.genders = {'m':'Masc', 'f':'Fem'}
        self.numbers = {'s':'Sing', 'p':'Plur', 'd':'Dual'}
        self.tenses = {"p":"Pres", "s":"Past", "f":"Fut"}
        self.parttypes_u = {"a":"Ad", "c":"Comp", "g":"Inf", "v":"Voc",
                            "p":"Pat", "o":"Num"}
        self.parttypes_q = {"Qa":"Cmpl", "Qn":"Cmpl", "Q-r":"Vb", "Qnr":"Vb", "Qq":"Vb",
                            "Qnm":"Vb"}
        self.polartypes_q = {"Qn":"Neg", "Qnr":"Neg", "Qnm":"Neg"}
        self.prontypes_q = {"Q-r":"Rel", "Qnr":"Rel", "Qq":"Int"}
        self.moodtypes_q = {"q":"Int"}

    def feats(self, xpos: str) -> dict:
        """Only seems to work for adjectives, nouns and articles?"""
        if xpos.startswith("A"):
            return self.feats_adj(xpos)
        if xpos.startswith("N"):
            return self.feats_noun(xpos)
        if xpos.startswith("T"):
            return self.feats_det(xpos)
        return {}

    def feats_adj(self, xpos: str) -> dict:
        """Marks degree, number, gender and case."""
        if xpos == "Apc":
            return {"Degree":["Cmp,Sup"]}
        result = {}
        if not xpos.startswith('Aq-'):
            return result
        result["Number"] = [self.numbers[xpos[3]]]
        if len(xpos) == 4:
            return result
        result["Gender"] = [self.genders[xpos[4]]]
        if len(xpos) == 5:
            return result
        result["Case"] = [self.cases[xpos[5]]]
        return result

    def feats_cop(self, xpos: str) -> dict:
        """Marks tense, mood, polarity and whether relative."""
        result = {}
        print(f"{xpos}")
        if len(xpos) > 1:
            result["Tense"] = [self.tenses[xpos[1]]]
        if len(xpos) > 2:
            if xpos[2] == "r":
                result["PronType"] = ["Rel"]
        if len(xpos) > 3:
            if xpos[3] == "q":
                result["Mood"] = ["Int"]
        if len(xpos) == 5:
            if xpos[4] == "n":
                result["Polarity"] = ["Neg"]
            elif xpos[4] == "a":
                result["Polarity"] = ["Aff"]
        print(result)

        return result

    def feats_det(self, xpos: str) -> dict:
        """Marks number, gender and case"""
        result = {}
        number = [self.numbers[xpos[2]]]
        result["Number"] = number
        if len(xpos) == 3:
            return result
        if xpos[3] != "-":
            result["Gender"] = [self.genders[xpos[3]]]
        if len(xpos) == 4:
            return result
        case = [self.cases[xpos[4]]]
        result["Case"] = case
        if xpos[3] == "-":
            return {"Case":case, "Number":number}
        return result

    def feats_noun(self, xpos: str) -> dict:
        """Marks case, gender, number and whether emphatic."""
        result = {}
        if xpos.endswith("e"):
            result["Form"] = ["Emp"]
        result["Case"] = [self.cases[xpos[4]]]
        if xpos[3] == "-":
            return result
        result["Gender"] = [self.genders[xpos[3]]]
        if xpos.startswith('Nn'):
            return result
        result["Number"] = [self.numbers[xpos[2]]]
        return result

    def feats_nv(self, prev_xpos: str, xpos: str) -> dict:
        """Marks whether a verbal noun or an infinitve."""
        result = {}
        if prev_xpos.startswith("Sa") or prev_xpos.startswith("Sp"):
            result["VerbForm"] = ["Vnoun"]
        elif prev_xpos == "Ug" or prev_xpos.startswith("Dp"):
            result["VerbForm"] = ["Inf"]
        else:
            result["VerbForm"] = ["Vnoun"]
        if xpos.endswith("e"):
            result["Form"] = ["Emp"]
        return result

    def feats_part(self, xpos: str) -> dict:
        """Marks particle type, mood, polarity, pronoun type, tense and mood."""
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

    def feats_prep(self, xpos: str) -> dict:
        '''Example: Spp1s'''
        result = {}
        result["Poss"] = ["Yes"]
        result["Person"] = [xpos[3]]
        result["Number"] = [self.numbers[xpos[4]]]
        if len(xpos) > 5 and xpos[5] in self.genders:
            result["Gender"] = [self.genders[xpos[5]]]
        if xpos.endswith('e'):
            result["Form"] = ['Emp']
        return result

    def feats_pron(self, xpos: str) -> dict:
        """Marks for possessiveness, person, number, gender and whether emphatic."""
        result = {}
        if xpos[1] == "p" and xpos[0] == "D":
            result["Poss"] = ["Yes"]
        result["Person"] = [xpos[2]]
        result["Number"] = [self.numbers[xpos[3]]]
        if len(xpos) > 4 and xpos[4] in self.genders:
            result["Gender"] = [self.genders[xpos[4]]]
        if xpos.endswith('e'):
            result["Form"] = ['Emp']
        return result

    def feats_verb(self, xpos: str) -> dict:
        """Marks for person, tense and mood."""
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
    """Adds CCG features"""
    def __init__(self):
        """Adds CCG features"""
        self.types = {}
        with open('resources/types.txt') as file:
            for line in file:
                if not line.startswith("#"):
                    tokens = line.split('\t')
                    self.types[tokens[0]] = tokens[1].strip()

    def type_verb(self, surface, pos, tag):
        """Adds CCG features"""
        clausetypes = {"p":"dcl","s":"dcl","f":"dcl","r":"rel","d":"dep"}
        clausetype = clausetypes[pos[-1]] if pos[-1] in clausetypes \
            else "small" if pos == "Nv" else "imp"
        tense = "pres" if "p" in pos else "past" if "s" in pos \
            else "fut" if "f" in pos else "hab" if "h" in pos else None
        phon = "vowel" if re.match("^[aeiouàèìòù]", surface) or surface.startswith("f") else "cons"
        features = (clausetype if tense is None else f"{clausetype} {tense}") + f" {phon}"
        newtag = tag + features.upper().replace(' ','')
        ccg_type = self.types[tag] % features
        if pos.startswith("Vm") or '0' in pos:
            newtag = newtag + "IMPERS"
        else:
            ccg_type = ccg_type + "/n"
        return (newtag, ccg_type)

    def type(self, surface, pos, tag):
        """Retypes it as a verb if it's a verb, copula or verbal noun."""
        if pos.startswith("V") or pos.startswith("W") or pos == "Nv":
            return self.type_verb(surface, pos, tag)
        return (tag, self.types[tag])
