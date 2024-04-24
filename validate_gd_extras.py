"""Checks for Gaelic-specific things that aren't covered by the standard UD validation tools."""
import sys
import pyconll

def read_fixed():
    """
    Returns a dictionary of lemmata keyed by surface.
    The lemmata are n - 1 and the surface is n.
    """

    allowed = {}
    with open("fixed.gd") as fixed:
        for phrase in fixed:
            tokens = phrase.split()
            if len(tokens) > 3:
                if tokens[3] in allowed:
                    allowed[tokens[3]].append(tokens[2])
                else:
                    allowed[tokens[3]] = [tokens[2]]
            if len(tokens) > 2:
                if tokens[2] in allowed:
                    allowed[tokens[2]].append(tokens[1])
                else:
                    allowed[tokens[2]] = [tokens[1]]
            if tokens[1] in allowed:
                allowed[tokens[1]].append(tokens[0])
            else:
                allowed[tokens[1]] = [tokens[0]]
    return allowed

def check_fixed(sentence, score):
    """Checks words linked by `fixed` against a list."""
    allowed = read_fixed()
    for token, prev_token in ud_words(sentence, lambda t: t.deprel == "fixed"):
        norm_token_form = token.form.lower().replace("‘", "'").replace("’", "'")
        norm_prev_token_form = prev_token.form.lower().replace("‘", "'").replace("’", "'")
        if norm_token_form not in allowed:
            score +=1
            print(f"E {sentence.id} {token.id} '{token.form}' not in fixed list")
        elif norm_prev_token_form not in allowed[norm_token_form]:
            score +=1
            print(f"E {sentence.id} {token.id} '{prev_token.form} {token.form}' not in fixed list")
    return score

def check_misc(sentence, score):
    """Checks the MISC column."""
    for token, _ in ud_words(sentence, lambda t: t.lemma in ["[Name]", "[Placename]"]):
        if "Anonymised" not in token.misc:
            score += 1
            print(f"E {sentence.id} {token.id} Anonymised=Yes missing from MISC column")
    return score

def check_others(sentence, score):
    """Checks for things that don't fit in anywhere else."""
    for token, prev_token in ud_words(sentence, lambda t: t.form in ["ais"] and t.upos != "NOUN"):
        score +=1
        print(f"E {sentence.id} {token.id} UPOS for 'ais' should be NOUN")

    for token, prev_token in ud_words(sentence, lambda t: t.xpos == t.upos and t.feats == {}):
        score +=1
        print(f"E {sentence.id} {token.id} XPOS {token.xpos} should not match UPOS if feats is empty")

    for token, prev_token in ud_words(sentence):
        if token.xpos == "Px" and token.deprel not in ["nmod", "fixed", "obl"]:
            score += 1
            print(f"E {sentence.id} {token.id} {token.form} should be nmod or obl (or fixed)")
        if token.xpos == "Up" and token.deprel != "flat:name" and prev_token is not None and prev_token.xpos == "Nn":
            score += 1
            print(f"E {sentence.id} {token.id} Patronymic should be flat:name")
        if token.deprel.startswith("mark") and token.upos not in ["PART", "SCONJ"]:
            score += 1
            print(f"E {sentence.id} {token.id} mark should only be for PART or SCONJ")
        if token.deprel == "flat" and token.xpos not in ["Mn", "Nt"]:
            score += 1
            print(f"E {sentence.id} {token.id} should be flat:name or flat:foreign")
    return score

