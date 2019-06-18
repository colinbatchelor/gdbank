import numpy as np
import os
import sys
import pyconll
from collections import Counter

corpus = pyconll.load_from_file(sys.argv[1])
dict = {"all":[], "fp":[], "f":[], "ns":[], "n":[], "pw":[]}
files = Counter()
for sentence in corpus:
    file = sentence.id.split('_')[0]
    files[file] +=1
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

for subcorpus in dict:
    print("%s: %s trees, longest: %s, mean: %s, shortest: %s" %
          (subcorpus, len(dict[subcorpus]), max([len(s) for s in dict[subcorpus]]),
           sum([len(s) for s in dict[subcorpus]])/len(dict[subcorpus]),
           min([len(s) for s in dict[subcorpus]])))

for file in files.most_common():
    print(file)
