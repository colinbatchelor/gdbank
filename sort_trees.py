import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
with open(sys.argv[2],'w') as clean:
    for sentence in sorted(corpus, key= lambda x: x.id):
        clean.write(sentence.conll())
        clean.write('\n\n')