def check_ranges(sentence, score, warnings):
    """
    Checks that deprels that can only go in one direction go in that direction and
    does some sanity checks on the length.
    """
    leftward_only = ["acl:relcl", "flat", "fixed"]
    rightward_only = ["case", "cc", "cop", "mark", "nummod"]
    short_range = {"compound": 2 ,"det": 3, "fixed": 2, "flat": 4}

    for token, prev_token in ud_words(sentence):
        deprel_range = abs(int(token.id) - int(token.head))
        if token.deprel in leftward_only and int(token.head) > int(token.id):
            warnings += 1
            print(f"W {sentence.id} {token.id} {token.deprel} goes wrong way (usually) for gd")
        if token.deprel in rightward_only and\
           int(token.head) < int(token.id) and\
           prev_token.xpos != "Uo" and\
               token.form not in ["ceud", "fichead"]:
            score += 1
            print(f"E {sentence.id} {token.id} {token.deprel} goes wrong way for gd")

        if token.deprel in short_range and\
           deprel_range > short_range[token.deprel] and\
           (prev_token is not None and token.deprel != prev_token.deprel):
            if deprel_range < short_range[token.deprel] + 3:
                warnings += 1
                code = "W"
            else:
                score += 1
                code = "E"
            print(f"{code} {sentence.id} {token.id} Too long a range ({deprel_range}) for {token.deprel}")
        if token.deprel in ["nsubj", "obj"] and\
           token.upos not in ["NOUN", "PART", "PRON", "PROPN", "NUM", "SYM", "X"] and\
           int(token.head) < int(token.id):
            score +=1
            print(f"E {sentence.id} {token.id} nsubj and (rightward) obj should only be for NOUN, PART, PRON, PROPN, NUM, SYM or X")

    return score, warnings

def check_heads_for_upos(sentence, score):
    """Checks that for example obl is headed by something verbal and nmod something nominal."""
    head_ids = {}
    heads = {
        "obl": ["VERB", "ADJ", "ADV"],
        "obl:smod": ["VERB", "ADJ", "ADV"],
        "obl:tmod": ["VERB", "ADJ", "ADV"],
        "nmod": ["NOUN", "NUM", "PRON", "PROPN", "SYM", "X"],
        "appos": ["NOUN", "NUM", "PRON", "PROPN", "SYM", "X"]
    }
    for token, _ in ud_words(sentence, lambda t: t.deprel in heads):
        head_ids[int(token.head)] = (token.deprel, token.id)

    for token, _ in ud_words(sentence, lambda t: int(t.id) in head_ids and "VerbForm" not in t.feats):
        actual = token.upos
        correct = heads[head_ids[int(token.id)][0]]
        if actual not in correct:
            score +=1
            print(f"E {sentence.id} {token.id} {head_ids[int(token.id)][1]} head of {head_ids[int(token.id)]} must be one of ({', '.join(correct)}) not {actual}")
        if token.form == "ais":
            score +=1
            print(f"E {sentence.id} {token.id} 'ais' should not be a head")
    return score

def check_reported_speech(sentence, score):
    """Checks that reported speech is a ccomp not parataxis"""
    head_ids = {}
    target_ids = {}
    for token, _ in ud_words(sentence, lambda t: t.deprel == "parataxis"):
        head_ids[int(token.head)] = (token.deprel, token.id)
        target_ids[int(token.id)] = token.deprel
    for token, _ in ud_words(sentence, lambda t: (int(t.id) in head_ids or int(t.id) in target_ids) and (t.upos == "VERB" or "VerbForm" in t.feats)):
        if int(token.id) in head_ids:
            print(f"{sentence.id} {token.id}<- {token.lemma}")
        else:
            print(f"{sentence.id} {token.id}-> {token.lemma}")
    return score
    

def check_target_deprels(sentence, score):
    """Checks that for example cc is the leaf of a conj."""
    target_ids = {}
    targets = {
        "cc": ["conj"],
        "case": ["dep", "obl", "advmod", "nmod", "nummod", "xcomp", "xcomp:pred", "ccomp",\
                 "acl", "acl:relcl", "conj", "csubj:cop"]
    }
    for token, _ in ud_words(sentence, lambda t: t.deprel in targets):
        target_ids[int(token.head)] = token.deprel

    for token, _ in ud_words(sentence, lambda t: int(t.id) in target_ids):
        actual = token.deprel
        correct = [*targets[target_ids[int(token.id)]], "root", "parataxis", "reparandum",\
                   "appos", "orphan"]
        if actual not in correct:
            score +=1
            print(f"E {sentence.id} {token.id} target of {target_ids[int(token.id)]} must be one of ({', '.join(correct)}) not {actual}")
    return score

