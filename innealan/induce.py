# -*- coding: utf-8 -*-
import sys
from nltk.tree import ParentedTree
from nltk import induce_pcfg
from nltk.grammar import Nonterminal
from nltk.parse import pchart

productions = []
leafses = []
with open(sys.argv[1]) as f:
    for line in f:
        tree = ParentedTree.fromstring(line.decode('utf8'))
        leafses.append(tree.leaves())
        productions += tree.productions()

sent = Nonterminal('sent')
grammar = induce_pcfg(sent, productions)

parser = pchart.InsideChartParser(grammar)
sentence = leafses[0]
print len(parser.parse(sentence))
