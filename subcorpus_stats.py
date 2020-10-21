"""ARCOSG-specific tool to count words in subcorpora."""
import csv
import sys
from collections import Counter
import pyconll

result = {"all":[], "fp":[], "f":[], "ns":[], "n":[], "pw":[], "c":[], "p":[], "s":[]}
lengths = {"all":35928 + 33720,
           "fp":5710 + 3179, "f":8042,
           "ns":4644 + 3503,
           "n":4535 + 4577, "pw":4261 + 3474,
           "c":3346 + 6781,
           "p":2591 + 6067,
           "s":2799 + 6139}
files = Counter()
tokens = Counter()

def get_subcorpus(sent_id):
    """Determines subcorpus from id"""
    if sent_id.startswith('fp'):
        return "fp"
    elif sent_id.startswith('f'):
        return "f"
    elif sent_id.startswith('ns'):
        return "ns"
    elif sent_id.startswith('n'):
        return "n"
    elif sent_id.startswith('pw'):
        return "pw"
    elif sent_id.startswith('c'):
        return "c"
    elif sent_id.startswith('p'):
        return "p"
    elif sent_id.startswith('s'):
        return "s"
    return "x"

with open(sys.argv[1], 'w') as g:
    writer = csv.writer(g)
    writer.writerow(['id', 'subcorpus', 'len'])
    for corpusfile in sys.argv[2:]:
        corpus = pyconll.load_from_file(corpusfile)
        for sentence in corpus:
            file = sentence.id.split('_')[0]
            files[file] +=1
            tokens[file] += len(sentence)
            result["all"].append(sentence)
            sc = get_subcorpus(sentence.id)
            result[sc].append(sentence)
            writer.writerow([sentence.id, sc, len(sentence)])

for subcorpus in result:
    size = len(result[subcorpus])
    print("%s: %s trees, longest: %s, mean: %.2f, shortest: %s, total %s, %.2f percent complete" %
          (subcorpus, size,
           max([len(s) for s in result[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in result[subcorpus]])/len(result[subcorpus]) if size > 0 else 0,
           min([len(s) for s in result[subcorpus]]) if size > 0 else 0,
           sum([len(s) for s in result[subcorpus]]) if size > 0 else 0,
           100*sum([len(s) for s in result[subcorpus]])/lengths[subcorpus]))
