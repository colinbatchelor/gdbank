# -*- coding: utf-8 -*-
import pickle
import sys
from gdtools.acainn import Lemmatizer, Retagger, Subcat, Typer

def tidy_word(string):
    """outputs string suitable for XMLification further down the pipeline"""
    if string == '''"''':
        return "&quot;"
    return string.replace("&", "&amp;")

brownfile = open(sys.argv[1], 'rb')
corpus = pickle.load(brownfile)
brownfile.close()
output = open(sys.argv[2], 'w')
# features
with open("resources/features.txt") as file:
    for line in file:
        output.write(line)
# type-changing and type-raising rules
with open("resources/rules.txt") as rules:
    for line in rules:
        output.write(line)
retagger = Retagger()
typer = Typer()
families = set()
words = set()
# assumes a single list rather than a list of lists (need to think about this)
for surface, pos in corpus:
    if pos != "":
        tags = retagger.retag(surface, pos)
        for tag in tags:
            newtagtype = typer.type(surface, pos, tag)
            newtag = newtagtype[0]
            newtype = newtagtype[1]
            families.add("family %s { entry: %s; }" % (newtag, newtype))
            words.add('word "%s_%s":%s; # %s' % (tidy_word(surface), newtag, newtag, pos))

for family in sorted(families):
    output.write(family + '\n')
for word in sorted(words):
    output.write(word + '\n')
output.close()
