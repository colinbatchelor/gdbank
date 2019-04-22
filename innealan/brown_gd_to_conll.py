from __future__ import print_function
import os
import sys
from acainn import Features

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

# See http://universaldependencies.org/u/pos/index.html
upostag_mapping_simple = { 'A':'ADJ', 'D':'DET', 'F':'PUNCT', 'I':'INTJ', 'M':'NUM', 'P':'PRON', 'Q':'PART', 'R':'ADV', 'T':'DET', 'V':'VERB', 'W':'AUX', 'X':'X', 'Y':'NOUN'  }
upostag_mapping_harder = { 'Cc':'CCONJ', 'Cs':'SCONJ', 'Nc':'NOUN', 'Nf':'ADP', 'Nt':'PROPN', 'Nn':'PROPN', 'nn':'PROPN', 'Nv':'VERB', 'Sa':'PART', 'Sp':'ADP', 'SP':'ADP', 'Ua':'PART', 'Uc':'PART', 'Uf':'NOUN', 'Ug':'PART', 'Um':'PART', 'Uo':'PART', 'Up':'NOUN', 'Uq':'PRON', 'Uv':'PART' }

def arcosg_to_upostag(tag):
    return upostag_mapping_simple[tag[0]] if tag[0] in upostag_mapping_simple else upostag_mapping_harder[tag[0] + tag[1]]

def process_file(f, filename):
    replacements = {"Aq-sfq":"Aq-sfd","Ncfsg":"Ncsfg","sa":"Sa","tdsm":"Tdsm"}
    print('# file = %s' % filename)
    file_id = filename.replace(".txt","")
    id = 1
    start_line = True
    sent_id = 0
    print('# sent_id = %s_%s' % (file_id, sent_id))
    for line in f:
        line = line.replace("na b'/ Uc", "na b'/Uc").replace("//Fb", "(slash)/Fb")
        tokens = line.strip().split()
        carry = ''
        for t in tokens:
            if '/' in t:
                form,tag = t.split('/')[0:2] # in case of multiple tags
                
                tag = tag.strip('*')
                if tag in replacements:
                    tag = replacements[tag]
                if tag == 'Xsc':
                    id = 1
                    if not(start_line):
                        print()
                        sent_id +=1
                        print('# sent_id = %s_%s' % (file_id, sent_id))
                try:
                    upostag = arcosg_to_upostag(tag)
                except:
                    eprint(t)
                feats = '_'
                try:
                    if tag.startswith('Aq'): feats = features.feats_adj(form, tag)
                    if tag.startswith('Nc') or tag.startswith('Nn-'): feats = features.feats_noun(form, tag)
                except:
                    eprint(t)
                if tag.startswith('Td'): feats = features.feats_det(form, tag)
                print('%s\t%s\t_\t%s\t%s\t%s\t_\t_\t_\t_' % (id, carry + form, upostag, tag, feats))
                carry = ''
                if form == '.':
                    id = 1
                    sent_id +=1
                    print()
                    print('# sent_id = %s_%s' % (file_id, sent_id))
                else:
                    id = id + 1
            else:
                carry = carry + t + '_'
        start_line = False
    print()

features = Features()
files = os.listdir(sys.argv[1])
for filename in files:
    if not filename.startswith('s'):
        with open(os.path.join(sys.argv[1], filename)) as f:
            process_file(f, filename)

