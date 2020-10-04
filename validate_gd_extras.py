import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
bi_pred_candidates = ["advmod","obl","xcomp","obl:smod","obl:tmod","obj"]
allowed = ["xcomp:pred", "ccomp"]
leftward_only = ["acl:relcl", "flat", "fixed"]
rightward_only = ["case", "cc", "cop", "mark", "nummod"]
clauses_to_check = ["ccomp", "advcl", "acl:relcl"]
targets = {"cc":["conj"], "case":["obl","xcomp","xcomp:pred","ccomp","acl","acl:relcl","conj"]}
short_range = {"compound":2 ,"det":3, "mark:prt":6, "fixed":2, "flat":4}
score = 0
warnings = 0

for sentence in corpus:
    bi_ids = []
    clause_ids = []
    target_ids = {}
    reparanda = []
    prev_token = None
    for token in sentence:
        if not token.is_multiword():
            range = abs(int(token.id) - int(token.head))
            if token.xpos == token.upos and token.feats == {}:
                score +=1
                print(f"E {sentence.id} {token.id} XPOS {token.xpos} should not match UPOS if feats is empty")
            if token.lemma == "bi":
                bi_ids.append(token.id)
            if token.deprel == "reparandum":
                ''' this is for when I rewrite this to work properly '''
                reparanda.append(token.id)
            if token.deprel is None:
                score +=1
                print(f"E {sentence.id} {token.id} deprel should not be None")
            else:
                if token.deprel in targets:
                    target_ids[int(token.head)] = token.deprel
                if token.deprel in clauses_to_check:
                    clause_ids.append(token.id)
                if token.deprel in rightward_only and int(token.head) < int(token.id):
                    score += 1
                    print(f"E {sentence.id} {token.id} {token.deprel} goes wrong way for gd")
                if token.deprel in leftward_only and int(token.head) > int(token.id):
                    warnings += 1
                    print(f"W {sentence.id} {token.id} {token.deprel} goes wrong way (usually) for gd")

                if token.deprel in short_range and range > short_range[token.deprel] and (prev_token is not None and token.deprel != prev_token.deprel):
                    if range < short_range[token.deprel] + 3:
                        warnings += 1
                        code = "W"
                    else:
                        score += 1
                        code = "E"
                    print(f"{code} {sentence.id} {token.id} Too long a range ({range}) for {token.deprel}")

                if token.xpos == "Up" and token.deprel != "flat" and prev_token is not None and prev_token.xpos == "Nn":
                    score +=1 
                    print(f"E {sentence.id} {token.id} Patronymic should be flat")
                if token.deprel.startswith("mark") and token.upos not in ["PART", "SCONJ"]:
                    score +=1
                    print(f"E {sentence.id} {token.id} mark should only be for PART or SCONJ")
                if token.deprel in ["nsubj", "obj"] and token.upos not in ["NOUN", "PRON", "PROPN", "NUM", "SYM", "X"] and int(token.head) < int(token.id):
                    score +=1
                    print(f"E {sentence.id} {token.id} nsubj and (rightward) obj should only be for NOUN, PRON, PROPN, NUM, SYM or X")
            prev_token = token

    if len(target_ids) > 0:
        for token in sentence:
            if '-' not in token.id:
                if int(token.id) in target_ids:
                    actual = token.deprel
                    correct = [*targets[target_ids[int(token.id)]], "root", "parataxis", "reparandum"]
                    if actual not in correct:
                        score +=1
                        print(f"E {sentence.id} {token.id} target of {target_ids[int(token.id)]} must be one of ({', '.join(correct)}) not {actual}")

    if len(bi_ids) > 0:
        ids = {}
        deprels = {}
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
    if len(clause_ids) > 0:
        ids = {}
        deprels = {}
        forms = {}
        feats = {}
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
            ''' mark beats mark:prt '''
            if 'mark' in deprels[key]:
                if sentence[key].deprel != "advcl":
                    warnings += 1
                    print(f"W {sentence.id} {key} deprel should be advcl")
                
            elif 'mark:prt' in deprels[key]:
                for g in feats[key]:
                    if "PartType" in g and "Cmpl" in g["PartType"] and sentence[key].deprel != "ccomp":
                        warnings += 1
                        print(f"W {sentence.id} {key} deprel should be ccomp")
                    if "PronType" in g and "Rel" in g["PronType"] and sentence[key].deprel != "acl:relcl":
                        warnings += 1
                        print(f"W {sentence.id} {key} deprel should be acl:relcl")

if score == 0:
    print("*** PASSED ***")
else:
    print("*** FAILED *** with %s error%s" % (score, "s" if score > 1 else ""))
