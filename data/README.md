# Data Handling

Raw participant-level datasets are not committed to this repository.

`data/raw/` is ignored except for `.gitkeep`. Any local raw-data copies should
be treated as private working files and should not be added to Git. Current
Sprouse verification copies were inspected under `/tmp/bard-data-check`, outside
the repository.

`data/derived/` is also ignored while reuse permissions and analysis scope are
being resolved. Generated crosswalks, schema summaries, and model outputs should
be created there during local work, then promoted deliberately if they are
appropriate to share.

For the Sprouse 2013 and 2017 public data files, the CSV headers say the data
are provided for verification of the original analyses and ask researchers to
contact Jon Sprouse about possible use for novel research. Until that question
is resolved, scripts may be drafted and structural inventory may be recorded,
but novel secondary results should not be treated as publication-ready.
