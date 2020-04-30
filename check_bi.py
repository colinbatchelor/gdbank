import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
candidates = ["advmod","obl","xcomp","obl:smod","obl:tmod","obj"]
allowed = ["xcomp:pred","ccomp"]
score = 0
with open(sys.argv[2],'w') as f:
    for sentence in corpus:
        bi_ids = []
        prev_token = None
        for token in sentence:
            if token.lemma == "bi":
                bi_ids.append(token.id)
            if token.xpos == "Up" and token.deprel != "flat" and prev_token is not None and prev_token.xpos == "Nn":
                score +=1 
                print("%s %s %s" % (sentence.id, token.id, "Patronymic should be flat"))
            prev_token = token
        if len(bi_ids) > 0:
            ids = {}
            deprels = {}
            for token in sentence:
                if token.head in bi_ids and token.deprel in candidates or token.deprel in allowed:
                    if token.head in ids:
                        ids[token.head].append(token.id)
                        deprels[token.head].append(token.deprel)
                    else:
                        ids[token.head] = [token.id]
                        deprels[token.head] = [token.deprel]
            for key in deprels:
                if "xcomp:pred" not in deprels[key] and "ccomp" not in deprels[key]:
                    if len(deprels[key]) > 1:
                        print("%s %s %s" % (sentence.id, key, list(zip(ids[key], deprels[key]))))
                        score += 1
                    else:
                        sentence[ids[key][0]].deprel = "xcomp:pred"
                if "obj" in deprels[key]:
                    score += 1
                    print("%s %s %s" % (sentence.id, key, "should not have obj"))
        f.write("%s\n\n" % sentence.conll())
if score == 0:
    print("*** PASSED ***")
else:
    print("*** FAILED *** with %s error%s" % (score, "s" if score > 1 else ""))