def check_target_upos(sentence, score):
    """Checks that for example amod is ADJ"""
    targets = {
        "amod": ["ADJ"],
       #  "flat:name": ["PART", "PROPN"], # consider when obl/nmod fixed
        "nmod": ["NOUN", "NUM", "PART", "PRON", "PROPN", "X"]
    }
    for token, _ in ud_words(sentence,\
                             lambda t: t.deprel in targets and t.upos not in targets[t.deprel]):
        score += 1
        print(f"E {sentence.id} {token.id} UPOS for {token.deprel} must be one of ({', '.join(targets[token.deprel])}) not {token.upos}")
    return score

def ud_words(ud_sentence, condition = lambda x: True):
    """Returns the 'words' and their predecessors in the UD sense by rejecting multiword tokens."""
    prev_token = None
    for word_token in [s for s in ud_sentence if not s.is_multiword()]:
        # the condition may only apply to UD words
        if condition(word_token):
            yield word_token, prev_token
        prev_token = word_token

def check_relatives(sentence, score):
    """Checks the possibilities for relative particles"""
    heads = {}
    for token, prev_token in ud_words(sentence,\
                                      lambda t: t.xpos in ["Q-r", "Qnr"] and\
                                      t.deprel == "mark:prt"):
        message_stub = f"E {sentence.id} {token.id} deprel for '{token.form}'"
        if prev_token is not None:
            if prev_token.upos == "ADP":
                score += 1
                print(f"E {message_stub} should be obl, nmod or xcomp:pred")
            elif prev_token.lemma in ["carson", "ciamar", "cuin'"]:
                score += 1
                print(f"E {message_stub} should be advmod or xcomp:pred")
            elif prev_token.upos not in ["CCONJ", "SCONJ"]:
                heads[token.head] = []
                score += 1
                print(f"E {message_stub} should usually be nsubj or obj")
    for token,_ in ud_words(sentence, lambda t: t.head in heads):
        heads[token.head].append(token.deprel)
    if heads != {}:
        for head in heads:
            print(f"{sentence.id} {head} {heads[head]} suggestion: {suggest_relative_deprel(heads[head])}")
    return score

def suggest_relative_deprel(deprels):
    """Suggests a deprel for the relative particle 'a'."""
    if "nsubj" not in deprels:
        return "nsubj"
    return "obj"

def check_bi(sentence, score):
    """Checks that xcomp:pred is set up properly for bi."""
    ids = {}
    deprels = {}
    upos = {}
    bi_pred_candidates = ["advmod", "obl", "xcomp", "obl:smod"]
    bi_ids = [t.id for t,_ in ud_words(sentence, lambda t: t.lemma == "bi")]
    allowed_deprels = ["xcomp:pred"]

    for token, _ in ud_words(sentence,\
                             lambda t: t.head in bi_ids and\
                             t.deprel in bi_pred_candidates or t.deprel in allowed_deprels):
        if token.head in ids:
            ids[token.head].append(token.id)
            deprels[token.head].append(token.deprel)
            upos[token.head].append(token.upos)
        else:
            ids[token.head] = [token.id]
            deprels[token.head] = [token.deprel]
            upos[token.head] = [token.upos]
    for key in deprels:
        stub = f"E {sentence.id} {key}"
        if "xcomp:pred" not in deprels[key] and "ccomp" not in deprels[key]:
            print(f"{stub} bi should have an xcomp:pred among {list(zip(ids[key], deprels[key]))}")
            score += 1
        if "obj" in deprels[key] and "PART" not in upos[key]:
            # check what Irish does about obj of bi.
            score += 1
            print(f"E {stub} bi should not have obj")
    return score

