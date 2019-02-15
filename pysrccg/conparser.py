import csv
import os
import sys

arcosg_path = sys.argv[1]

def process_line(line):
  if not('/' in line): return []
  dual = line.split('/')
  line_1 = dual[0].replace(' ', '_')
  for token in dual[1:]:
    spacetokens = token.split()
    if len(spacetokens) > 1:
      line_1 = line_1 + "/" + spacetokens[0] + " " + "_".join(spacetokens[1:])
    else:
      line_1 = line_1 + "/" + token
  if line_1.endswith("."):
    line_1 = line_1 + "/Fe"
  elif line_1.endswith(","):
    line_1 = line_1 + "/Fi"
  elif line_1.endswith('"'):
    line_1 = line_1 + "/Fz"
  tokens = line_1.split()
  return [(t.split('/')[0],t.split('/')[1]) for t in tokens], 'Fe' in line
      
def arcosgToDoc(filename):
    with open(filename, 'r') as f:
      doc = []
      sentence = []
      for line in f:
        processed, eos = process_line(line)
        sentence.extend(processed)
        if eos:
          doc.append(sentence)
          sentence = []
    return doc

def reduce(stack, tokens, productions):
  # we only do binary productions
  types = [s[1] for s in stack[-2:]]
  print("in reduce: %s - %s " % ([s[0] for s in stack[-2:]], types))
  for production in productions:
    if production[1] == types:
      stack[-2:] = [(stack[-2:], production[0])]
      print("in reduce: %s" % stack[-2:])
      return True, stack, tokens
  return False, stack, tokens

def shift(stack, tokens):
  stack.append(tokens[0])
  tokens = tokens[1:]
  return stack,tokens
  
def parse(tokens, productions):
  stack = []
  while len(tokens) > 0:
    stack, tokens = shift(stack, tokens)
    reduction, stack, tokens = reduce(stack, tokens, productions)
    while reduction:
      reduction, stack, tokens = reduce(stack, tokens, productions)

  print("finished")
  return stack[0], len(stack)

productions = []
with open('productions.csv') as f:
  reader = csv.reader(f)
  for line in reader:
    productions.append((line[0], [line[1],line[2]]))

doc = arcosgToDoc(os.path.join(arcosg_path, 'f01.txt'))
for sentence in doc:
  print(" ".join([s[0] for s in sentence]))
  print(parse(sentence, productions))
  print()
