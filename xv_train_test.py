import numpy as np
from sklearn.model_selection import train_test_split
import os
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
loaded_corpus = []
for sentence in corpus:
    loaded_corpus.append(sentence)
for split in range(1,11):
    train, test = train_test_split(loaded_corpus, test_size = 0.1)
    if not os.path.exists('xv'):
        os.makedirs('xv')
    with open(os.path.join('xv', 'train%s.conll' % split),'w') as f, open(os.path.join('xv', 'test%s.conll' % split),'w') as g:
        for sentence in train:
            f.write(sentence.conll())
            f.write('\n\n')
        for sentence in test:
            g.write(sentence.conll())
            g.write('\n\n')
