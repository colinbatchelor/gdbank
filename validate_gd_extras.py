"""Checks for Gaelic-specific things that aren't covered by the standard UD validation tools."""
import sys
import pyconll

def check_fixed(sentence, score):
    """allowed is a dictionary of lemmata keyed by surface. The lemmata are n - 1 and the surface is n."""
    allowed = {}
    with open("fixed.gd") as f:
        for phrase in f:
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

    prev_token = None
    for token in [s for s in sentence if not s.is_multiword()]:
        if token.deprel == "fixed":
            if token.form.lower().replace("‘", "'").replace("’", "'") not in allowed:
                score +=1
                print(f"E {sentence.id} {token.id} '{token.form}' not in fixed list")
            elif prev_token.form.lower().replace("‘", "'").replace("’", "'") not in allowed[token.form.lower().replace("‘", "'").replace("’", "'")]:
                score +=1
                print(f"E {sentence.id} {token.id} '{prev_token.form} {token.form}' not in fixed list")
        prev_token = token
    return score

def check_misc(sentence, score):
    """Checks for things that don't fit in anywhere else."""
    prev_token = None
    for token in [s for s in sentence if not s.is_multiword()]:

        if token.xpos == token.upos and token.feats == {}:
            score +=1
            print(f"E {sentence.id} {token.id} XPOS {token.xpos} should not match UPOS if feats is empty")
        if token.deprel is not None:
            if token.xpos == "Up" and token.deprel != "flat:name" and prev_token is not None and prev_token.xpos == "Nn":
                score += 1
                print(f"E {sentence.id} {token.id} Patronymic should be flat:name")
            if token.deprel.startswith("mark") and token.upos not in ["PART", "SCONJ"]:
                score += 1
                print(f"E {sentence.id} {token.id} mark should only be for PART or SCONJ")
            if token.deprel == "flat" and token.xpos not in ["Mn", "Nt"]:
                score += 1
                print(f"E {sentence.id} {token.id} should be flat:name or flat:foreign")
        if token.form in ["ais"]:
            if token.upos != "NOUN":
                score +=1
                print(f"E {sentence.id} {token.id} UPOS for 'ais' should be NOUN")
        prev_token = token
    return score

def check_ranges(sentence, score, warnings):
    """Checks that deprels that can only go in one direction go in that direction."""
    leftward_only = ["acl:relcl", "flat", "fixed"]
    rightward_only = ["case", "cc", "cop", "mark", "nummod"]
    short_range = {"compound":2 ,"det":3, "mark:prt":6, "fixed":2, "flat":4}
    prev_token = None
    for token in [s for s in sentence if not s.is_multiword()]:
        deprel_range = abs(int(token.id) - int(token.head))
        if token.deprel in leftward_only and int(token.head) > int(token.id):
            warnings += 1
            print(f"W {sentence.id} {token.id} {token.deprel} goes wrong way (usually) for gd")
        if token.deprel in rightward_only and int(token.head) < int(token.id) and prev_token.xpos != "Uo":
            score += 1
            print(f"E {sentence.id} {token.id} {token.deprel} goes wrong way for gd")

        if token.deprel in short_range and deprel_range > short_range[token.deprel] and (prev_token is not None and token.deprel != prev_token.deprel):
            if deprel_range < short_range[token.deprel] + 3:
                warnings += 1
                code = "W"
            else:
                score += 1
                code = "E"
            print(f"{code} {sentence.id} {token.id} Too long a range ({deprel_range}) for {token.deprel}")
        if token.deprel in ["nsubj", "obj"] and token.upos not in ["NOUN", "PART", "PRON", "PROPN", "NUM", "SYM", "X"] and int(token.head) < int(token.id):
            score +=1
            print(f"E {sentence.id} {token.id} nsubj and (rightward) obj should only be for NOUN, PART, PRON, PROPN, NUM, SYM or X")

        prev_token = token
    return score, warnings

