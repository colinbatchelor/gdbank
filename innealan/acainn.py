# -*- coding: utf-8 -*-
import re

class Lemmatizer:
    def __init__(self):
        self.irregulars = [ ('bi', ['tha', 'bha', 'robh', 'eil', 'bheil', 'bith', 'bhith', "bh'", "bhà", "thà", "th'", 'bhios', 'bidh', 'biodh', 'bhiodh', "'eil", "bhithinn", "bhitheadh", "bitheamaid", "thathas", "thathar", "robhar"]),
                            ('arsa', ["ars'", "ar", "ars", "as"]),
                            ('abair', ['ràdh', 'thuirt', 'their', 'theirear']),
                            ('beir', ['breith', 'bhreith', 'rug', 'beiridh']),
                            ('cluinn', ['cluinntinn', 'chluinntinn', 'cuala', "cual'", 'chuala', 'cluinnidh']),
                            ('rach', ['chaidh', 'dol', 'dhol', 'thèid', 'tèid', "deach"]),
                            ('dèan', ['rinn', 'dèanamh', 'dhèanamh', 'nì']),
                            ('faic', ['chunnaic', 'chunna', 'faicinn', 'fhaicinn', 'chì', 'chithear', 'chitheadh', 'fhaca', 'faca']),
                            ('faigh', ['faighinn', 'fhaighinn', 'fhuair', 'gheibh', 'gheibhear']),
                            ('ruig', ['ruigsinn', 'ràinig', 'ruigidh']),
                            ('thoir', ['toirt', 'thoirt', 'thug', 'bheir', 'bheirear', 'tug']),
                            ('thig', ['tighinn', 'thighinn', 'thàinig', 'thig', 'tig', 'tàinig', 'dàinig'])]
        self.vns = []
        with open('resources/vns.txt') as f:
            for line in f:
                tokens = line.split('\t')
                for vn in tokens[1:]:
                    pair = (tokens[0], vn)
                    self.vns.append(pair)

    def delenite(self, s):
        return s[0] + s[2:] if s[1] == 'h' else s

    def lemmatize_vn(self, s):
        for vn in self.vns:
            if s in vn[1]:
                return vn[0]
        if s.endswith("sinn"):
            return s.replace("sinn", "")
        elif s.endswith("eachadh"):
            return s.replace("eachadh", "ich")
        elif s.endswith("achadh"):
            return s.replace("achadh", "aich")
        elif s.endswith("gladh"):
            return s.replace("gladh", "gail")
        elif s.endswith("eadh"):
            return s.replace("eadh", "")
        elif s.endswith("adh"):
            return s.replace("adh", "")
        elif s.endswith("tainn"):
            return s.replace("tainn", "")
        else:
            return s

    """surface is the text you are lemmatizing, pos is the POS tag according to ARCOSG"""
    def lemmatize(self, surface, pos):
        s = surface.replace('\xe2\x80\x99', "'").replace('\xe2\x80\x98', "'").lower()
        # do in this order because of "as"
        if pos.startswith("W"):
            return "is"
        for irregular in self.irregulars:
            if s in irregular[1]:
                return irregular[0]
        if pos == "Nv":
            return self.lemmatize_vn(self.delenite(s))
        if pos.startswith("Vm-1p"):
            return s.replace("eamaid", "") if s.endswith("eamaid") else s.replace("amaid", "")
        if pos == "Vm-2s" or pos == "Vm": # singular imperative; easiest to deal with
            return s
        if pos == "Vm-2p": # plural imperative
            return s.replace("aibh", "") if s.endswith("aibh") else s.replace("ibh", "")
        if pos == "V-f": 
            return s.replace("aidh", "") if s.endswith("aidh") else s.replace("idh","")
        if pos.endswith("r"): # relative form
            if s.endswith("eas"):
                return s.replace("eas","")
            else:
                return s.replace("as","")
        elif pos.startswith("V-s0"):
            return self.delenite(s.replace("eadh", "")) if s.endswith("eadh") else self.delenite(s.replace("adh", ""))
        elif pos.startswith("V-p0") or pos.startswith("V-f0"):
            return self.delenite(s.replace("ear", "")) if s.endswith("ear") else self.delenite(s.replace("ar", ""))
        elif pos.startswith("V-s"): # past tense
            return self.delenite(s)
        elif pos.startswith("V-h") or pos.startswith("Vm-3"): # conditional or third person imperative
            return self.delenite(s).replace("eadh", "") if s.endswith("eadh") else self.delenite(s).replace("adh", "")
        elif pos.endswith("d"): # dependent form
            return self.delenite(s)
        return s

class Retagger:
    def __init__(self):
        self.sub = Subcat()
        self.retaggings = {}
        with open('resources/retaggings.txt') as f:
            for line in f:
                if not line.startswith("#"):
                    tokens = line.split('\t')
                    self.retaggings[tokens[0]] = tokens[1].strip()
        self.specials = {'Mgr':['FIRSTNAME'], "Mghr":['FIRSTNAME'], 'Dh’':['ADVPRE'], "Dh'":['ADVPRE'], 'dragh':['NPROP'], 'dùil':['NPROP'],
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

class Typer:
    def __init__(self):
        self.types = {}
        with open('resources/types.txt') as f:
            for line in f:
                if not line.startswith("#"):
                    tokens = line.split('\t')
                    self.types[tokens[0]] = tokens[1].strip()

    def type_verb(self, surface, pos, tag):
        clausetype = "dcl" if pos.endswith("p") or pos.endswith("s") or pos.endswith("f") else "dep" if pos.endswith("d") else "rel" if pos.endswith("r") else "small" if pos == "Nv" else "imp"
        tense = "pres" if "p" in pos else "past" if "s" in pos else "fut" if "f" in pos else "hab" if "h" in pos else None
        phon = "vowel" if re.match("^[aeiouàèìòù]", surface) or surface.startswith("f") else "cons"
        features = (clausetype if tense is None else clausetype + " " + tense) + " " + phon
        newtag = tag + features.upper().replace(' ','')
#        print surface + " " + pos + " " + tag + " " + self.types[tag] + " " + features
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
                    
