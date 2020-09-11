import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
bi_pred_candidates = ["advmod","obl","xcomp","obl:smod","obl:tmod","obj"]
allowed = ["xcomp:pred","ccomp"]
leftward_only = ["acl:relcl"]
rightward_only = ["case", "cc", "cop", "mark"]
clauses_to_check = ["ccomp", "advcl", "acl:relcl"]
short_range = {"compound":2 ,"det":3, "mark:prt":5}
score = 0
warnings = 0
with open(sys.argv[2],'w') as f:
    for sentence in corpus:
        bi_ids = []
        clause_ids = []
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
                    if token.deprel in clauses_to_check:
                        clause_ids.append(token.id)
                    if token.deprel in rightward_only and int(token.head) < int(token.id):
                        score += 1
                        print(f"E {sentence.id} {token.id} {token.deprel} goes wrong way for gd")
                    if token.deprel in leftward_only and int(token.head) > int(token.id):
                        warnings += 1
                        print(f"W {sentence.id} {token.id} {token.deprel} goes wrong way (usually) for gd")
                        
                    if token.deprel in short_range and range > short_range[token.deprel]:
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
                        print(f"E {sentence.id} {key} {list(zip(ids[key], deprels[key]))}")
                        score += 1
                    else:
                        sentence[ids[key][0]].deprel = "xcomp:pred"
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
                    sentence[key].deprel = "advcl"
                elif 'mark:prt' in deprels[key]:
                    
                    for g in feats[key]:
                        if "PartType" in g:
                            if "Cmpl" in g["PartType"]: sentence[key].deprel = "ccomp"
                        if "PronType" in g:
                            if "Rel" in g["PronType"]: sentence[key].deprel = "acl:relcl"

        f.write("%s\n\n" % sentence.conll())
if score == 0:
    print("*** PASSED ***")
else:
    print("*** FAILED *** with %s error%s" % (score, "s" if score > 1 else ""))
