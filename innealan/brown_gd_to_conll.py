import os
import sys
from acainn import Lemmatizer
from acainn import Features

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

# See http://universaldependencies.org/u/pos/index.html
upos_mapping_simple = {
    'A':'ADJ', 'D':'DET', 'F':'PUNCT', 'I':'INTJ', 'M':'NUM', 'P':'PRON',
    'Q':'PART', 'R':'ADV', 'T':'DET', 'V':'VERB', 'W':'AUX', 'X':'X', 'Y':'NOUN'  }
upos_mapping_harder = {
    'Cc':'CCONJ', 'Cs':'SCONJ', 'Nc':'NOUN', 'Nf':'ADP', 'Nt':'PROPN',
    'Nn':'PROPN', 'nn':'PROPN', 'Nv':'NOUN', 'Sa':'PART', 'Sp':'ADP', 'SP':'ADP',
    'Ua':'PART', 'Uc':'PART', 'Uf':'NOUN', 'Ug':'PART', 'Um':'PART', 'Uo':'PART',
    'Up':'NOUN', 'Uq':'PRON', 'Uv':'PART' }

def xpos_to_upos(xpos):
    return upos_mapping_simple[xpos[0]] if xpos[0] in upos_mapping_simple \
        else upos_mapping_harder[xpos[0] + xpos[1]]

def output_line(token_id, form, lemma, upos, xpos, feats):
    if '_' in form:
        new_forms = form.split('_')
        new_deprel = "flat" if xpos.startswith("Nt") else "flat:name" if xpos.startswith("Nn") else "fixed"
        for i,new_form in enumerate(new_forms):
            print("\t".join([str(token_id + i), new_form, lemma, upos, xpos, feats, "_" if i == 0 else str(token_id), "_" if i == 0 else new_deprel, "_", "_"]))
    else:
        print("\t".join([str(token_id), form, lemma, upos, xpos, feats, "_", "_", "_", "_"]))    

def process_file(f, filename):
    l = Lemmatizer()
    replacements = {
        "Aq-sfq": "Aq-sfd",
        "Ncfsg": "Ncsfg",
        "sa": "Sa",
        "tdsm": "Tdsm"}
    print('# file = %s' % filename)
    file_id = filename.replace(".txt","")
    token_id = 1
    start_line = True
    sent_id = 0

    for line in f:
        line = line.replace("na b'/ Uc", "na b'/Uc").replace("//Fb", "(slash)/Fb")
        tokens = line.strip().split()
        if len(tokens) > 0 and start_line:
            print('# sent_id = %s_%s' % (file_id, sent_id))            
        carry = ''
        for t in tokens:
            if '/' in t:
                form, xpos = t.split('/')[0:2] # in case of multiple tags
        
                xpos = xpos.strip('*')
                if xpos == "Uo" and form != "a":
                    carry = form
                else:
                    if xpos in replacements:
                        xpos = replacements[xpos]
                    if xpos == 'Xsc':
                        token_id = 1
                        if not start_line:
                            print()
                            sent_id +=1
                            print('# sent_id = %s_%s' % (file_id, sent_id))
                    try:
                        upos = xpos_to_upos(xpos)
                    except:
                        eprint(t)
                    # use fix_feats.py to populate the feats column
                    feats = '_'
                    lemma = l.lemmatize(form, xpos)
                    output_line(token_id, carry + form, lemma, upos, xpos, feats)
                    carry = ""
                    if form in ['.','?','!']:
                        token_id = 1
                        sent_id +=1
                        print()
                        print('# sent_id = %s_%s' % (file_id, sent_id))
                    else:
                        token_id = token_id + 1
            else:
                carry = carry + t + '_'
        start_line = False
    print()

files = os.listdir(sys.argv[1])
for filename in files:
    if not filename.startswith('s'):
        with open(os.path.join(sys.argv[1], filename)) as file:
            process_file(file, filename)
