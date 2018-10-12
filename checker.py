from gaelic_pos import GaelicTokeniser
from gaelic_pos import postagger
from innealan.acainn import Features
from dataframes import Frame
import numpy as np
import pandas as pd
import re

class Checker():
    def __init__(self):
       #             if token in self.apos:
       #         code = "GOC-APOS"
       #         message = "apostrophe and space out"
       #     elif token in self.noapos:
       #         code = "GOC-NOAPOS"
       #         message = "no apostrophe and close up"
       #     if token in self.hyphens:
       #         code = "GOC-HYPHEN"
       #         message = "hyphen needed"
       #     if token in self.micheart:
       #         code = "MICHEART"
       #         message = self.micheart[token]

        self.t = GaelicTokeniser.Tokeniser()
        self.p = postagger.PosTagger()
        self.f = Frame()
        
        self.hyphen_series = ["a màireach", "a nis", "a nochd", "a raoir", "a rithist", "am bliadhna", "an ceartuair", "an dè", "an diugh", "an dràsta",   "an earar", "an-uiridh", "a bhàn", "a bhos", "an àird", "a nall", "a nìos", "a nuas", "a null", "a chaoidh", "a cheana", "am feast", "a mhàin", "a riamh", "a mach", "a muigh", "a staigh", "a steach"]
        self.hyphens = pd.DataFrame({
            "token": self.hyphen_series,
            "code": np.resize(["GOC-HYPHEN"], len(self.hyphen_series))
            })
        self.apos = ["Sann", "Se", "sann", "se"]
        self.noapos = ["de'n", "do'n", "fo'n", "mu'n", "ro'n", "tro'n"]
        self.micheart = pd.DataFrame({
            "token": ['radh','cearr'],
            "code": ["spelling","spelling"],
            'message': ['should be ràdh','should be ceàrr' ]})
        self.lenite_Ar_series = ["deagh","droch"]
        self.lenite_Ar = pd.DataFrame({
            "token": self.lenite_Ar_series,
            "code": np.resize(["LENITE"], len(self.lenite_Ar_series))
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
            "_p_1": ["Qq"], "_c0": ["f"], "code": ["45iia"]})
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
        self.lenitest_1 = pd.DataFrame({
            "_t_1": self.lenite_Ar,
            "_p_1": np.resize(["Ar"], len(self.lenite_Ar)),
            "code":"LENITE"})
    
    def _check(self, tagged_tokens):
        df = self.f.feats(self.f.make(tagged_tokens))
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
                  merge(self.fh, on=("_p_1","_c0"), how="left", suffixes = ("-i", "-j")).
                  merge(self.t_1_case, on=("_t_1","_genitivesing"), how="left").
                  merge(self.t_1_number, on=("_t_1","_pl"), how="left", suffixes = ("-k", "-l")).
                  merge(self.lantest, on=("_t_1","_genitive"), how="left").
                  merge(self.genitest, on=("_t_1","_p_1","_genitive"), how="left", suffixes = ("-m", "-n")).
                  merge(self.lenitest_1, on=("_t_1","_p_1"), how="left").
                  merge(self.micheart, on="token", how="left", suffixes = ("-o", "-p")).
                  merge(self.hyphens, on="token", how="left").
                  merge(self.lenite_Ar, on="token", how="left", suffixes = ("-q","-r"))
                  )
        result = result.fillna('')
        result['code'] = result.filter(regex="code-").agg(lambda x:",".join(x),axis="columns")
        return result.drop(columns = result.filter(regex="[_-]"))

    def _acutes(self, s):
        return s.match(r"[óéá]")
    
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

