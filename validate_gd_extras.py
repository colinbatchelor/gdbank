import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
bi_pred_candidates = ["advmod","obl","xcomp","obl:smod","obl:tmod","obj"]
allowed = ["xcomp:pred","ccomp"]
rightward_only = ["case", "cc", "cop", "mark"]
score = 0
with open(sys.argv[2],'w') as f:
    for sentence in corpus:
        bi_ids = []
        ccomp_ids = []
        prev_token = None
        for token in sentence:
            if not token.is_multiword():
                if token.lemma == "bi":
                    bi_ids.append(token.id)
                if token.deprel is None:
                    score +=1
                    print(f"{sentence.id} {token.id} deprel should not be None")
                else:
                    if token.deprel == "ccomp":
                        ccomp_ids.append(token.id)
                    if token.deprel in rightward_only and int(token.head) < int(token.id):
                        score += 1
                        print(f"{sentence.id} {token.id} {token.deprel} goes wrong way for gd")
                    if token.xpos == "Up" and token.deprel != "flat" and prev_token is not None and prev_token.xpos == "Nn":
                        score +=1 
                        print(f"{sentence.id} {token.id} Patronymic should be flat")
                    if token.deprel.startswith("mark") and token.upos not in ["PART", "SCONJ"]:
                        score +=1
                        print(f"{sentence.id} {token.id} mark should only be for PART or SCONJ")
                    if token.deprel in ["nsubj", "obj"] and token.upos not in ["NOUN", "PRON", "PROPN", "NUM", "SYM", "X"] and int(token.head) < int(token.id):
                        score +=1
                        print(f"{sentence.id} {token.id} nsubj and (rightward) obj should only be for NOUN, PRON, PROPN, NUM, SYM or X")
                prev_token = token
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
                    if len(deprels[key]) > 1:
                        print(f"{sentence.id} {key} {list(zip(ids[key], deprels[key]))}")
                        score += 1
                    else:
                        sentence[ids[key][0]].deprel = "xcomp:pred"
                if "obj" in deprels[key]:
                    score += 1
                    print(f"{sentence.id} {key} bi should not have obj")
        if len(ccomp_ids) > 0:
            ids = {}
            deprels = {}
            forms = {}
            for token in sentence:
                if token.head in ccomp_ids:
                    if token.head in ids:
                        ids[token.head].append(token.id)
                        deprels[token.head].append(token.deprel)
                        forms[token.head].append(token.form)
                    else:
                        ids[token.head] = [token.id]
                        forms[token.head] = [token.form]
                        deprels[token.head] = [token.deprel]
            for key in deprels:
                if 'mark' in deprels[key]:
                    sentence[key].deprel = "advcl"
                if 'case' in deprels[key]:
                    sentence[key].deprel = "acl:relcl"

        f.write("%s\n\n" % sentence.conll())
if score == 0:
    print("*** PASSED ***")
else:
    print("*** FAILED *** with %s error%s" % (score, "s" if score > 1 else ""))
