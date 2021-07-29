import re
import sys
from collections import namedtuple

Token = namedtuple("token", "id form lemma upos xpos feats head deprel edeprel other")

def assign_deprel(token, in_pp, nouny, last_token):
    deprel = "dep"
    xpos_mapping = {
        "Cc": "cc", "Cs": "mark", "Dd": "det", "Dq": "det", "I": "discourse",
        "Mc": "nummod", "Mo": "nummod", "Nv": "xcomp:pred", "Px": "nmod",
        "Nn-mv": "vocative", "Nn-fv": "vocative",
        "Q-r": "mark:prt",
        "Sa": "case", "Sp": "case", "Spa-s": "case", "Uv": "case:voc",
        "Xx": "dep"
    }
    upos_mapping = {
        "ADJ": "amod", "ADV": "advmod", "AUX": "cop", "PUNCT": "punct", "PART": "mark:prt"
    }
    if token.xpos in xpos_mapping:
        return xpos_mapping[token.xpos], in_pp
    if token.upos in upos_mapping:
        return upos_mapping[token.upos], in_pp
    if token.form == "ais":
        deprel = "obl"
    if token.id == "1":
        deprel = "root"

    if token.lemma == "airson":
        deprel = "case"
    if (token.xpos in ["Nn", "Nt"]) and last_token.upos == "NOUN":
        deprel = "nmod"
    if token.xpos.startswith("Td"):
        deprel = "det"
    if token.xpos.startswith("Dp"):
        deprel = "nmod:poss"
    if re.match('^V.*d$', token.xpos):
        deprel = "ccomp"
    if last_token.deprel == "cc":
        deprel = "conj"
    if last_token.deprel == "cop" and (token.form in ["e", "an"]):
        deprel = "fixed"
    if nouny:
        if last_token.upos == "VERB":
            return "nsubj", in_pp
        if in_pp:
            return "obl", False
        return "obj", in_pp
    if last_token.xpos == "Q-r":
        deprel = "acl:relcl"
    if last_token.xpos == "Qq":
        deprel = "ccomp"
    return deprel, in_pp

def assign_head(root, deprel, noun_id, verb_id, token):
    head = 0
    if deprel == "root":
        return head
    if deprel in ["acl:relcl", "amod"]:
        head = noun_id
    if deprel == "advmod" and token.form == "ro":
        head = int(token.id) + 1
    if deprel in ["advmod", "ccomp", "nsubj", "obl", "xcomp:pred", "punct"]:
        head = verb_id
    if deprel == "case" and token.upos == "ADP":
        head = int(token.id) + 2
    if deprel == "case" and token.upos == "PART":
        head = int(token.id) + 1
    if token.form == "math" and token.upos == "ADV":
        head = int(token.id) + 1
    if deprel in ["case:voc", "cc", "cop", "mark", "mark:prt", "nmod:poss"]:
        head = int(token.id) + 1

    if deprel == "conj" and root != -1:
        head = root
    if deprel in ["dep", "discourse"]:
        head = verb_id
    if deprel in ["compound", "fixed", "nmod"]:
        head = int(token.id) - 1

    if deprel == "det":
        if token.xpos == "Dd":
            head = int(token.id) - 1
        else:
            head = int(token.id) + 1
    if deprel == "nummod":
        head = int(token.id) + 1
    if deprel == "obj" and token.upos == "PART":
        head = int(token.id) + 1

    return head

def process_line(line, last_token, in_pp, verb_id, noun_id, root):
    token = Token(*line.split("\t"))

    if token.deprel == "root":
        root = int(token.id)
        verb_id = root

    nouny = token.upos in ["NOUN", "PRON", "PROPN"]
    if nouny:
        noun_id = int(token.id)

    if token.deprel == "_":
        deprel, in_pp = assign_deprel(token, in_pp, nouny, last_token)
    else:
        deprel = token.deprel

    if token.head == "_":
        head = assign_head(root, deprel, noun_id, verb_id, token)
    else:
        head = token.head

    if deprel == "case":
        in_pp = True
    if deprel in ["obl", "nmod"]:
        in_pp = False

    if token.upos == "VERB" or token.xpos == "Nv":
        verb_id = int(token.id)
    tokens = (token.id, token.form, token.lemma, token.upos, token.xpos,
              token.feats, str(head), deprel, token.edeprel, token.other)
    print("\t".join(tokens).strip())
    return Token(*tokens), in_pp, verb_id, noun_id, root

def guess_deprels(file):
    last_token = Token("", "", "", "", "", "", "", "", "", "")
    in_pp = False
    verb_id = -1
    noun_id = -1
    root = -1
    for line in file:
        if line.startswith('#'):
            print(line.strip())
            root = 0
            in_pp = False
            last_token = Token("", "", "", "", "", "", "", "", "", "")
            verb_id = 1
        elif line.strip() == "":
            print(line.strip())
        elif "-" in line.split("\t")[0]:
            print(line.strip())
        else:
            last_token, in_pp, verb_id, noun_id, root = process_line(line, last_token, in_pp, verb_id, noun_id, root)

guess_deprels(open(sys.argv[1]))
