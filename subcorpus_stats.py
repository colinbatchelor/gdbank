import numpy as np
import os
import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
dict = {"fp":[], "f":[], "ns":[], "n":[], "pw":[]}
for sentence in corpus:
    if sentence.id.startswith('fp'):
        dict["fp"].append(sentence)
    elif sentence.id.startswith('f'):
        dict["f"].append(sentence)
    elif sentence.id.startswith('ns'):
        dict["ns"].append(sentence)
    elif sentence.id.startswith('n'):
        dict["n"].append(sentence)
    elif sentence.id.startswith('pw'):
        dict["pw"].append(sentence)

for subcorpus in dict:
    print(subcorpus)
    print(len(dict[subcorpus]))
    print(max([len(s) for s in dict[subcorpus]]))
    print(sum([len(s) for s in dict[subcorpus]])/len(dict[subcorpus]))
    print(min([len(s) for s in dict[subcorpus]]))
