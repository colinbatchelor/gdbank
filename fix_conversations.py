import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as fixed:
    speaker = None
    for sentence in corpus:
        print(sentence.id)
        tokens = []
        for token in sentence:
            if token.xpos != "Xsc":
                tokens.append(token)
            else:
                speaker = token.form
        if sentence.meta_present('comment'):
            fixed.write('# comment = %s\n' % sentence.meta_value('comment'))
        if sentence.meta_present('speaker'):
            fixed.write('# speaker = %s\n' % sentence.meta_value('speaker'))
        else:
            fixed.write('# speaker = %s\n' % speaker)            
        fixed.write('# sent_id = %s\n' % sentence.id)
        fixed.write('# text = %s\n' % sentence.text.replace("%s " % speaker, ''))
        for token in tokens:
            fixed.write("%s\n" % token.conll())
        fixed.write('\n')