def check_heads(sentence, score):
    """Checks that for example obl is headed by something verbal and nmod something nominal."""
    head_ids = {}
    heads = {
        "obl": ["VERB", "ADJ", "ADV"],
        "obl:smod": ["VERB", "ADJ", "ADV"],
        "obl:tmod": ["VERB", "ADJ", "ADV"],
        "nmod": ["NOUN", "NUM", "PRON", "PROPN", "SYM"]
    }
    for token in [t for t in sentence if t.deprel in heads and not t.is_multiword()]:
        head_ids[int(token.head)] = (token.deprel, token.id)
    for token in [s for s in sentence if not s.is_multiword()]:
        if int(token.id) in head_ids and "VerbForm" not in token.feats:
            actual = token.upos
            correct = heads[head_ids[int(token.id)][0]]
            if actual not in correct:
                score +=1
                print(f"E {sentence.id} {token.id} {head_ids[int(token.id)][1]} head of {head_ids[int(token.id)]} must be one of ({', '.join(correct)}) not {actual}")
            if token.form == "ais":
                score +=1
                print(f"E {sentence.id} {token.id} 'ais' should not be a head")
    return score

def check_target_deprels(sentence, score):
    """Checks that for example cc is the leaf of a conj."""
    target_ids = {}
    targets = {
        "cc": ["conj"],
        "case": ["dep", "obl", "nmod", "xcomp", "xcomp:pred", "ccomp", "acl", "acl:relcl", "conj", "csubj:cop"]
    }
    for token in [t for t in sentence if t.deprel in targets and not t.is_multiword()]:
        target_ids[int(token.head)] = token.deprel

    for token in [s for s in sentence if not s.is_multiword()]:
        if int(token.id) in target_ids:
            actual = token.deprel
            correct = [*targets[target_ids[int(token.id)]], "root", "parataxis", "reparandum"]
            if actual not in correct:
                score +=1
                print(f"E {sentence.id} {token.id} target of {target_ids[int(token.id)]} must be one of ({', '.join(correct)}) not {actual}")
    return score

def check_target_upos(sentence, score):
    """Checks that for example amod is ADJ"""
    target_ids = {}
    targets = {
        "amod": ["ADJ"],
       #  "flat:name": ["PART", "PROPN"], # consider when obl/nmod fixed
        "nmod": ["NOUN", "NUM", "PRON", "PROPN", "X"]
    }
    for token in [s for s in sentence if not s.is_multiword()]:
        if token.deprel in targets:
            if token.upos not in targets[token.deprel]:
                score += 1
                print(f"E {sentence.id} {token.id} UPOS for {token.deprel} must be one of ({', '.join(targets[token.deprel])}) not {token.upos}")
    return score

def check_bi(sentence, score):
    """Checks that xcomp:pred is set up properly for bi."""
    ids = {}
    deprels = {}
    bi_pred_candidates = ["advmod","obl","xcomp","obl:smod","obl:tmod","obj"]
    bi_ids = [t.id for t in sentence if t.lemma == "bi"]
    allowed = ["xcomp:pred", "ccomp"]

    for token in sentence:
        if token.head in bi_ids and token.deprel in bi_pred_candidates or token.deprel in allowed:
            if token.head in ids:
                ids[token.head].append(token.id)
                deprels[token.head].append(token.deprel)
            else:
                ids[token.head] = [token.id]
                deprels[token.head] = [token.deprel]
    for key in deprels:
        if "xcomp:pred" not in deprels[key] and "ccomp" not in deprels[key]:
            print(f"E {sentence.id} {key} bi should have an xcomp:pred or a ccomp among {list(zip(ids[key], deprels[key]))}")
            score += 1
        if "obj" in deprels[key]:
            score += 1
            print(f"E {sentence.id} {key} bi should not have obj")
    return score

def check_clauses(sentence, score, warnings):
    """Checks that mark and mark:prt and ccomp, advcl and acl:relcl work together properly."""
    ids = {}
    deprels = {}
    forms = {}
    feats = {}
    deprels_to_check = ["ccomp", "advcl", "acl:relcl"]

    clause_ids = [t.id for t in sentence if t.deprel in deprels_to_check]
    for token in sentence:
        if token.head in clause_ids:
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
                if "PronType" in feat and "Rel" in feat["PronType"] and sentence[key].deprel != "acl:relcl":
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
        total_score = check_misc(tree, total_score)
        total_score = check_fixed(tree, total_score)
        total_score, total_warnings = check_ranges(tree, total_score, total_warnings)
        total_score = check_heads(tree, total_score)
        total_score = check_target_deprels(tree, total_score)
        total_score = check_target_upos(tree, total_score)
        total_score = check_bi(tree, total_score)
        total_score, total_warnings = check_clauses(tree, total_score, total_warnings)

    if total_score == 0:
        print("*** PASSED ***")
    else:
        print("*** FAILED *** with %s error%s" % (total_score, "s" if total_score > 1 else ""))

validate_corpus(pyconll.load_from_file(sys.argv[1]))
