import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        prev_token = None
        for token in sentence:
            if token.head != "0":
                if token.xpos == "Px" and prev_token.xpos != "Px":
                    token.deprel = "nmod"
            if token.head == "0":
                token.deprel = "root"
            prev_token = token
        clean.write(sentence.conll())
        clean.write('\n\n')
