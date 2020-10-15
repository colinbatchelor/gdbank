import csv
import os
import sys
import pyconll
from collections import Counter

dict = {"all":[], "fp":[], "f":[], "ns":[], "n":[], "pw":[], "c":[], "p":[], "s":[]}
lengths = {"all":35928 + 33720,
           "fp":5710 + 3179, "f":8042,
           "ns":4644 + 3503,
           "n":4535 + 4577, "pw":4261 + 3474,
           "c":3346 + 6781,
           "p":2591 + 6067,
           "s":2799 + 6139}
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
    print("%s: %s trees, longest: %s, mean: %.2f, shortest: %s, total %s, %.2f percent complete" %
          (subcorpus, size,
           max([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in dict[subcorpus]])/len(dict[subcorpus]) if size > 0 else 0,
           min([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in dict[subcorpus]]) if size > 0 else 0,
           100*sum([len(s) for s in dict[subcorpus]])/lengths[subcorpus]))
