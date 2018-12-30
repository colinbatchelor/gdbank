import csv
from gaelic_pos import GaelicTokeniser
from gaelic_pos import postagger
from checker import Checker

t = GaelicTokeniser.Tokeniser()
p = postagger.PosTagger()
c = Checker()

tokens = []
with open('test.txt') as f:
    reader = csv.reader(f)
    for row in reader:
        token = row[0]
        pos = row[1]
        tokens.append(token)

result = p.tagfile_default(tokens)
print(result)
