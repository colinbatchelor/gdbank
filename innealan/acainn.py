# -*- coding: utf-8 -*-

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

        self.vns = [ ('ath-giullaich', 'ath-giollachd'),
                ('feuch', 'feuchainn'),
                ('fuadaich', 'fuadach'),
                ('èigh', 'èigheachd'),
                ('èist', 'èisteachd'),
                ('èist', 'èisdeachd'),
                ('èist', 'éisteachd'),
                ('èist', 'éisdeachd'),
                ('àitich', 'àiteach'),
                ('gabh', 'gabhail'),
                ('gluais', 'gluasad'),
                ('ceannaich', 'ceannach'),
                ('iasgaich', 'iasgach'),
                ('coisinn', 'cosnadh'),
                ('coisich', 'coiseachd'),
                ('faotainn', 'faigh'),
                ('feith', 'feitheamh'),
                ('caidil', 'cadal'),
                ('cùm', 'cumail'),
                ('cuir', 'cur'),
                ('dùin', 'dùnadh'),
                ('fàg', 'fàgail'),
                ('faighinn', 'faighneachd'),
                ('fairich', 'faireachdainn'),
                ('fuirich', 'fuireach'),
                ('iarr', 'iarraidh'),
                ('inns', 'innse'),
                ('iomair', 'iomradh'),
                ('ceangail', 'ceangal'),
                ('tachair', 'tachairt'),
                ('tadhail', 'tadhal'),
                ('tagh', 'taghadh'),
                ('leig', 'leigeil'),
                ('cluinn', 'cluinnteil'),
                ('lean', 'leanail'),
                ('loisg', 'losgadh'),
                ('obraich', 'obair'),
                ('pòs', 'pòsadh'),
                ('caith', 'caitheamh'),
                ('seas', 'seasamh'),
                ('toirmisg', 'toirmeasg'),
                ('ruig', 'ruigheachd'), ('tionndaidh', 'tionndadh'),
                ('smaoinich', 'smaointinn'),
                ('sruigheil', 'sruighleadh'), ('tataidh', 'tatadh'),
                ('till', 'tilleadh'), ('thoir', 'toir'),
                ('tog', 'togail'), ('tuit', 'tuiteam')]

    def delenite(self, s):
        return s[0] + s[2:] if s[1] == 'h' else s

    def lemmatize_vn(self, s):
        for vn in self.vns:
            if s == vn[1]:
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
            return self.delenite(s).replace("eadh", "") if s.endswith("eadh") else delenite(s).replace("adh", "")
        elif pos.endswith("d"): # dependent form
            return self.delenite(s)
        return s
