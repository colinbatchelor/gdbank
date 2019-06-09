import sys
import pyconll

tenses = {"p":"Pres", "s":"Past", "f":"Fut"}
genders = {"m":"Masc", "f":"Fem"}
numbers = {"s":"Sing", "p":"Plur"}

def get_verb_feats(xpos):
    result = {}
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

def get_pron_feats(xpos):
    result = {}
    result["Person"] = [xpos[2]]
    result["Number"] = [numbers[xpos[3]]]
    if len(xpos) > 4 and xpos[4] in genders:
        result["Gender"] = [genders[xpos[4]]]
    if xpos.endswith('e'):
        result["PronType"] = ['Emp']
    return result

def get_adj_feats(xpos):
    result = {}
    if xpos == "Apc":
        result["Degree"] = ["Cmp,Sup"]
    return result

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            if "-" not in token.id:
                if token.xpos.startswith("V"):
                    token.feats = get_verb_feats(token.xpos)
                elif token.xpos.startswith("Pp") or token.xpos.startswith("Dp"):
                    token.feats = get_pron_feats(token.xpos)
                elif token.xpos.startswith("Pr"):
                    token.upos = "ADP"
                    token.feats = get_pron_feats(token.xpos)
                elif token.xpos == "Px":
                    token.feats = {"Reflex":["Yes"]}
                elif token.xpos == "Apc":
                    token.feats = get_adj_feats(token.xpos)
        clean.write(sentence.conll())
        clean.write('\n\n')