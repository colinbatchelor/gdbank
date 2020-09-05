Some tools and resources for natural language processing of Scottish Gaelic.

ud
--
A conversion of the Annotated Reference Corpus of Scottish Gaelic (ARCOSG) to a dependency treebank.
You can acquire ARCOSG itself from http://datashare.is.ed.ac.uk/handle/10283/2011

https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/ will contain the final version of this.

`innealan/brown_gd_to_conll.py` performs a rudimentary conversion of ARCOSG to CoNLL-U format.

In practice I have postprocessed the results with the following Python 3 scripts:
* `fix_feats.py` fills out the feature set.
* `fix_multiword.py` and `fix_text.py` bring the tokenisation scheme into line with Universal Dependencies.
* `fix_whitespace.py` adds `SpaceAfter=No` to the relevant parts of the tree.
* `fix_conversations.py` removes the tokens indicating the speaker and adds a `# speaker =` line to the preamble for each tree.

The current treebank files in the dev branch of UD_Scottish_Gaelic-ARCOSG are `gd_arcosg-ud-train.conllu`, `gd_arcosg-ud-dev.conllu` and `gd_arcosg-ud-test.conllu`.

There are four others:
* `arcosg_unseen.conll` is the main file containing as-yet-unchecked treebanks.
* `arcosg_sport.conll` contains football commentary.
* `arcosg_conversations.conll` contains conversations.
* `gd_iomasgladh-ud-test.conllu` is a hand-built corpus from 2014 which has been converted to UD.

This is written up in:
* Colin Batchelor, 2019. Universal dependencies for Scottish Gaelic: syntax, in _Proceedings of CLTW2019 at Machine Translation Summit XVII_, Dublin, August.

Earlier work
--
### gramaran
Contains a categorial grammar generated from ARCOSG in dotccg format.

### ccg
Contains an earlier, smaller, hand-built corpus in CoNLL-X format.

#### gdbank.txt

The corpus annotated in CoNLL-X format with the categorial annotations in column 6.

Each sentence has three lines beginning with hashes preceding it. These are an ID for the sentence, some versioning information, and the source.

#### gdbank_guidelines.tex

The guidelines used for the construction of the corpus in LaTeX format. Currently no special packages are used for it.

### innealan
Tools covered by unit tests require Python 3.

* `acainn.py` is the main code in this. It currently contains a lemmatizer, a retagger that assigns tags that more closely match CCG categories, a subcategorization tool for verbs, and code to map the new tags onto CCG categories.
* `test_acainn.py` contains unit tests.
* `BrownToDotccg.py` takes a Brown-format corpus assuming ARCOSG tags and outputs a .ccg file
* `mendxml.py` fixes the output of OpenCCG's ccg2xml.
* `prepareARCOSG.py` takes a local installation of the Annotated Reference Corpus of Scottish Gaelic (ARCOSG), replaces spaces within tokens with underscores and puts the results in `arcosg.pkl`.

In development
--
### `checker.py`
In Python 3. In-progress grammar checker based largely on Richard Cox's _Gearr-Ghràmar na Gàidhlig_ (2018). Does not run from the command line yet but `test_checker.py` shows how the methods work.

### gaelic_pos
This is my local copy of https://bitbucket.org/gaelic_nlp/gaelic_pos/ which I am adding unit tests to.

Is all of this written up somewhere?
--

The blog is at http://www.tantallon.org.uk/cggblog/ 

The citation for the files in `conll/` is:
  `@InProceedings{batchelor:2014:CLTW14, author    = {Batchelor, Colin}, title     = {gdbank: The beginnings of a corpus of dependency structures and type-logical grammar in Scottish Gaelic}, booktitle = {Proceedings of the First Celtic Language Technology Workshop}, month     = {August}, year      = {2014}, address   = {Dublin, Ireland}, publisher = {Association for Computational Linguistics and Dublin City University}, pages     = {60--65}, url       = {http://www.aclweb.org/anthology/W14-4609} }`

The citation for the material in `innealan` and `gramaran` is:
  `@InProceedings{batchelor:2016:CLTW, author = {Batchelor, Colin}, title = {Automatic derivation of categorial grammar from a part-of-speech-tagged corpus in Scottish Gaelic}, booktitle = {Actes de la conf\'erence conjointe JEP-TALN-RECITAL 2016, volume 6 : CLTW}, month = {July}, year = {2016}, address = {Paris, France}, pages = 1, url = {https://jep-taln2016.limsi.fr/actes/Actes%20JTR-2016/V06-CLTW.pdf} }`

Colin Batchelor

2020-09-01
