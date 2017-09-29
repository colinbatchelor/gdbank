
# -*- coding: utf-8 -*-                                                           #
# Brill-based Scottish Gaelic Tokeniser and Part-of-Speech Tagger                 #
#                                                                                 #
# Copyright (C) 2013-2016 University of Edinburgh                                 #
#                                                                                 #
# Authors: William Lamb <w.lamb@ed.ac.uk> and Samuel Danso <sdanso@gmail.com>     #
#                                                                                 #
# For license information, see AboutFile.txt                                      #
###################################################################################

import codecs
import csv
import os
import pickle
import time
from tkinter import *

datadir = os.path.join(os.getcwd(), "Data")
aboutFN = os.path.join(datadir, "AboutFile.txt")
helpFN = os.path.join(datadir, "HelpFile.txt")
abbrevFN = os.path.join(datadir, "Abbrv.csv")  # list of Gaelic and English abbreviations
englishlexFN = os.path.join(datadir, "EnglishLexiconFinal11062015.csv")  # list of English words

modeldir = os.path.join(os.getcwd(), "Model")
defaultFN = os.path.join(modeldir, "DefaultModel_310516.pkl")  # trained on 117,381 manually-tagged tokens
simplifiedFN = os.path.join(modeldir, "SimplifiedModel_010616.pkl")  # trained on 117,381 manually-tagged tokens

inputFile = ''
tokenisedFile = ''
taggerFile = ''
directory = ''
directory1 = ''
time2 = time.strftime("%d%m%Y")
currentdir = os.getcwd()
defaultModel = ''
simplifiedModel = ''
filename1 = ''
filename2 = ''
englishLexicon = list(csv.reader(codecs.open(englishlexFN, 'r')))


def about():
    abtFile = codecs.open(aboutFN, 'r', 'utf-8-sig').readlines()

    for abtline in abtFile:
        print(abtline)

    return


def helpfile():
    helpFile = codecs.open(helpFN, 'r', 'utf-8-sig').readlines()

    for helpline in helpFile:
        print(helpline)

    return


def mquit():
    quit()

    return


def mopenfiles(x):
    gPoS = GaelicSentenceSplitter()

    if x:
        inputfile = gPoS.readinputfile(codecs.open(x, 'r', 'utf-8-sig'))
        print(x + ' ' + 'is being processed')

    else:
        print("No input file supplied... please supply an input file")

    return inputfile


def tokenisefile(xx):
    """Main tokenise function, inherits from GaelicTokeniser class"""
    tk = GaelicTokeniser()

    if xx:
        tokenisedFile = tk.tokenise(xx)
        return (tokenisedFile)

    else:
        print("No input file supplied... please supply an input file")

    return


def load_defaultmodel():
    dModel = open(defaultFN, "rb")
    model = pickle.load(dModel)
    dModel.close()
    return model


def load_simplifiedmodel():
    sModel = open(simplifiedFN, "rb")
    model = pickle.load(sModel)
    sModel.close()
    return model


