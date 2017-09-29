# -*- coding: utf-8 -*-

import re
import codecs
import os

datadir = os.path.join(os.getcwd(), "Data")
aboutFN = os.path.join(datadir, "AboutFile.txt")
helpFN = os.path.join(datadir, "HelpFile.txt")
abbrevFN = os.path.join(datadir, "Abbrv.csv")  # list of Gaelic and English abbreviations


class Tokeniser():

    def tokenise(self, text):
        self.text = text

        self.Pnamedict = {}

        self.PnameValues = []

        self.tokensetF = []

        self.tokensetF1 = []

        self.tokensetF2 = []

        self.tokensetF3 = []

        self.tokensetF4 = []

        self.tokensetF5 = []

        self.Junk = []

        self.abbr = re.findall(r"\w+\S+", str(codecs.open(abbrevFN, 'r')))

        self.exceptions = ["'ac", "[?]", '`ac', "'gam", "`gam", "'gad", "`gad", "'ga", "`ga", "'gar", "`gar", "'gur",
                           "`gur", "'gan", "`gan", "'m", "`m", "'n", "`n", "'nam", "`nam", "'nad", "`nad", "'na", "`na",
                           "'nar", "`nar", "‘nar", "'nur", "`nur", "'nan", "`nan", "'san", "'San", "‘San", "`san",
                           "‘sa", "`sa", "‘S", "'S", "`S", "‘ac", "‘ga", "`ga", "‘gan", "`gan"]

        # self.alltokens = re.findall(r"\w+['-]+\w+|['''""]+\w+|\S+['',.!?':]+\S+|\w+['',.!?"":]|[''""]\w+|\w+[.!?,']+\S|\W+\S+\w+[']|[^\W\s]+", self.text)

        self.alltokens = re.findall(
            r"\w+[“'-’]+\w+|\w+[-.!?,'"":’`/“”]+\s+|[-'’`“]+\w+|[(]\W+|[(]+[0-9]+[)]|[(]+\S+[)]|\S+[)]|\w+[)]+[,.]+\s+|\w\+[-]+\w+[)]+[.]+\s|\S+[)]+[;.]+\s+|\s+[',.!?:’`/=]+\s+|(?<!=[‘',.!?:’/`])+\w+|\S[^]+\S+|\w+[',.!?:""’/`‘]+|(?<=['"":’`‘])+\S+|[£$]+[0-9]+|\w+[""''’”/]+|[aA-zZ]*[.:,’`”)]+[,;.]+\s+|[aA-zZ]*[.:,’`”!?]+|[aA-zZ]*[?]+[”]+\s|[‘]+\w+[’]+[,]|[‘]+\w+[’]+\s+|\w+[@]+\w+[.]+\w+|\w+[?]+[:]+[//]+[^\s<>']+|\W\w+\s|[^\W\s]+",
            self.text)

        for n in self.alltokens:
            self.tokensetF.append(n.strip())

        for nx in self.tokensetF:
            if nx == self.abbr:
                self.tokensetF1.append(nx)

            if nx in self.exceptions:
                self.tokensetF1.append(nx)

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

                    self.tokensetF1.append(''.join(x[:len(x) - 1]))

                    xx = x[len(x) - 1:]

                    self.tokensetF1.append(''.join(xx))

                    nx = ''

                if beforeDoubleQ:
                    self.tokensetF1.append(''.join(beforeDoubleQ))

                    self.tokensetF1.append(''.join(afterDoubleQ[1:]))

                    nx = ''

                if beforeOpenBra:
                    self.tokensetF1.append(''.join(afterOpenBra[:1]))

                    self.tokensetF1.append(''.join(afterOpenBra[1:2]))

                    self.tokensetF1.append(''.join(afterOpenBra[2:]))

                    nx = ''

                if beginAccent2:
                    if ''.join(beginAccentT2[:2]) == 'a’':
                        self.tokensetF1.append(''.join(beginAccentT2[:2]))

                        self.tokensetF1.append(''.join(beginAccentT2[2:]))

                        nx = ""

                if beforeComma1:
                    if ''.join(beforeComma1) == ''.join(afterComma1[len(afterComma1) - 1:]):
                        self.tokensetF1.append(''.join(afterComma1[:len(afterComma1) - 1]))

                        self.tokensetF1.append(''.join(beforeComma1))

                        nx = ''

                if beforePeriod1:
                    if ''.join(beforePeriod1) == ''.join(afterPeriod1[len(afterPeriod1) - 1:]):
                        self.tokensetF1.append(''.join(afterPeriod1[:len(afterPeriod1) - 1]))

                        self.tokensetF1.append(''.join(beforePeriod1))

                        nx = ''

                if beforeQmark and nx not in ["[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                    if ''.join(beforeQmark) == ''.join(afterQmark[:1]):
                        ''

                    else:
                        x = afterQmark[len(afterQmark) - 1:]

                        self.tokensetF1.append(''.join(afterQmark[:len(afterQmark) - 1]))

                        self.tokensetF1.append(''.join(beforeQmark))

                        nx = ''

                if beforeComma:
                    x = afterComma[
                        len(afterComma) - 2:]  ## filtering for (eg: ],) type of tokens normally used in accademic text

                    y = afterComma[:1]  ## filtering for (eg: [ ,) type of tokens normally used in accademic text

                    if ''.join(x[:len(x) - 1]) in [']', ')'] and ''.join(y) in ['[', '(']:
                        self.tokensetF1.append(''.join(y))

                        self.tokensetF1.append(''.join(afterComma[1:len(afterComma) - 2]))

                        self.tokensetF1.append(''.join(x[:len(x) - 1]))

                        self.tokensetF1.append(''.join(beforeComma))

                        nx = ''

                    if ''.join(x[:len(x) - 1]) in [']', ')'] and ''.join(y) not in ['[', '(']:
                        self.tokensetF1.append(''.join(afterComma[:len(afterComma) - 2]))

                        self.tokensetF1.append(''.join(x[:len(x) - 1]))

                        self.tokensetF1.append(''.join(beforeComma))

                        nx = ''

                    if ''.join(x[:len(x) - 1]) not in [']', ')'] and ''.join(y) not in ['[', '(']:
                        xx = x[:len(x) - 1]

                        if xx:
                            if ''.join(afterComma[:1]) == '‘':
                                xxx = afterComma[len(afterComma) - 2:]

                                xxxx = afterComma[:]

                                self.tokensetF1.append(''.join(afterComma[:1]))

                                self.tokensetF1.append(''.join(afterComma[1: len(afterComma) - 2]))

                                self.tokensetF1.append(''.join(xxx[:1]))

                                self.tokensetF1.append(''.join(afterComma[len(afterComma) - 1:]))

                                nx = ''

                            else:
                                if len(afterComma) == 3:
                                    self.tokensetF1.append(''.join(afterComma[1:2]))

                                    self.tokensetF1.append(''.join(afterComma[len(afterComma) - 1:]))

                                    nx = ''



                                else:
                                    if len(afterComma) == 2:
                                        self.tokensetF1.append(''.join(afterComma[:1]))

                                        self.tokensetF1.append(''.join(afterComma[len(afterComma) - 1:]))

                                        nx = ''

                if beginAccent and ''.join(beginAccentT[len(beginAccentT) - 1:]) == '’' and not xx:
                    x = beginAccentT[1:]

                    self.tokensetF1.append(''.join(beginAccent))

                    self.tokensetF1.append(''.join(x[:len(x) - 1]))

                    self.tokensetF1.append(''.join(beginAccentT[len(beginAccentT) - 1:]))

                    self.Junk.append(''.join(beginAccentT[1:]))

                    nx = ''

                if beginAccent and ''.join(beginAccentT[len(beginAccentT) - 1:]) == ',' and not xx:
                    self.tokensetF1.append(''.join(beginAccent))

                    self.tokensetF1.append(''.join(beginAccentT[1:len(beginAccentT) - 1]))

                    self.tokensetF1.append(''.join(beginAccentT[len(beginAccentT) - 1:]))

                    self.Junk.append(''.join(beginAccent + beginAccentT[1:len(beginAccentT) - 1]))

                    nx = ''

                if beginAccent and ''.join(beginAccentT[len(beginAccentT) - 1:]) == '?' and not xx:
                    x = beginAccentT[len(beginAccentT) - 2:]

                    if ''.join(x[:len(x) - 1]) == '’':
                        self.tokensetF1.append(''.join(beginAccent))

                        self.tokensetF1.append(''.join(beginAccentT[1:len(beginAccentT) - 2]))

                        self.tokensetF1.append(''.join(x[:len(x) - 1]))

                        self.tokensetF1.append(''.join(beginAccentT[len(beginAccentT) - 1:]))

                        self.Junk.append(''.join(beginAccent) + beginAccentT[1:len(beginAccentT) - 1])

                        self.Junk.append(
                            ''.join(beginAccentT[1:len(beginAccentT) - 1] + beginAccentT[len(beginAccentT) - 1:]))

                        nx = ""

                if beginAccent and not beforeComma1 and not xx:
                    nx = ''

                if beforeAccent and ''.join(afterAccent[len(afterAccent) - 1:]) not in ['s']:
                    x = afterAccent[:3]

                    if ''.join(x[1:2]) == "’":
                        self.tokensetF1.append(''.join(afterAccent[:2]))

                        self.tokensetF1.append(''.join(afterAccent[2:]))

                        nx = ''

                    if ''.join(x[2:3]) == "’":
                        self.tokensetF1.append(''.join(afterAccent[:3]))

                        self.tokensetF1.append(''.join(afterAccent[3:]))

                        nx = ''

                if beforeEqual:
                    self.tokensetF1.append(''.join(beforeEqual))

                    self.tokensetF1.append(''.join(afterEqual[1:2]))

                    nx = ''

                if beforestroke:
                    self.tokensetF1.append(''.join(afterstroke[:1]))

                    self.tokensetF1.append(''.join(beforestroke))

                    self.tokensetF1.append(''.join(afterstroke[1:]))

                    nx = ''

                if currency:
                    x = len(currencySub)

                    self.tokensetF1.append(''.join(currency[:1]))

                    self.tokensetF1.append(''.join(currencySub[1: x - 1]))

                    self.tokensetF1.append(''.join(currencySub[x - 1:]))

                    nx = ''

                if doublQpnt and nx not in ["[?]", "[Name]", "[Placename]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]",
                                            "[7]", "[8]", "[9]"]:
                    x = doublQSub[1:len(doublQSub) - 1]

                    y = ''.join(doublQSub[len(doublQSub) - 1:])

                    m = ''.join(doublQpnt)

                    if y != '"' or y != '' and y == ')' and m != '(':
                        xy = (x + doublQSub[len(doublQSub) - 1:])

                        if ''.join(xy[len(xy) - 1:]) not in [')', ':', '?', ']']:
                            self.tokensetF1.append(''.join(m))

                            self.tokensetF1.append(''.join(xy))

                            nx = ' '


                        else:
                            self.tokensetF1.append(m)

                            self.tokensetF1.append(''.join(xy[:len(xy) - 1]))

                            self.tokensetF1.append(y)

                            nx = ''

                    if y == '"':
                        self.tokensetF1.append(''.join(doublQpnt))

                        self.tokensetF1.append(''.join(doublQSub[1:len(doublQSub) - 1]))

                        self.tokensetF1.append(''.join(y))

                        nx = ' '

                if comparativeParticles and len(comparativeParticles1) > 0:
                    if len(''.join(comparativeParticles1[1:])) > 1:
                        self.tokensetF1.append(''.join(comparativeParticles[:1]))

                        self.tokensetF1.append(''.join(comparativeParticles1[1:]))

                        nx = ""

                    if len(''.join(comparativeParticles1[1:])) == 1:
                        self.tokensetF1.append(''.join(comparativeParticles[:1] + comparativeParticles1[1:]))

                        nx = ''

                if hyphenT:
                    self.tokensetF1.append(''.join(hyphenT))

                    self.tokensetF1.append(''.join(hyphenT1))

                    nx = ''

                if hyphenN:
                    self.tokensetF1.append(''.join(hyphenN))  ## then append the stripped token into the list container

                    self.tokensetF1.append(''.join(hyphenN1))  ## then append the stripped token into the list container

                    nx = ''

                if hyphenH and nx not in ["h-uile", "h-ana-miannaibh"]:
                    self.tokensetF1.append(''.join(hyphenH))  ## then append the stripped token into the list container

                    self.tokensetF1.append(''.join(hyphenH1))  ## then append the stripped token into the list container

                    nx = ''

                if hyphenSe:
                    self.tokensetF1.append(''.join(hyphenSa[:1]))

                    self.tokensetF1.append(''.join(XhyphenSe[:1]))

                    nx = ''

                if hyphenSan:
                    self.tokensetF1.append(''.join(XhyphenSan[:1]))

                    self.tokensetF1.append(''.join(XhyphenSan[:1]))

                    nx = ''



                else:
                    self.tokensetF1.append(nx)

        for i, DA in enumerate(self.tokensetF1):
            """Here follows a long list of token elements. A future improvement would be to pull all of these
            elements into a csv file loaded into the tagger"""
            if DA == '1':
                self.tokensetF2.append('[1]')

                DA = ''

            if DA == '2':
                self.tokensetF2.append('[2]')

                DA = ''

            if DA == '3':
                self.tokensetF2.append('[3]')

                DA = ''

            if DA == '4':
                self.tokensetF2.append('[4]')

                DA = ''

            if DA == '5':
                self.tokensetF2.append('[5]')

                DA = ''

            if DA == '6':
                self.tokensetF2.append('[6]')

                DA = ''

            if DA == '7':
                self.tokensetF2.append('[7]')

                DA = ''

            if DA == '8':
                self.tokensetF2.append('[8]')

                DA = ''

            if DA == '9':
                self.tokensetF2.append('[9]')

                DA = ''

            if DA == ']':
                self.tokensetF2.append('')

                DA = ''

            if DA == 'Placename':
                self.tokensetF2.append('[Placename]')

                DA = ''

            if DA == 'a-réir':
                self.tokensetF2.append('a')

                self.tokensetF2.append('-')

                self.tokensetF2.append('réir')

                DA = ''

            if DA == "mi '":
                self.tokensetF2.append('mi')

                self.tokensetF2.extend("'")

                DA = ''

            if DA == "!)":
                self.tokensetF2.append('!')

                self.tokensetF2.extend(")")

                DA = ''

            if DA == "le'r":
                self.tokensetF2.append('le')

                self.tokensetF2.extend("'r")

                DA = ''

            if DA == "mi.”":
                self.tokensetF2.append("mi")

                self.tokensetF2.extend(".")

                self.tokensetF2.extend("”")

                # self.tokensetF1.remove("mi.”")

                DA = ''

            if DA == "mi,”":
                self.tokensetF2.append("mi")

                self.tokensetF2.extend(",")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "].":
                self.tokensetF2.append(']')

                self.tokensetF2.extend(".")

                DA = ''

            if DA == "?)":
                self.tokensetF2.append('?')

                self.tokensetF2.extend(")")

                DA = ''

            if DA == ".)":
                self.tokensetF2.append('.')

                self.tokensetF2.extend(")")

                DA = ''

            if DA == "”)":
                self.tokensetF2.append('”')

                self.tokensetF2.extend(")")

                DA = ''

            if DA == '); ':
                self.tokensetF2.append(')')

                self.tokensetF2.extend(";")

                DA = ''

            if DA == ") ":
                self.tokensetF2.append(')')

                DA = ''

            if DA == "?”":
                self.tokensetF2.append('?')

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "i.”":
                self.tokensetF2.append('i')

                self.tokensetF2.extend(".")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == ".’”":
                self.tokensetF2.append('.')

                self.tokensetF2.extend("”")

                DA = ''

            if DA == ",”":
                self.tokensetF2.append(',')

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "tu,”":
                self.tokensetF2.append('tu')

                self.tokensetF2.extend(",")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "”.":
                self.tokensetF2.append('”')

                self.tokensetF2.extend(".")

                DA = ''

            if DA == "às.”":
                self.tokensetF2.append('às')

                self.tokensetF2.extend(".")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "sa,”":
                self.tokensetF2.append('sa')

                self.tokensetF2.extend(",")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "’, ":
                self.tokensetF2.append('’')

                self.tokensetF2.extend(",")

                DA = ''

            if DA == ").":
                self.tokensetF2.append(')')

                self.tokensetF2.extend(".")

                DA = ''

            if DA == "),":
                self.tokensetF2.append(')')

                self.tokensetF2.extend(",")

                DA = ''

            if DA == "), ":
                self.tokensetF2.append(')')

                self.tokensetF2.extend(",")

                DA = ''

            if DA == ".”":
                self.tokensetF2.append('.')

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "’.”":
                self.tokensetF2.append('’')

                self.tokensetF2.extend(".")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == ",”":
                self.tokensetF2.append(',')

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "’,":
                self.tokensetF2.append('’')

                self.tokensetF2.extend(",")

                DA = ""

            if DA == "’.":
                self.tokensetF2.append("'")

                self.tokensetF2.extend(".")

                DA = ""

            if DA == "’ ":
                self.tokensetF2.append('’')

                DA = ''

            if DA == ");":
                self.tokensetF2.append(')')

                self.tokensetF2.extend(";")

                DA = ''

            if DA == "s’.”":
                self.tokensetF2.append('s’')

                self.tokensetF2.extend(".")

                self.tokensetF2.extend("”")

                DA = ''

            if DA == "tus":
                self.tokensetF2.append("tus'")

                DA = ''

            if DA == "aic":
                self.tokensetF2.append("aic'")

                DA = ''

            if DA == 'mi-fhìn':
                self.tokensetF2.append('mi')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhìn')

                DA = ''

            if DA == 'dh’èireas':
                self.tokensetF2.append('dh’')

                self.tokensetF2.append('èireas')

                DA = ''

            if DA == 'mi-fhèin':
                self.tokensetF2.append('mi')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhèin')

                DA = ''

            if DA == 'thu-fhèin':
                self.tokensetF2.append('thu')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhèin')

                DA = ''

            if DA == 'e-fhèin':
                self.tokensetF2.append('e')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhèin')

                DA = ''

            if DA == 'i-fhèin':
                self.tokensetF2.append('i')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhèin')

                DA = ''

            if DA == 'sinn-fhìn':
                self.tokensetF2.append('sinn')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhìn')

                DA = ''

            if DA == 'sibh-fhèin':
                self.tokensetF2.append('sibh')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhèin')

                DA = ''

            if DA == 'iad-fhèin':
                self.tokensetF2.append('iad')

                self.tokensetF2.append('-')

                self.tokensetF2.append('fhèin')

                DA = ''

            if DA == 'h-ana-miannaibh':
                self.tokensetF2.append('h-')

                self.tokensetF2.append('ana-miannaibh')

                DA = ''

            if DA == "a b'":
                self.tokensetF2.append('a')

                self.tokensetF2.append("b'")

                DA = ''

            if DA == 'dh’obair-riaghaltais':
                self.tokensetF2.append('dh’')

                self.tokensetF2.append('obair-riaghaltais')

                DA = ''

            if DA == "dh’fheumas":
                self.tokensetF2.append("dh'")

                self.tokensetF2.append('fheumas')

                DA = ''

            if DA == "dh'fheumas":
                self.tokensetF2.append("dh'")

                self.tokensetF2.append('fheumas')

                DA = ''

            if DA == "dh'fhaodas":
                self.tokensetF2.append("dh'")

                self.tokensetF2.append('fhaodas')

                DA = ''

            if DA == "dh’fhaodas":
                self.tokensetF2.append("dh'")

                self.tokensetF2.append('fhaodas')

                DA = ''

            if DA == "dh’fhàs":
                self.tokensetF2.append("dh’")

                self.tokensetF2.append('fhàs')

                DA = ''

            if DA == "dh'fhàs":
                self.tokensetF2.append("dh'")

                self.tokensetF2.append('fhàs')

                DA = ''

            if DA == 'Ban-righ' and "'nn" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'nn")

                DA = ''

            if DA == 'Dh' and "’fhaodainn" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append('Dh’')

                self.tokensetF2.append('fhaodainn')

                self.tokensetF1.remove("’fhaodainn")

                DA = ''

            if DA == 'Ban-righ' and "'nn" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'nn")

                DA = ''

            if DA == 'bhrist' and "’" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'ars' and "’" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'ars' and "'" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == 'mis' and "’" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'mis' and "'" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == 'thus' and "’" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'thus' and "'" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == 'oirr' and "’" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'ars' and "'" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == 'oidhch' and "’" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == '[' and "Placename]." in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append("[Placename]")

                self.tokensetF2.append(".")

                self.tokensetF1.remove("Placename].")

                DA = ''

            if DA == '[' and "Placename]" in self.tokensetF1[i:i + 2]:
                #  print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append("[Placename]")

                self.tokensetF1.remove("Placename].")

                DA = ''

            if DA == "A" and "n" in self.tokensetF1[
                                    i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is a blank token created in between

                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "do’" and "n" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "oirr" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "aig" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "chalp" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "chual" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "chual" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "tein" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "creids" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "creids" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "dhòmhs" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "toilicht" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "toilicht" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "dhòmhs" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "innt" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "innt" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "chreach-s" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "chreach-s" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "Do’" and "n" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "prionns" and "'" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == "prionns" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "De’" and "n" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "comhairl" and "’" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "òrain-“pop" and "”" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("”")

                DA = ''

            if DA == "f’" and "a" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a")

                DA = ''

            if DA == "F’" and "a" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a")

                DA = ''

            if DA == "de’" and "n" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "Gu" and "dé" in self.tokensetF1[i:i + 2]:
                # print (''.join(self.tokensetF1[i:i+3]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("dé")

                DA = ''

            if DA == "mu" and "thràth" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("thràth")

                DA = ''

            if DA == "Mu’" and "n" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "mu’" and "n" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "An" and "dràsda" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("dràsda")

                DA = ''

            if DA == "an" and "dràsda" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("dràsda")

                DA = ''

            if DA == "Srath" and "Chluaidh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Chluaidh")

                DA = ''

            if DA == "ma" and "tha" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("tha")

                DA = ''

            if DA == 'Roinn' and "Eòrpa" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Eòrpa")

                DA = ''

            if DA == 'Phort' and "Rìgh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Rìgh")

                DA = ''
            #
            # if DA == 'dhen' and "an" in self.tokensetF1[i:i + 2]:
            #     self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))
            #
            #     self.tokensetF1.remove("an")
            #
            #     DA = ''

            # if DA == 'bhon' and "'n" in self.tokensetF1[i:i + 2]:
            #     self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))
            #
            #     # self.tokensetF1.remove("bhon")
            #
            #     self.tokensetF1.remove("'n")
            #
            #     DA = ''

            if DA == 'làn' and "-Ghàidhealtachd" in self.tokensetF1[
                                                    i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 3]))

                # self.tokensetF1.remove("bhon")

                self.tokensetF1.remove("-Ghàidhealtachd")

                DA = ''

            if DA == 'leth' and "-Ghàidhealtachd" in self.tokensetF1[
                                                     i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between

                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 3]))

                # self.tokensetF1.remove("bhon")

                self.tokensetF1.remove("-Ghàidhealtachd")

                DA = ''

            if DA == 'bhon' and "an" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ''

            if DA == "o’" and "n" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == 'bhon' and "a'" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a'")

                DA = ''

            if DA == 'Loch' and "Aillse" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Aillse")

                DA = ''

            if DA == 'a' and "b'" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("b'")

                DA = ''

            if DA == 'a' and "b’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("b’")

                DA = ''

            if DA == "a'" and "shineach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                # self.tokensetF1.remove("a'")

                self.tokensetF1.remove("shineach")

                DA = ''

            if DA == "a’" and "s" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                # self.tokensetF1.remove("a'")

                self.tokensetF1.remove("s")

                DA = ''

            if DA == "a" and "shineach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("shineach")

                DA = ''

            if DA == "Caledonian" and "Mac" in self.tokensetF1[i:i + 2] and "a’ " in self.tokensetF1[
                                                                                     i:i + 3] and "Bhruthainn" in self.tokensetF1[
                                                                                                                  i:i + 4]:
                # print (' '.join(self.tokensetF1[i:i+4]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 4]))

                DA = ''

            if DA == "Caledonian" and "Mac" in self.tokensetF1[i:i + 2] and "a' " in self.tokensetF1[
                                                                                     i:i + 3] and "Bhruthainn" in self.tokensetF1[
                                                                                                                  i:i + 4]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 4]))

                self.tokensetF1.remove("Mac")

                self.tokensetF1.remove("a'")

                self.tokensetF1.remove("Bhruthainn")

                DA = ''

            if DA == 'dhan' and "an" in self.tokensetF1[i:i + 2] and "sin" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append('dhan')

                self.tokensetF2.append('an sin')

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("sin")

                DA = ''
            #
            # if DA == 'fon' and "a'" in self.tokensetF1[i:i + 2]:
            #     self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))
            #
            #     self.tokensetF1.remove("a'")
            #
            #     DA = ''

            if DA == 's' and "a" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a")

                DA = ''

            if DA == 'prionns' and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'leams' and "'" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == 'leams' and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'fon' and "an" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ''

            if DA == 'fon' and "an" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ''

            if DA == 'ionnsaicht' and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == 'ionnsaicht' and "'" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("'")

                DA = ''

            if DA == 'Dùn' and "Èideann" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Èideann")

                DA = ''

            if DA == 'an' and "toiseach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("toiseach")

                DA = ''

            if DA == "‘n" and "toiseach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("toiseach")

                DA = ''

            if DA == "'n" and "toiseach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("toiseach")

                DA = ''

            if DA == "a" and "tuath" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("tuath")

                DA = ''

            if DA == "air" and "choireigin-ach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("choireigin-ach")

                DA = ''

            if DA == "an" and "raoir" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("raoir")

                DA = ''

            if DA == "a" and "chaoidh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("chaoidh")

                DA = ''

            if DA == 'mun' and "a'" in self.tokensetF1[i:i + 2]:
                # print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a'")

                DA = ''

            if DA == 'mun' and "an" in self.tokensetF1[i:i + 2]:
                # print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ''

            if DA == 'on' and "a'" in self.tokensetF1[i:i + 2]:
                # print (' '.join(self.tokensetF1[i:i+2]))

                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a'")

                DA = ''

            if DA == 'on' and "an" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ''

            # if DA == 'ron' and "a'" in self.tokensetF1[i:i + 2]:
            #     self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))
            #
            #     self.tokensetF1.remove("a'")
            #
            #     DA = ''

            if DA == 'oidhch' and "’." in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("oidhch’")

                self.tokensetF2.append(".")

                self.tokensetF1.remove("’.")

                DA = ''

            # if DA == 'ron' and "an" in self.tokensetF1[i:i + 2]:
            #     self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))
            #
            #     self.tokensetF1.remove("an")
            #
            #     DA = ''
            #
            # if DA == 'tron' and "a'" in self.tokensetF1[i:i + 2]:
            #     self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))
            #
            #     self.tokensetF1.remove("a'")
            #
            #     DA = ''

            if DA == 'Coille' and "Chaoil" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Chaoil")

                DA = ''

            if DA == 'Gleann' and "Dail" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Dail")

                DA = ''

            if DA == 'Ruaidh' and "Mhònaidh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Mhònaidh")

                DA = ''

            if DA == 'tron' and "an" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ''

            if DA == "de'" and "n" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "mu'" and "n" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "do'" and "n" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("n")

                DA = ''

            if DA == "doesn'" and "t" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("t")

                DA = ''

            if DA == "a" and "staigh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("staigh")

                DA = ''

            if DA == "a" and "steach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("steach")

                DA = ''

            if DA == "a" and "mach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("mach")

                DA = ''

            if DA == "sam" and "bith" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bith")

                DA = ''

            if DA == "Roinn" and "Eorpa" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Eorpa")

                DA = ''

            if DA == "air" and "choireigin" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("choireigin")

                DA = ''

            if DA == "a" and "sin" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("sin")

                DA = ''

            if DA == "an" and "sin" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("sin")

                DA = ''

            if DA == "Eilean" and "Sgitheanach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Sgitheanach")

                DA = ''

            if DA == "Fairy" and "Bridge" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Bridge")

                DA = ''

            if DA == "Eilean" and "Tiridhe" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Tiridhe")

                DA = ''

            if DA == "a" and "chèile" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("chèile")

                DA = ''

            if DA == "Dùn" and "Bheagain" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Bheagain")

                DA = ''

            if DA == "Gleann" and "Ois" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Ois")

                DA = ''

            if DA == "ana" and "nàdarra" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("nàdarra")

                DA = ''

            if DA == "An" and "Aodann" in self.tokensetF1[i:i + 2] and "Bàn" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("Aodann")

                self.tokensetF1.remove("Bàn")

                DA = ''

            if DA == "[" and "?" in self.tokensetF1[i:i + 2] and "]" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("?")

                self.tokensetF1.remove("]")

                DA = ''

            if DA == "a" and "bhòn-dè" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bhòn-dè")

                DA = ''

            if DA == "a'" and "bhòn-dè" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bhòn-dè")

                DA = ''

            if DA == "Pholl" and "a'" in self.tokensetF1[i:i + 2] and "Ghrùthain" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("Ghrùthain")

                self.tokensetF1.remove("a'")

                DA = ''

            if DA == "ann" and "a" in self.tokensetF1[i:i + 2] and "shiud" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("shiud")

                DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "shiud" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("shiud")

                DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "seo" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("ann")

                DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "siud" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("siud")

                DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "sin" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("sin")

                DA = ''

            if DA == "a'" and "bhòn-raoir" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a'")

                self.tokensetF1.remove("bhòn-raoir")

                DA = ''

            if DA == "a'" and "s" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("s")

                DA = ''

            if DA == "a" and "bhòn-raoir" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("bhòn-raoir")

                DA = ''

            if DA == "a" and "bhòn" in self.tokensetF1[i:i + 2] and "raoir" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("bhòn")

                self.tokensetF1.remove("raoir")

                DA = ''

            if DA == "a'" and "bhòn-uiridh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a'")

                self.tokensetF1.remove("bhòn-uiridh")

                DA = ""

            if DA == "a" and "bhòn-uiridh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("bhòn-uiridh")

                DA = ""

            if DA == "a" and "bhòn" in self.tokensetF1[i:i + 2] and "uiridh" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("bhòn")

                self.tokensetF1.remove("uiridh")

                DA = ""

            if DA == "a'" and "bhòn-uiridh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bhòn-uiridh")

                DA = ""

            if DA == "a" and "bhos" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bhos")

                DA = ""

            if DA == "a" and "bhàn" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bhàn")

                DA = ""

            if DA == "a" and "mach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("mach")

                DA = ""

            if DA == "a" and "màireach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("màireach")

                DA = ""

            if DA == "am" and "bliadhna" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('am')

                self.tokensetF1.remove("bliadhna")

                DA = ""

            if DA == "a" and "muigh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('a')

                self.tokensetF1.remove("muigh")

                DA = ""

            if DA == "a" and "nall" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("nall")

                DA = ""

            if DA == "an" and "ath-bhliadhna" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("ath-bhliadhna")

                DA = ""

            if DA == "an" and "ath" in self.tokensetF1[i:i + 2] and "bhliadhna" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("ath")

                self.tokensetF1.remove("bhliadhna")

                DA = ""

            if DA == "an" and "ath-oidhche" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("ath-oidhche")

                DA = ""

            if DA == "an" and "ath" in self.tokensetF1[i:i + 2] and "oidhche" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("ath")

                self.tokensetF1.remove("oidhche")

                DA = ""

            if DA == "an" and "ath" in self.tokensetF1[i:i + 2] and "oidhch'" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("ath")

                self.tokensetF1.remove("oidhch'")

                DA = ""

            if DA == "an" and "ath-oidhche" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("ath-oidhche")

                DA = ""

            if DA == "an" and "ath-sheachdainn" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("ath-sheachdainn")

                DA = ""

            if DA == "an" and "ath" in self.tokensetF1[i:i + 2] and "sheachdainn" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("sheachdainn")

                DA = ""

            if DA == "an" and "ath-sheachdain" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("ath-sheachdain")

                DA = ""

            if DA == "an" and "ath" in self.tokensetF1[i:i + 2] and "sheachdain" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                DA = ""

            if DA == "an" and "còmhnaidh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ""

            if DA == "an" and "de" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("de")

                DA = ""

            if DA == "an" and "diugh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("diugh")

                DA = ""

            if DA == "an" and "dràsta" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("dràsta")

                DA = ""

            if DA == "an" and "earar" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("earar")

                DA = ''

            if DA == "an" and "earair" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("earair")

                DA = ""

            if DA == "a" and "nis" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("nis")

                DA = ''

            if DA == "a" and "nisd" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("nisd")

                DA = ""

            if DA == "a" and "nuas" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("nuas")

                DA = ""

            if DA == "a" and "uiridh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("uiridh")

                DA = ''

            if DA == "a" and "null" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("null")

                DA = ""

            if DA == "a" and "raoir" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("raoir")

                DA = ""

            if DA == "a" and "rithist" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("rithist")

                DA = ""

            if DA == "a" and "staidh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("staidh")

                DA = ""

            if DA == "a" and "steach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("steach")

                DA = ""

            if DA == "b" and "e" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("b'")

                self.tokensetF2.append("e")

                self.tokensetF1.remove("b")

                DA = ""

            if DA == "mi'":
                self.tokensetF2.append("mi")

                self.tokensetF2.append("'")

                self.tokensetF1.remove("mi'")

                DA = ""

            if DA == "na" and "s" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("na's")

                self.tokensetF1.remove('s')

                DA = ""

            if DA == "na" and "bu" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('bu')

                DA = ""

            if DA == "a" and "bu'" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bu'")

                DA = ""

            if DA == "Inbhir" and "Nis" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("Nis")

                DA = ""

            if DA == "ann" and "am" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("am")

                DA = ""

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("an")

                DA = ""

            if DA == "an" and "siud" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("siud")

                DA = ""

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "siud" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("siud")

                DA = ""

            if DA == "an" and "am" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("am")

                DA = ""

            if DA == "pòs" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('’')

                DA = ''

            if DA == "gàir" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('’')

                DA = ''

            if DA == "an" and "ceart-uair" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('ceart-uair')

                DA = ''

            if DA == "an" and "uairsin" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('uairsin')

                DA = ''

            if DA == "an" and "sineach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('sineach')

                DA = ''

            if DA == "an" and "dràsda" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('dràsda')

                DA = ''

            if DA == "ma" and "tha" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('tha')

                DA = ''

            if DA == "a" and "sineach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('sineach')

                DA = ''

            if DA == "an" and "ceartuair" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('ceartuair')

                DA = ''

            if DA == "fhad" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "ge" and "brì" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('brì')

                DA = ''

            if DA == "ge" and "brith" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove('brith')

                DA = ''

            if DA == "ge" and "be" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("be")

                DA = ''

            if DA == "ge" and "'s" in self.tokensetF1[i:i + 2] and "bith" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("'s")

                self.tokensetF1.remove("bith")

                DA = ''

            if DA == "gar" and "bith" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("bith")

                DA = ''

            if DA == "air" and "falbh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("falbh")

                DA = ''

            if DA == "an" and "làrna-mhàireach" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("làrna-mhàireach")

                DA = ''

            if DA == "ma" and "dh'" in self.tokensetF1[i:i + 2] and "fhaoidhte" in self.tokensetF1[i:i + 3]:
                x = self.tokensetF1[i:i + 3]

                xx = ' '.join(x[:2])

                y = ''.join(x[2:])

                # print (xx + y)

                self.tokensetF2.append(xx + y)

                self.tokensetF1.remove("dh'")

                self.tokensetF1.remove("fhaoidhte")

                DA = ''

            if DA == "ma" and "dh'" in self.tokensetF1[i:i + 2] and "fhaoite" in self.tokensetF1[i:i + 3]:
                x = self.tokensetF1[i:i + 3]

                xx = ' '.join(x[:2])

                y = ''.join(x[2:])

                self.tokensetF2.append(xx + y)

                self.tokensetF1.remove("dh'")

                self.tokensetF1.remove("fhaoite")

                DA = ''

            if DA == "math" and "dh'" in self.tokensetF1[i:i + 2] and "fhaoite" in self.tokensetF1[i:i + 3]:
                x = self.tokensetF1[i:i + 3]

                xx = ' '.join(x[:2])

                y = ''.join(x[2:])

                self.tokensetF2.append(xx + y)

                self.tokensetF1.remove("dh'")

                self.tokensetF1.remove("fhaoite")

                DA = ''

            if DA == "math" and "dh'" in self.tokensetF1[i:i + 2] and "fhaoidte" in self.tokensetF1[i:i + 3]:
                x = self.tokensetF1[i:i + 3]

                # print (x)

                xx = ' '.join(x[:2])

                y = ''.join(x[2:])

                # print (xx + y)

                self.tokensetF2.append(xx + y)

                self.tokensetF1.remove("dh'")

                self.tokensetF1.remove("fhaoidte")

                DA = ''

            if DA == "gu" and "dè" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("gu")

                DA = ''

            if DA == "a" and "chèil" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("chèil")

                DA = ''

            if DA == "mu" and "dheireadh" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("dheireadh")

                DA = ''

            if DA == "a" and "h-uile" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("h-uile")

                DA = ''

            if DA == "a" and "seo" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("seo")

                DA = ''

            if DA == "an" and "seo" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("seo")

                DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "seo" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("seo")

                DA = ''

            if DA == "a" and "niste" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("niste")

                DA = ''

            if DA == "a" and "niste" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("niste")

                DA = ''

            if DA == "ge" and "b'" in self.tokensetF1[i:i + 2] and "e" in self.tokensetF1[
                                                                          i:i + 3] and "air" in self.tokensetF1[
                                                                                                i:i + 4] and "bith" in self.tokensetF1[
                                                                                                                       i:i + 5]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 5]))

                self.tokensetF1.remove("b'")

                self.tokensetF1.remove("e")

                self.tokensetF1.remove("air")

                self.tokensetF1.remove("bith")

                DA = ''

            if DA == "tuilleadh" and "'s" in self.tokensetF1[i:i + 2] and "a" in self.tokensetF1[
                                                                                 i:i + 3] and "chòir" in self.tokensetF1[
                                                                                                         i:i + 4]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 4]))

                self.tokensetF1.remove("'s")

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("chòir")

                DA = ''

            if DA == "tuilleadh" and "'s" in self.tokensetF1[i:i + 2] and "a" in self.tokensetF1[
                                                                                 i:i + 3] and "chòir" in self.tokensetF1[
                                                                                                         i:i + 4]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 4]))

                self.tokensetF1.remove("'s")

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("chòir")

                DA = ''

            if DA == "tuilleadh" and "sa" in self.tokensetF1[i:i + 2] and "chòir" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("sa")

                self.tokensetF1.remove("chòir")

                DA = ''

            if DA == "ann" and "a'" in self.tokensetF1[i:i + 2] and "shiudach" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("shiudach")

                self.tokensetF1.remove("a'")

                DA = ''

            if DA == "ann" and "a" in self.tokensetF1[i:i + 2] and "shiudach" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("shiudach")

                self.tokensetF1.remove("a")

                DA = ''

            if DA == "a's" and "a" in self.tokensetF1[i:i + 2] and "sineach" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("sineach")

                DA = ''

            if DA == "ann" and "a" in self.tokensetF1[i:i + 2] and "shineach" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("ann")

                DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "shin" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("shin")

                DA = ''

            else:
                if DA == "ann" and "an" in self.tokensetF1[i:i + 2]:
                    self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                    self.tokensetF1.remove("an")

                    # self.tokensetF1.remove("shin")

                    DA = ''

            if DA == "ann" and "an" in self.tokensetF1[i:i + 2] and "seo" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("an")

                self.tokensetF1.remove("seo")

                DA = ''


            else:
                if DA == "ann" and "seo" in self.tokensetF1[i:i + 2]:
                    self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 2]))

                    self.tokensetF1.remove("seo")

                    # self.tokensetF1.remove("shin")

                    DA = ''

            if DA == "brist" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "lost-s" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "thoilicht" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "thus" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "ath-oidhch" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "bonnant" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "bheath" and "’." in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("bheath’")

                self.tokensetF2.append(".")

                self.tokensetF1.remove("’.")

                DA = ''

            if DA == "bheath" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "chual" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "uisg" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "uisg" and "’." in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("uisg’")

                self.tokensetF2.append(".")

                self.tokensetF1.remove("’.")

                DA = ''

            if DA == "teoth" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "do-sheachant" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "dòch" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "bioraicht" and "’" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append(''.join(self.tokensetF1[i:i + 2]))

                self.tokensetF1.remove("’")

                DA = ''

            if DA == "ann" and "a" in self.tokensetF1[i:i + 2] and "shin" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("shin")

                DA = ''

            if DA == "ann" and "a" in self.tokensetF1[i:i + 2] and "sheo" in self.tokensetF1[i:i + 3]:
                self.tokensetF2.append(' '.join(self.tokensetF1[i:i + 3]))

                self.tokensetF1.remove("a")

                self.tokensetF1.remove("sheo")

                DA = ''

            if DA == "(’" and "S" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("(")

                self.tokensetF2.append("’S")

                self.tokensetF1.remove("S")

                DA = ''

            if DA == "(’" and "s" in self.tokensetF1[i:i + 2]:
                self.tokensetF2.append("(")

                self.tokensetF2.append("’s")

                self.tokensetF1.remove("s")

                DA = ''


            else:
                self.tokensetF2.append(DA)

        for i, nn in enumerate(self.tokensetF2):
            secondQuots = re.findall(r"(\w+[' " "])", str(nn))  ## apostrophe

            secondQuots1 = re.findall(r"(?<!=[' " "])\w+", str(nn))

            if len(nn) < 4 and secondQuots and "s" in self.tokensetF2[
                                                      i:i + 2]:  ##  reconstructs possessive tokens (eg M's)



                dd = ''.join(self.tokensetF2[i:i + 2])

                self.tokensetF3.append(dd.strip())

                nn = ''

            if nn in self.abbr and "." in self.tokensetF2[i:i + 2]:
                self.tokensetF3.append(''.join(self.tokensetF2[i:i + 2]))

                nn = ''

            if nn == "la’" and "r-na-mhàireach" in self.tokensetF2[i:i + 2]:
                self.tokensetF3.append(''.join(self.tokensetF2[i:i + 2]))

                nn = ''

                self.Junk.append("r-na-mhàireach")

            if nn == "dhìoms" and "’" in self.tokensetF2[i:i + 2]:
                self.tokensetF3.append(''.join(self.tokensetF2[i:i + 2]))

                self.tokensetF2.remove("’")


            else:
                self.tokensetF3.append(nn.strip())

        for q in self.tokensetF3:
            if q not in self.Junk and ''.join(q) != '':
                self.tokensetF4.append(q)

        for x in self.tokensetF4:
            y = re.sub("[‘’´`]", "'", str(x))  # normalising apostrophes

            w = re.sub("[“”]", '"', str(y))

            self.tokensetF5.append(w)

        return self.tokensetF5
