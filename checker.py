from gaelic_pos import GaelicTokeniser
from gaelic_pos import postagger
import re

class Checker():
    def __init__(self):
        self.t = GaelicTokeniser.Tokeniser()
        self.p = postagger.PosTagger()
        self.hyphens = ["a màireach", "a nis", "a nochd", "a raoir", "a rithist", "am bliadhna", "an ceartuair", "an dè", "an diugh", "an dràsta",   "an earar", "an-uiridh", "a bhàn", "a bhos", "an àird", "a nall", "a nìos", "a nuas", "a null", "a chaoidh", "a cheana", "am feast", "a mhàin", "a riamh", "a mach", "a muigh", "a staigh", "a steach"]
        self.apos = ["Sann", "Se", "sann", "se"]
        self.noapos = ["de'n", "do'n", "fo'n", "mu'n", "ro'n", "tro'n"]
        self.micheart = {
            'radh': 'should be ràdh',
            'cearr': 'should be ceàrr' 
        }
        self.lenite_Ar = ["deagh","droch"]

    def _check(self, tagged_tokens):
        result = []
        n_tokens = len(tagged_tokens)
        for i,pair in enumerate(tagged_tokens):
            token,pos = pair
            t_1,p_1 = tagged_tokens[i-1] if i > 0 else ("<START>","")
            t1,p1 = tagged_tokens[i+1] if i < n_tokens - 1 else ("<END>","")
            t2,p2 = tagged_tokens[i+2] if i < n_tokens - 2 else ("<END>","")
            code = ''
            message = ''
            if p_1 in ["Dp1s", "Dp2s", "Dp3sm"]:
                if not self._lenited(token):
                    code = "LENITE"
                    message = "Nouns lenite after mo, do, a (masculine). Cox §45iaε"
            elif p_1 in ["Dp3sf", "Dp1p", "Dp2p", "Dp3p"]:
                if not self._unlenited(token):
                    code = "NOLENITE"
                    message = "Nouns do not lenite after a (feminine), ar, ur, an. Cox §45iaε"
            if re.match("V-h[123][sp]", pos) or re.match("V-[hs]$", pos):
                if not self._lenited(token):
                    code = "LENITE"
                    message = "Independent forms in the past and mixed tenses lenite: Cox §44iiia,§44iiib/§246ii"
            elif re.match("V-[hs]--d",pos):
                if not self._unlenited(token):
                    code = "NOLENITE"
                    message = "Dependent forms in the past and mixed tenses do not lenite."
            # thinking about how to implement Cox §44iiic/§45iaα.
            if pos == "Nn-mg":
                if not self._lenited(token):
                    code = "LENITE"
                    message = "Masculine names in the genitive lenite: Cox §45iaβ"
            if pos == "Nn-fg":
                if self._lenited(token):
                    code = "NOLENITE"
                    message = "Feminine names in the genitive do not usually lenite: Cox §45iaβ"
            # Cox §45iaδ is complicated to do on the basis of tagging.
            # consider doing based on the surface form
            if p_1 in ["Dp1s", "Dp2s", "Dp3sm"]:
                if not self._lenited(token):
                    code = "LENITE"
                    message = "Nouns lenite after mo, do, a (masculine). Cox §45iaε"
            elif p_1 in ["Dp3sf", "Dp1p", "Dp2p", "Dp3p"]:
                if not self._unlenited(token):
                    code = "NOLENITE"
                    message = "Nouns do not lenite after a (feminine), ar, ur, an. Cox §45iaε"
            if t_1 == "aon":
                if not self._nondental_lenited(token):
                    code = "LENITE"
                    message = "Nouns lenite after aon. Cox §45iaζ"
            if t_1 == "dà" or t_1 =="dhà":
                if not self._lenited(token):
                    code = "LENITE"
                    message = "nouns lenite after dà/dhà. Cox §45iaζ"
            # Cox distinguishes air, air^s, and air^n. How to deal with this?        
            if p_1 == "Sp" and t_1 in ["bho","o","de","do","eadar","fo","gun","mu","ro","thar","tre","tro"]:
                if not self._lenited(token):
                    code = "LENITE"
                    message = "nouns lenite after prepositions bho, o, de, do, eadar, fo, gun, mu, ro, thar tre and tro. Cox §45iaι"
            if (t_1, p_1) == ("ma","Cs") or (t_1,p_1) == ("Ma","Cs"):
                if not self._lenited(token) and pos.startswith("V"):
                    code = "LENITE"
                    message = "verbs lenite after ma. Cox §45ieα"
            if (t_1,p_1) == ("a","Q-r"):
                if not self._lenited(token) and pos.startswith("V"):
                    code = "LENITE"
                    message = "relative-form verbs lenite after a. Cox §45ieα"
            if (t_1,p_1) == ("do","Q--s"):
                if not self._lenited(token) and pos.startswith("V"):
                    code = "LENITE"
                    message = "past-tense verbs lenite after do. Cox §45ieβ"
            if (t_1,p_1) == ("cha","Qn") or (t_1,p_1) == ("Cha","Qn"):
                if not self._chalenited(token) and pos.startswith("V"):
                    code = "LENITE"
                    message = "verbs immediately after cha lenite. Cox §45ieγ"

            if p_1 == "Qq" and token.startswith("f"):
                if not self._lenited(token):
                    code = "LENITE"
                    message = "verbs beginning with f after a question particle lenite. Cox §45iia"
            if pos.startswith("Nc") and not re.match("Ncs.g", pos):
                if t_1 == "barrachd":
                    code = "GINIDEACH/SINGILTE"
                    message = "barrachd takes the genitive singular: Cox §170"
                if t_1 == "tuilleadh":
                    code = "GINIDEACH/SINGILTE"
                    message = "tuilleadh takes the genitive singular: Cox §176"
            if pos.startswith("Nc") and not re.match("Nc..g", pos):
                if t_1 == "làn":
                    code = "GINIDEACH"
                    message = "làn takes the genitive: Cox §174"
                elif t_1 == "chum" and p_1 == "Sp":
                    code = "GINIDEACH"
                    message = "(a) chum takes the genitive: Cox §344"                    
            if pos.startswith("Ncp") and t_1 == "iomadh":
                code = "SINGILTE"
                message = "iomadh is followed by a singular noun: Cox §173"
            if ((pos == "Ar" and token in self.lenite_Ar) or (token == "de" and p1.startswith("N"))) and not self._lenited(t1):
                code = "LENITE"
                message = token + " lenites the following"
            if 'ó' in token or 'é' in token or 'á' in token:
                code = "GOC"
                message = "graves only"
            if token in self.apos:
                code = "GOC-APOS"
                message = "apostrophe and space out"
            elif token in self.noapos:
                code = "GOC-NOAPOS"
                message = "no apostrophe and close up"
            if token in self.hyphens:
                code = "GOC-HYPHEN"
                message = "hyphen needed"
            if token in self.micheart:
                code = "MICHEART"
                message = self.micheart[token]
            result.append((token, pos, code, message))
        return result

    def _lenited(self, s):
        unlenitable = re.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]", s)
        return unlenitable or s[1] == 'h'

    def _chalenited(self, s):
        unlenitable = re.match(r"[AEIOUaeiouLlNnRrDTSdts]", s)
        return unlenitable or s[1] == 'h'
    
    def _unlenited(self, s):
        return s[1] != 'h'
        
    def check(self, text):
        tokens = self.t.tokenise(text)
        tagged_tokens = self.p.tagfile_default(tokens)
        return _check(tagged_tokens)

