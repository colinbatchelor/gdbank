_This document is being transferred to the UD documentation._

# Grammar
## The verbal noun
Annotate as a `NOUN` and an `xcomp:pred` of the `VERB`.

In inversion structures, the object is `obj` of the verbal noun.

### With aspect markers (continuous tenses and depictives)
_ag_, _air_, _ri_ and so forth preceding it have a `case` relationship as in Irish.
### Inversion structures
The noun preceding it is an `obj` of it.

## _air ais_

While _ais_ is tagged as _Nf_ in phrases like _air ais no air adhart_ there seems to be no good reason to treat the first half differently from the second half, so _air_ is `case` of _ais_ and _ais_ is the head and `obl` of whatever it is modifying.

## _bi_
Auxiliary use: we follow the Irish UD treebank and treat _bi_ as a `VERB`, and the verbal noun as a `NOUN` linked back to _bi_ with an `xcomp:pred` deprel.

Predicative use: again, we follow Irish and use `xcomp:pred` for predicative adjectives, PPs and adverbs. There is a construction exemplified in c02_009a, c02_009b and c02_010 _bi... agam... ri dhol..._ and in this case we assume that the PP with _aig_ is the quirky experiencer and _ri_ is the predicate.

However (see f01_028), there are also uses of _bi_ for extent in time (n03_041) and space.

## _còrr is_ and friends

Example taken from pw01_015: in _còrr is deich bliadhna_, _bliadhna_ is conjoined with _còrr_ and _deich_ is a `nummod` of _bliadhna_.

## _feuch_

When this is tagged as `Vm-2s` the sense in which it is usually used is 'to try to', in which case it is linked to the higher clause with an `xcomp` deprel.
For example n04_002: _... gu robh e 'dol a dh’fhalbh feuch a faigheadh..._, _feuch_ is an `xcomp` of _dh’fhalbh_.

## _an ìre mhath_

This means 'almost'. See s08_061b for an example. Use `nmod`.

## _is_
_'S_, _b'_, _bu_, _'se_, _'sann_ and so on are `cop` and the root is whatever has been fronted by it.
We treat _'S e_ as a fixed expression where _e_ has a `fixed` relation with the `AUX`.
Again we follow Irish and whatever comes after the root is a subject, be it a nominal subject, `nsubj`, or a clausal subject, `csubj:cop`.

## _nach maireann_

This is `acl:relcl` of the deceased because _nach_ is the negative relativiser.

## `parataxis`

Where you have a big long sentence with lots of "ars' esan" and "ars' ise"s in it, treat them like punctuation and make them `parataxis` of the most contentful content word in the nearest quoted text so as to avoid non-projectivity. Sentence n01_038 is an example of this.

## _an t-seachdain seo chaidh_ and others

Treat _chaidh_ as being `acl:relcl` of _t-seachdain_ (pw05_005, also _ceud_ in the sense of 'century': see fp01_034).

## _urrainn_
In most dialects the person (or thing) that can follows the preposition _do_ so is of course `obl`. In some, however, you can say, for example, _'s urrainn mi_, so in this case _mi_ is `obl` of _urrainn_.
