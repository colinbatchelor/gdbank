import sys
import pyconll
from innealan.acainn import Lemmatizer


corpus = pyconll.load_from_file(sys.argv[1])
l = Lemmatizer()
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            token.lemma = l.lemmatize(token.form, token.xpos)
        clean.write(sentence.conll())
        clean.write('\n\n')
