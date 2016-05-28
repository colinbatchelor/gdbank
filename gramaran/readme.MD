Use with OpenCCG
==
This grammar is auto-generated from ARCOSG and the scripts in innealan/

To convert it from dotccg format, use:
`ccg2xml arcosg.ccg`
`python innealan/mendxml.py arcosg.ccg`

The second tidy-up script renames files and works round a small bug in ccg2xml
which can prevent words with the same surface form appearing in more than one
family.

2016-05-28
