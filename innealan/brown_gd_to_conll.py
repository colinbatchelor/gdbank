from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

# See http://universaldependencies.org/u/pos/index.html
upostag_mapping_simple = { 'A':'ADJ', 'D':'DET', 'F':'PUNCT', 'I':'INTJ', 'M':'NUM', 'P':'PRON', 'Q':'PART', 'R':'ADV', 'T':'DET', 'V':'VERB', 'W':'AUX', 'X':'X', 'Y':'NOUN'  }
upostag_mapping_harder = { 'Cc':'CCONJ', 'Cs':'SCONJ', 'Nc':'NOUN', 'Nf':'ADP', 'Nt':'PROPN', 'Nn':'PROPN', 'nn':'PROPN', 'Nv':'VERB', 'Sa':'PART', 'Sp':'ADP', 'SP':'ADP', 'Ua':'PART', 'Uc':'PART', 'Uf':'NOUN', 'Ug':'PART', 'Um':'PART', 'Uo':'PART', 'Up':'NOUN', 'Uq':'PRON', 'Uv':'PART' }

def arcosg_to_upostag(tag):
    return upostag_mapping_simple[tag[0]] if tag[0] in upostag_mapping_simple else upostag_mapping_harder[tag[0] + tag[1]]

id = 1
with open(sys.argv[1]) as f:
    for line in f:
        tokens = line.strip().split()
        carry = ''
        for t in tokens:
            if '/' in t:
                form,tag = t.split('/')[0:2] # in case of multiple tags
                if tag == 'Xsc':
                    id = 1
                    print ()
                try:
                    upostag = arcosg_to_upostag(tag)
                except:
                    eprint(tag)
                print('%s\t%s\t_\t%s\t%s\t_\t_\t_\t_\t_' % (id, carry + form, upostag, tag))
                carry = ''
                if form == '.':
                    id = 1
                    print()
                else:
                    id = id + 1
            else:
                carry = carry + t + '_' 
