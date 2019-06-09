import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as fixed:
    for sentence in corpus:
        if sentence.meta_present('comment'):
            fixed.write('# comment = %s\n' % sentence.meta_value('comment'))
        if sentence.meta_present('speaker'):
            fixed.write('# comment = %s\n' % sentence.meta_value('speaker'))
        print(sentence.id)
        fixed.write('# sent_id = %s\n' % sentence.id)
        fixed.write('# text = %s\n' % sentence.text.replace('_', ' '))
        offset = 0
        skip = False
        mapping = {}
        new_tokens = {}
        i = 0
        for token in sentence:
            i+=1
            if int(token.id) != i:
                mapping[token.id] = str(i)
                token.id = str(i)
        for token in sentence:
            if token.head in mapping:
                print("%s %s" % (token.head, mapping[token.head]))
                token.head = mapping[token.head]
            fixed.write("%s\n" % token.conll())
        fixed.write('\n')