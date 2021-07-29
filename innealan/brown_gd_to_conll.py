"""
Converts a text file in Brown format into CoNLL-U.
Assumes Scottish Gaelic.
"""
import csv
import os
import re
import sys
from collections import namedtuple
from acainn import Lemmatizer
from acainn import Features
from pyconll.unit import Conll

Split = namedtuple("split", "form1 upos1 xpos1 form2 upos2 xpos2")

class Splitter:
    """Splits multiword (in the UD sense) tokens"""
    def __init__(self):
        folder = os.path.dirname(__file__)
        split_path = os.path.join(folder, "resources", "splits.csv")
        self.splittables = ["Spa-s", "Spa-p", "Spr", "Spv"]
        self.splits = {}
        with open(split_path) as split_file:
            reader = csv.reader(split_file)
            next(reader)
            for row in reader:
                form, xpos, form1, upos1, xpos1, form2, upos2, xpos2 = row
                self.splits[(form, xpos)] = Split(form1, upos1, xpos1, form2, upos2, xpos2)

    def get_split(self, form, xpos):
        """Returns a list of tuples (consider named-tupling this)"""
        return self.splits[(form, xpos)]

    def xpos_to_be_split(self, xpos):
        """Is the xpos in the splittable list from our file?"""
        return xpos in self.splittables

def classify_line(genre, first_xpos, closing_punct):
    '''SOBIE except we never return O'''
    splits = ['Nn', 'V-p', 'V-s', 'V-f', 'V-h', 'Pd', 'Wp-i', 'Wp-in', 'Wp-i-x', 'V-s0', 'Vm-2p',
              'Vm-3', 'Rg', 'Uo', 'Xsc', 'I', 'Uq', 'Rs', 'Qn', 'Qq', 'Ncsmn', 'Ncsfn']

    if genre == "oral":
        if first_xpos in splits and closing_punct:
            return "S"
        if first_xpos in splits:
            return "B"
        if closing_punct:
            return "E"
        return "I"
    if closing_punct:
        return "E"
    return "I"

def retokenise_line(tokens, genre):
    """Splits Brown tokens into forms and xpos and assigns SOBIE"""
    parsed = [parse_brown_token(t) for t in tokens]
    forms = [p[0] for p in parsed]
    xposes = [p[1] for p in parsed]
    complete = "." in forms or "?" in forms or "!" in forms
    classification = classify_line(genre, xposes[0], complete)
    return parsed, classification

def output_token(token_id, form, lemma, upos, xpos):
    '''rewrite with namedtuple'''
    deprels = {"DET": "det", "PART": "mark:prt", "ADP": "fixed"}
    splitter = Splitter()

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
        new_forms = form.split("_")
        new_deprel = "flat" if xpos.startswith("Nt") else \
            "flat:name" if xpos.startswith("Nn") else "fixed"
        for i, new_form in enumerate(new_forms):
            result.append(output_word(str(token_id + i), new_form, lemma, upos, xpos, "_" if i == 0 else str(token_id), "_" if i == 0 else new_deprel))

    elif splitter.xpos_to_be_split(xpos):
        split = splitter.get_split(form.lower().replace("‘","'").replace("’","'"), xpos)
        deprel = deprels[split.upos2]
        head = str(token_id) if deprel == "fixed" else str(token_id + 2)

        return [output_word(f"{token_id}-{token_id + 1}", form),
                output_word(str(token_id), split.form1, split.form1, split.upos1, split.xpos1, str(token_id + 2), "case"),
                output_word(str(token_id + 1), split.form2, split.form2, split.upos2, split.upos2, head, deprel)], True

    elif xpos == "Csw":
        return [output_word(f"{token_id}-{token_id + 1}", form),
                output_word(f"{token_id}", "ma", "ma", "SCONJ", "Cs", str(token_id + 2), "mark"),
                output_word(f"{token_id + 1}", "is", "is", "AUX", "Wp-i", str(token_id + 2), "cop")], True

    elif xpos == "Wp-i-3":
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(str(token_id), "is", "is", "AUX", "Wp-i"))
        if form.endswith("e"):
            result.append(output_word(f"{token_id + 1}", "e", "e", "PRON", "Pp3sm", str(token_id), "fixed"))
        else:
            result.append(output_word(f"{token_id + 1}", "i", "i", "PRON", "Pp3sf", str(token_id), "fixed"))

    elif xpos == "Wp-i-x":
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 2}", form))
        result.append(output_word(f"{token_id}", "is", "is", "AUX", "Wp-i", "_", "cop"))
        result.append(output_word(f"{token_id + 1}", "an", "an", "ADP", "Sp", f"{token_id}", "fixed"))
        result.append(output_word(f"{token_id + 2}", "e", "e", "PRON", "Pp3sm", f"{token_id}", "fixed"))

    elif xpos.startswith("Pr"):
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(f"{token_id}", lemma, lemma, "ADP", "Sp", f"{token_id + 1}", "case"))
        result.append(output_word(f"{token_id + 1}", pron[xpos[2:]], pron[xpos[2:]], "PRON", xpos.replace("r", "p")))

    elif xpos.startswith("Sap"):
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(f"{token_id}", "ag", "ag", "PART", "Sa", f"{token_id + 2}", "case"))
        result.append(output_word(f"{token_id + 1}", poss_pron[xpos[3:]], poss_pron[xpos[3:]], "PRON", xpos.replace("Sa", "D"), str(token_id + 2), "obj"))

    elif xpos.startswith("Spp"):
        is_mwt = True
        result.append(output_word(f"{token_id}-{token_id + 1}", form))
        result.append(output_word(str(token_id), lemma, lemma, "ADP", "Sp", str(token_id + 2), "case"))
        result.append(output_word(str(token_id + 1), poss_pron[xpos[3:]], poss_pron[xpos[3:]], "PRON", xpos.replace('Sp','D'), str(token_id + 2), "nmod:poss"))
    else:
        return [output_word(str(token_id), form, lemma, upos, xpos)], False
    return result, is_mwt

