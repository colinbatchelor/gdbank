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

    def _unlenited(self, s):
        return s[1] != 'h'
        
    def check(self, text):
        tokens = self.t.tokenise(text)
        tagged_tokens = self.p.tagfile_default(tokens)
        return _check(tagged_tokens)