def tagfile_default(xx):
    """Uses default, morphologically detailed tag set (246 tags)"""
    tk = GaelicTokeniser()

    algT = []

    algV = []

    tokenisedFile = xx

    defmodel = load_defaultmodel()

    BrillTag = defmodel.tag(tk.tokenise(tokenisedFile))

    for (c, d) in BrillTag:  # algorithm output

        algT.append(c)

        algV.append(d)

    Sp = ["Spp3sm", "Spp3sf", "Spp3p", "Spp1s", "Spa-s", "Spa-p", "Spa", "Sp"]  # removed 'Spv' (verbal part) from list

    for x, b in enumerate(algV):
        Nouncasesd = re.findall(r"(\bN+.*d\b)", str(b))

        Nouncasesn = re.findall(r"(\bN+.*n\b)", str(b))

        Nouncasesg = re.findall(r"(\bN+.*g\b)", str(b))

        temp = []

        temp2 = []

        temp.append(''.join(algV[x - 1]))

        temp.append(''.join(algV[x - 2]))

        temp.append(''.join(algV[x - 3]))

        tp = (set(temp) & set(Sp))

        if (Nouncasesd and not tp):
            nc = ''.join(Nouncasesd)

            cc = re.findall(r"\S", str(nc))

            cca = cc[:len(cc) - 1]

            cca.extend('n')

            algV[x] = ''.join(cca)

        if (Nouncasesg and not tp):
            ng = ''.join(Nouncasesg)

            cc = re.findall(r"\S", str(ng))

            cca = cc[:len(cc) - 1]

            cca.extend('d')

            algV[x] = ''.join(cca)

        if ''.join(b) == 'Sp' and 'Ug' in algV[:3]:
            algV[x] = 'Sa'

    for y, c in enumerate(algT):
        for x, b in enumerate(algV):
            if x == y:
                for d in englishLexicon:
                    if str(''.join(d)).lower() == c and c not in ['air', 'shine', 'gun', 'sin', 'far', 'fear', 'a',
                                                                  'can', 'coin'] and b != 'Xfe':
                        algV[x] = 'Xfe'

                Verbcases = ''.join(re.findall(r"(\bV+.*\b)", str(b)))

                Wcases = ''.join(re.findall(r"(\bW+.*\b)", str(b)))

                if str(''.join(c)) in ['Sann', 'sann', "'sann"]:
                    algV[x] = 'Wp-i-x'

                if ''.join(b) == 'Sap3sf' and ''.join(algT[y + 1][:2]) in ['ph', 'bh', 'ch', 'th', 'dh', 'mh', 'sh',
                                                                           'fh']:
                    algV[x] = 'Sap3sm'

                if ''.join(b) == 'Sap3sm' and ''.join(algT[y + 1][:2]) in ['pa', 'pe', 'pi', 'po', 'pu', 'pl', 'pm',
                                                                           'pn', 'ba', 'be', 'bi', 'bo', 'bu', 'bl',
                                                                           'bm', 'bn', 'ca', 'ce', 'ci', 'co', 'cu',
                                                                           'cl', 'cm', 'cn', 'ga', 'ge', 'gi', 'go',
                                                                           'gu', 'gl', 'gm', 'gn', 'ta', 'te', 'ti',
                                                                           'to', 'tu', 'tl', 'tm', 'tn', 'da', 'de',
                                                                           'di', 'do', 'du', 'dl', 'dm', 'dn', 'ma',
                                                                           'me', 'mi', 'mo', 'mu', 'ml', 'mm', 'mn',
                                                                           'sa', 'se', 'si', 'so', 'su', 'sl', 'sm',
                                                                           'sn', 'fa', 'fe', 'fi', 'fo', 'fu', 'fl',
                                                                           'fm', 'fn']:
                    algV[x] = 'Sap3sf'

                if ''.join(b) == 'Sap3sm' and ''.join(algT[y + 1][:1]) == 'h-':
                    algV[x] = 'Sap3sf'

                if ''.join(algT[y]) == "an" and ''.join(algT[y + 1]) == 'sàs':
                    algV[x] = 'Sp'

                    algV[x + 1] = 'Ncsmd'

                if ''.join(algT[y]) in ["nam", "nan"] and ''.join(algV[x + 1]) == Verbcases:
                    algV[x] = 'Q-s'

                if ''.join(algT[y]) == 'a' and ''.join(algV[x + 1]) == Verbcases:
                    algV[x] = 'Q-r'

                if ''.join(algT[y]) == 'na' and ''.join(algV[x - 1]) == "Sp":
                    algV[x] = 'Tdpm'

                if ''.join(algT[y]) == 'am' and ''.join(algV[x]) != "Tdsm":
                    algV[x] = 'Tdsm'

                if ''.join(algT[y]) in ["gum", "gun", "gu"] and ''.join(algV[x + 1]) in [Verbcases, Wcases]:
                    algV[x] = 'Qa'

                if ''.join(b) == 'Dp3sf' and ''.join(algT[y + 1][:2]) in ['ph', 'bh', 'ch', 'th', 'dh', 'mh', 'sh',
                                                                          'fh']:
                    algV[x] = 'Dp3sm'

                if ''.join(b) == 'Dp3sm' and ''.join(algT[y + 1][:2]) in ['pa', 'pe', 'pi', 'po', 'pu', 'pl', 'pm',
                                                                          'pn', 'ba', 'be', 'bi', 'bo', 'bu', 'bl',
                                                                          'bm', 'bn', 'ca', 'ce', 'ci', 'co', 'cu',
                                                                          'cl', 'cm', 'cn', 'ga', 'ge', 'gi', 'go',
                                                                          'gu', 'gl', 'gm', 'gn', 'ta', 'te', 'ti',
                                                                          'to', 'tu', 'tl', 'tm', 'tn', 'da', 'de',
                                                                          'di', 'do', 'du', 'dl', 'dm', 'dn', 'ma',
                                                                          'me', 'mi', 'mo', 'mu', 'ml', 'mm', 'mn',
                                                                          'sa', 'se', 'si', 'so', 'su', 'sl', 'sm',
                                                                          'sn', 'fa', 'fe', 'fi', 'fo', 'fu', 'fl',
                                                                          'fm', 'fn']:
                    algV[x] = 'Dp3sf'

                if ''.join(b) == 'Dp3sm' and ''.join(algT[y + 1][:1]) == 'h-':
                    algV[x] = 'Dp3sf'

                if ''.join(b) == 'Spp3sf' and ''.join(algT[y + 1][:2]) in ['ph', 'bh', 'ch', 'th', 'dh', 'mh', 'sh',
                                                                           'fh']:
                    algV[x] = 'Spp3sm'

                if ''.join(b) == 'Spp3sm' and ''.join(algT[y + 1][:2]) in ['pa', 'pe', 'pi', 'po', 'pu', 'pl', 'pm',
                                                                           'pn', 'ba', 'be', 'bi', 'bo', 'bu', 'bl',
                                                                           'bm', 'bn', 'ca', 'ce', 'ci', 'co', 'cu',
                                                                           'cl', 'cm', 'cn', 'ga', 'ge', 'gi', 'go',
                                                                           'gu', 'gl', 'gm', 'gn', 'ta', 'te', 'ti',
                                                                           'to', 'tu', 'tl', 'tm', 'tn', 'da', 'de',
                                                                           'di', 'do', 'du', 'dl', 'dm', 'dn', 'ma',
                                                                           'me', 'mi', 'mo', 'mu', 'ml', 'mm', 'mn',
                                                                           'sa', 'se', 'si', 'so', 'su', 'sl', 'sm',
                                                                           'sn', 'fa', 'fe', 'fi', 'fo', 'fu', 'fl',
                                                                           'fm', 'fn']:
                    algV[x] = 'Spp3sf'

                if ''.join(b) == 'Spp3sm' and ''.join(algT[y + 1][:1]) == 'h-':
                    algV[x] = 'Spp3sf'

                if ''.join(b) != 'Mn' and ''.join(algT[y][:1]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                   '9'] and ''.join(algT[y][len(algT[y]) - 1:]) in ['0',
                                                                                                                    '1',
                                                                                                                    '2',
                                                                                                                    '3',
                                                                                                                    '4',
                                                                                                                    '5',
                                                                                                                    '6',
                                                                                                                    '7',
                                                                                                                    '8',
                                                                                                                    '9']:
                    algV[x] = 'Mn'

                if ''.join(b) != 'Mn' and ''.join(algT[y][:1]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                   '9'] and ''.join(algT[y][len(algT[y]) - 2:]) in [
                    'an']:
                    algV[x] = 'Mn'

                if ''.join(b) != 'Mo' and ''.join(algT[y][:1]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                   '9'] and ''.join(algT[y][len(algT[y]) - 2:]) in [
                    'mh']:
                    algV[x] = 'Mo'

                if ''.join(b) != 'Fb' and ''.join(algT[y]) == '—':
                    algV[x] = 'Fb'

    taggerFile = list(zip(algT, algV))
    return taggerFile


