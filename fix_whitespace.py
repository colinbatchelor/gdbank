import re
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
trees = []
with open(sys.argv[2],'w') as clean:
    for sentence in corpus:
        for token in sentence:
            if token.xpos in ["Fe", "Fg", "Fi", "Fu", "Fz"] or token.form == "...":
                sentence[int(token.id) - 2].misc['SpaceAfter'] = ["No"]
            if re.match("[hnt]-", token.form) or token.form == "(" or re.match("dh['’]", token.form) or token.xpos == "Fq":
                sentence[int(token.id) - 1].misc['SpaceAfter'] = ["No"]                
        clean.write(sentence.conll())
        clean.write('\n\n')

