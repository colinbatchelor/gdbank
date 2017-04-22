from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

# See http://universaldependencies.org/u/pos/index.html
upostag_mapping_simple = { 'A':'ADJ', 'D':'DET', 'F':'PUNCT', 'M':'NUM', 'P':'PRON', 'Q':'PART', 'R':'ADV', 'S':'ADP', 'T':'DET', 'U':'PART', 'V':'VERB', 'W':'AUX', 'X':'X'  }
upostag_mapping_harder = { 'Cc':'CCONJ', 'Cs':'SCONJ', 'Nc':'NOUN', 'Nf':'ADP', 'Nt':'PROPN', 'Nn':'PROPN', 'Nv':'VERB' }

def arcosg_to_upostag(tag):
    return upostag_mapping_simple[tag[0]] if tag[0] in upostag_mapping_simple else upostag_mapping_harder[tag[0] + tag[1]]

id = 1
with open(sys.argv[1]) as f:
    for line in f:
        # assume that any in-token spaces have been converted to underlines
        tokens = line.strip().split()
        for t in tokens:
            try:
                form,tag = t.split('/')
                upostag = arcosg_to_upostag(tag)
                print('%s\t%s\t_\t%s\t%s\t_\t_\t_\t_\t_' % (id, form, upostag, tag))
                if form == '.':
                    id = 1
                    print()
                else:
                    id = id + 1
            except:
                # print any unannotated tokens to stderr
                eprint(t)
            