def tagfile_simplified(xx):
    """Uses simplified, 41 tag tagset - i.e. word classes only"""
    tk = GaelicTokeniser()

    algT = []

    algV = []

    tokenisedFile = xx

    simmodel = load_simplifiedmodel()

    BrillTag = simmodel.tag(tk.tokenise(tokenisedFile))

    for (c, d) in BrillTag:  # algorithm output

        algT.append(c)

        algV.append(d)

    for y, c in enumerate(algT):
        for x, b in enumerate(algV):
            if x == y:
                for d in englishLexicon:
                    if str(''.join(d)).lower() == c and c not in ['air', 'shine', 'gun', 'sin', 'far', 'fear', 'a',
                                                                  'can'] and b != 'Xfe':
                        algV[x] = 'Xfe'

                if ''.join(b) != 'Mn' and ''.join(algT[y][:1]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                   '9'] and ''.join(algT[y][len(algT[y]) - 1:]) in ['0',
                                                                                                                    '1',
                                                                                                                    '2',
                                                                                                                    '3',
                                                                                                                    '4',
                                                                                                                    '5',
                                                                                                                    '6',
                                                                                                                    '7',
                                                                                                                    '8',
                                                                                                                    '9']:
                    algV[x] = 'Mn'

                if ''.join(b) != 'Mn' and ''.join(algT[y][:1]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                   '9'] and ''.join(algT[y][len(algT[y]) - 2:]) in [
                    'an']:
                    algV[x] = 'Mn'

                if ''.join(b) != 'Mo' and ''.join(algT[y][:1]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                   '9'] and ''.join(algT[y][len(algT[y]) - 2:]) in [
                    'mh']:
                    algV[x] = 'Mo'

                if ''.join(b) != 'Fb' and ''.join(algT[y]) == '—':
                    algV[x] = 'Fb'

    taggerFile = list(zip(algT, algV))

    return taggerFile


