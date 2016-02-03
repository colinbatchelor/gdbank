# 
# This takes a tidied form of Will Lamb's Gold Standard corpus XML and converts the news scripts
# and prose into CoNLL-X format as they have consistently-identifiable sentence boundaries.
# Assumes that the POS tags are attached to the tokens with an underscore, for example cothromach_Aq-smn.
#
# Splitting the conversations into utterances will have to be done separately. 
#
# See http://ilk.uvt.nl/conll/ for more details on the format.
# We treat the first character of the POSTAG as being a CPOSTAG (coarse part-of-speech tag).
# Spaces in multiword expressions such as "sam bith" and "anns an" are converted to underscores.
#
# Some of the logic around detecting quotation boundaries is a bit iffy.
#
# Colin Batchelor, February 2016

import xml.etree.ElementTree

def toCoNLL(text):
    result = u""
    tokens = iter(text.split())
    accum = u""
    count = 0
    inQuote = False
    sentenceEnd = False
    for token in tokens:
        if u"_" in token:
            form = (accum + token.split(u"_")[0]).replace(u" ", u"_")
            postag = token.split(u"_")[1]
            cpostag = postag[0]
            accum = u""
            count = count + 1
            line = u'\t' + form + u'\t_\t' + cpostag + u'\t' + postag + u'\t_\t_\t_\n'
            if sentenceEnd:
                sentenceEnd = False
                if form == u'"':
                    # newline + reset goes after this token
                    result = result + str(count) + line + u'\n'
                    count = 0
                else:
                    count = 1
                    result = result + u'\n' + str(count) + line 
                    # newline goes before this token
            else:
                result = result + str(count) + line
            if form == u'"' and inQuote:
                inQuote = False       
            elif form == u'"' and not inQuote:
                inQuote = True            
        else:
            accum = accum + token + u" "
        if (token == u"._Fe" or token == u"?_Fg") and not inQuote:
            count = 0
            result = result + "\n"
        elif (token == u"._Fe" or token == u"?_Fg") and inQuote:
            sentenceEnd = True
        else:
            sentenceEnd = False
    return result

docs = xml.etree.ElementTree.parse('fixed.xml')
f = open('gsconll.txt', 'w')
for doc in docs.findall('doc'):
    # As a first pass this takes prose and news scripts.
    # Conversations and sports commentary may need to be handled in a different way.
    if doc.find('mode').text == u' writing ' or doc.find('register').text == u' news script ':
        for pubPlaces in doc.findall('pubPlace'):
            if pubPlaces.tail is None:
                pass
            else:
                result = toCoNLL(pubPlaces.tail)
                if result is None:
                    pass
                else:
                    f.write(result.encode('utf8'))
        for publisher in doc.findall('publisher'):
            f.write(toCoNLL(publisher.tail).encode('utf8'))
f.close()
