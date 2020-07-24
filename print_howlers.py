import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
min_score = int(sys.argv[2])
for sentence in corpus:
    for token in sentence:
        if not token.is_multiword():
            start = int(token.id)
            end = int(token.head)
            score = abs(start-end)
            if score > min_score and score < len(sentence) - 1:
                print(f"{sentence.id} {token.id} {score}")
