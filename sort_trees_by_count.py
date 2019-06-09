import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
for sentence in sorted(corpus, key= len)[:10]:
    print("%s %s" % (sentence.id, len(sentence)))
