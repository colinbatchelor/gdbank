from collections import Counter
import sys
import pyconll

cnt = Counter()
corpus = pyconll.load_from_file(sys.argv[1])
for sentence in corpus:
    for token in sentence:
        if "-" not in token.id:
            cnt[(token.form, token.lemma, token.xpos)] += 1

for tup in cnt.most_common():
    print(tup)
