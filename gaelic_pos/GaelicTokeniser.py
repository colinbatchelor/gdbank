import re
import codecs
import os

class FullTokeniser():
    def __init__(self):
        lines = []
        # list of Gaelic and English abbreviations
        datadir = os.path.join(os.getcwd(), "Data")
        with open(os.path.join(datadir,"Abbrv.csv")) as f:
            for line in f:
                lines.append(str(line))
        self.abbr = re.findall(r"\w+\S+", " ".join(lines))
        self.exceptions = ["'ac", "[?]", '`ac', "'gam", "`gam", "'gad", "`gad", "'ga", "`ga", "'gar", "`gar", "'gur",
                           "`gur", "'gan", "`gan", "'m", "`m", "'n", "`n", "'nam", "`nam", "'nad", "`nad", "'na", "`na",
                           "'nar", "`nar", "‘nar", "'nur", "`nur", "'nan", "`nan", "'san", "'San", "‘San", "`san",
                           "‘sa", "`sa", "‘S", "'S", "`S", "‘ac", "‘ga", "`ga", "‘gan", "`gan", "h-uile"]
        self.big_re = re.compile(r"""\w+[“'-’]+\w+|
\w+[-.!?,'"":’`/“”]+\s+|
[-'’`“]+\w+|
[(]\W+|
[(]+[0-9]+[)]|
[(]+\S+[)]|
\S+[)]|
\w+[)]+[,.]+\s+|
\w\+[-]+\w+[)]+[.]+\s|
\S+[)]+[;.]+\s+|
\s+[',.!?:’`/=]+\s+|
(?<!=[‘',.!?:’/`])+\w+|
\S[^]+\S+|
\w+[',.!?:""’/`‘]+|
(?<=['"":’`‘])+\S+|
[£$]+[0-9]+|
\w+[""''’”/]+|
[aA-zZ]*[.:,’`”)]+[,;.]+\s+|
[aA-zZ]*[.:,’`”!?]+|
[aA-zZ]*[?]+[”]+\s|
[‘]+\w+[’]+[,]|
[‘]+\w+[’]+\s+|
\w+[@]+\w+[.]+\w+|
\w+[?]+[:]+[//]+[^\s<>']+|
\W\w+\s|
[^\W\s]+""", re.VERBOSE)
        
    def normalise_quotes(self, token):
        y = re.sub("[‘’´`]", "'", str(token))  # normalising apostrophes
        w = re.sub("[“”]", '"', str(y))
        return w

    def _firstpass(self, text):
        return re.findall(self.big_re, text)
    
    def tokenise(self, text):
        self.text = text
        Junk = []

        self.alltokens = self._firstpass(self.text)
        tokensetF = [n.strip() for n in self.alltokens]
        tokensetF1 = []
        for nx in tokensetF:
            if nx == self.abbr:
                tokensetF1.append(nx)

            if nx in self.exceptions:
                tokensetF1.append(nx)

            else:
                xx = ''
                hyphenT = re.findall(r"(\bt-)", str(nx))  ## takes all t-hyphenated tokens

                hyphenT1 = re.findall('(?<=t-)\w+', str(nx))

                hyphenN = re.findall(r"(\bn-)", str(nx))  ## takes all n-hyphenated tokens

                hyphenN1 = re.findall('(?<=n-)\w+', str(nx))

                hyphenH = re.findall(r"(\bh-)", str(nx))  ## takes all h-hyphenated tokens

                hyphenH1 = re.findall('(?<=h-)\w+', str(nx))

                hyphenSa = re.findall(r"(\b-sa\b)", str(nx))  ## takes all -sa hyphenated tokens

                XhyphenSa = re.findall('(?<!=-sa)\w+', str(nx))  ## takes all tokens before hyphenated -sa

                hyphenSe = re.findall(r"(\b-se\b)", str(nx))  ## takes all -se hyphenated tokens

                XhyphenSe = re.findall('(?<!=-se)\w+', str(nx))  ## takes token before hyhpenated -se

                hyphenSan = re.findall(r"(\b-san\b)", str(nx))  ## takes all -san hyphenated tokens

                XhyphenSan = re.findall(r'(?<!=-san)\w+', str(nx))  ## takes token before hyhpenated -san

                doublQpnt = re.findall(r'(\A[" / \ ( [ ])\w+',
                                       str(nx))  ## determines whether there is an initial quote in a string

                doublQSub = re.findall(r'(?<!=["])\S', str(
                    nx))  ## find strings that start with quotes and end with non-white space

                qMark = re.findall(r"(?<=(\b[?.!,:' " "]))",
                                   str(nx))  ## determine whether there is a puntuation mark at end of string

                BeforeqMark = re.findall(r"(?<!=[?.!,:'])\w+", str(
                    nx))  ## find strings that ends with puntuation mark and non-white space

                singleQpnt = re.findall(r"(\A[']+)",
                                        str(nx))  ## determines whether there is an initial single quote in a string

                singleQSub = re.findall(r"(?<!=['])\S", str(
                    nx))  ## find strings that start with single quotes and end with non-white space

                currency = re.findall(r"(\A[$£]+)",
                                      str(nx))  ## determines whether there is an initial currency sign in a string

                currencySub = re.findall(r"(?<!=[$£])\S", str(nx))  ##

                comparativeParticles = re.findall(r"(\w+['])", str(nx))  ## appostrophe

                comparativeParticles1 = re.findall(r"(?<!=[']\w)\w+", str(nx))

                doubleAfter = re.findall(r'(\w+["]+)',
                                         str(nx))  ## determines whether there is an initial quote in a string

                beforestroke = re.findall(r"(\b/\b)", str(nx))  ## takes all  -strock words

                afterstroke = re.findall('(?<!=/)\w+', str(nx))  ## takes all   word -strock words

                beforeEqual = re.findall(r"(\A[=]+)", str(nx))  ## takes all  -strock words

                afterEqual = re.findall("(?<!=\A[='])\S", str(nx))  ## takes all   word -strock words

                beforeAccent = re.findall(r"(\b’\b)", str(nx))  ## takes all  -accen words

                afterAccent = re.findall('(?<!= ’ )\S', str(nx))  ## takes all -accented words

                beginAccent = re.findall(r"(\A[‘]+)", str(nx))  ## takes all -accented words

                beginAccentT = re.findall('(?<!= ‘ )\S', str(nx))  ## takes all -accented words

                beforePeriod = re.findall(r"(\B[.]\B)", str(nx))  ## takes all - words with periods at end

                afterPeriod = re.findall('(?<!= [.] )\S', str(nx))  ## takes all - period

                beforeComma = re.findall(r"(\B[,]\B)", str(nx))  ## takes all - words with comma at end

                afterComma = re.findall('(?<!= [,] )\S', str(nx))  ## takes all - comma

                beforeQmark = re.findall(r"(\B[?]+\B)", str(nx))  ## takes all - words with question marks at end

                afterQmark = re.findall('(?<!= [?] )\S', str(nx))  ## takes all - comma

                beforePeriod1 = re.findall(r"(\b[.])", str(nx))  ## takes all - words with periods at end

                afterPeriod1 = re.findall('(?<!= [.] )\S', str(nx))  ## takes all - period

                beforeComma1 = re.findall(r"(\b[,])", str(nx))  ## takes all - words with comma at end

                afterComma1 = re.findall('(?<!= [,] )\S', str(nx))  ## takes all  - comma

                beginAccent2 = re.findall(r"(\b[’]+)", str(nx))  ## takes all - accented words

                beginAccentT2 = re.findall('(?<!= ’ )\S', str(nx))  ## takes all - accented words

                beforeOpenBra = re.findall(r"(\A[(]+[(‘])", str(nx))  ## takes all - words with comma at end

                afterOpenBra = re.findall("(?<!= [(])\S", str(nx))  ## takes all - comma

                beforeDoubleQ = re.findall(r"(\A[“])", str(nx))  ## takes all - words with double quote at end

                afterDoubleQ = re.findall("(?<!= [“])\S", str(nx))  ## takes all - comma

                qColon = re.findall(r"(?<=(\b[:]))",
                                    str(nx))  ## determines whether there is a puntuation mark at end of string

                if qColon:
                    x = re.findall(r"\S", str(nx))
                    tokensetF1.append(''.join(x[:len(x) - 1]))
                    xx = x[len(x) - 1:]
                    tokensetF1.append(''.join(xx))
                    nx = ''

                if beforeDoubleQ:
                    tokensetF1.append(''.join(beforeDoubleQ))
                    tokensetF1.append(''.join(afterDoubleQ[1:]))
                    nx = ''

                if beforeOpenBra:
                    tokensetF1.append(''.join(afterOpenBra[:1]))
                    tokensetF1.append(''.join(afterOpenBra[1:2]))
                    tokensetF1.append(''.join(afterOpenBra[2:]))

                    nx = ''

                if beginAccent2:
                    if ''.join(beginAccentT2[:2]) == 'a’':
                        tokensetF1.append(''.join(beginAccentT2[:2]))

                        tokensetF1.append(''.join(beginAccentT2[2:]))

                        nx = ""

                if beforeComma1:
                    if ''.join(beforeComma1) == ''.join(afterComma1[len(afterComma1) - 1:]):
                        tokensetF1.append(''.join(afterComma1[:len(afterComma1) - 1]))

                        tokensetF1.append(''.join(beforeComma1))

                        nx = ''

                if beforePeriod1:
                    if ''.join(beforePeriod1) == ''.join(afterPeriod1[len(afterPeriod1) - 1:]):
                        tokensetF1.append(''.join(afterPeriod1[:len(afterPeriod1) - 1]))

                        tokensetF1.append(''.join(beforePeriod1))

                        nx = ''

                if beforeQmark and nx not in ["[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                    if ''.join(beforeQmark) == ''.join(afterQmark[:1]):
                        ''

                    else:
                        x = afterQmark[len(afterQmark) - 1:]

                        tokensetF1.append(''.join(afterQmark[:len(afterQmark) - 1]))

                        tokensetF1.append(''.join(beforeQmark))

                        nx = ''

                if beforeComma:
                    x = afterComma[
                        len(afterComma) - 2:]  ## filtering for (eg: ],) type of tokens normally used in accademic text

                    y = afterComma[:1]  ## filtering for (eg: [ ,) type of tokens normally used in accademic text

                    if ''.join(x[:len(x) - 1]) in [']', ')'] and ''.join(y) in ['[', '(']:
                        tokensetF1.append(''.join(y))

                        tokensetF1.append(''.join(afterComma[1:len(afterComma) - 2]))

                        tokensetF1.append(''.join(x[:len(x) - 1]))

                        tokensetF1.append(''.join(beforeComma))

                        nx = ''

                    if ''.join(x[:len(x) - 1]) in [']', ')'] and ''.join(y) not in ['[', '(']:
                        tokensetF1.append(''.join(afterComma[:len(afterComma) - 2]))

                        tokensetF1.append(''.join(x[:len(x) - 1]))

                        tokensetF1.append(''.join(beforeComma))

                        nx = ''

                    if ''.join(x[:len(x) - 1]) not in [']', ')'] and ''.join(y) not in ['[', '(']:
                        xx = x[:len(x) - 1]

                        if xx:
                            if ''.join(afterComma[:1]) == '‘':
                                xxx = afterComma[len(afterComma) - 2:]

                                xxxx = afterComma[:]

                                tokensetF1.append(''.join(afterComma[:1]))

                                tokensetF1.append(''.join(afterComma[1: len(afterComma) - 2]))

                                tokensetF1.append(''.join(xxx[:1]))

                                tokensetF1.append(''.join(afterComma[len(afterComma) - 1:]))

                                nx = ''

                            else:
                                if len(afterComma) == 3:
                                    tokensetF1.append(''.join(afterComma[1:2]))

                                    tokensetF1.append(''.join(afterComma[len(afterComma) - 1:]))

                                    nx = ''

                                else:
                                    if len(afterComma) == 2:
                                        tokensetF1.append(''.join(afterComma[:1]))

                                        tokensetF1.append(''.join(afterComma[len(afterComma) - 1:]))

                                        nx = ''

                if beginAccent and ''.join(beginAccentT[len(beginAccentT) - 1:]) == '’' and not xx:
                    x = beginAccentT[1:]

                    tokensetF1.append(''.join(beginAccent))

                    tokensetF1.append(''.join(x[:len(x) - 1]))

                    tokensetF1.append(''.join(beginAccentT[len(beginAccentT) - 1:]))

                    Junk.append(''.join(beginAccentT[1:]))

                    nx = ''

                if beginAccent and ''.join(beginAccentT[len(beginAccentT) - 1:]) == ',' and not xx:
                    tokensetF1.append(''.join(beginAccent))

                    tokensetF1.append(''.join(beginAccentT[1:len(beginAccentT) - 1]))

                    tokensetF1.append(''.join(beginAccentT[len(beginAccentT) - 1:]))

                    Junk.append(''.join(beginAccent + beginAccentT[1:len(beginAccentT) - 1]))

                    nx = ''

                if beginAccent and ''.join(beginAccentT[len(beginAccentT) - 1:]) == '?' and not xx:
                    x = beginAccentT[len(beginAccentT) - 2:]

                    if ''.join(x[:len(x) - 1]) == '’':
                        tokensetF1.append(''.join(beginAccent))

                        tokensetF1.append(''.join(beginAccentT[1:len(beginAccentT) - 2]))

                        tokensetF1.append(''.join(x[:len(x) - 1]))

                        tokensetF1.append(''.join(beginAccentT[len(beginAccentT) - 1:]))

                        Junk.append(''.join(beginAccent) + beginAccentT[1:len(beginAccentT) - 1])

                        Junk.append(
                            ''.join(beginAccentT[1:len(beginAccentT) - 1] + beginAccentT[len(beginAccentT) - 1:]))

                        nx = ""

                if beginAccent and not beforeComma1 and not xx:
                    nx = ''

                if beforeAccent and ''.join(afterAccent[len(afterAccent) - 1:]) not in ['s']:
                    x = afterAccent[:3]

                    if ''.join(x[1:2]) == "’":
                        tokensetF1.append(''.join(afterAccent[:2]))
                        tokensetF1.append(''.join(afterAccent[2:]))
                        nx = ''

                    if ''.join(x[2:3]) == "’":
                        tokensetF1.append(''.join(afterAccent[:3]))
                        tokensetF1.append(''.join(afterAccent[3:]))
                        nx = ''

                if beforeEqual:
                    tokensetF1.append(''.join(beforeEqual))
                    tokensetF1.append(''.join(afterEqual[1:2]))
                    nx = ''

                if beforestroke:
                    tokensetF1.append(''.join(afterstroke[:1]))
                    tokensetF1.append(''.join(beforestroke))
                    tokensetF1.append(''.join(afterstroke[1:]))
                    nx = ''

                if currency:
                    x = len(currencySub)

                    tokensetF1.append(''.join(currency[:1]))

                    tokensetF1.append(''.join(currencySub[1: x - 1]))

                    tokensetF1.append(''.join(currencySub[x - 1:]))

                    nx = ''

                if doublQpnt and nx not in ["[?]", "[Name]", "[Placename]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]",
                                            "[7]", "[8]", "[9]"]:
                    x = doublQSub[1:len(doublQSub) - 1]

                    y = ''.join(doublQSub[len(doublQSub) - 1:])

                    m = ''.join(doublQpnt)

                    if y != '"' or y != '' and y == ')' and m != '(':
                        xy = (x + doublQSub[len(doublQSub) - 1:])

                        if ''.join(xy[len(xy) - 1:]) not in [')', ':', '?', ']']:
                            tokensetF1.append(''.join(m))

                            tokensetF1.append(''.join(xy))

                            nx = ' '
                        else:
                            tokensetF1.append(m)

                            tokensetF1.append(''.join(xy[:len(xy) - 1]))

                            tokensetF1.append(y)

                            nx = ''

                    if y == '"':
                        tokensetF1.append(''.join(doublQpnt))

                        tokensetF1.append(''.join(doublQSub[1:len(doublQSub) - 1]))

                        tokensetF1.append(''.join(y))

                        nx = ' '

                if comparativeParticles and len(comparativeParticles1) > 0:
                    if len(''.join(comparativeParticles1[1:])) > 1:
                        tokensetF1.append(''.join(comparativeParticles[:1]))

                        tokensetF1.append(''.join(comparativeParticles1[1:]))

                        nx = ""

                    if len(''.join(comparativeParticles1[1:])) == 1:
                        tokensetF1.append(''.join(comparativeParticles[:1] + comparativeParticles1[1:]))

                        nx = ''

                if hyphenT:
                    tokensetF1.append(''.join(hyphenT))
                    tokensetF1.append(''.join(hyphenT1))
                    nx = ''

                if hyphenN:
                    tokensetF1.append(''.join(hyphenN))  ## then append the stripped token into the list container
                    tokensetF1.append(''.join(hyphenN1))  ## then append the stripped token into the list container
                    nx = ''

                if hyphenSe:
                    tokensetF1.append(''.join(hyphenSa[:1]))
                    tokensetF1.append(''.join(XhyphenSe[:1]))
                    nx = ''

                if hyphenSan:
                    tokensetF1.append(''.join(XhyphenSan[:1]))
                    tokensetF1.append(''.join(XhyphenSan[:1]))
                else:
                    tokensetF1.append(nx)

        tokensetF2 = []
        for i,w0 in enumerate(tokensetF1):
            w1 = tokensetF1[i+1] if i < len(tokensetF1) - 1 else "<END>"
            w2 = tokensetF1[i+2] if i < len(tokensetF1) - 2 else "<END>"
            """Here follows a long list of token elements. A future improvement would be to pull all of these
            elements into a csv file loaded into the tagger"""
            if w0 == '1':
                tokensetF2.append('[1]')
            elif w0 == '2':
                tokensetF2.append('[2]')
            elif w0 == '3':
                tokensetF2.append('[3]')

            elif w0 == '4':
                tokensetF2.append('[4]')

            elif w0 == '5':
                tokensetF2.append('[5]')
            elif w0 == '6':
                tokensetF2.append('[6]')
            elif w0 == '7':
                tokensetF2.append('[7]')
            elif w0 == '8':
                tokensetF2.append('[8]')

            elif w0 == '9':
                tokensetF2.append('[9]')

            elif w0 == ']':
                tokensetF2.append('')

            elif w0 == 'Placename':
                tokensetF2.append('[Placename]')

            elif w0 == 'a-réir':
                tokensetF2.extend(['a','-','réir'])

            elif w0 == "mi '":
                tokensetF2.extend(['mi',"'"])

            elif w0 == "!)":
                tokensetF2.extend(['!',")"])
            elif w0 == "le'r":
                tokensetF2.extend(['le', "'r"])
            elif w0 == "mi.”":
                tokensetF2.extend(["mi",".","”"])
            elif w0 == "mi,”":
                tokensetF2.extend(["mi",",","”"])
            elif w0 == "].":
                tokensetF2.extend([']',"."])
            elif w0 == "?)":
                tokensetF2.append('?')
                tokensetF2.extend(")")
            elif w0 == ".)":
                tokensetF2.append('.')
                tokensetF2.extend(")")
            elif w0 == "”)":
                tokensetF2.append('”')

                tokensetF2.extend(")")

            elif w0 == '); ':
                tokensetF2.append(')')

                tokensetF2.extend(";")

            elif w0 == ") ":
                tokensetF2.append(')')

            elif w0 == "?”":
                tokensetF2.append('?')

                tokensetF2.extend("”")

            elif w0 == "i.”":
                tokensetF2.append('i')

                tokensetF2.extend(".")

                tokensetF2.extend("”")

            elif w0 == ".’”":
                tokensetF2.append('.')

                tokensetF2.extend("”")

            elif w0 == ",”":
                tokensetF2.append(',')

                tokensetF2.extend("”")

            elif w0 == "tu,”":
                tokensetF2.append('tu')

                tokensetF2.extend(",")

                tokensetF2.extend("”")

            elif w0 == "”.":
                tokensetF2.append('”')

                tokensetF2.extend(".")

            elif w0 == "às.”":
                tokensetF2.append('às')

                tokensetF2.extend(".")

                tokensetF2.extend("”")

            elif w0 == "sa,”":
                tokensetF2.append('sa')

                tokensetF2.extend(",")

                tokensetF2.extend("”")

            elif w0 == "’, ":
                tokensetF2.append('’')

                tokensetF2.extend(",")

            elif w0 == ").":
                tokensetF2.append(')')

                tokensetF2.extend(".")

            elif w0 == "),":
                tokensetF2.append(')')

                tokensetF2.extend(",")

            elif w0 == "), ":
                tokensetF2.append(')')

                tokensetF2.extend(",")

            elif w0 == ".”":
                tokensetF2.append('.')

                tokensetF2.extend("”")

            elif w0 == "’.”":
                tokensetF2.append('’')

                tokensetF2.extend(".")

                tokensetF2.extend("”")

            elif w0 == ",”":
                tokensetF2.append(',')

                tokensetF2.extend("”")

            elif w0 == "’,":
                tokensetF2.append('’')

                tokensetF2.extend(",")

            elif w0 == "’.":
                tokensetF2.append("'")

                tokensetF2.extend(".")

            elif w0 == "’ ":
                tokensetF2.append('’')

            elif w0 == ");":
                tokensetF2.append(')')

                tokensetF2.extend(";")

            elif w0 == "s’.”":
                tokensetF2.append('s’')

                tokensetF2.extend(".")

                tokensetF2.extend("”")

            elif w0 == "tus":
                tokensetF2.append("tus'")

            elif w0 == "aic":
                tokensetF2.append("aic'")

            elif w0 == 'mi-fhìn':
                tokensetF2.append('mi')

                tokensetF2.append('-')

                tokensetF2.append('fhìn')

            elif w0 == 'dh’èireas':
                tokensetF2.append('dh’')

                tokensetF2.append('èireas')

            elif w0 == 'mi-fhèin':
                tokensetF2.append('mi')

                tokensetF2.append('-')

                tokensetF2.append('fhèin')

            elif w0 == 'thu-fhèin':
                tokensetF2.append('thu')

                tokensetF2.append('-')

                tokensetF2.append('fhèin')

            elif w0 == 'e-fhèin':
                tokensetF2.append('e')

                tokensetF2.append('-')

                tokensetF2.append('fhèin')

            elif w0 == 'i-fhèin':
                tokensetF2.append('i')

                tokensetF2.append('-')

                tokensetF2.append('fhèin')

            elif w0 == 'sinn-fhìn':
                tokensetF2.append('sinn')

                tokensetF2.append('-')

                tokensetF2.append('fhìn')

            elif w0 == 'sibh-fhèin':
                tokensetF2.append('sibh')

                tokensetF2.append('-')

                tokensetF2.append('fhèin')

            elif w0 == 'iad-fhèin':
                tokensetF2.extend(['iad','-','fhèin'])
            elif w0 == 'h-ana-miannaibh':
                tokensetF2.extend(['h-','ana-miannaibh'])
            elif w0 == "a b'":
                tokensetF2.extend(['a',"b'"])
            elif w0 == 'dh’obair-riaghaltais':
                tokensetF2.append('dh’')

                tokensetF2.append('obair-riaghaltais')

            elif w0 == "dh’fheumas":
                tokensetF2.append("dh'")

                tokensetF2.append('fheumas')

            elif w0 == "dh'fheumas":
                tokensetF2.append("dh'")

                tokensetF2.append('fheumas')

            elif w0 == "dh'fhaodas":
                tokensetF2.append("dh'")

                tokensetF2.append('fhaodas')

            elif w0 == "dh’fhaodas":
                tokensetF2.append("dh'")

                tokensetF2.append('fhaodas')

            elif w0 == "dh’fhàs":
                tokensetF2.append("dh’")

                tokensetF2.append('fhàs')

            elif w0 == "dh'fhàs":
                tokensetF2.append("dh'")

                tokensetF2.append('fhàs')

            elif w0 == 'Ban-righ' and "'nn" in tokensetF1[i:i + 2]:
  
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("'nn")

            elif w0 == 'Dh' and "’fhaodainn" in tokensetF1[i:i + 2]:
  
                tokensetF2.append('Dh’')

                tokensetF2.append('fhaodainn')

                tokensetF1.remove("’fhaodainn")

            elif w0 == 'Ban-righ' and "'nn" in tokensetF1[i:i + 2]:
    
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("'nn")

            elif w0 == 'bhrist' and "’" in tokensetF1[i:i + 2]:
   
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == 'ars' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == 'ars' and "'" in tokensetF1[i:i + 2]:
    
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("'")

            elif w0 == 'mis' and "’" in tokensetF1[i:i + 2]:
    
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == 'mis' and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("'")

            elif w0 == 'thus' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == 'thus' and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("'")

            elif w0 == 'oirr' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("’")

            elif w0 == 'ars' and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("'")

            elif w0 == 'oidhch' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == '[' and "Placename]." in tokensetF1[i:i + 2]:
                #  print (' '.join(tokensetF1[i:i+2]))
                tokensetF2.append("[Placename]")
                tokensetF2.append(".")
                tokensetF1.remove("Placename].")
              
            elif w0 == '[' and "Placename]" in tokensetF1[i:i + 2]:
                #  print (' '.join(tokensetF1[i:i+2]))
                tokensetF2.append("[Placename]")
                tokensetF1.remove("Placename].")
              
            elif w0 == "A" and "n" in tokensetF1[i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is a blank token created in between
                # print (''.join(tokensetF1[i:i+3]))
                tokensetF2.append(''.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("n")
              
            elif w0 == "do’" and "n" in tokensetF1[i:i + 2]:
                # print (''.join(tokensetF1[i:i+3]))
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("n")
              
            elif w0 in ["aig","chalp","chual","creids","oirr"] and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 in ["chual","creids"] and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("'")

            elif w0 == "tein" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 in ["chreach-s","cuimhn","dhòmhs","innt","prionns","toilicht"] and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 in ["chreach-s","cuimhn","dhòmhs","innt","prionns","toilicht"] and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("'")

            elif w0 == "Do’" and "n" in tokensetF1[i:i + 2]:

                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("n")

            elif w0 == "De’" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("n")
            elif w0 == "comhairl" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == "òrain-“pop" and "”" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("”")

            elif w0 == "f’" and "a" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("a")

            elif w0 == "F’" and "a" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("a")

            elif w0 == "de’" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("n")

            elif w0 == "Gu" and "dé" in tokensetF1[i:i + 2]:
                tokensetF2.append("Gu dé")
                tokensetF1.remove("dé")
            elif w0 == "mu" and "thràth" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("thràth")

            elif w0 == "Mu’" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("n")

            elif w0 == "mu’" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("n")

            elif w0 == "An" or w0 =="an" and "dràsda" in tokensetF1[i:i + 2]:
                tokensetF2.append(w0 + " dràsda")
                tokensetF1.remove("dràsda")
              
            elif w0 == "Srath" and "Chluaidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("Chluaidh")
              
            elif w0 == "ma" and "tha" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("tha")
              
            elif w0 == 'Roinn' and "Eòrpa" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("Eòrpa")
              
            elif (w0 == 'Phort' or w0 == 'Port') and "Rìgh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("Rìgh")
              
            elif w0 == 'làn' and "-Ghàidhealtachd" in tokensetF1[i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between

                tokensetF2.append(''.join(tokensetF1[i:i + 3]))

                # tokensetF1.remove("bhon")

                tokensetF1.remove("-Ghàidhealtachd")

            elif w0 == 'leth' and "-Ghàidhealtachd" in tokensetF1[i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between

                tokensetF2.append(''.join(tokensetF1[i:i + 3]))

                # tokensetF1.remove("bhon")

                tokensetF1.remove("-Ghàidhealtachd")

            elif w0 == 'bhon' and w1 in ["an","a'"]:
                tokensetF2.append(' '.join([w0, w1]))
                tokensetF1.remove(w1)

            elif w0 == "o’" and w1 == "n":
                tokensetF2.append("%s%s" % (w0, w1))
                tokensetF1.remove("n")
            # toponyms
            elif w0 in ['Caolas', 'Chaolas', 'Dùn', 'Eilean', 'Gleann', 'Loch', 'Rubha', 'Tràigh'] and re.match('[A-Z][a-z]+', w1):
                tokensetF2.append(' '.join([w0, w1]))
                tokensetF1.remove(w1)

            elif w0 == 'a' and w1 in ["b'", "b’"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)
              
            elif w0 == "a'" and "shineach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("shineach")

            elif w0 == "a’" and "s" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s%s" % (w0, w1))
                tokensetF1.remove("s")
          
            elif w0 == "a" and "shineach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("shineach")
          
            elif w0 == "Caledonian" and "Mac" in tokensetF1[i:i + 2] and "a’" in tokensetF1[i:i + 3] and "Bhruthainn" in tokensetF1[i:i + 4]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 4]))
          
            elif w0 == "Caledonian" and "Mac" in tokensetF1[i:i + 2] and "a'" in tokensetF1[i:i + 3] and "Bhruthainn" in tokensetF1[i:i + 4]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 4]))
                tokensetF1.remove("Mac")
                tokensetF1.remove("a'")
                tokensetF1.remove("Bhruthainn")
          
            elif w0 == 'dhan' and "an" in tokensetF1[i:i + 2] and "sin" in tokensetF1[i:i + 3]:
                tokensetF2.append('dhan')
                tokensetF2.append('an sin')
                tokensetF1.remove("an")
                tokensetF1.remove("sin")

            elif w0 == 's' and "a" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("a")

            elif w0 == 'prionns' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("’")

            elif w0 == 'leams' and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("'")

            elif w0 == 'leams' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("’")

            elif w0 == 'fon' and "an" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("an")

            elif w0 == 'fon' and "an" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("an")

            elif w0 == 'ionnsaicht' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("’")
      
            elif w0 == 'ionnsaicht' and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("'")

            elif w0 == 'Dùn' and "Èideann" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("Èideann")

            elif w0 == 'an' and "toiseach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("toiseach")

            elif w0 == "‘n" and "toiseach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("toiseach")

            elif w0 == "'n" and "toiseach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("toiseach")

            elif w0 == "a" and "tuath" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("tuath")

            elif w0 == "air" and "choireigin-ach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("choireigin-ach")

            elif w0 == "an" and "raoir" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("raoir")

            elif w0 == "a" and "chaoidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("chaoidh")

            elif w0 == 'mun' and "a'" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("a'")

            elif w0 == 'mun' and "an" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

            elif w0 == 'on' and "a'" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("a'")

            elif w0 == 'on' and "an" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

            elif w0 == 'oidhch' and "’." in tokensetF1[i:i + 2]:
                tokensetF2.append("oidhch’")

                tokensetF2.append(".")

                tokensetF1.remove("’.")

            elif w0 == 'Coille' and "Chaoil" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("Chaoil")

            elif w0 == 'Gleann' and "Dail" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("Dail")

            elif w0 == 'Ruaidh' and "Mhònaidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("Mhònaidh")

            elif w0 == 'tron' and "an" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

            elif w0 == "de'" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("n")

            elif w0 == "mu'" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("n")

            elif w0 == "do'" and "n" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("n")

            elif w0 == "doesn'" and "t" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("t")

            elif w0 == "a" and "staigh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("staigh")

            elif w0 == "a" and "steach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("steach")

            elif w0 == "a" and "mach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("mach")
          
            elif w0 == "sam" and "bith" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("bith")
              
            elif w0 == "air" and "choireigin" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("choireigin")
              
            elif w0 == "a" and "sin" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("sin")
              
            elif w0 == "an" and "sin" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("sin")
              
            elif re.match('^[A-Z][a-z]+',w0) and w1 == "Bridge":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("Bridge")
              
            elif w0 == "a" and "chèile" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("chèile")
              
            elif w0 == "ana" and "nàdarra" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("nàdarra")

            elif w0 == "An" and "Aodann" in tokensetF1[i:i + 2] and "Bàn" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("Aodann")
                tokensetF1.remove("Bàn")

            elif w0 == "[" and "?" in tokensetF1[i:i + 2] and "]" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("?")

                tokensetF1.remove("]")

            elif w0 == "a" and "bhòn-dè" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bhòn-dè")

            elif w0 == "a'" and "bhòn-dè" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bhòn-dè")

            elif w0 == "Pholl" and "a'" in tokensetF1[i:i + 2] and "Ghrùthain" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("Ghrùthain")

                tokensetF1.remove("a'")

                

            elif w0 == "ann" and "a" in tokensetF1[i:i + 2] and "shiud" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("a")

                tokensetF1.remove("shiud")

                

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "shiud" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("an")

                tokensetF1.remove("shiud")

                

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "seo" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("an")
                tokensetF1.remove("ann")
                

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "siud" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("an")
                tokensetF1.remove("siud")
                

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "sin" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("an")
                tokensetF1.remove("sin")
                

            elif w0 == "a'" and "bhòn-raoir" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("a'")
                tokensetF1.remove("bhòn-raoir")

            elif w0 == "a'" and "s" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("s")

            elif w0 == "a" and "bhòn-raoir" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("a")

                tokensetF1.remove("bhòn-raoir")

                

            elif w0 == "a" and "bhòn" in tokensetF1[i:i + 2] and "raoir" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("a")

                tokensetF1.remove("bhòn")

                tokensetF1.remove("raoir")

                

            elif w0 == "a'" and "bhòn-uiridh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("a'")

                tokensetF1.remove("bhòn-uiridh")

                w0 = ""

            elif w0 == "a" and w1 == "bhòn-uiridh":
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w0)

                tokensetF1.remove(w1)

            elif w0 == "a" and "bhòn" in tokensetF1[i:i + 2] and "uiridh" in tokensetF1[i:i + 3]:
                tokensetF2.append("%s %s %s" % (w0, w1, w2))
                tokensetF1.remove(w0)
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "a'" and "bhòn-uiridh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bhòn-uiridh")

                

            elif w0 == "a" and "bhos" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bhos")

                

            elif w0 == "a" and "bhàn" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bhàn")

                

            elif w0 == "a" and "mach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("mach")

                

            elif w0 == "a" and "màireach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("màireach")

                

            elif w0 == "am" and "bliadhna" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove('am')
                tokensetF1.remove("bliadhna")
                

            elif w0 == "a" and "muigh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove('a')
                tokensetF1.remove("muigh")

                

            elif w0 == "a" and "nall" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("a")

                tokensetF1.remove("nall")

                

            elif w0 == "an" and "ath-bhliadhna" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

                tokensetF1.remove("ath-bhliadhna")

                

            elif w0 == "an" and "ath" in tokensetF1[i:i + 2] and "bhliadhna" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("ath")

                tokensetF1.remove("bhliadhna")

                

            elif w0 == "an" and "ath-oidhche" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("ath-oidhche")

            elif w0 == "an" and "ath" in tokensetF1[i:i + 2] and "oidhche" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("ath")

                tokensetF1.remove("oidhche")

            elif w0 == "an" and "ath" in tokensetF1[i:i + 2] and "oidhch'" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("ath")

                tokensetF1.remove("oidhch'")

            elif w0 == "an" and "ath-oidhche" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("ath-oidhche")

            elif w0 == "an" and "ath-sheachdainn" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("ath-sheachdainn")

            elif w0 == "an" and "ath" in tokensetF1[i:i + 2] and "sheachdainn" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("an")

                tokensetF1.remove("sheachdainn")

            elif w0 == "an" and "ath-sheachdain" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("ath-sheachdain")

            elif w0 == "an" and "ath" in tokensetF1[i:i + 2] and "sheachdain" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("an")

            elif w0 == "an" and "còmhnaidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

            elif w0 == "an" and "de" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("de")

            elif w0 == "an" and "diugh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("diugh")

            elif w0 == "an" and "dràsta" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("dràsta")

            elif w0 == "an" and "earar" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("earar")

            elif w0 == "an" and "earair" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("earair")

            elif w0 == "a" and "nis" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("nis")

            elif w0 == "a" and "nisd" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("nisd")

            elif w0 == "a" and "nuas" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("nuas")

            elif w0 == "a" and "uiridh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("uiridh")

            elif w0 == "a" and "null" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("null")

            elif w0 == "a" and "raoir" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("raoir")

            elif w0 == "a" and "rithist" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("rithist")

            elif w0 == "a" and "staidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("staidh")

            elif w0 == "a" and "steach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("steach")

            elif w0 == "b" and "e" in tokensetF1[i:i + 2]:
                tokensetF2.append("b'")

                tokensetF2.append("e")

                tokensetF1.remove("b")

            elif w0 == "mi'":
                tokensetF2.append("mi")

                tokensetF2.append("'")

                tokensetF1.remove("mi'")

            elif w0 == "na" and "s" in tokensetF1[i:i + 2]:
                tokensetF2.append("na's")

                tokensetF1.remove('s')

            elif w0 == "na" and "bu" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('bu')

            elif w0 == "a" and "bu'" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bu'")

            elif w0 == "Inbhir" and "Nis" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("Nis")

            elif w0 == "ann" and "am" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("am")
            elif w0 == "ann" and "an" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

            elif w0 == "an" and "siud" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("siud")

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "siud" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("an")

                tokensetF1.remove("siud")

            elif w0 == "an" and "am" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("am")

            elif w0 == "pòs" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove('’')

            elif w0 == "gàir" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove('’')

            elif w0 == "an" and "ceart-uair" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('ceart-uair')

            elif w0 == "an" and "uairsin" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('uairsin')

            elif w0 in ["a","an"] and "sineach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('sineach')

            elif w0 == "an" and w1 == "dràsda":
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('dràsda')

            elif w0 == "ma" and w1 == "tha":
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('tha')

            elif w0 == "an" and "ceartuair" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('ceartuair')

            elif w0 == "fhad" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == "ge" and "brì" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('brì')

            elif w0 == "ge" and "brith" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove('brith')

            elif w0 == "ge" and "be" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("be")

            elif w0 == "ge" and "'s" in tokensetF1[i:i + 2] and "bith" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("'s")

                tokensetF1.remove("bith")

            elif w0 == "gar" and "bith" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("bith")

            elif w0 == "air" and "falbh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("falbh")

            elif w0 == "an" and "làrna-mhàireach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("làrna-mhàireach")

            elif w0 in ["ma", "math"] and w1 == "dh'" and w2 in ["fhaoite", "fhaoidte", "fhaoidhte"]:
                tokensetF2.append("%s %s%s" % (w0, w1, w2))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "gu" and "dè" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("gu")

            elif w0 == "a" and "chèil" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("chèil")

            elif w0 == "mu" and "dheireadh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("dheireadh")

            elif w0 == "a" and "h-uile" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("h-uile")

            elif w0 == "a" and "seo" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("seo")

            elif w0 == "an" and "seo" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("seo")

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "seo" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("an")

                tokensetF1.remove("seo")

            elif w0 == "a" and "niste" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("niste")

            elif w0 == "a" and "niste" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("niste")

            elif w0 == "ge" and "b'" in tokensetF1[i:i + 2] and "e" in tokensetF1[i:i + 3] and "air" in tokensetF1[i:i + 4] and "bith" in tokensetF1[i:i + 5]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 5]))

                tokensetF1.remove("b'")

                tokensetF1.remove("e")

                tokensetF1.remove("air")

                tokensetF1.remove("bith")

            elif w0 == "tuilleadh" and "'s" in tokensetF1[i:i + 2] and "a" in tokensetF1[i:i + 3] and "chòir" in tokensetF1[i:i + 4]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 4]))

                tokensetF1.remove("'s")

                tokensetF1.remove("a")

                tokensetF1.remove("chòir")

            elif w0 == "tuilleadh" and "'s" in tokensetF1[i:i + 2] and "a" in tokensetF1[
                                                                                 i:i + 3] and "chòir" in tokensetF1[
                                                                                                         i:i + 4]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 4]))

                tokensetF1.remove("'s")

                tokensetF1.remove("a")

                tokensetF1.remove("chòir")

            elif w0 == "tuilleadh" and "sa" in tokensetF1[i:i + 2] and "chòir" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("sa")

                tokensetF1.remove("chòir")

            elif w0 == "ann" and "a'" in tokensetF1[i:i + 2] and "shiudach" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("shiudach")

                tokensetF1.remove("a'")

            elif w0 == "ann" and "a" in tokensetF1[i:i + 2] and "shiudach" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("shiudach")

                tokensetF1.remove("a")

            elif w0 == "a's" and "a" in tokensetF1[i:i + 2] and "sineach" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("a")

                tokensetF1.remove("sineach")

            elif w0 == "ann" and "a" in tokensetF1[i:i + 2] and "shineach" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("a")

                tokensetF1.remove("ann")

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "shin" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("an")

                tokensetF1.remove("shin")

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "seo" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("an")

                tokensetF1.remove("seo")

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2]:
                    tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                    tokensetF1.remove("an")
            elif w0 == "ann" and "seo" in tokensetF1[i:i + 2]:
                    tokensetF2.append("%s %s" % (w0, w1))

                    tokensetF1.remove("seo")

            elif w0 == "bheath" and "’." in tokensetF1[i:i + 2]:
                tokensetF2.extend(["bheath’","."])

                tokensetF1.remove("’.")

            elif w0 == "uisg" and "’." in tokensetF1[i:i + 2]:
                tokensetF2.extend(["uisg’","."])
                tokensetF1.remove("’.")

            elif w0 in ["ath-oidhch","bheath","bonnant","brist","chual","dòch","do-sheachant","bioraicht","lost-s","teoth","thoilicht","thus","uisg"] and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("’")

            elif w0 == "ann" and "a" in tokensetF1[i:i + 2] and "shin" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("a")
                tokensetF1.remove("shin")
                
            elif w0 == "ann" and "a" in tokensetF1[i:i + 2] and "sheo" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("a")
                tokensetF1.remove("sheo")
            elif w0 == "(’" and "S" in tokensetF1[i:i + 2]:
                tokensetF2.extend(["(","’S"])
                tokensetF1.remove("S")
            elif w0 == "(’" and "s" in tokensetF1[i:i + 2]:
                tokensetF2.extend(["(","’s"])
                tokensetF1.remove("s")
            else:
                tokensetF2.append(w0)

        tokensetF3 = []
        for i, nn in enumerate(tokensetF2):
            secondQuots = re.findall(r"(\w+[' " "])", str(nn))  ## apostrophe

            secondQuots1 = re.findall(r"(?<!=[' " "])\w+", str(nn))

            if len(nn) < 4 and secondQuots and "s" in tokensetF2[i:i + 2]:  ##  reconstructs possessive tokens (eg M's)

                dd = ''.join(tokensetF2[i:i + 2])

                tokensetF3.append(dd.strip())

            elif nn in self.abbr and "." in tokensetF2[i:i + 2]:
                tokensetF3.append(''.join(tokensetF2[i:i + 2]))

            elif nn == "la’" and "r-na-mhàireach" in tokensetF2[i:i + 2]:
                tokensetF3.append(''.join(tokensetF2[i:i + 2]))

                Junk.append("r-na-mhàireach")

            elif nn == "dhìoms" and "’" in tokensetF2[i:i + 2]:
                tokensetF3.append(''.join(tokensetF2[i:i + 2]))
                tokensetF2.remove("’")

            else:
                tokensetF3.append(nn.strip())

        tokensetF4 = []
        for q in tokensetF3:
            if q not in Junk and ''.join(q) != '':
                tokensetF4.append(q)
        return tokensetF4
