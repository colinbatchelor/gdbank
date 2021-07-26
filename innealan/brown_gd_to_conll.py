import csv
import os
import re
import sys
from acainn import Lemmatizer
from acainn import Features
from pyconll.unit import Conll

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

def feats_to_string(feats: dict) -> str:
    if feats == {}:
        return '_'
    return '|'.join(['%s=%s' % (t, list(feats[t])[0]) for t in sorted(feats)])

class Splitter:
    def __init__(self):
        folder = os.path.dirname(__file__)
        split_path = os.path.join(folder, "resources", "splits.csv")
        self.splits = {}
        with open(split_path) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                form, xpos, form1, upos1, xpos1, form2, upos2, xpos2 = row
                self.splits[(form, xpos)] = [(form1, upos1, xpos1), (form2, upos2, xpos2)]

    def get_split(self, form, xpos):
        return self.splits[(form, xpos)]

    def to_be_split(self, xpos):
        return xpos in ["Spa-s", "Spa-p", "Spr", "Spv"]

def classify_line(genre, first_xpos, closing_punct):
    '''SOBIE except we never return O'''
    splits = ['Nn', 'V-p', 'V-s', 'V-f', 'V-h', 'Pd', 'Wp-i', 'Wp-in', 'Wp-i-x', 'V-s0', 'Vm-2p', 'Vm-3', 'Rg', 'Uo', 'Xsc', 'I', 'Uq', 'Rs', 'Qn', 'Qq', 'Ncsmn', 'Ncsfn'] 
    no_splits = ["Cc", "Q-r", 'Wpdia', 'Qa', 'Um']
    if genre == "oral":
        if xposes[0] in splits and closing_punct:
            return "S"
        elif xposes[0] in splits:
            return "B"
        elif closing_punct:
            return "E"
        else:
            return "I"
    else:
        if closing_punct:
            return "E"
        else:
            return "I"

def retokenise_line(tokens, genre):
    parsed = [parse_token(t) for t in tokens]
    forms = [p[0] for p in parsed]
    xposes = [p[1] for p in parsed]
    complete = "." in forms or "?" in forms or "!" in forms
    classification = classify_line(genre, xposes[0], complete)
    return parsed, classification

def output_token(token_id, form, lemma, upos, xpos, feats):
    '''rewrite with namedtuple'''
    deprels = {"DET":"det", "PART":"mark:prt", "ADP":"fixed"}
    s = Splitter()

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

    result = []
    is_mwt = False
    if "_" in form:
        new_forms = form.split('_')
        length = len(new_forms)
        new_deprel = "flat" if xpos.startswith("Nt") else \
            "flat:name" if xpos.startswith("Nn") else "fixed"
        for i, new_form in enumerate(new_forms):
            result.append(output_word(str(token_id + i), new_form, lemma, upos, xpos, feats, "_" if i == 0 else str(token_id), "_" if i == 0 else new_deprel))

    elif s.to_be_split(xpos):
        split = s.get_split(form.lower().replace("‘","'").replace("’","'"), xpos)

        deprel = deprels[split[1][1]]
        head = str(token_id) if deprel == "fixed" else str(token_id + 2)

        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(str(token_id), split[0][0], split[0][0], split[0][1], split[0][2], "_", str(token_id + 2), "case"))
        result.append(output_word(str(token_id + 1), split[1][0], split[1][0], split[1][1], split[1][2], "_", head, deprel))

    elif xpos == "Csw":
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(f"{token_id}", "ma", "ma", "SCONJ", "Cs", feats, str(token_id + 2), "mark"))
        result.append(output_word(f"{token_id + 1}", "is", "is", "AUX", "Wp-i", feats, str(token_id + 2), "cop"))

    elif xpos == "Wp-i-3":
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(str(token_id), "is", "is", "AUX", "Wp-i"))
        if form.endswith("e"):
            result.append(output_word(f"{token_id + 1}", "e", "e", "PRON", "Pp3sm", "_", str(token_id), "fixed"))
        else:
            result.append(output_word(f"{token_id + 1}", "i", "i", "PRON", "Pp3sf", "_", str(token_id), "fixed"))

    elif xpos == "Wp-i-x":
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 2}", form))
        result.append(output_word(f"{token_id}", "is", "is", "AUX", "Wp-i", "_", "_", "cop"))
        result.append(output_word(f"{token_id + 1}", "an", "an", "ADP", "Sp", "_", f"{token_id}", "fixed"))
        result.append(output_word(f"{token_id + 2}", "e", "e", "PRON", "Pp3sm", "_", f"{token_id}", "fixed"))

    elif xpos.startswith("Pr"):
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(f"{token_id}", lemma, lemma, "ADP", "Sp", feats, f"{token_id + 1}", "case"))
        result.append(output_word(f"{token_id + 1}", pron[xpos[2:]], pron[xpos[2:]], "PRON", xpos.replace("r", "p")))

    elif xpos.startswith("Sap"):
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(f"{token_id}", "ag", "ag", "PART", "Sa", "_", f"{token_id + 2}", "case"))
        result.append(output_word(f"{token_id + 1}", poss_pron[xpos[3:]], poss_pron[xpos[3:]], "PRON", xpos.replace("Sa", "D"), "_", str(token_id + 2), "obj"))

    elif xpos.startswith("Spp"):
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(str(token_id), lemma, lemma, "ADP", "Sp", "_", str(token_id + 2), "case"))
        result.append(output_word(str(token_id + 1), poss_pron[xpos[3:]], poss_pron[xpos[3:]], "PRON", xpos.replace('Sp','D'), "_", str(token_id + 2), "nmod:poss"))
    else:
        result = [output_word(str(token_id), form, lemma, upos, xpos, feats)]
    return result, is_mwt

