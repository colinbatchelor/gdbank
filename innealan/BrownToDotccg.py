# -*- coding: utf-8 -*-
from acainn import Lemmatizer, Retagger, Subcat, Typer
import pickle
import sys

# outputs string suitable for XMLification further down the pipeline
def tidyword(s):
    if s == '''"''':
        return "&quot;"
    else:
        return s.replace("&", "&amp;")

brownfile = open(sys.argv[1], 'rb')
corpus = pickle.load(brownfile)
brownfile.close()
output = open(sys.argv[2], 'w')
# features
with open("resources/features.txt") as f:
    for line in f:
        output.write(line)
# type-changing and type-raising rules
with open("resources/rules.txt") as r:
    for line in r:
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
            type = newtagtype[1]
            families.add("family %s { entry: %s; }" % (newtag, type))
            words.add('word "%s_%s":%s; # %s' % (tidyword(surface), newtag, newtag, pos))

for family in sorted(families):
    output.write(family + '\n')
for word in sorted(words):
    output.write(word + '\n')
output.close()
