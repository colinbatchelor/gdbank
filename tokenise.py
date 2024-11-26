import re

def tokenise_words(sentence):
    '''
    Returns a conllu object representing the sentence tokenised according to the UD Scottish Gaelic rules
    Hyphens are not word boundaries.
    Apostrophes aren't word boundaries either.
    '''
    token = ""
    token_id = 0
    for i, character in enumerate(sentence):
        if character in " ":
            if token != "":
                yield (token, "_")
                token = ""
        elif character in ".,[]()":
            if token != "":
                yield (token, "SpaceAfter=None")
            if i < len(sentence) - 1 and sentence[i] != " ":
                yield (character, "SpaceAfter=None")
            else:
                yield (character, "_")
            token = ""
        else:
            token = token + character
    if token != "":
        yield (token, "_")
            
print([t for t in tokenise_words("Am falbh thu leam")])
print([t for t in tokenise_words("[Rugadh DOMHNALL MAC EACHARNA air latha Nollaig anns a' bhliadhna 1836, ann an Gleann-garasdail an taobh tuath eilein Dhiùra laimh ri Coire Bhreacain.")])
print([t for t in tokenise_words("Thigeadh iad an sin 'n an ruith 's 'n an leum a dh' fhaicinn ciod an tubaist a dh' éirich do'n bhuachaille.")])