def output_word(token_id, form, lemma = "_", upos = "_", xpos = "_", head = "_", deprel = "_"):
    """
    In UD a token may consist of several 'words'.
    We follow this for things like 'agam' which we split into 'aig' and 'mi'.
    """
    return "\t".join([token_id, form, lemma, upos, xpos, "_", head, deprel, "_", "_"])

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

def parse_brown_token(brown_token):
    """Takes a Brown-format token and returns form and xpos"""
    subtokens = brown_token.split("/")[0:2] # in case of multiple tags
    if len(subtokens) == 1:
        return subtokens[0], "__MW" # special cases for multiword expressions like "ann an"
    return subtokens[0], subtokens[1].strip("*")

def process_file(brown_file, filename):
    """Does the initial conversion to CoNLL-U format."""
    lemmatizer = Lemmatizer()
    result = []
    file_id = filename.replace(".txt", "")
    subcorpus = re.match(file_id, "^\\D*")
    if subcorpus in ["c", "p", "s"] or file_id in ["n06", "n07", "n08", "n09", "n10"]:
        genre = "oral"
    else:
        genre = "written"
    sent_id = 0

    for sentence in split_sentences(brown_file, genre):
        conllu_tokens = [s for s in process_sentence(sentence, lemmatizer)]
        if len(conllu_tokens) > 0:
            result.append(f"# sent_id = {file_id}_{sent_id}")
            result.extend(conllu_tokens)
            result.append('')
            sent_id += 1
    return result

def split_sentences(brown_file, genre):
    """Splits a file of Brown-format text into sentences."""
    result = []
    for line in brown_file:
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

def process_sentence(sentence, lemmatizer):
    """Generator which takes form/xpos pairs and yields CoNLLU-L tokens"""
    replacements = {
        "Aq-sfq": "Aq-sfd",
        "Ncfsg": "Ncsfg",
        "sa": "Sa",
        "tdsm": "Tdsm"
    }
    carry = ""
    token_id = 1
    for form, xpos in sentence:
        if xpos == "Uo" and form != "a":
            carry = form
        elif xpos == "Sa" and form == "'":
            carry = form
        else:
            xpos = replacements.get(xpos, xpos)
            upos = xpos_to_upos(xpos)
            # use fix_feats.py to populate the feats column
            lemma = lemmatizer.lemmatize(form, xpos)
            conllu_tokens, is_mwt = output_token(token_id, carry + form, lemma, upos, xpos)
            length = len(conllu_tokens) - 1 if is_mwt else len(conllu_tokens)
            token_id = token_id + length
            carry = ""
            for conllu_token in conllu_tokens:
                yield conllu_token

def add_comments(sentence):
    """Provide CoNLL-U metadata."""
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
    """Use Features to assign UD features to token"""
    features = Features()
    result = []
    for sentence in corpus:
        result.extend(add_comments(sentence))
        prev_token = None
        for token in sentence:
            if "-" not in token.id:

                if prev_token is not None:
                    token.feats = features.feats(token.xpos, prev_token.xpos)
                else:
                    token.feats = features.feats(token.xpos)

            result.append(token.conll())
            prev_token = token
        result.append("")
    return Conll(result)

def add_text(corpus):
    """Extract continuous text from forms."""
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
