# -*- coding: utf-8 -*-
# Ma tha craobh gun feartan ach le feartan air na duilleagan, thoir feartan
# bho na duilleagan do na phàrantan aca.
import sys
from nltk.tree import ParentedTree
from nltk import induce_pcfg
from nltk.grammar import Nonterminal
from nltk.parse import pchart
from acainn import Lemmatizer
import re

file_out = sys.argv[2]

def seorsa_S(craobh):
    for nod in craobh:
        if type(nod[0]) is ParentedTree:
            leubail = nod.label()
            if leubail == "S":
                nod.set_label('S[type=SUB]')
            else:
                if leubail.startswith("S"):
                    nod.set_label(leubail[0] + '[type='+ leubail[1:] + ']')
            seorsa_S(nod)
        else: # 's e sreath a th' ann
            pass

def seorsa_P(craobh):
    l = Lemmatizer()
    for nod in craobh:
        if type(nod[0]) is ParentedTree:
            leanbh = ""
            leubail = nod.label()
            if leubail== "PP":
                leanbh = nod[0]
                if not leanbh.label().startswith('PP'):
                    nod.set_label('PP[type='+l.lemmatize_preposition(str(leanbh).split(' ')[1][:-1])+']')
                else:
                    nod.set_label(leanbh.label())
            seorsa_P(nod)
        else:
            pass

def tuiseal_NP(craobh):
    for nod in craobh:
        if type(nod[0]) is ParentedTree:
            leanbh =""
            if nod.label() == "NP":
                if nod[0].label().startswith('S'):
                    print 'error:' + " ".join([l.encode('utf-8') for l in nod.leaves()]) 
                # dearbhaich nòd le tuiseal
                if nod[0].label() == 'Ar' or nod[0].label() == 'Uo' or nod[0].label() == 'Dq' or nod[0].label().startswith('Dp') or nod[0].label() =='Mc' or nod[0].label().startswith('Td'):
                    leanbh = nod[1].label()
                else:
                    leanbh = nod[0].label()
                if leanbh.startswith('T') or leanbh.startswith('N'):
                    tuiseal = leanbh.rstrip("*")[-1]
                    if tuiseal in 'ngd':
                        nod.set_label('NP[case='+tuiseal+']')
                        if leanbh.startswith('P'): tuiseal = 'n'
            tuiseal_NP(nod)
        else: # this is a string
            pass

# feum a bhith aonaraidh: Fe
aonaraidh = ['Fe']
# feum a bhith càraideach: SDCL
caraideach = ['S','SDCL','SASP','SSMALL','SGUN','SDEP','S0DEP','SREL','SINF','SBAR','NP','PP']
craobhan = []
with open(sys.argv[1]) as f:
    for loidhne in f:
        craobh = ParentedTree.fromstring(loidhne.decode('utf8'))
        craobhan.append(craobh)

# check trees
c = 1
for craobh in craobhan:
    for nod in craobh:
        if len(nod) == 2:
            if nod.label() in aonaraidh: print '%s 2ary error (%s %s %s)' % (c, nod.label(), nod[0].label(), nod[1].label())
        if len(nod) == 1:
            if nod.label() in caraideach: print '%s 1ary error (%s %s %s)' % (c, nod.label(), nod[0].label(), " ".join(nod.leaves()))
    c = c + 1

# assign cases to NP
with open(file_out,'w') as g:
    for craobh in craobhan:
        tuiseal_NP(craobh)
        seorsa_S(craobh)
        seorsa_P(craobh)
        g.write(re.sub(r'\s+',' ',str(craobh)))

