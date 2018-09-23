from gaelic_pos import GaelicTokeniser
from gaelic_pos import postagger

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

    def _check(self, tagged_tokens):
        result = []
        for (token, pos) in tagged_tokens:
            code = ''
            message = ''
            if 'ó' in token:
                code = "GOC"
                message = "graves only"
            elif token in self.apos:
                code = "GOC-APOS"
                message = "apostrophe and space out"
            elif token in self.noapos:
                code = "GOC-NOAPOS"
                message = "no apostrophe and close up"
            elif token in self.hyphens:
                code = "GOC-HYPHEN"
                message = "hyphen needed"
            elif token in self.micheart:
                code = "MICHEART"
                message = self.micheart[token]
            result.append((token, pos, code, message))
        return result
        
    def check(self, text):
        tokens = self.t.tokenise(text)
        tagged_tokens = self.p.tagfile_default(tokens)
        return _check(tagged_tokens)
