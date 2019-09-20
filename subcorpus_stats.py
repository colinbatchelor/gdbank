import numpy as np
import os
import sys
import pyconll
from collections import Counter

dict = {"all":[], "fp":[], "f":[], "ns":[], "n":[], "pw":[], "c":[], "p":[], "s":[]}
files = Counter()
tokens = Counter()

for corpusfile in sys.argv[1:]:
    corpus = pyconll.load_from_file(corpusfile)
    for sentence in corpus:
        file = sentence.id.split('_')[0]
        files[file] +=1
        tokens[file] += len(sentence)
        dict["all"].append(sentence)
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
        elif sentence.id.startswith('c'):
            dict["c"].append(sentence)
        elif sentence.id.startswith('p'):
            dict["p"].append(sentence)
        elif sentence.id.startswith('s'):
            dict["s"].append(sentence)

for subcorpus in dict:
    size = len(dict[subcorpus])
    print("%s: %s trees, longest: %s, mean: %s, shortest: %s, total %s" %
          (subcorpus, size,
           max([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in dict[subcorpus]])/len(dict[subcorpus]) if size >0 else 0,
           min([len(s) for s in dict[subcorpus]]) if size >0 else 0,
           sum([len(s) for s in dict[subcorpus]]) if size>0 else 0))

for file in files.most_common():
    print("%s %s" % (file, tokens[file[0]]))
