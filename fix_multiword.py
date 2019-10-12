import sys
import pyconll

def dict_to_string(dict):
    if dict == {}:
        return '_'
    return '|'.join(['%s=%s' % (t, list(dict[t])[0]) for t in sorted(dict)])

corpus = pyconll.load_from_file(sys.argv[1])
with open(sys.argv[2],'w') as fixed:
    for sentence in corpus:
        print(sentence.id)
        if sentence.meta_present('speaker'):
            fixed.write('# speaker = %s\n' % sentence.meta_value('speaker'))
        if sentence.meta_present('comment'):
            fixed.write('# comment = %s\n' % sentence.meta_value('comment'))
        fixed.write('# sent_id = %s\n' % sentence.id)
        fixed.write('# text = %s\n' % sentence.text.replace('_', ' '))
        offset = 0
        mapping = {0:0}
        skip = False
        new_tokens = {}
        for token in sentence:
            if skip:
                skip = False
            else:
                new_token_id = int(token.id) + offset
                mapping[int(token.id)] = new_token_id
                if token.lemma == None: token.lemma = "_"
                if token.head == None: token.head = "_"
                if token.deprel == None: token.deprel = "_"
                if '_' in token.form:
                    new_forms = token.form.split('_')
                    offset = offset + (len(new_forms) - 1)
                    new_deprel = 'flat' if token.upos == "PROPN" else 'fixed'
                    for i,new_form in enumerate(new_forms):
                        new_tokens[new_token_id + i] = (new_form, '_', token.upos, token.xpos, dict_to_string(token.feats), token.head if i == 0 else token.id, token.deprel if i == 0 else new_deprel, '_', dict_to_string(token.misc) if i == len(new_forms) - 1 else '_')
                elif token.xpos == "Uo" and "SpaceAfter" in token.misc or token.lemma == "dh'":
                    next_token = sentence[int(token.id)]
                    new_form = "%s%s" % (token.form, next_token.form)
                    new_tokens[new_token_id] = (new_form, next_token.lemma, next_token.upos, next_token.xpos, dict_to_string(next_token.feats), token.head, token.deprel, '_', dict_to_string(next_token.misc))
                    mapping[int(token.id) + 1] = new_token_id
                    offset = offset - 1
                    skip = True
                else:
                    new_tokens[new_token_id] = (token.form, token.lemma, token.upos, token.xpos, dict_to_string(token.feats), token.head, token.deprel, '_', dict_to_string(token.misc))
        
        for token in new_tokens:
            updated = [str(token)]
            updated.extend(new_tokens[token])
            if updated[2] is None: updated[2] ='"'
            if updated[6] != "_": updated[6] = str(mapping[int(updated[6])])
            fixed.write('%s\n' % '\t'.join(updated))
        fixed.write('\n')
