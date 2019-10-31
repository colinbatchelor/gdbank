import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            if token.head != "0":
                if token.upos == "AUX" and token.xpos != "Wp-i-3":
                    token.deprel = "cop"
                if token.upos == "INTJ":
                    token.deprel = "discourse"
                if token.upos == "PUNCT":
                    token.deprel = "punct"
                if token.upos == "PART" and token.deprel == "mark" and token.xpos != "Uv":
                    token.deprel = "mark:prt"
                if token.xpos == "Uv":
                    token.deprel = "case:voc"
                if token.xpos == "Ncsmv" or token.xpos == "Ncsfv":
                    token.deprel = "vocative"
                if token.xpos == "Nv":
                    token.upos = "NOUN"
                if token.upos == "DET" and token.xpos.startswith("Dp") and token.deprel == "det":
                    next_token = sentence[int(token.id)]
                    if next_token.xpos != "Nv":
                        if next_token.upos == "NOUN":
                            token.deprel = "nmod:poss"
                if token.deprel == "csubj:cop":
                    prev_token = sentence[int(token.id) - 2]
                    if prev_token.xpos == "Q-r":
                        token.deprel = "csubj:cleft"
            if token.head == "0":
                token.deprel = "root"
        clean.write(sentence.conll())
        clean.write('\n\n')
