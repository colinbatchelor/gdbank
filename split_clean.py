import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as clean,open(sys.argv[3],'w') as dirty:
    for sentence in corpus:
        ROOT = False
        for token in sentence:
            if token.deprel == "ROOT":
                ROOT = True
        if not ROOT:
            clean.write(sentence.conll())
            clean.write('\n')
            clean.write('\n')
        else:
            dirty.write(sentence.conll())
            dirty.write('\n')
            dirty.write('\n')
