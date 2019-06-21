# Conversion
## Reconstructing spacing

Context: ARCOSG does not contain the original texts, so we have to reconstruct them in a consistent way.
We use GOC (Gaelic Orthographic Conventions, https://www.sqa.org.uk/files_ccc/SQA-Gaelic_Orthographic_Conventions-En-e.pdf) for consistency in reconstructing spacing, but don't apply any other corrections.

According to the latest GOC:
* There are spaces after _a'_, _b'_, _d'_ or _m'_.
* There are no spaces after _dh'_.
* Do not close up before _'m_ or _'n_.

Also (not covered explicitly by GOC but shown in examples):
* Close up _h-_, _t-_, and _n-_.
* Don't close up after _th'_ and _bh'_.

If an elided _a'_ or _ag_ before a verbal noun is indicated by _'_, close this up.

Close up around the hyphen in _a-measg_, _a-rèir_, _a-thaobh_ and similar but don't close up around hyphens if they're being used as dashes.
Also don't attempt to bring into line with GOC by adding or taking away hyphens.

## Multiword tokens

The original version of the Brown to CoNLL converter replaced internal spaces with underscores.
For UD, however, we need to split these up. For the moment we duplicate the UPOS and the XPOS.
PROPNs have a `flat` relation, others have a `fixed` relation but this needs to be improved.

Some difficult cases follow:
### _na b'_/_na bu_
Ideally this should be exactly parallel with _nas_.
### _sam bith_
Currently both are marked as `ADJ` but there is clearly internal structure.

# Grammar
## The verbal noun
Annotate as a `NOUN` and an `xcomp` of the `VERB`.

### With aspect markers (continuous tenses and depictives)
_ag_, _air_, _ri_ and so forth preceding it have a `case` relationship as in Irish.
### Inversion structures
The noun preceding it is an `obj` of it.

## _bi_
Auxiliary use: we follow the Irish UD treebank and treat _bi_ as a `VERB`, and the verbal noun as a `NOUN` linked back to _bi_ with an `xcomp` deprel.

Predicative use: again, we follow Irish and use `xcomp:pred` for predicative adjectives.

However (see f01_028), there are also uses of _bi_ for extent in time (n03_041) and space.

## _còrr is_ and friends

Example taken from pw01_015: in _còrr is deich bliadhna_, _bliadhna_ is conjoined with _còrr_ and _deich_ is a `nummod` of _bliadhna_.

## _feuch_

When this is tagged as `Vm-2s` the sense in which it is usually used is 'to try to', in which case it is linked to the higher clause with an `xcomp` deprel.
For example n04_002: _... gu robh e 'dol a dh’fhalbh feuch a faigheadh..._, _feuch_ is an `xcomp` of _dh’fhalbh_.

## _is_
_'S_, _b'_, _bu_, _'se_, _'sann_ and so on are `cop` and the root is whatever has been fronted by it.
We treat _'S e_ as a fixed expression where _e_ has a `fixed` relation with the `AUX`.
Again we follow Irish and whatever comes after the root is a subject, be it a nominal subject, `nsubj`, or a clausal subject, `csubj:cop`.

## _nach maireann_

This is `acl:relcl` of the deceased because _nach_ is the negative relativiser.

## _urrainn_
In most dialects the person (or thing) that can follows the preposition _do_ so is of course `obl`. In some, however, you can say, for example, _'s urrainn mi_, so in this case _mi_ is `obl` of _urrainn_.

## Special deprels
### `case:voc`
This is borrowed from Irish and is for the vocative particle _a_.
### `obl:smod`
This is experimental and is for expressing things like lengths which are direct arguments of _bi_.
However, as in ns05_003, if the time expression qualifies a noun, use `nmod` as usual.
### `obl:tmod`
This is borrowed from Irish and is used for nouns or NPs being used as temporal expressions.