def output_word(token_id, form, lemma = "_", upos = "_", xpos = "_", feats = "_", head = "_", deprel = "_"):
    """In UD a token may consist of several 'words'. We follow this for things like 'agam'."""
    if feats != "_":
        print(f"{token_id} {form} {lemma} {upos} {xpos} {feats} {head}")
        dijfidj
    return "\t".join([token_id, form, lemma, upos, xpos, feats, head, deprel, "_", "_"])

def xpos_to_upos(xpos):
    """Mappings from http://universaldependencies.org/u/pos/index.html"""
    upos_mapping_simple = {
        'A':'ADJ', 'D':'DET', 'F':'PUNCT', 'I':'INTJ', 'M':'NUM', 'P':'PRON',
        'Q':'PART', 'R':'ADV', 'T':'DET', 'V':'VERB', 'W':'AUX', 'X':'X', 'Y':'NOUN'  }
    upos_mapping_harder = {
        'Cc':'CCONJ', 'Cs':'SCONJ', 'Nc':'NOUN', 'Nf':'ADP', 'Nt':'PROPN',
        'Nn':'PROPN', 'nn':'PROPN', 'Nv':'NOUN', 'Sa':'PART', 'Sp':'ADP', 'SP':'ADP',
        'Ua':'PART', 'Uc':'PART', 'Uf':'NOUN', 'Ug':'PART', 'Um':'PART', 'Uo':'PART',
        'Up':'NOUN', 'Uq':'PRON', 'Uv':'PART', "__": "__" }
    return upos_mapping_simple[xpos[0]] if xpos[0] in upos_mapping_simple \
        else upos_mapping_harder[xpos[0] + xpos[1]]

def parse_token(t):
    subtokens = t.split("/")[0:2] # in case of multiple tags
    if len(subtokens) == 1:
        return subtokens[0], "__MW" # special cases for multiword expressions like "ann an"
    else:
        return subtokens[0], subtokens[1].strip("*")

