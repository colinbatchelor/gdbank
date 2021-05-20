# -*- coding: utf-8 -*-
from shutil import copyfile
# assumes that the output files have been called arcosg-*
# clearly one could mend this with an optional command-line parameter.
#
# Michael White's suggested fix for this:
# https://sourceforge.net/p/openccg/discussion/255819/thread/b6c93813/
#
#
import xml.etree.ElementTree as et

morph = et.parse('arcosg-morph.xml')
root = morph.getroot()
for entry in root.findall('entry'):
    wordtokens = entry.get('word').split("_")
    trimmed = "_".join(wordtokens[:len(wordtokens) - 1])
    entry.set('word', trimmed)
    entry.set('stem', trimmed)
morph.write("arcosg-morph.xml")

lexicon = et.parse('arcosg-lexicon.xml')
r2 = lexicon.getroot()
for family in r2.findall('family'):
    for member in family.findall('member'):
        wordtokens = member.get('stem').split("_")
        trimmed = "_".join(wordtokens[:len(wordtokens) - 1])
        member.set('stem', trimmed)
lexicon.write('arcosg-lexicon.xml')

copyfile("arcosg-testbed.xml", "testbed.xml")
copyfile("arcosg-grammar.xml", "grammar.xml")






