import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])

for sentence in corpus:
    print(sentence.id)
