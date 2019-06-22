import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            if token.xpos == "Nv":
                token.upos = "NOUN"
            if token.upos == "DET" and token.xpos.startswith("Dp") and token.deprel == "det":
                next_token = sentence[int(token.id)]
                if next_token.xpos != "Nv":
                    if next_token.upos == "NOUN":
                        token.deprel = "nmod:poss"
        clean.write(sentence.conll())
        clean.write('\n\n')
