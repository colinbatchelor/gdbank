"""Sorts trees in a conll file by sentence id."""
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        print(sentence.id)
    for sentence in sorted(corpus, key= lambda x: x.id):
        clean.write(sentence.conll())
        clean.write('\n\n')
