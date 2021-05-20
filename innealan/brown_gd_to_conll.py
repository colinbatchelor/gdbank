import os
import sys
from acainn import Lemmatizer
from acainn import Features

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

def feats_to_string(feats: dict) -> str:
    if feats == {}:
        return '_'
    return '|'.join(['%s=%s' % (t, list(feats[t])[0]) for t in sorted(feats)])

def output_token(token_id, form, lemma, upos, xpos, feats):
    to_be_split = ["Spa-s", "Spa-p", "Spr", "Spv"]
    deprels = {"DET":"det", "PART":"mark:prt", "ADP":"fixed"}
    splits = {
    
        ("as","Spa-s"): [("anns", "ADP", "Sp"), ("an", "ADP", "Sp")],
        ("bhon","Spa-s"): [("bho", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("chun","Spa-s"): [("gu", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("den","Spa-s"): [("de", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("dhan","Spa-s"): [("do", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("dhen","Spa-s"): [("de", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("don","Spa-s"): [("do", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("fon","Spa-s"): [("fo", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("gun","Spa-s"): [("gu", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("man","Spa-s"): [("mu", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("mun","Spa-s"): [("mu", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("on", "Spa-s"): [("o", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("o'n", "Spa-s"): [("o", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("ron", "Spa-s"): [("ro", "ADP", "Sp"), ("an", "DET", "Tds")],
        ("'sa", "Spa-s"): [("anns", "ADP", "Sp"),("an", "ADP", "Sp")],
        ("'sa'", "Spa-s"): [("anns", "ADP", "Sp"),("an", "ADP", "Sp")],
        ("sa", "Spa-s"): [("anns", "ADP", "Sp"),("an", "ADP", "Sp")],
        ("sa'", "Spa-s"): [("anns", "ADP", "Sp"),("an", "ADP", "Sp")],
        ("'san", "Spa-s"): [("anns", "ADP", "Sp"), ("an", "ADP", "Sp")],
        ("san", "Spa-s"): [("anns", "ADP", "Sp"), ("an", "ADP", "Sp")],
        ("tron", "Spa-s"): [("tro", "ADP", "Sp"), ("an", "DET", "Tds")],
        
        ("'sna", "Spa-p"): [("anns", "ADP", "Sp"), ("na", "ADP", "Sp")],
        ("sna", "Spa-p"): [("anns", "ADP", "Sp"), ("na", "ADP", "Sp")],
    
        ("bhon", "Spv"): [("bho", "ADP", "Sp"), ("an", "PART", "Qq")],
        ("dam","Spv"): [("do", "ADP", "Sp"), ("am", "PART", "Qq")],
        ("dham","Spv"): [("do", "ADP", "Sp"), ("am", "PART", "Qq")],
        ("dhe","Spv"): [("de", "ADP", "Sp"), ("am", "PART", "Qq")],
        ("do'm","Spv"): [("do", "ADP", "Sp"), ("am", "PART", "Qq")],
        ("don", "Spv"): [("do", "ADP", "Sp"), ("an", "PART", "Qq")],
        ("sa","Spv"): [("anns", "ADP", "Sp"), ("a", "PART", "Q-r")],
        ("'sa","Spv"): [("anns", "ADP", "Sp"), ("a", "PART", "Q-r")],
        ("'sam","Spv"): [("anns", "ADP", "Sp"), ("am", "PART", "Qq")],
        ("sam","Spv"): [("anns", "ADP", "Sp"), ("am", "PART", "Qq")],
        ("'san","Spv"): [("anns", "ADP", "Sp"), ("an", "PART", "Qq")],
        ("san","Spv"): [("anns", "ADP", "Sp"), ("an", "PART", "Qq")]
    }
    pron = {
        "1s": "mi", "1s--e": "mise",
        "2s": "thu", "2s--e": "thusa",
        "3sm": "e", "3sm-e": "esan",
        "3sf": "i", "3sf-e": "ise",
        "1p": "sinn", "1p--e": "sinne",
        "2p": "sibh", "2p--e": "sibhse",
        "3p": "iad", "3p--e": "iadsan"}
    poss_pron = {
        "1s": "mo", "2s": "do",
        "3sm": "a", "3sf": "a",
        "1p": "ar", "2p": "ur",
        "3p": "an"}

    if '_' in form:
        new_forms = form.split('_')
        length = len(new_forms)
        new_deprel = "flat" if xpos.startswith("Nt") else "flat:name" if xpos.startswith("Nn") else "fixed"
        for i, new_form in enumerate(new_forms):
            print("\t".join([str(token_id + i), new_form, lemma, upos, xpos, feats, "_" if i == 0 else str(token_id), "_" if i == 0 else new_deprel, "_", "_"]))
    elif xpos in to_be_split:
        split = splits[(form.lower().replace("‘","'").replace("’","'"), xpos)]

        deprel = deprels[split[1][1]]
        head = str(token_id) if deprel == "fixed" else str(token_id + 2)

        output_word(f"{token_id}-{token_id + 1}", form)
        output_word(str(token_id), split[0][0], split[0][0], split[0][1], split[0][2], "_", str(token_id + 2), "case")
        output_word(str(token_id + 1), split[1][0], split[1][0], split[1][1], split[1][2], "_", head, deprel)
        length = 2
    elif xpos == "Csw":
        output_word(f"{token_id}-{token_id + 1}", form)
        output_word(f"{token_id}", "ma", "ma", "SCONJ", "Cs", feats, str(token_id + 2), "mark")
        output_word(f"{token_id + 1}", "is", "is", "AUX", "Wp-i", feats, str(token_id + 2), "cop")
        length = 2
    elif xpos == "Wp-i-3":
        output_word(f"{token_id}-{token_id + 1}", form)
        output_word(str(token_id), "is", "is", "AUX", "Wp-i")
        if form.endswith("e"):
            output_word(f"{token_id + 1}", "e", "e", "PRON", "Pp3sm", "_", str(token_id), "fixed")
        else:
            output_word(f"{token_id + 1}", "i", "i", "PRON", "Pp3sf", "_", str(token_id), "fixed")
        length = 2
    elif xpos == "Wp-i-x":
        output_word(f"{token_id}-{token_id + 2}", form)
        print("\t".join([f"{token_id}", "is", "is", "AUX", "Wp-i", "_", "_", "cop", "_", "_"]))
        print("\t".join([f"{token_id + 1}", "an", "an", "ADP", "Sp", "_", f"{token_id}", "fixed", "_", "_"]))
        print("\t".join([f"{token_id + 2}", "e", "e", "PRON", "Pp3sm", "_", f"{token_id}", "fixed", "_", "_"]))
        length = 3
    elif xpos.startswith("Pr"):
        output_word(f"{token_id}-{token_id + 1}", form)
        output_word(f"{token_id}", lemma, lemma, "ADP", "Sp", feats, f"{token_id + 1}", "case")
        output_word(f"{token_id + 1}", pron[xpos[2:]], pron[xpos[2:]], "PRON", xpos.replace("r", "p"), feats)
        length = 2
    elif xpos.startswith("Sap"):
        output_word(f"{token_id}-{token_id + 1}", form)
        output_word(f"{token_id}", "ag", "ag", "PART", "Sa", f"{token_id + 2}", "case")
        output_word(f"{token_id + 1}", poss_pron[xpos[3:]], poss_pron[xpos[3:]], "PRON", xpos.replace("Sa", "D"), str(token_id + 2), "obj")
        length = 2
    elif xpos.startswith("Spp"):
        output_word(f"{token_id}-{token_id + 1}", form)
        output_word(str(token_id), lemma, lemma, "ADP", "Sp", "_", str(token_id + 2), "case")
        output_word(str(token_id + 1), poss_pron[xpos[3:]], poss_pron[xpos[3:]], "PRON", xpos.replace('Sp','D'), str(token_id + 2), "nmod:poss")
        length = 2
    else:
        output_word(str(token_id), form, lemma, upos, xpos, feats)
        length = 1
    return length

def output_word(token_id, form, lemma = "_", upos = "_", xpos = "_", feats = "_", head = "_", deprel = "_"):
    """In UD a token may consist of several 'words'. We follow this for things like 'agam'."""
    print("\t".join([token_id, form, lemma, upos, xpos, feats, head, deprel, "_", "_"]))

def xpos_to_upos(xpos):
    """Mappings from http://universaldependencies.org/u/pos/index.html"""
    upos_mapping_simple = {
        'A':'ADJ', 'D':'DET', 'F':'PUNCT', 'I':'INTJ', 'M':'NUM', 'P':'PRON',
        'Q':'PART', 'R':'ADV', 'T':'DET', 'V':'VERB', 'W':'AUX', 'X':'X', 'Y':'NOUN'  }
    upos_mapping_harder = {
        'Cc':'CCONJ', 'Cs':'SCONJ', 'Nc':'NOUN', 'Nf':'ADP', 'Nt':'PROPN',
        'Nn':'PROPN', 'nn':'PROPN', 'Nv':'NOUN', 'Sa':'PART', 'Sp':'ADP', 'SP':'ADP',
        'Ua':'PART', 'Uc':'PART', 'Uf':'NOUN', 'Ug':'PART', 'Um':'PART', 'Uo':'PART',
        'Up':'NOUN', 'Uq':'PRON', 'Uv':'PART' }
    return upos_mapping_simple[xpos[0]] if xpos[0] in upos_mapping_simple \
        else upos_mapping_harder[xpos[0] + xpos[1]]

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
                    length = output_token(token_id, carry + form, lemma, upos, xpos, feats)
                    carry = ""
                    if form in ['.','?','!']:
                        token_id = 1
                        sent_id +=1
                        print()
                        print('# sent_id = %s_%s' % (file_id, sent_id))
                    else:
                        token_id = token_id + length
            else:
                carry = carry + t + '_'
        start_line = False
    print()

files = os.listdir(sys.argv[1])
for filename in files:
    if not filename.startswith('s'):
        with open(os.path.join(sys.argv[1], filename)) as file:
            process_file(file, filename)
