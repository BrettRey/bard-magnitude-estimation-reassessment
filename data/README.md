# Data Handling

Raw participant-level datasets are not committed to this repository.

`data/raw/` is ignored except for `.gitkeep`. Any local raw-data copies should
be treated as private working files and should not be added to Git. Current
Sprouse working copies are refreshed under `/tmp/bard-data-check`, outside the
repository.

`data/derived/` is also ignored. Generated crosswalks, schema summaries, model
outputs, and descriptive secondary-analysis tables should be created there
during local work, then promoted deliberately if they are appropriate to share.

For the Sprouse 2013 and 2017 public data files, the CSV headers say the data
are provided for verification of the original analyses and ask researchers to
contact Jon Sprouse about possible use for novel research. Brett received
permission from Jon Sprouse on 2026-07-07, after Sprouse checked with Diogo
Almeida, for the limited secondary methodological analysis of magnitude
estimation's contribution to an item-level signal.

That permission does not make the participant-level raw files redistributable.
Do not commit the raw files. If the project drifts beyond the approved
magnitude-estimation/item-level-signal question, contact Sprouse/Almeida again
before proceeding.
