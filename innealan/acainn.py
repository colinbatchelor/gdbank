"""Mixture of generically-useful classes, UD-specific ones and CCG-specific ones."""
import os
import re
import csv

class Morphology:
    """Static methods for grammar checker."""
    @staticmethod
    def can_follow_de(surface: str) -> bool:
        """this is dè the interrogative"""
        return surface in ["cho", "am", "an", "a'", "na", "mar", "bha", "tha"]

    @staticmethod
    def lenited(surface: str) -> bool:
        """
Generic test for whether the orthographic form of a word has been lenited.

Words beginning with n, l and r also lenite but this is orthographically silent.
"""
        unlenitable = re.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]", surface)
        return bool(unlenitable) | (surface[1] == 'h')

    @staticmethod
    def lenited_pd(surface: str) -> bool:
        """
TODO: Work out why this is separate from the previous function and delete if unnecessary.
"""
        unlenitable = surface.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]")
        return unlenitable | (surface[1] == 'h')

    @staticmethod
    def chalenited_pd(surface: str) -> bool:
        """There are different rules for lenition after cha."""
        unlenitable = surface.match(r"[AEIOUaeiouLlNnRrDTSdts]")
        return unlenitable | (surface[1] == 'h')

    @staticmethod
    def ndlenited_pd(surface: str) -> bool:
        """TODO: rename to non_dental_lenited."""
        unlenitable = surface.match(r"[AEIOUaeiouDdTtNnRrSs]")
        return unlenitable | (surface[1] == 'h')

