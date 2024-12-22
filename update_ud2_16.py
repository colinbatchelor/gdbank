"""
Applies updates for Scottish Gaelic CONLL files for Universal Dependencies release 2.16.
"""
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []

def ud_words(ud_sentence, condition = lambda x: True):
    """
    Returns the 'words' and their predecessors in the UD sense by rejecting multiword tokens.
    """
    prev_word = None
    for word in [s for s in ud_sentence if not s.is_multiword()]:
        # the condition may only apply to UD words
        if condition(word):
            yield word, prev_word
        prev_word = word

advtype_mapping = { "Rs": "Loc", "Rt": "Tim", "Rg": "Man", "Uf": "Man", "Uq": "Man", "Xsi": "Loc" }

with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        cop_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel == "cop")]
        cleft_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel in ["csubj:cleft", "csubj:outer"])]
        case_heads = { t.head: t.form for t, _ in ud_words(sentence, lambda t: t.deprel == "case") }
        for word, prev_word in ud_words(sentence, lambda t: t):
            if word.id in cop_heads and word.id in cleft_heads:
                if word.upos == "ADJ":
                    word.feats["CleftType"] = ["Adj"]
                elif word.upos == "ADV":
                    word.feats["CleftType"] = ["Adv"]
                elif word.upos in ["NOUN", "NUM", "PART", "PRON", "PROPN"]:
                    if word.upos == "PART" and "Pat" not in word.feats["PartType"]:
                        print(f"{sentence.id} {word.id} {word.form} {word.upos} {word.feats}")
                    elif word.id in case_heads:
                        word.feats["CleftType"] = ["Obl"]
                    else:
                        word.feats["CleftType"] = ["Nom"]
                elif word.upos == "VERB":
                    word.feats["CleftType"] = ["Verb"]
                else:
                    print(f"{sentence.id} {word.id} {word.form} {word.upos}")
            if word.id in cop_heads and word.id not in cleft_heads:
                word.feats.pop("CleftType", None)
            if word.upos == "ADV":
                if word.xpos not in advtype_mapping:
                    print(sentence.id, word.id, word.form, word.upos, word.xpos)
                else:
                    word.feats["AdvType"] = [advtype_mapping[word.xpos]]
            if word.xpos == "Nt":
                word.upos = "PROPN"
                word.feats["NounType"] = ["Top"]
                if word.deprel == "flat":
                    word.deprel = "flat:name"
                    word.misc["FlatType"] = ["Top"]
            if word.xpos == "Q-s":
                """
                https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/34
                """
                word.deprel = "mark"
            if prev_word is not None:
                if word.deprel == "fixed" and prev_word.deprel != "fixed":
                    if "ExtPos" not in prev_word.feats:
                        prev_word.feats["ExtPos"] = [prev_word.upos]

        clean.write(sentence.conll())
        clean.write('\n\n')
