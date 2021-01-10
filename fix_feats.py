import re
import sys
import pyconll
from innealan.acainn import Features

f = Features()

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
stops = ["Q-s"]
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        print(sentence.id)
        for token in sentence:
            if "-" not in token.id and token.xpos not in stops:
                if token.xpos in ["Xfe","Xf"]:
                    token.feats = {"Foreign":["Yes"]}
                elif token.xpos.startswith("Dp") and token.deprel == "det":
                    next_token = sentence[int(token.id)]
                    if next_token.xpos.startswith("Nc"):
                        token.deprel = "nmod:poss"
                    else:
                        token.deprel = "obj"
                elif token.xpos.startswith('T'):
                    token.feats = f.feats_det(token.xpos)
                elif token.xpos == "Nv":
                    token.upos = "NOUN"
                    if token.id != "1":
                        prev_token = [sentence[str(int(token.id) - 1)]][0]
                        token.feats = f.feats_nv(prev_token.xpos, token.xpos)
                elif token.xpos.startswith("V"):
                    token.feats = f.feats_verb(token.xpos)
                elif token.xpos.startswith("Pp") or token.xpos.startswith("Dp") or token.upos == "PRON":
                    print(token.conll())
                    token.feats = f.feats_pron(token.xpos)
                elif token.xpos.startswith("Pr"):
                    token.upos = "ADP"
                    token.feats = f.feats_pron(token.xpos)
                elif token.xpos == "Um":
                    token.upos = "ADP"
                elif token.xpos.startswith("A"):
                    token.feats = f.feats_adj(token.xpos)
                elif token.xpos.startswith("Sap") or token.xpos.startswith("Spp"):
                    token.feats = f.feats_prep(token.xpos)
                elif token.xpos.startswith("U") or token.xpos.startswith("Q"):
                    token.feats = f.feats_part(token.xpos)
                elif token.xpos.startswith("W"):
                    print(token.form)
                    token.feats = f.feats_cop(token.xpos)
        clean.write(sentence.conll())
        clean.write('\n\n')