class Lemmatizer:
    """Relies heavily on POS information."""
    def __init__(self):
        folder = os.path.dirname(__file__)
        self.prepositions = {}
        prep_path = os.path.join(folder, 'resources', 'prepositions.csv')
        with open(prep_path) as file:
            reader = csv.reader(file)
            for row in reader:
                self.prepositions[row[0]] = row[1]
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

        vn_path = os.path.join(folder, 'resources', 'verbal_nouns.csv')
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

    @staticmethod
    def delenite(surface: str) -> str:
        """Removes h as the second letter except for special cases."""
        if len(surface) < 3:
            return surface
        if surface in ["Shaw", "Christie"]:
            return surface
        return surface[0] + surface[2:] if surface[1] == 'h' else surface

    @staticmethod
    def deslenderize(surface: str) -> str:
        """Converts from slender to broad."""
        if re.match('.*ei.h?$', surface):
            return re.sub("(.*)ei(.h?)", r"\1ea\2", surface)
        if re.match('.*[bcdfghmnprst]i.h?e?$', surface):
            return re.sub("(.*)i(.h?)e?", r"\1ea\2", surface)
        return re.sub("(.*[aiouàòù])i([bcdfghmnpqrst]+)[e']?$", r"\1\2", surface)

    def lemmatize_adjective(self, surface: str, xpos: str) -> str:
        """The small number of special plurals are dealt with in lemmata.csv"""
        if xpos in ["Apc", "Aps"]:
            return self.lemmatize_comparative(surface)
        surface = self.delenite(surface)
        surface = self.remove_apostrophe(surface)
        if surface in self.lemmata:
            return self.lemmata[surface]
        if xpos == "Av":
            return re.sub("(is)?[dt][ae]?$", "", surface)
        if surface.endswith("òir"):
            return re.sub("òir$", "òr", surface)
        return surface

    def lemmatize_comparative(self, surface: str) -> str:
        """Relies on external file. If surface not in file delenites and slenderises."""
        if surface in self.lemmata:
            return self.lemmata[surface]
        if re.match(".*i[cgl]e$",surface):
            return re.sub("(i[cgl])e$", r"\1", surface)
        return re.sub("e$", "", self.delenite(self.deslenderize(surface)))

    def lemmatize_proper_noun(self, surface: str, oblique: bool) -> str:
        """May need xpos information to deal with the vocative."""
        surface = self.delenite(surface)
        if surface == "a'":
            return "an"
        surface = surface.replace("Mic", "Mac")
        if surface in self.lemmata:
            return self.lemmata[surface]
        if oblique and surface not in ["Iain", "Keir", "Magaidh"]:
            return self.deslenderize(surface)
        return surface

    def lemmatize_noun(self, surface: str, xpos: str) -> str:
        """
        Master function which uses other functions for Nc, Nn, Nt and Nv.
        Nf is _usually_ more like a preposition so is dealt with elsewhere.
        """
        oblique = re.match('.*[vdg]$', xpos)
        if xpos.startswith("Nn"):
            return self.lemmatize_proper_noun(surface, oblique)

        surface = self.delenite(surface)

        surface = self.remove_apostrophe(surface)
        if surface in self.lemmata:
            return self.lemmata[surface]

        if surface not in ["dusan", "mìosan", "pìosan"]:
            surface = re.sub('-?san$', '', surface)

        if xpos == "Nv":
            return self.lemmatize_vn(surface)
        if xpos == "Nt":
            return "Alba" if surface in ["Albann", "Albainn"] else surface
        return self.lemmatize_common_noun(surface, xpos, oblique)

    @staticmethod
    def lemmatize_common_noun(surface: str, xpos: str, oblique: bool) -> str:
        """Looks as if it needs to be refactored."""
        if surface.startswith("luchd"):
            return surface.replace("luchd", "neach")

        plural_replacements = [
            ('eachan', 'e'), ('achan', 'a'), ('aich', 'ach'),
            ('aidhean', 'adh'), ('aichean', 'ach'), ('ichean', 'iche'),
            ('ean', ''), ('eannan', 'e'), ('ean', ''), ('annan', 'a'), ('an', '')
            ]

        if xpos.startswith("Ncp"):
            for replacement in plural_replacements:
                if surface.endswith(replacement[0]):
                    return re.sub(f"{replacement[0]}$", replacement[1], surface)
        m_replacements = [('aich', 'ach'), ('aidh', 'adh'), ('ais', 'as'), ('uis', 'us')]
        f_replacements = [('eig', 'eag'), ('eige', 'eag'), ('the', 'th')]
        if oblique and 'f' in xpos:
            for replacement in f_replacements:
                if surface.endswith(replacement[0]):
                    return re.sub(f"{replacement[0]}$", replacement[1], surface)
        if oblique and 'm' in xpos:
            for replacement in m_replacements:
                if surface.endswith(replacement[0]):
                    return re.sub(f"{replacement[0]}$", replacement[1], surface)
        if re.match(".*[bcdfghlmnprst]ich$", surface):
            return re.sub("ich$", "each", surface)
        return surface

    def lemmatize_possessive(self, xpos: str) -> str:
        """Does not look at the surface, only the POS tag."""
        return self.possessives[xpos[0:4]]

    def lemmatize_preposition(self, surface: str) -> str:
        """Relies on resources/prepositions.csv"""
        if surface.startswith("'") and len(surface) > 1:
            surface = surface[1:]
        surface = self.remove_apostrophe(surface.replace(' ', '_'))
        surface = re.sub('^h-', '', surface)
        if not re.match("^'?s[ae]n?$", surface):
            surface = re.sub("-?s[ae]n?$", "", surface)
        for pattern in self.prepositions:
            if re.match("^("+pattern+")$", surface):
                return self.prepositions[pattern]
        return "bho" if surface.startswith("bh") else self.delenite(surface)

    def lemmatize_pronoun(self, surface: str) -> str:
        """Consider rewriting based on POS tag."""
        for key in self.pronouns:
            if surface in self.pronouns[key]:
                return key
        if surface.startswith("fh") or surface.startswith("ch"):
            return self.delenite(surface)
        return surface

    def lemmatize_verb(self, surface: str, xpos: str) -> str:
        """Hybrid replacement dictionary/XPOS method."""
        for form in self.lemmata:
            if surface == form:
                return self.lemmata[form]
        replacements = [
            ("Vm-1p", "e?amaid$"), ("Vm-2p", "a?ibh$"),
            ("V-s0", "e?adh$"), ("V-p0", "e?ar$"), ("V-f0", "e?ar$"),
            ("V-h", "e?adh$"), ("Vm-3", "e?adh$"), ("V-f", "a?(idh|s)$")
        ]
        for replacement in replacements:
            if xpos.startswith(replacement[0]):
                surface = self.delenite(surface)
                return re.sub(replacement[1], "", surface)

        if xpos.endswith("r"): # relative form
            if surface.endswith("eas"):
                return surface.replace("eas","")
            if surface.endswith("as"):
                return surface.replace("as","")

        return self.delenite(surface)

    def lemmatize_vn(self, surface: str) -> str:
        """Hybrid replacement dictionary/XPOS method"""
        if surface.startswith("'"):
            surface = surface[1:]
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

    @staticmethod
    def remove_apostrophe(surface: str) -> str:
        """Makes a guess based on slenderness of last vowel"""
        if surface.endswith("'") and surface != "a'":
            result = re.sub("'$", "", surface)
            stem = re.sub("[bcdfghlmnprst]+'$", "", surface)
            if re.match(".*[aouàòù]$", stem):
                return "%sa" % result
            return "%se" % result
        return surface

    def lemmatize(self, surface: str, xpos: str) -> str:
        """Lemmatize surface based on xpos."""
        surface = surface.replace('\xe2\x80\x99', "'").replace('\xe2\x80\x98', "'")
        surface = re.sub("[’‘]", "'", surface)
        surface = re.sub("^(h-|t-|n-|[Dd]h')", "", surface)
        specials = [("Q--s", "do"), ("W", "is"), ("Csw", "is"), ("Td", "an")]
        for special in specials:
            if xpos.startswith(special[0]):
                return special[1]
        if xpos[0:2] not in ["Nn", "Nt", "Up", "Y"]:
            surface = surface.lower()
        if xpos.startswith("R") or xpos == "I":
            if surface not in ["bhuel", "chaoidh", "cho", "fhathast", "mhmm",
                               "thall", "thairis", "thì"]:
                return self.delenite(surface)
        if xpos[0:2] in ["Ap", "Aq", "Ar", "Av"]:
            return self.lemmatize_adjective(surface, xpos)
        if xpos[0:2] in ["Sa", "Sp", "Pr", "Nf"]:
            return self.lemmatize_preposition(surface)
        if xpos.startswith("Pp") or xpos == "Px":
            return self.lemmatize_pronoun(surface)
        if xpos.startswith("V"):
            return self.lemmatize_verb(surface, xpos)
        if xpos.startswith("N"):
            return self.lemmatize_noun(surface, xpos)
        if xpos.startswith("Dp"):
            return self.lemmatize_possessive(xpos)
        return surface

