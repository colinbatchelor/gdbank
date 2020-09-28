import csv
import os
import sys
import pyconll
from collections import Counter

dict = {"all":[], "fp":[], "f":[], "ns":[], "n":[], "pw":[], "c":[], "p":[], "s":[]}
lengths = {"all":63775,"fp":8320,"f":7372,"ns":7795,"n":8223,"pw":7096,"c":9074,"p":7874,"s":8021}
files = Counter()
tokens = Counter()

with open(sys.argv[1], 'w') as g:
    writer = csv.writer(g)
    writer.writerow(['id', 'subcorpus', 'len'])
    for corpusfile in sys.argv[2:]:
        corpus = pyconll.load_from_file(corpusfile)
        for sentence in corpus:
            file = sentence.id.split('_')[0]
            files[file] +=1
            tokens[file] += len(sentence)
            dict["all"].append(sentence)
            if sentence.id.startswith('fp'): sc = "fp"
            elif sentence.id.startswith('f'): sc = "f"
            elif sentence.id.startswith('ns'): sc = "ns"
            elif sentence.id.startswith('n'): sc = "n"
            elif sentence.id.startswith('pw'): sc = "pw"
            elif sentence.id.startswith('c'): sc = "c"
            elif sentence.id.startswith('p'): sc = "p"
            elif sentence.id.startswith('s'): sc = "s"
            dict[sc].append(sentence)
            writer.writerow([sentence.id, sc, len(sentence)])

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
    print(f"{file[0]}: {tree_count} trees, {token_count} tokens (avg. length {token_count/tree_count:0.4})")
