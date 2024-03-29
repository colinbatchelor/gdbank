import re
import sys
import pyconll
from gd_tools.acainn import Features

f = Features()

corpus = pyconll.load_from_file(sys.argv[1])
trees = []

with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        print(sentence.id)
        prev_token = None
        for token in sentence:
            if "-" not in token.id and prev_token is not None:
                token.feats = f.feats(token.xpos, token.feats, prev_token.xpos)
            prev_token = token
        clean.write(sentence.conll())
        clean.write('\n\n')