def check_passive(sentence, score):
    """
    Checks for the deprecated pattern where rach is the head and the infinitive is the dependent.

    The correct pattern is for the infinitive to be the head and rach to be connected with aux:pass.
    Exceptions are made for where somebody goes to do something, which is similar to the deprecated
    pattern but not, of course, a passive.

    There is a further pattern rach + aig... + infinitive which is not deprecated but I haven't
    coded in.
    Example n02_026 in test.
    """

    ids = {}
    rach_ids = [t.id for t,_ in ud_words(sentence,\
                                         lambda t: t.lemma == "rach" and t.upos != "NOUN")]

    for token, _ in ud_words(sentence, lambda t: t.head in rach_ids):
        if token.head in ids:
            ids[token.head].append(token.id)
        else:
            ids[token.head] = [token.id]
    for key in ids:
        deprels = [sentence[i].deprel for i in ids[key]]
        if "xcomp" in deprels and "nsubj" not in deprels:
            for token in ids[key]:
                if sentence[token].deprel == "xcomp":
                    message_stub = f"E {sentence.id} {sentence[token].id} '{sentence[token].form}'"
                    print(f"{message_stub} should be the head")
                    score +=1
    return score

def check_clauses(sentence, score, warnings):
    """Checks that mark and mark:prt and ccomp, advcl and acl:relcl work together properly."""
    ids = {}
    deprels = {}
    forms = {}
    feats = {}
    deprels_to_check = ["ccomp", "advcl", "acl:relcl"]

    clause_ids = [t.id for t in sentence if t.deprel in deprels_to_check]
    for token, _ in ud_words(sentence, lambda t: t.head in clause_ids):
        if token.head in ids:
            ids[token.head].append(token.id)
            deprels[token.head].append(token.deprel)
            forms[token.head].append(token.form)
            feats[token.head].append(token.feats)
        else:
            ids[token.head] = [token.id]
            forms[token.head] = [token.form]
            deprels[token.head] = [token.deprel]
            feats[token.head] = [token.feats]
    for key in deprels:
        # mark beats mark:prt
        if 'mark' in deprels[key]:
            if sentence[key].deprel != "advcl":
                warnings += 1
                print(f"W {sentence.id} {key} deprel should be advcl")
        elif 'mark:prt' in deprels[key]:
            for feat in feats[key]:
                if "PartType" in feat and "Cmpl" in feat["PartType"]\
                   and sentence[key].deprel != "ccomp":
                    warnings += 1
                    print(f"W {sentence.id} {key} deprel should be ccomp")
                if "PronType" in feat and "Rel" in feat["PronType"]\
                   and sentence[key].deprel != "acl:relcl":
                    warnings += 1
                    print(f"W {sentence.id} {key} deprel should be acl:relcl")

    return score, warnings

def validate_corpus(corpus):
    """Prints a number of errors and a number of warnings."""
    total_score = 0
    total_warnings = 0

    old_id = ""
    for tree in corpus:
        doc_id = tree.id.split("_")[0]
        if doc_id != old_id and not tree.meta_present("newdoc id"):
            print(f"E newdoc id declaration missing for {tree.id}")
            total_score += 1
        old_id = doc_id
        total_score = check_others(tree, total_score)
        total_score = check_misc(tree, total_score)
        total_score = check_fixed(tree, total_score)
        total_score, total_warnings = check_ranges(tree, total_score, total_warnings)
        total_score = check_heads_for_upos(tree, total_score)
        total_score = check_target_deprels(tree, total_score)
        total_score = check_target_upos(tree, total_score)
        total_score = check_bi(tree, total_score)
        total_score = check_reported_speech(tree, total_score)
        total_score = check_passive(tree, total_score)
        total_score = check_relatives(tree, total_score)
        total_score, total_warnings = check_clauses(tree, total_score, total_warnings)

    if total_score == 0:
        print("*** PASSED ***")
    else:
        print("*** FAILED *** with %s error%s" % (total_score, "s" if total_score > 1 else ""))

validate_corpus(pyconll.load_from_file(sys.argv[1]))
