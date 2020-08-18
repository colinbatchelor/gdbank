import numpy as np
import os
import sys
import pyconll
from collections import Counter

dict = {"all":[], "fp":[], "f":[], "ns":[], "n":[], "pw":[], "c":[], "p":[], "s":[]}
lengths = {"all":63775,"fp":8320,"f":7372,"ns":7795,"n":8223,"pw":7096,"c":9074,"p":7874,"s":8021}
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
    print("%s: %s trees, longest: %s, mean: %s, shortest: %s, total %s, %s percent complete" %
          (subcorpus, size,
           max([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in dict[subcorpus]])/len(dict[subcorpus]) if size > 0 else 0,
           min([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           100*sum([len(s) for s in dict[subcorpus]])/lengths[subcorpus]))

for file in files.most_common():
    tree_count = file[1]
    token_count = tokens[file[0]]
    print(f"{file[0]}: {tree_count} trees, {token_count} tokens ({token_count/tree_count:0.4})")
