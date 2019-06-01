import sys
import pyconll

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as fixed:
    for sentence in corpus:
        fixed.write('# sent_id = %s' % sentence.id)
        fixed.write('\n')
        text = " ".join([t.form for t in sentence]).replace("h- ", "h-").replace("t- ", "t-").replace("n- ", "n-").replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace("( ", "(").replace(" )",")").replace("dh' ", "dh'").replace("  ", " ")
        fixed.write('# text = %s\n' % text)
        offset = int(sentence[0].id)
        for token in sentence:
            if token.form == "," or token.form == "." or token.form =="?" or token.form ==")" or token.xpos =="Fz":
                sentence[(int(token.id) - offset) -1].misc['SpaceAfter'] = ["No"]
            if token.form == "h-" or token.form == "dh'" or token.form == "t-" or token.form =="n-" or token.form == "(" or token.xpos == "Fq":
                sentence[(int(token.id) - offset)].misc['SpaceAfter'] = ["No"]
        for token in sentence:
            token.id = str(1 + int(token.id) - offset)
            fixed.write("%s\n" % token.conll())
        fixed.write('\n')
       

