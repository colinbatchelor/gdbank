"""Overwrites the lemmata in a CoNLL-U file based on the form and XPOS."""
import sys
import pyconll
from innealan.acainn import Lemmatizer

corpus = pyconll.load_from_file(sys.argv[1])
l = Lemmatizer()
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            if '-' not in token.id:
                token.lemma = l.lemmatize(token.form, token.xpos)
        clean.write(sentence.conll())
        clean.write('\n\n')
