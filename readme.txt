== gdbank.txt ==

The corpus annotated in CoNLL-X format with the categorial annotations in column 6.

Each sentence has three lines beginning with hashes preceding it. These are an ID for the sentence, some versioning information, and the source.

== gdbank_guidelines.tex ==

The guidelines used for the construction of the corpus in LaTeX format. Currently no special packages are used for it.

== readme.txt ==

This file.

== Is all of this written up somewhere? ==

The blog is at http://www.tantallon.org.uk/cggblog/ 

The citation is:
@InProceedings{batchelor:2014:CLTW14,  author    = {Batchelor, Colin},  title     = {gdbank: The beginnings of a corpus of dependency structures and type-logical grammar in Scottish Gaelic},  booktitle = {Proceedings of the First Celtic Language Technology Workshop},  month     = {August},  year      = {2014},  address   = {Dublin, Ireland},  publisher = {Association for Computational Linguistics and Dublin City University},  pages     = {60--65},  url       = {http://www.aclweb.org/anthology/W14-4609}}

== Revision log ==

0.8: Annotation rules added to deal with "a cheile".

0.7: Type-changing rules added to deal with aspectual phrases qualifying a noun and cases where the aspectualizer has been omitted!

0.6: Changed aspectual phrases (aig, air, ann, gu and ri followed by verbal noun) to S[asp] from PP[*]. Abolished S[inf]. Added four type-changing rules to turn predicative adjectives into attributive, and deal with PPs.

Colin Batchelor
2014-08-22
