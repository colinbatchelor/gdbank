import re
import sys
from collections import namedtuple

Token = namedtuple("token", "id form lemma upos xpos feats head deprel edeprel other")

def assign_deprel(token, in_pp, last_deprel, nouny, last_xpos, last_upos):
    deprel = "dep"
    xpos_mapping = {
        "Cc": "cc", "Cs": "mark", "Dd": "det", "Dq": "det", "I": "discourse",
        "Mc": "nummod", "Mo": "nummod", "Nv": "xcomp:pred", "Px": "nmod",
        "Nn-mv": "vocative", "Nn-fv": "vocative",
        "Q-r": "mark:prt",
        "Sa": "case", "Sp": "case", "Spa-s": "case", "Uv": "case:voc",
        "Xx": "dep"
    }
    if token.xpos in xpos_mapping:
        return xpos_mapping[token.xpos], in_pp
    if token.form == "ais":
        deprel = "obl"
    if token.id == "1":
        deprel = "root"

    if token.lemma == "airson":
        deprel = "case"
    if (token.xpos in ["Nn", "Nt"]) and last_upos == "NOUN":
        deprel = "nmod"
    if token.xpos in ["Qa", "Qn", "Ua", "Uc", "Ug", "Uo", "Qq", "Q--s"]:
        deprel = "mark:prt"
    if token.xpos.startswith("Td"):
        deprel = "det"
    if token.xpos.startswith("Dp"):
        deprel = "nmod:poss"
    if token.upos == "ADJ": deprel = "amod"
    if token.upos == "ADV": deprel = "advmod"
    if token.upos == "PUNCT": deprel = "punct"
    if re.match('^V.*d$', token.xpos): deprel = "ccomp"
    if token.xpos.startswith("W"): deprel = "cop"
    if last_deprel == "cc": deprel = "conj"
    if last_deprel == "cop" and (token.form in ["e", "an"]):
        deprel = "fixed"
    if last_upos == "VERB" and nouny: deprel = "nsubj"
    if last_xpos == "Q-r": deprel = "acl:relcl"
    if last_xpos == "Qq": deprel = "ccomp"
    if nouny and in_pp:
        deprel = "obl"
        in_pp = False
    elif nouny:
        deprel = "nsubj"
    return deprel, in_pp

def assign_head(head, root, deprel, noun_id, verb_id, token_id, form, upos, xpos):
    if deprel == "root":
        head = 0
    if deprel in ["acl:relcl", "amod"]:
        head = noun_id
    if deprel == "advmod" and form == "ro":
        head = int(token_id) + 1
    if deprel in ["advmod", "ccomp", "nsubj", "obl", "xcomp:pred", "punct"]:
        head = verb_id
    if deprel == "case" and upos == "ADP":
        head = int(token_id) + 2
    if deprel == "case" and upos == "PART":
        head = int(token_id) + 1
    if form == "math" and upos == "ADV": head = int(token_id) + 1
    if deprel in ["case:voc", "cc", "cop"]:
        head = int(token_id) + 1

    if deprel == "compound": head = int(token_id) - 1
    if deprel == "conj" and root != -1: head = root
    if deprel in ["dep", "discourse"]:
        head = verb_id
    if deprel in ["fixed", "nmod"]:
        head = int(token_id) - 1

    if deprel in ["mark", "mark:prt", "nmod:poss"]:
        head = int(token_id) + 1
    if deprel == "det":
        if xpos == "Dd":
            head = int(token_id) - 1
        else:
            head = int(token_id) + 1
    if deprel == "nummod":
        head = int(token_id) + 1
    if deprel == "obj" and upos == "PART":
        head = int(token_id) + 1

    if str(head) == str(id):
        head = verb_id

    return head

def process_line(line, last_deprel, last_upos, last_xpos, in_pp, verb_id, noun_id, root):
    token = Token(*line.split("\t"))

    if token.deprel == "root":
        root = int(token.id)
        verb_id = root

    nouny = token.upos in ["NOUN", "PRON", "PROPN"]
    if nouny:
        noun_id = int(token.id)

    if token.deprel == "_":
        deprel, in_pp = assign_deprel(token, in_pp, last_deprel, nouny, last_xpos, last_upos)
    else:
        deprel = token.deprel

    if token.head == "_":
        head = assign_head(token.head, root, deprel, noun_id, verb_id, token.id, token.form, token.upos, token.xpos)
    else:
        head = token.head

    if deprel == "case":
        in_pp = True
    if deprel in ["obl", "nmod"]:
        in_pp = False
                            
    if token.upos == "VERB" or token.xpos == "Nv":
        verb_id = int(token.id)
    tokens = (token.id, token.form, token.lemma, token.upos, token.xpos, token.feats, str(head), deprel, token.edeprel, token.other)
    print("\t".join(tokens).strip())
    return token.deprel, token.upos, token.xpos, in_pp, verb_id, noun_id, root

def guess_deprels(file):
    last_deprel = ""
    last_upos = ""
    last_xpos = ""
    in_pp = False
    verb_id = -1
    noun_id = -1
    root = -1
    for line in file:
        if line.startswith('#'):
            print(line.strip())
            root = 0
            in_pp = False
            last_deprel = ""
            verb_id = 1
        elif line.strip() == "":
            print(line.strip())
        elif "-" in line.split("\t")[0]:
            print(line.strip())
        else:
            last_deprel, last_upos, last_xpos, in_pp, verb_id, noun_id, root = process_line(line, last_deprel, last_upos, last_xpos, in_pp, verb_id, noun_id, root)

guess_deprels(open(sys.argv[1]))
