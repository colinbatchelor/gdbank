import re
import sys
import pyconll

tenses = {"p":"Pres", "s":"Past", "f":"Fut"}
genders = {"m":"Masc", "f":"Fem"}
numbers = {"s":"Sing", "p":"Plur"}
parttypes_u = {"a":"Ad", "c":"Comp", "g":"Inf", "v":"Voc", "p":"Pat", "o":"Num"}
parttypes_q = {"Qn":"Cmpl", "Q-r":"Vb", "Qnr":"Vb", "Qq":"Vb", "Qnm":"Vb"}
polartypes_q = {"Qn":"Neg", "Qnr":"Neg", "Qnm":"Neg"}
prontypes_q = {"Q-r":"Rel", "Qnr":"Rel", "Qq":"Int"}
moodtypes_q = {"q":"Int"}

def get_adj_feats(xpos):
    result = {}
    if xpos == "Apc":
        result["Degree"] = ["Cmp,Sup"]
    return result

def get_nv_feats(token, prev_token):
    result = {}
    if prev_token.xpos.startswith("Sa") or prev_token.xpos.startswith("Sp"):
        result["VerbForm"] = ["Vnoun"]
    elif prev_token.xpos == "Ug" or prev_token.xpos.startswith("Dp"):
        result["VerbForm"] = ["Inf"]
    else:
        print("%s %s %s" % (token.xpos, prev_token.form, prev_token.xpos))
    return result

def get_part_feats(xpos):
    result = {}
    if xpos[1] in parttypes_u:
        result["PartType"] = [parttypes_u[xpos[1]]]
    if xpos[1] in moodtypes_q:
        result["Mood"] = [moodtypes_q[xpos[1]]]
    if xpos in parttypes_q:
        result["PartType"] = [parttypes_q[xpos]]
        if xpos in polartypes_q:
            result["Polarity"] = [polartypes_q[xpos]]
        if xpos in prontypes_q:
            result["PronType"] = [prontypes_q[xpos]]
    if xpos == "Q--s":
        result["Tense"] = ["Past"]
    if xpos == "Qnm":
        result["Mood"] = ["Imp"]
    return result

def get_pron_feats(xpos):
    result = {}
    result["Person"] = [xpos[2]]
    result["Number"] = [numbers[xpos[3]]]
    if len(xpos) > 4 and xpos[4] in genders:
        result["Gender"] = [genders[xpos[4]]]
    if xpos.endswith('e'):
        result["PronType"] = ['Emp']
    return result

def get_verb_feats(xpos):
    result = {}
    if '0' in xpos:
        result["Person"] = ["0"]
    elif '1' in xpos:
        result["Person"] = ["1"]
    elif '2' in xpos:
        result["Person"] = ["2"]
    if len(xpos) == 2: # this may well be a mistagging
        result["Mood"] = ["Imp"]
        return result
    if xpos[2] in tenses:
        result["Tense"] = [tenses[xpos[2]]]
    if xpos[2] == "h":
        result["Mood"] = ["Cnd"]
    if xpos[1] == "m":
        result["Mood"] = ["Imp"]
    return result

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
stops = ["Q-s"]
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            if "-" not in token.id and token.xpos not in stops:
                if token.xpos.startswith("Dp") and token.deprel == "det":
                    next_token = sentence[int(token.id)]
                    if next_token.xpos.startswith("Nc"):
                        token.deprel = "nmod:poss"
                    else:
                        token.deprel = "obj"
                
                if token.xpos == "Nv":
                    token.upos = "NOUN"
                    if token.id != "1":
                        token.feats = get_nv_feats(token, sentence[str(int(token.id) - 1)])
                elif token.xpos.startswith("V"):
                    token.feats = get_verb_feats(token.xpos)
                elif token.xpos.startswith("Pp") or token.xpos.startswith("Dp"):
                    token.feats = get_pron_feats(token.xpos)
                elif token.xpos.startswith("Pr"):
                    token.upos = "ADP"
                    token.feats = get_pron_feats(token.xpos)
                elif token.xpos == "Px":
                    token.feats = {"Reflex":["Yes"]}
                elif token.xpos == "Um":
                    token.upos = "ADP"
                elif token.xpos == "Apc":
                    token.feats = get_adj_feats(token.xpos)
                elif token.xpos.startswith("U") or token.xpos.startswith("Q"):
                    token.feats = get_part_feats(token.xpos)
        clean.write(sentence.conll())
        clean.write('\n\n')