def process_file(f, filename):
    l = Lemmatizer()
    result = []
    result.append('# file = %s' % filename)
    file_id = filename.replace(".txt", "")
    subcorpus = re.match(file_id, "^\\D*")
    if subcorpus in ["c", "p", "s"] or file_id in ["n06", "n07", "n08", "n09", "n10"]:
        genre = "oral"
    else:
        genre = "written"
    sent_id = 0

    for sentence in split_sentences(f, genre):
        lines = [s for s in process_sentence(sentence, l)]
        if len(lines) > 0:
            result.append(f"# sent_id = {file_id}_{sent_id}")
            result.extend(lines)
            result.append('')
            sent_id += 1
    return result
    
def split_sentences(f, genre):
    result = []
    for line in f:
        tokens = line.strip().split()
        retokenised = retokenise_line(tokens, genre)

        if genre == "written":
            result.extend(retokenised[0])
            if retokenised[1] == "E":
                yield result
                result = []
        if genre == "oral":
            if retokenised[1] == "S":
                yield result
                result = retokenised[0]
    yield result

def process_sentence(sentence, l):
    replacements = {
        "Aq-sfq": "Aq-sfd",
        "Ncfsg": "Ncsfg",
        "sa": "Sa",
        "tdsm": "Tdsm"
    }
    result = []
    carry = ""
    token_id = 1
    for form, xpos in sentence:
        if xpos == "Uo" and form != "a":
            carry = form
        elif xpos == "Sa" and form == "'":
            carry = form
        else:
            if xpos in replacements:
                xpos = replacements[xpos]
            upos = xpos_to_upos(xpos)
            # use fix_feats.py to populate the feats column
            feats = "_"
            lemma = l.lemmatize(form, xpos)
            lines, is_mwt = output_token(token_id, carry + form, lemma, upos, xpos, feats)
            length = len(lines) - 1 if is_mwt else len(lines)
            token_id = token_id + length
            carry = ""
            for line in lines:
                yield line

def add_comments(sentence):
    result = []
    if sentence.meta_present("newdoc"):
        result.append('# newdoc = %s' % sentence.meta_value("newdoc"))
    if sentence.meta_present('comment'):
        result.append('# comment = %s' % sentence.meta_value('comment'))
    result.append('# sent_id = %s' % sentence.id)
    if sentence.meta_present('speaker'):
        result.append('# speaker = %s' % sentence.meta_value('speaker'))
    if sentence.meta_present('text'):
        result.append('# text = %s' % sentence.meta_value('text'))
    return result

def add_feats(corpus):
    f = Features()
    result = []
    for sentence in corpus:
        result.extend(add_comments(sentence))
        prev_token = None
        for token in sentence:
            if "-" not in token.id:
                try:

                    if prev_token is not None:
                        token.feats = f.feats(token.xpos, prev_token.xpos)
                    else:
                        token.feats = f.feats(token.xpos)
                except:
                    eprint(token.xpos)
            result.append(token.conll())
            prev_token = token
        result.append("")
    return Conll(result)

def add_text(corpus):
    result = []
    for sentence in corpus:
        result.extend(add_comments(sentence))
        mws = []
        for mwt in [t.id for t in sentence if "-" in t.id]:
            mws.extend([*mwt.split("-")])
        surfaces = [(t.id, t.form, t.xpos) for t in sentence if t.id not in mws]
        
        text = " ".join([s[1] for s in surfaces]).replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace("( ", "(").replace(" )",")").replace("  ", " ")
        result.append(f"# text = {text}")
        for i, surface in enumerate(surfaces):
            if surface[1] in [",", ".", "?", ")"] or surface[2] == "Fz":
                sentence[surfaces[i - 1][0]].misc["SpaceAfter"] = ["No"]
            if surface[1] == "(" or surface[2] == "Fq":
                sentence[surfaces[i][0]].misc["SpaceAfter"] = ["No"]
        for token in sentence:
            result.append(token.conll())
        result.append("")
    return Conll(result)

files = os.listdir(sys.argv[1])
for filename in files:
    if filename.startswith(sys.argv[2]):
        with open(os.path.join(sys.argv[1], filename)) as file:
            lines = process_file(file, filename)

            c = Conll(lines)
            with_text = add_text(c)
            with_feats = add_feats(with_text)
            print(with_feats.conll())
