# Status

## 2026-06-23

Created lower-case project scaffold at:

`/Users/brettreynolds/Documents/LLM-CLI-projects/papers/bard-magnitude-estimation-reassessment`

Initial framing:

- Working title: *Was magnitude estimation necessary? A secondary-data reassessment of Bard, Robertson, and Sorace (1996)*.
- Project type: no-new-data archival and secondary-data reassessment.
- Conceptual target: Bard, Robertson, and Sorace (1996).
- Empirical base to verify: Sprouse, Schuetze, and Almeida (2013); Langsford et al. (2018); later acceptability datasets and benchmarks.
- Contemporary afterlife to verify: CoLA, BLiMP, Syntactic Acceptability Dataset, and related acceptability resources.

Infrastructure:

- Uses central house-style symlinks only.
- Uses central `references.bib` symlink only.
- No local house-style snapshot.
- No datasets downloaded.
- No local BibTeX entries added.
- Central LaTeX style linter with strict checks passes.
- XeLaTeX/Biber/XeLaTeX/XeLaTeX build passes; final log scan found no undefined citations, no overfull boxes, and no empty bibliography warnings.

Next steps:

1. Verify the Bard, Sprouse, Langsford, CoLA, BLiMP, and SAD sources against authoritative pages.
2. Add verified missing BibTeX entries either to the central bibliography or, if truly project-specific, to `references-local.bib`.
3. Decide whether the paper's empirical core is method comparison, construct drift, or acceptability/grammaticality divergence.
4. Build a dataset inventory before downloading or transforming data.
