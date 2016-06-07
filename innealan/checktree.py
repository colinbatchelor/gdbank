# -*- coding: utf-8 -*-
import sys
from nltk.tree import *

sum = 0
secondsum = 0
results = []
nochildren = {}
with open(sys.argv[1]) as f:
    for line in f:
        try:
            tree = ParentedTree.fromstring(line.decode('utf8'))
            for position in tree.treepositions():
                t = tree[position]
                if not isinstance(t, basestring):
                    l = len(t)
                    if l == 0:
                        print "zero-length?: " + line
                    if l > 20:
                        print l
                        print t
                        print ""
                    if l in nochildren:
                        nochildren[l] = nochildren[l] + 1
                    else:
                        nochildren[l] = 1
            sum = sum + len(tree.treepositions())
            success = len(tree)
            secondsum = secondsum + success
            results.append((success, " ".join(tree.leaves()[:8])))
        except:
            print "problem with line beginning %s" % (line[:32])
            e = sys.exc_info()[0]
            print e

# longest overall sentences
for result in sorted(results)[-4:]:
    print result
print sum
print secondsum

print nochildren

