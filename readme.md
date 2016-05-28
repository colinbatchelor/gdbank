gdbank
==

Some tools and resources for natural language processing of Scottish Gaelic.

innealan
--
Tools require Python 2.

`mendxml.py` fixes the output of OpenCCG's ccg2xml.
`prepareARCOSG.py` takes a local installation of the Annotated Reference Corpus of Scottish Gaelic (ARCOSG), replaces spaces within tokens with underscores and puts the results in `arcosg.pkl`.

You can acquire ARCOSG itself from http://datashare.is.ed.ac.uk/handle/10283/2011

gramaran
--
Contains a grammar generated from ARCOSG in dotccg format.

conll
--
Contains an earlier, smaller, hand-built corpus in CoNLL-X format.

gdbank.txt
---

The corpus annotated in CoNLL-X format with the categorial annotations in column 6.

Each sentence has three lines beginning with hashes preceding it. These are an ID for the sentence, some versioning information, and the source.

gdbank_guidelines.tex
---

The guidelines used for the construction of the corpus in LaTeX format. Currently no special packages are used for it.

readme.md
--

This file.

Is all of this written up somewhere?
--

The blog is at http://www.tantallon.org.uk/cggblog/ 

The citation for the files in conll/ is:
  `@InProceedings{batchelor:2014:CLTW14, author    = {Batchelor, Colin}, title     = {gdbank: The beginnings of a corpus of dependency structures and type-logical grammar in Scottish Gaelic}, booktitle = {Proceedings of the First Celtic Language Technology Workshop}, month     = {August}, year      = {2014}, address   = {Dublin, Ireland}, publisher = {Association for Computational Linguistics and Dublin City University}, pages     = {60--65}, url       = {http://www.aclweb.org/anthology/W14-4609} }`

Citation for the other material to follow.

Revision log
--

2016-05-28: Started to add files for the second CLTW paper, mainly scripts to process ARCOSG.

Colin Batchelor
2016-05-28
