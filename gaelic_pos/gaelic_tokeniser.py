import re
import codecs
import os

class Tokeniser():
    def __init__(self):
        lines = []
        # list of Gaelic and English abbreviations
        with open(os.path.join(os.path.dirname(__file__), "Data", "Abbrv.csv")) as f:
            for line in f:
                lines.append(str(line))
        self.abbr = re.findall(r"\w+\S+", " ".join(lines))
        self.exceptions = ["'ac", "[?]", '`ac', "'gam", "`gam", "'gad", "`gad", "'ga", "`ga", "'gar", "`gar", "'gur",
                           "`gur", "'gan", "`gan", "'m", "`m", "'n", "`n", "'nam", "`nam", "'nad", "`nad", "'na", "`na",
                           "'nar", "`nar", "‘nar", "'nur", "`nur", "'nan", "`nan", "'san", "'San", "‘San", "`san",
                           "‘sa", "`sa", "‘S", "'S", "`S", "‘ac", "‘ga", "`ga", "‘gan", "`gan", "h-uile"]
        
    def normalise_quotes(self, token):
        y = re.sub("[‘’´`]", "'", str(token))  # normalising apostrophes
        w = re.sub("[“”]", '"', str(y))
        return w

    def _punctuation(self, tokens):
        '''Also does abbreviations.'''
        result = []
        
        for nx in tokens:
            if nx == self.abbr or nx in self.exceptions:
                result.append(nx)
            elif re.findall(r"(\A[$£])", str(nx)):
                result.extend([nx[:1], nx[1:]])

            elif re.match(r'\W+\w+', nx):

                result.extend([c for c in re.search(r'^\W+',nx).group(0)])
                result.append(re.search(r'\w+$', nx).group(0))
            elif re.match(r'\W+\w+\W+', nx):
                result.extend([c for c in re.search(r'^\W+',nx).group(0)])
                result.append(re.search(r'\w+', nx).group(0))
                result.extend([c for c in re.search(r'["),.;:?!’”]+$', nx).group(0)])
                
            elif re.match(r'''\w*["),.;:?!”]+''', nx):

                text = ''.join(re.search(r'\w*', nx).group(0))
                if text != '': result.append(text)
                result.extend([c for c in re.search(r'["),.;:?!’”]+$', nx).group(0)])

            elif nx.startswith("h-") or nx.startswith("n-") or nx.startswith("t-"):
                result.extend([nx[:2], nx[2:]])

            else:
                result.append(nx)
        return result
    
    def tokenise(self, text):
        Junk = []
        tokensetF1 = self._punctuation(text.split())
        tokensetF2 = []
        for i,w0 in enumerate(tokensetF1):
            w1 = tokensetF1[i+1] if i < len(tokensetF1) - 1 else "<END>"
            w2 = tokensetF1[i+2] if i < len(tokensetF1) - 2 else "<END>"
            w3 = tokensetF1[i+3] if i < len(tokensetF1) - 3 else "<END>"
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

            elif w0 == "le'r":
                tokensetF2.extend(['le', "'r"])
            elif w0 == "].":
                tokensetF2.extend([']',"."])
            elif w0 == "?)":
                tokensetF2.append('?')
                tokensetF2.extend(")")
            elif w0 == "”)":
                tokensetF2.append('”')

                tokensetF2.extend(")")
            elif w0 == "?”":
                tokensetF2.append('?')

                tokensetF2.extend("”")

            elif w0 == ".’”":
                tokensetF2.append('.')

                tokensetF2.extend("”")

            elif w0 == ",”":
                tokensetF2.append(',')

                tokensetF2.extend("”")

            elif w0 == "”.":
                tokensetF2.append('”')

                tokensetF2.extend(".")

            elif w0 == ".”":
                tokensetF2.append('.')

                tokensetF2.extend("”")

            elif w0 == "’,":
                tokensetF2.append('’')

                tokensetF2.extend(",")

            elif w0 == "’.":
                tokensetF2.append("'")

                tokensetF2.extend(".")

            elif w0 == "s’.”":
                tokensetF2.append('s’')

                tokensetF2.extend(".")

                tokensetF2.extend("”")
                
            elif re.match('(mi|e|i|thu|sibh|iad)-fhèin$', w0):
                tokensetF2.extend([w0[:-6], '-', w0[-5:]])

            elif re.match('(sinn|mi)-fhìn$',w0):
                tokensetF2.extend([w0[:-5],'-',w0[-4:]])

            elif w0 == 'h-ana-miannaibh':
                tokensetF2.extend(['h-','ana-miannaibh'])
            elif w0 == "a b'":
                tokensetF2.extend(['a',"b'"])
            elif w0 == 'dh’obair-riaghaltais':
                tokensetF2.append('dh’')

                tokensetF2.append('obair-riaghaltais')

            elif w0 in ["dh’fheumas","dh'fheumas","dh'fhaodas", "dh’fhaodas", "dh’fhàs", "dh'fhàs"]:
                tokensetF2.extend([w0[0:3], w0[3:]])

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


            elif w0 in ['ars','bhrist','mis','oidhch','oirr','thus'] and w1 in ["’", "'"]:
                tokensetF2.append("%s%s" % (w0,w1))
                tokensetF1.remove("’")

            elif w0 == '[' and "Placename]." in tokensetF1[i:i + 2]:
                tokensetF2.append("[Placename]")
                tokensetF2.append(".")
                tokensetF1.remove("Placename].")
              
            elif w0 == '[' and "Placename]" in tokensetF1[i:i + 2]:

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
              
            elif w0 in ["aig","chalp","chual","comhairl","creids","oirr","chreach-s","cuimhn","dhòmhs","innt","prionns","tein","toilicht"] and w1 in ["'", "’"]:
                tokensetF2.append("%s%s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 in ["Do’","De’","de’","Mu’","mu’"] and w1 == "n":
                tokensetF2.append("%s%s" % (w0,w1))
                tokensetF1.remove(w1)

            elif w0 == "òrain-“pop" and "”" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("”")

            elif w0 == "f’" and "a" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("a")

            elif w0 == "F’" and "a" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("a")

            elif w0 == "Gu" and "dé" in tokensetF1[i:i + 2]:
                tokensetF2.append("Gu dé")
                tokensetF1.remove("dé")
            elif w0 == "mu" and "thràth" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("thràth")

            elif w0 in ["An","an"] and w1 in ["dràsda", "dràsta"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)
              
            elif w0 == "ma" and "tha" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove("tha")
              
            elif w0 in ['làn','leth'] and "-Ghàidhealtachd" in tokensetF1[i:i + 3]:  # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between

                tokensetF2.append(''.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("-Ghàidhealtachd")

            elif w0 == 'bhon' and w1 in ["an","a'"]:
                tokensetF2.append(' '.join([w0, w1]))
                tokensetF1.remove(w1)

            elif w0 == "o’" and w1 == "n":
                tokensetF2.append("%s%s" % (w0, w1))
                tokensetF1.remove("n")
            # toponyms
            elif w0 in ['Caolas', 'Chaolas', 'Coille', 'Dùn', 'Eilean', 'Gleann', 'Inbhir', 'Loch', 'Phort', 'Port', 'Roinn', 'Ruaidh', 'Rubha', 'Srath', 'Tràigh'] and re.match('[A-ZÈ][a-zìò]+', w1):
                tokensetF2.append(' '.join([w0, w1]))
                tokensetF1.remove(w1)

            elif w0 == 'a' and w1 in ["b'", "b’"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)
              
            elif w0 in ["a'", "a"] and w1 == "shineach":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "a’" and w1 == "s":
                tokensetF2.append("%s%s" % (w0, w1))
                tokensetF1.remove("s")
          
            elif w0 == "Caledonian" and w1 == "Mac" and w2 in ["a’", "a'"] and w3 == "Bhruthainn":
                tokensetF2.append("%s %s %s %s" % (w0,w1,w2,w3))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)
                tokensetF1.remove(w3)
                    
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

            elif w0 == 'ionnsaicht' and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))
                tokensetF1.remove("’")
      
            elif w0 == 'ionnsaicht' and "'" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("'")

            elif w0 in ['an', "‘n", "'n"] and w1 == "toiseach":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "a" and w1 in ["deas", "tuath"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "air" and "choireigin-ach" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("choireigin-ach")

            elif w0 == "an" and "raoir" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("raoir")

            elif w0 == "a" and "chaoidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("chaoidh")

            elif w0 in ['mun', "on", "tron"] and w1 in ["a'", "an"]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w1)

            elif w0 == 'oidhch' and "’." in tokensetF1[i:i + 2]:
                tokensetF2.append("oidhch’")

                tokensetF2.append(".")

                tokensetF1.remove("’.")

            elif w0 in ["de'", "mu'", "do'"] and w1 == "n":
                tokensetF2.append("%s%s" % (w0, w1))

                tokensetF1.remove(w1)

            elif w0 == "doesn'" and "t" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("t")

            elif w0 == "a" and w1 in ["mach", "muigh", "steach", "staigh"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)
          
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

            elif w0 == "An" and w1 == "Aodann" and w2 == "Bàn":
                tokensetF2.append("%s %s %s" % (w0,w1,w2))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "[" and "?" in tokensetF1[i:i + 2] and "]" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("?")

                tokensetF1.remove("]")

            elif w0 in ["a","a'"] and w1 in ["bhòn-dè","bhòn-raoir", "bhòn-uiridh"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "Pholl" and "a'" in tokensetF1[i:i + 2] and "Ghrùthain" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove("Ghrùthain")
                tokensetF1.remove("a'")

            elif w0 == "ann" and w1 in ["a","an"] and w2 in ["seo","shiud","sin","siud"]:
                tokensetF2.append("%s %s %s" % (w0,w1,w2))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "a'" and "s" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("s")
                

            elif w0 == "a" and "bhòn" in tokensetF1[i:i + 2] and "raoir" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("a")

                tokensetF1.remove("bhòn")

                tokensetF1.remove("raoir")


            elif w0 == "a" and "bhòn" in tokensetF1[i:i + 2] and "uiridh" in tokensetF1[i:i + 3]:
                tokensetF2.append("%s %s %s" % (w0, w1, w2))
                tokensetF1.remove(w0)
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

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

            elif w0 == "an" and w1 in ["ath-bhliadhna", "ath-oidhche", "ath-sheachdainn","de", "diugh", "earar", "earair"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "an" and w1 == "ath" and w2 in ["bhliadhna", "oidhche", "oidhch'","sheachdain","sheachdainn"]:
                tokensetF2.append("%s %s %s" % (w0,w1,w2))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "an" and "còmhnaidh" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("an")

            elif w0 == "a" and w1 in ["nis", "nisd", "raoir", "rithist", "uiridh"]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w1)

            elif w0 == "a" and w1 in ["nall", "nuas", "null", "staidh","steach"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)
    
            elif w0 == "b" and "e" in tokensetF1[i:i + 2]:
                tokensetF2.append("b'")

                tokensetF2.append("e")

                tokensetF1.remove("b")

            elif w0 == "mi'":
                tokensetF2.extend(["mi", "'"])

            elif w0 == "na" and w1 == "s":
                tokensetF2.append("na's")

                tokensetF1.remove('s')

            elif w0 in ["a", "na"] and w1 == "bu":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "ann" and w1 in ["am","an"]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w1)
       
            elif w0 == "an" and w1 == "siud":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

            elif w0 == "ann" and "an" in tokensetF1[i:i + 2] and "siud" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "an" and "am" in tokensetF1[i:i + 2]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove("am")

            elif w0 == "pòs" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove('’')

            elif w0 == "gàir" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove('’')

            elif w0 == "fhad" and "’" in tokensetF1[i:i + 2]:
                tokensetF2.append(''.join(tokensetF1[i:i + 2]))

                tokensetF1.remove("’")

            elif w0 == "an" and w1 in ["ceartuair", "ceart-uair", "uairsin"]:
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w1)

            elif w0 in ["a","an"] and w1 == "sineach":
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w1)

            elif w0 == "ma" and w1 == "tha":
                tokensetF2.append("%s %s" % (w0, w1))

                tokensetF1.remove(w1)
 
            elif w0 == "ge" and w1 in ["be", "brì", "brith"]:
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

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
                
            elif w0 == "h-" and w1 == "uile":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)
                
            elif w0 == "a" and w1 == "h-uile":
                tokensetF2.append("%s %s" % (w0, w1))
                tokensetF1.remove(w1)

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

            elif w0 == "a's" and "a" in tokensetF1[i:i + 2] and "sineach" in tokensetF1[i:i + 3]:
                tokensetF2.append(' '.join(tokensetF1[i:i + 3]))

                tokensetF1.remove("a")

                tokensetF1.remove("sineach")

            elif w0 == "ann" and w1 == "an"  and w2 in ["seo", "shin"]:
                tokensetF2.append("%s %s %s" % (w0,w1,w2))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

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

            elif w0 == "ann" and w1 in ["a", "a'"] and w2 in ["sheo", "shin", "shineach", "shiudach"]:
                tokensetF2.append("%s %s %s" % (w0, w1, w2))
                tokensetF1.remove(w1)
                tokensetF1.remove(w2)

            elif w0 == "(’" and w1 in ["s","S"]:
                tokensetF2.extend(["(","’" + w1])
                tokensetF1.remove(w1)

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
