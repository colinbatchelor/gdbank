import numpy as np
from sklearn.model_selection import KFold
import os
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
loaded_corpus = []
for sentence in corpus:
    loaded_corpus.append(sentence)
kf = KFold(n_splits = 10)
split = 1
for train, test in kf.split(loaded_corpus):
    if not os.path.exists('xv'):
        os.makedirs('xv')
    with open(os.path.join('xv', 'train%s.conll' % split),'w') as f, open(os.path.join('xv', 'test%s.conll' % split),'w') as g:
        for sentence in [loaded_corpus[t] for t in train]:
            f.write(sentence.conll())
            f.write('\n\n')
        for sentence in [loaded_corpus[t] for t in test]:
            g.write(sentence.conll())
            g.write('\n\n')
    split = split + 1
