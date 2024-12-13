import re
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []

def ud_words(ud_sentence, condition = lambda x: True):
    """
    Returns the 'words' and their predecessors in the UD sense by rejecting multiword tokens.
    """
    prev_token = None
    for word_token in [s for s in ud_sentence if not s.is_multiword()]:
        # the condition may only apply to UD words
        if condition(word_token):
            yield word_token, prev_token
        prev_token = word_token

advtype_mapping = { "Rs": "Loc", "Rt": "Tim", "Rg": "Man", "Uf": "Man", "Uq": "Man", "Xsi": "Loc" }

with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        cop_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel == "cop")]
        cleft_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel in ["csubj:cleft", "csubj:outer"])]
        case_heads = { t.head: t.form for t, _ in ud_words(sentence, lambda t: t.deprel == "case") }
        for token, prev_token in ud_words(sentence, lambda t: t):
            if token.id in cop_heads and token.id in cleft_heads:
                if token.upos == "ADJ":
                    token.feats["CleftType"] = ["Adj"]
                elif token.upos == "ADV":
                    token.feats["CleftType"] = ["Adv"]
                elif token.upos in ["NOUN", "NUM", "PART", "PRON", "PROPN"]:
                    if token.upos == "PART" and "Pat" not in token.feats["PartType"]:
                        print(f"{sentence.id} {token.id} {token.form} {token.upos} {token.feats}")
                    elif token.id in case_heads:
                        token.feats["CleftType"] = ["Obl"]
                    else:
                        token.feats["CleftType"] = ["Nom"]
                elif token.upos == "VERB":
                    token.feats["CleftType"] = ["Verb"]
                else:
                    print(f"{sentence.id} {token.id} {token.form} {token.upos}")
            if token.upos == "ADV":
                if token.xpos not in advtype_mapping:
                    print(sentence.id, token.id, token.form, token.upos, token.xpos)
                else:
                    token.feats["AdvType"] = [advtype_mapping[token.xpos]]
            if token.xpos == "Nt":
                token.upos = "PROPN"
                token.feats["NounType"] = ["Top"]
                if token.deprel == "flat":
                    token.deprel = "flat:name"
                    token.misc["FlatType"] = ["Top"]
            if prev_token is not None:
                if token.deprel == "fixed" and prev_token.deprel != "fixed":
                    if "ExtPos" not in prev_token.feats:
                        prev_token.feats["ExtPos"] = [prev_token.upos]

        clean.write(sentence.conll())
        clean.write('\n\n')
