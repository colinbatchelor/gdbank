import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as strings:
    for sentence in corpus:
        strings.write(sentence.id)
        strings.write('\n')
        strings.write(" ".join([t.form for t in sentence]))
        strings.write('\n')

