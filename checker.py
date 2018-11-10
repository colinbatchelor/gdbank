from gaelic_pos import GaelicTokeniser
from gaelic_pos import postagger
from innealan.acainn import Features, Lemmatizer
import numpy as np
import pandas as pd
import re

class Checker():
    # for simple matches
    def _list_to_df(self, list, code):
        return pd.DataFrame({
            "token": list,
            "code": np.resize([code], len(list))
            })
    
    def _make_df(self, tagged_tokens):
        tokens = [t[0] for t in tagged_tokens]
        postags = [t[1] for t in tagged_tokens]
        t_1 = ['<START>'] + tokens[:-1]
        p_1 = ['<START>'] + postags[:-1]
        t_2 = ['<START>'] + t_1[:-1]
        p_2 = ['<START>'] + p_1[:-1]
        t1 = tokens[1:] + ['<END>']
        t2 = t1[1:] + ['<END>']
        p1 = postags[1:] + ['<END>']
        p2 = p1[1:] + ['<END>']
        return pd.DataFrame(
            { 'token': tokens, 'pos': postags, '_t_1': t_1, '_p_1': p_1,
              '_t_2': t_2, '_p_2': p_2, '_t1': t1, '_p1': p1, '_t2': t2, '_p2': p2 }
        )

    def _feats(self, df):
        return df.assign(
            _lenited = lambda x: self.l.lenited_pd(x.token.str),
            _chalenited = lambda x: self.l.chalenited_pd(x.token.str),
            _nondentallenited = lambda x: self.l.ndlenited_pd(x.token.str),
            _genitive = lambda x: x.pos.str.match('N.*g'),
            _sing = lambda x: x.pos.str.match('N.s'),
            _genitivesing = lambda x: x.pos.str.match('N.s.g'),
            _pl = lambda x: x.pos.str.match('N.p'),
            _c0 = lambda x: x.token.str[0],
            _coarsepos = lambda x: x.pos.str[0],
            _acute = lambda x: self._acutes(x.token.str),
            code = lambda x: '')
    
    def __init__(self):
        self.l = Lemmatizer()
        self.t = GaelicTokeniser.Tokeniser()
        self.p = postagger.PosTagger()
        
        hyphen_series = ["a màireach", "a nis", "a nochd", "a raoir", "a rithist", "am bliadhna", "an ceartuair", "an dè", "an diugh", "an dràsta", "an earar", "an-uiridh", "a bhàn", "a bhos", "an àird", "a nall", "a nìos", "a nuas", "a null", "a chaoidh", "a cheana", "am feast", "a mhàin", "a riamh", "a mach", "a muigh", "a staigh", "a steach"]
        personalnumber_series = ["dithis", "tri", "ceathrar", "cignear",
                                      "sianar", "seachdnar", "ochdnar", "naoinear",
                                      "deichnear"]
        self.personalnumber_adjs = pd.DataFrame({
            "_t_1": personalnumber_series,
            "_coarsepos": np.resize(["A"], len(personalnumber_series)),
            "_lenited": [False, False, True, True, True, True, True, True, True],
            "code": np.resize(["144ii"], len(personalnumber_series))
        })
        self.personalnumber_nouns = pd.DataFrame({
            "_t_1": personalnumber_series,
            "_coarsepos": np.resize(["N"], len(personalnumber_series)),
            "_lenited": np.resize([False], len(personalnumber_series)),
            "code": np.resize(["144iii"], len(personalnumber_series))
        })
        self.acutes = pd.DataFrame({"_acute": [True], "code":["GOC-ACUTE"]})

        
        self.hyphens = self._list_to_df(hyphen_series, "GOC-HYPHEN")
        self.apos = self._list_to_df(["Sann", "Se", "sann", "se"], "GOC-APOS")
        self.noapos = self._list_to_df(["de'n", "do'n", "fo'n", "mu'n", "ro'n", "tro'n"], "GOC-NOAPOS")
        self.micheart = pd.DataFrame({
            "token": ['radh','cearr'],
            "code": ["spelling","spelling"],
            'message': ['should be ràdh','should be ceàrr' ]})
        lenite_Ar_series = ["deagh","droch"]
        self.lenite_Ar = pd.DataFrame({
            "_t_1": lenite_Ar_series,
            "code": np.resize(["LENITE"], len(lenite_Ar_series)),
            "_lenited": np.resize([False], len(lenite_Ar_series))
            })
        self.messages = {
            "45iaepsilon": "Nouns lenite after mo, do, a (masculine). Cox §45iaε",
            "45iaepsilon-": "Nouns do not lenite after a (feminine), ar, ur, an. Cox §45iaε",
            "44iiia": "Independent forms in the past and mixed tenses lenite: Cox §44iiia,§44iiib/§246ii",
            "44iiia-":"Dependent forms in the past and mixed tenses do not lenite.",
        # thinking about how to implement Cox §44iiic/§45iaα.
            "45iabeta": "Masculine names in the genitive lenite: Cox §45iaβ",
            "45iabeta-": "Feminine names in the genitive do not usually lenite: Cox §45iaβ",
            # Cox §45iaδ is complicated to do on the basis of tagging.
            # consider doing based on the surface form
            "45iazeta":"Nouns lenite after aon, dà, dhà. Cox §45iaζ",
            # Cox distinguishes air, air^s, and air^n. How to deal with this?   
            "45iaiota":"nouns lenite after prepositions bho, o, de, do, eadar, fo, gun, mu, ro, thar tre and tro. Cox §45iaι",
            "45iealpha":"verbs lenite after ma and relative-form verbs lenite after a. Cox §45ieα",
            "45iebeta":"past-tense verbs lenite after do. Cox §45ieβ",
            "45iegamma":"verbs immediately after cha lenite. Cox §45ieγ",
            "45iia":"verbs beginning with f after a question particle lenite. Cox §45iia",
            "170": "barrachd takes the genitive singular: Cox §170",
            "173": "iomadh is followed by a singular noun: Cox §173",
            "176":"tuilleadh takes the genitive singular: Cox §176"
        }
        self.lenitesp_1 = pd.DataFrame({
            "_p_1": ["Dp1s", "Dp2s", "Dp3sm"],
            "_lenited": [False, False, False],
            "code": ["45iaepsilon","45iaepsilon","45iaepsilon"]})
        self.nolenitesp_1 = pd.DataFrame({
            "_p_1": ["Dp3sf", "Dp1p", "Dp2p", "Dp3p"],
            "_lenited": [True, True, True, True],
            "code": ["45iaepsilon-","45iaepsilon-","45iaepsilon-","45iaepsilon-"]})
        self.lenitepos = pd.DataFrame({
            "pos": ["V-h", "V-s", "V-h1s", "Nn-mg","V-h--d","V-s--d", "Nn-fg"],
            "_lenited": [False, False, False, False,True,True,True],
            "code": ["44iiia","44iiia", "44iiia", "45iabeta","44iiia-","44iiia-","45iabeta-"]})
        self.nd_lenite_t_1 = pd.DataFrame({
            "_t_1":["aon"],
            "_nondentallenited": [False],
            "code": ["45iazeta"]})
        self.lenite_t_1 = pd.DataFrame({
            "_t_1": ["dà", "dhà"],
            "_lenited":[False,False],
            "code": ["45iazeta","45iazeta"]})
        self.lenite_p_1_t_1 = pd.DataFrame({
            "_p_1": np.resize(["Sp"],12),
            "_lenited": np.resize([False],12),
            "_t_1": ["bho", "o","de","do","eadar","fo","gun","mu","ro","thar","tre","tro"],
            "code": np.resize(["45iaiota"],12)})
        # check for verb here?
        self.lenite_p_1_t_1a = pd.DataFrame({
            "_p_1": ["Cs", "Q-r", "Q--s"],
            "_t_1": ["ma", "a", "do"],
            "_lenited":[False,False,False],
            "code":["45iealpha","45iealpha","45iebeta"]})
        self.chalenite_p_1_t_1 = pd.DataFrame({
            "_p_1": ["Qn"],
            "_t_1": ["cha"],
            "_chalenited": [False],
            "code":["45iegamma"]})
        self.fh = pd.DataFrame({
            "_p_1": ["Qq"],
            "_c0": ["f"],
            "_lenited": [False],
            "code": ["45iia"]})
        self.t_1_case = pd.DataFrame({
            "_t_1": ["barrachd","tuilleadh"],
            "_genitivesing": [False,False],
            "code": ["170","176"]})
        self.t_1_number = pd.DataFrame({
            "_t_1": ["iomadh"],
            "_pl": [True],
            "code": ["173"]})
        self.lantest = pd.DataFrame({
            "_t_1":["làn"], "_genitive": False, "code":"174"})
        self.genitest = pd.DataFrame({
            "_t_1":["chum"], "_p_1":"Sp", "_genitive":False, "code":"344"})
        
    def _check(self, tagged_tokens):
        df = self._feats(self._make_df(tagged_tokens))
        return self._checkdf(df)

    def _checkdf(self, df):
        result = (df.
            merge(self.lenitesp_1, on=("_p_1","_lenited"), how="left", suffixes = ("-a","-b")).
            merge(self.nolenitesp_1, on =("_p_1","_lenited"), how="left").
            merge(self.lenitepos, on=("pos","_lenited"), how="left", suffixes = ("-c","-d")).
            merge(self.lenite_t_1, on=("_t_1","_lenited"), how="left").
            merge(self.nd_lenite_t_1, on=("_t_1","_nondentallenited"),how="left", suffixes = ("-e","-f")).
            merge(self.lenite_p_1_t_1, on=("_p_1","_t_1","_lenited"), how="left").
            merge(self.lenite_p_1_t_1a, on=("_p_1","_t_1","_lenited"), how="left", suffixes = ("-g","-h")).
            merge(self.chalenite_p_1_t_1, on=("_p_1","_t_1","_chalenited"), how="left").
            merge(self.fh, on=("_p_1","_c0", "_lenited"), how="left", suffixes = ("-i", "-j")).
            merge(self.t_1_case, on=("_t_1","_genitivesing"), how="left").
            merge(self.t_1_number, on=("_t_1","_pl"), how="left", suffixes = ("-k", "-l")).
            merge(self.lantest, on=("_t_1","_genitive"), how="left").
            merge(self.genitest, on=("_t_1","_p_1","_genitive"), how="left", suffixes = ("-m", "-n")).
            merge(self.micheart, on="token", how="left").
            merge(self.hyphens, on="token", how="left", suffixes = ("-o", "-p")).
            merge(self.apos, on="token", how="left").
            merge(self.lenite_Ar, on=("_t_1","_lenited"), how="left", suffixes = ("-q","-r")).
            merge(self.acutes, on=("_acute"), how="left").
            merge(self.personalnumber_adjs, on=("_t_1", "_coarsepos", "_lenited"), how="left", suffixes = ("-s","-t")).
            merge(self.personalnumber_nouns, on=("_t_1", "_coarsepos", "_lenited"), how="left").
            merge(self.personalnumber_nouns, on=("_t_1", "_coarsepos", "_lenited"), how="left", suffixes = ("-u","-v"))
        )
        result = result.fillna('')
        result['code'] = result.filter(regex="code-").agg(lambda x:",".join(x),axis="columns")
        return result.drop(columns = result.filter(regex="[_-]"))

    def _acutes(self, s):
        return s.contains(r"[úóíéá]")
    
    def _lenited(self, s):
        unlenitable = s.match(r"[AEIOUaeiouLlNnRr]|[Ss][gpt]")
        return unlenitable | (s[1] == 'h')

    def _chalenited(self, s):
        unlenitable = s.match(r"[AEIOUaeiouLlNnRrDTSdts]")
        return unlenitable | (s[1] == 'h')
    
    def _unlenited(self, s):
        return s[1] != 'h'
        
    def check(self, text):
        tokens = self.t.tokenise(text)
        tagged_tokens = self.p.tagfile_default(tokens)
        return _check(tagged_tokens)

