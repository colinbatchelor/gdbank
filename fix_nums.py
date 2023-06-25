import re
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []

with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        prev_token = None
        for token in sentence:
            if token.upos == "NUM":
                if token.lemma == "cheud" and token.xpos == "Mo":
                    token.lemma = "ciad"
                if len(token.lemma) > 1 and token.lemma[1] == "h" and token.xpos != "Xfe":
                    token.lemma = token.lemma[0] + token.lemma[2:]
                if token.xpos == "Mc":
                    token.feats["NumType"] = ["Card"]
                if token.xpos == "Mn":
                    token.feats["NumType"] = ["Card"]
                if token.xpos == "Mo":
                    token.feats["NumType"] = ["Ord"]
                if token.xpos == "Mr":
                    token.feats["NumForm"] = ["Roman"]
                    token.feats["NumType"] = ["Ord"]
                else:
                    if re.match("^[0-9]", token.form):
                        token.feats["NumForm"] = ["Digit"]
                    else:
                        token.feats["NumForm"] = ["Word"]
            prev_token = token
        clean.write(sentence.conll())
        clean.write('\n\n')
