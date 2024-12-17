import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])

for sentence in corpus:
    q = -1
    z = -1
    fq = 0
    fz = 0
    blocks = []
    parataxes = []
    root_id = 0
    for i, token in enumerate(sentence):
        if token.deprel == "parataxis":
            parataxes.append((token.id, token.lemma, token.head))
        if token.deprel == "root":
            root_id = int(token.id)
        if token.xpos == "Fq":
            fq = fq + 1
            q = token.id
        if token.xpos == "Fz" or i == len(sentence) - 1 and q != -1:
            fz = fz + 1
            z = token.id
            blocks.append((q, z))
            q = z = -1
    if (fq > 1 or fz > 1) and len(parataxes) > 0:
        root_in_quote = False
        for block in blocks:
            if int(block[0]) < root_id < int(block[1]):
                root_in_quote = True

        for parataxis in parataxes:
            inside = False
            head_inside = False
            for block in blocks:
                if int(block[0]) < int(parataxis[0]) < int(block[1]):
                    inside = True
                if int(block[0]) < int(parataxis[2]) < int(block[1]):
                    head_inside = True
            if inside != head_inside:
                print(f"{sentence.id} {parataxis} In quote: {inside}; Head in quote: {head_inside}")
        if int(blocks[0][0]) < 2 and not root_in_quote:
            print(f"{sentence.id} ERROR root should be inside quote")
        if int(blocks[0][0]) < 2 and blocks[-1][1] == sentence[len(sentence) - 1].id:
            print(f"{sentence.id} a quote containing non-quote material")
        if int(blocks[0][0]) > 1 and blocks[-1][1] == sentence[len(sentence) - 1].id:
            print(f"{sentence.id} normal text then quote containing non-quote material")
        if int(blocks[0][0]) > 1 and int(blocks[-1][1]) < int(sentence[len(sentence) - 1].id):
            l_coda = int(sentence[len(sentence) - 1].id) - int(blocks[-1][1])
            print(f"{sentence.id} normal text then quote then coda of length {l_coda}")
        if int(blocks[0][0]) < 2 and int(blocks[-1][1]) < int(sentence[len(sentence) - 1].id):
            l_coda = int(sentence[len(sentence) - 1].id) - int(blocks[-1][1])
            print(f"{sentence.id} quote then coda of length {l_coda}")
        print(f"{sentence.id} {len(parataxes)}, {fq}, {fz}, {blocks}, {sentence[len(sentence) - 1].id}")


