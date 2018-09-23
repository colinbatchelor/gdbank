import re

class SimpleTokeniser():
    def __init__(self):
        self.bigrams = []
        with open('./Data/bigrams.txt') as f:
            for line in f:
                self.bigrams.append(line.strip())
        self.trigrams = ["(Beinn) (na) (Faoghla)", "dhan an sin", "Pholl a Ghr\xf9thain"]
        self.fourgrams = ["(Caledonian) (Mac) (a') (Bhruthainn)"]

    def normalise_quotes(self, s):
        y = re.sub("[‘’´`]", "'", str(s))  # normalising apostrophes
        w = re.sub("[“”]", '"', str(y))
        return w

    def find_ngrams(self, text):
        # protect ngrams by replacing spaces with underscores
        for fourgram in self.fourgrams:
            text = re.sub(fourgram, r"\1_\2_\3_\4", text) if re.match(fourgram, text) else text
        for trigram in self.trigrams:
            text = re.sub(trigram, r"\1_\2_\3", text) if re.match(trigram, text) else text
        for bigram in self.bigrams:
            text = re.sub(bigram, r"\1_\2", text) if re.match(bigram, text) else text
        return text
    
    def tokenise(self, text):
        token = ''
        tokens = []
        text = text.replace("a h-uile", "a#h#uile")
        for t in self.normalise_quotes(self.find_ngrams(text)):
            if re.match("[hnt]-", token) or token == "dh'":
                tokens.append(token)
                token = t
            elif t == ' ':
                if len(token) > 0: tokens.append(token)
                token = ''
            elif t in '''()[],.?!"''':
                if len(token) > 0: tokens.append(token)
                tokens.append(t)
                token = ''
            else:
                token = token + t
        if len(token) > 0: tokens.append(token)
        return [u.replace('_', ' ').replace("a#h#uile", "a h-uile") for u in tokens]

