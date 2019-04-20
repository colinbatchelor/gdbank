from collections import Counter
from random import shuffle
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
  if line_1.endswith(".") or line_1.endswith("…"):
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
      print(filename)
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
  for production in productions:
    if production[1] == types:
      stack[-2:] = [(stack[-2:], production[0])]
      return True, stack, tokens
  return False, stack, tokens

def shift(stack, tokens):
  stack.append(tokens[0])
  tokens = tokens[1:]
  return stack,tokens
  
def parse(tokens, productions):
  stack = []
  print(tokens)
  while len(tokens) > 0:
    stack, tokens = shift(stack, tokens)
    reduction, stack, tokens = reduce(stack, tokens, productions)
    while reduction:
      reduction, stack, tokens = reduce(stack, tokens, productions)
  print("finished")
  return stack[0], len(stack)

def retag(rawpos, surface):
  specials = {
    'Sa':'PART','Sap1p':'NOUN','Sap1s':'NOUN',
    'Sap3sm*':'NOUN',
              'Sap3sf':'NOUN','Sap3p':'NOUN','Spa-p':'PREP',
              'Sp':'PREP', 'Sp+Dp2s':'PREP','SP':'PREP',
              'Spp1s':'PREP','Spp1p':'PREP','Spp2s':'PREP',
    'Spv':'PREP','Spv]':'PREP',
              'Spp3sm':'PREP', 'Spp3sf':'PREP','Spp3p':'PREP','Spa-s':'PREP',
    'Ug]':'PART','Uo':'PART','Uo*':'PART','Uc':'PART','Ua':'SCONJ','Uf':'NOUN',
    'Ug':'PART','Ug*':'PART','Uq':'INTERR','Uv':'PART','Um':'NOUN','Up':'NOUN',
              'Sap3sm':'NOUN',
    'Sp+Q-r':'PREP',
    'Xa':'NOUN',
    'Xsc':'UNK','Xf':'NOUN','Xsi':'NOUN',
    '':'',
    'Xfe':'NOUN','Xx':'UNK','Xy':'NOUN',
    'Cc':'CONJ','Cs':'SCONJ','Csw':'SCONJ','Cs+Qq':'SCONJ'}
  initials = {
    'I':'INT','T':'DET','t':'DET','Q':'PART','V':'VERB','W':'VERB','A':'ADJ','M':'NUM',
    'N':'NOUN','n':'NOUN','F':'PUNC','D':'PRON','P':'PRON','R':'ADV','Y':'NOUN'}
  if rawpos in specials:
    return specials[rawpos]
  try:
    return initials[rawpos[0]]
  except:
    print((rawpos,surface))
    raise

def bigrams(doc, counts):
  for sentence in doc:
    for i,token in enumerate(sentence[:-1]):
      key = (token[1], sentence[i+1][1])
      counts[key] = counts[key] + 1
  return counts

def trigrams(doc, counts):
  for sentence in doc:
    for i,token in enumerate(sentence[:-2]):
      key = (token[1], sentence[i+1][1], sentence[i+2][1])
      counts[key] = counts[key] + 1
  return counts

def coarse(doc):
  new_doc = []
  for sentence in doc:
    result = []
    for token in sentence:
      result.append((token[0], token[1], retag(token[1],token[0])))
    new_doc.append(result)
  return new_doc

productions = []
with open('productions.csv') as f:
  reader = csv.reader(f)
  next(reader)
  for line in reader:
    productions.append((line[0], [line[1],line[2]],line[3]))

def parse_sentences(arcosg_path, filename, counts, counts3):
  doc = arcosgToDoc(os.path.join(arcosg_path, filename))
  result2 = bigrams(doc, counts)
  result3 = trigrams(doc, counts3)
  sentence_count = 0
  production_count = 0
  for sentence in coarse(doc):
    stack,stack_length = parse(sentence, productions)
    print((stack,stack_length))
    sentence_count += 1
    production_count += stack_length
    print()
  return result2,result3,sentence_count,production_count

files = os.listdir(arcosg_path)
counts = Counter()
counts3 = Counter()
sentence_total = 0
production_total = 0
shuffle(files)
for file in files:
  if file.endswith('txt'):
    result = parse_sentences(arcosg_path, file, counts, counts3)
    counts, counts3, sentence_count, production_count = result
    sentence_total += sentence_count
    production_total += production_count
print(counts.most_common(16))
print(counts3.most_common(16))
print("%s/%s (%s)" % (production_total, sentence_total, production_total/sentence_total))