def savefile(myfile, msave, msavetype):
    msavefile = myfile

    tagger1 = Tagger()

    if msave > 0:
        if msavetype == 1 and len(tokenisedFile) > 1:
            taggerFile = ''

            print('Yes is chosen - txt')

            print(directory)

            tagger1.writeouputfile(msavefile, myGui.filename, 'txt', 'tk')

            messageinfo = 'File is saved... please check your output: ' + myGui.filename

            messagebox.showinfo(title="File Saved", message=messageinfo)

            return

        if msavetype == 0 and len(myGui.tokenisedFile) > 1:
            myGui.taggerFile = ''

            tagger1.writeouputfile(msavefile, myGui.filename, 'csv', 'tk')

            messageinfo = 'File is saved..please check your output: ' + myGui.filename

            messagebox.showinfo(title="File Saved", message=messageinfo)

            return

        if msavetype == 1 and myGui.taggerFile and len(myGui.tokenisedFile) < 1:
            myGui.filename1 = filedialog.asksaveasfilename()

            tagger1.writeouputfile(msavefile, myGui.filename1, 'txt', 'tg')

            messageinfo = 'File is saved... please check your output: ' + myGui.filename1

            messagebox.showinfo(title="File Saved", message=messageinfo)

            return

        if msavetype == 0 and myGui.taggerFile and len(myGui.tokenisedFile) < 1:
            myGui.filename1 = filedialog.asksaveasfilename()

            tagger1.writeouputfile(msavefile, myGui.filename1, 'csv', 'tg')

            messageinfo = 'File is saved... please check your output: ' + myGui.filename1

            messagebox.showinfo(title="File Saved", message=messageinfo)

            return

        else:
            if msavetype == None:
                print('Cancel is chosen')

                return

    else:
        return


class GaelicPartOfSpeechTagger:
    def __init__(self, inputfile, outputfile):
        self.inputfile = inputfile

        self.outputfile = outputfile

    def readinputfile(self, inputfile):
        self.inputfile = inputfile

        # self.item = ''

        self.item = self.inputfile.read()

        return self.item

    def writeouputfile(self, inputfile, output, outputformat, process):
        self.inputfile = inputfile  # for API

        self.output = output

        self.outputformat = outputformat

        self.process = process

        if self.outputformat == 'csv' and self.process == 'tg':
            self.output2 = codecs.open(self.output + '.csv', 'w')

            print('This is the output', self.outputformat)

            wr = csv.writer(self.output2, delimiter=',', lineterminator='\n')

            for (v, y) in self.inputfile:
                wr.writerow((v, y))

            return

        if self.outputformat == 'txt' and self.process == 'tg':
            self.output1 = codecs.open(self.output + '.txt', 'w')

            print('This is the output', self.outputformat)

            for (v, y) in self.inputfile:
                self.output1.write(''.join(v) + '/' + ''.join(y) + ' ')

            self.output1.close()

            return

        if self.outputformat == 'csv' and self.process == 'tk':
            self.output2 = codecs.open(self.output + '.csv', 'w')

            print('This is the output', self.outputformat)

            wr = csv.writer(self.output2, delimiter=',', lineterminator='\n')

            for v in self.inputfile:
                wr.writerow([v])

            return

        if self.outputformat == 'txt' and self.process == 'tk':
            self.output1 = codecs.open(self.output + '.txt', 'w')

            print('This is the output', self.outputformat)

            for v in self.inputfile:
                self.output1.write(''.join(v) + '\n')

            self.output1.close()

            return

    def __str__(self):
        return self.inputfile


class GaelicSentenceSplitter(GaelicPartOfSpeechTagger):
    def __init__(self):
        GaelicPartOfSpeechTagger.__init__(self, 'inputfile', 'outputfile')

    def splitsentence(self, text):
        self.text = text
        self.sentences = re.split(r'\\.', self.text)
        return self.sentences

class Tagger(GaelicTokeniser, GaelicPartOfSpeechTagger):
    def __init__(self):
        GaelicTokeniser.__init__(self)
        GaelicPartOfSpeechTagger.__init__(self, 'inputfile', 'outputfile')

if __name__ == "__main__":
    x = mopenfiles('/Users/WLamb/Dropbox/Temp/ScG_system/poilis.txt')
    print(tagfile_default(x))
