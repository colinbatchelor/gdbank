import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as conversations,open(sys.argv[3],'w') as others:
    for sentence in corpus:
        if sentence.id.startswith('c') or sentence.id.startswith('p0'):
            conversations.write(sentence.conll())
            conversations.write('\n\n')
        else:
            others.write(sentence.conll())
            others.write('\n\n')