class CCGRetagger:
    """Relies on the subcategoriser, largely."""
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

    @staticmethod
    def retag_article(xpos):
        """Articles are N/N unless they are in the genitive in which case they are N/N/N/N"""
        return ['DET'] if not xpos.endswith('g') else ['DETNMOD']

    def retag_verb(self, surface, xpos):
        """Relies on surface."""
        return self.sub.subcat_tuple(surface, xpos)

    def retag(self, surface, rawpos):
        """Relies on surface and xpos."""
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
        """Wrapper for subcat. Relies on lemmatizer."""
        return self.subcat(self.lemmatizer.lemmatize(surface, pos))

    def subcat(self, lemma):
        """Relies on lemma."""
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
        self.parttypes = {"Qa":"Cmpl", "Qn":"Cmpl", "Q-r":"Vb", "Qnr":"Vb", "Qq":"Vb",
                            "Qnm":"Vb", "Ua":"Ad", "Uc":"Comp", "Ug":"Inf", "Uv":"Voc",
                            "Up":"Pat", "Uo":"Num"}
        self.polartypes_q = {"Qn":"Neg", "Qnr":"Neg", "Qnm":"Neg"}
        self.prontypes_q = {"Q-r": "Rel", "Qnr": "Rel", "Qq": "Int", "Uq": "Int"}

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

    @staticmethod
    def feats_nv(prev_xpos: str, xpos: str) -> dict:
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
        if xpos in self.parttypes:
            result["PartType"] = [self.parttypes[xpos]]
            if xpos in self.polartypes_q:
                result["Polarity"] = [self.polartypes_q[xpos]]
            if xpos in self.prontypes_q:
                result["PronType"] = [self.prontypes_q[xpos]]
        if xpos == "Q--s":
            result["Tense"] = ["Past"]
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
        """Marks for possessiveness, person, number, gender, whether emphatic and if interrogative."""
        result = {}
        if xpos[1] == "p" and xpos[0] == "D":
            result["Poss"] = ["Yes"]
        if len(xpos) > 2:
            result["Person"] = [xpos[2]]
            result["Number"] = [self.numbers[xpos[3]]]
        if len(xpos) > 4 and xpos[4] in self.genders:
            result["Gender"] = [self.genders[xpos[4]]]
        if xpos.endswith('e'):
            result["Form"] = ['Emp']
        if xpos in self.prontypes_q:
            result["PronType"] = [self.prontypes_q[xpos]]
        if xpos == "Px":
            result["Reflex"] = ["Yes"]
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
