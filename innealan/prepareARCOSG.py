# -*- coding: utf-8 -*-
import os
import sys
import string
import pickle

def arcosgToDoc(filename):
    if filename.endswith(".txt"):
        f = open(filename, 'r')
        doc = []
        for line in f:
            dual = line.split('/')
            newline = dual[0].replace(' ', '_')
            for token in dual[1:]:
                spacetokens = token.split()
                if len(spacetokens) > 1:
                    newline = newline + "/" + spacetokens[0] + " " + "_".join(spacetokens[1:])
                else:
                    newline = newline + "/" + token

            if newline.endswith("."):
                newline = newline + "/Fe"
            elif newline.endswith("…"): # check correct tag here
                newline = newline + "/Fe"
            elif newline.endswith(","):
                newline = newline + "/Fi"
            elif newline.endswith('"'):
                newline = newline + "/Fz"

            tokens = newline.split() 
            pairs = [(t.split('/')[0],t.split('/')[1]) for t in tokens]
            doc.extend(pairs)
        f.close()
        return doc

local = sys.argv[1]
doc = []
for dir_entry in os.listdir(local):
    filename = os.path.join(local,dir_entry)
    if filename.endswith(".txt"):
        doc.extend([ arcosgToDoc(filename)]) 

flattenedlist = [item for sublist in doc for item in sublist]

arcosgfile = open('arcosg.pkl', 'wb')
pickle.dump(flattenedlist, arcosgfile)
arcosgfile.close()


