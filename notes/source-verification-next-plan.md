# Source Verification Gate

## Scope

Verify the project sources against authoritative pages before adding citations, downloading datasets, or revising the manuscript's evidential claims.

## First pass

1. Confirm bibliographic metadata for Bard, Robertson, and Sorace (1996), including DOI, journal issue, page range, and whether any public participant-level data exists.
2. Verify Sprouse, Schuetze, and Almeida (2013), prioritizing the official publication page and any author-controlled or publisher-linked supplements.
3. Verify Langsford et al. (2018), including article metadata, open data or materials links, measures compared, and reliability claims.
4. Verify CoLA, BLiMP, and the Syntactic Acceptability Dataset only as contemporary afterlife sources, keeping benchmark labels separate from magnitude-estimation evidence.

## Outputs

- Update `notes/source-verification.md` with verified metadata, authoritative links, and unresolved gaps.
- Add project-specific BibTeX only to `references-local.bib` if a source is verified and absent from the central bibliography.
- Leave raw data untouched until dataset documentation and licensing have been checked.

## Focused-pass result

- Bard: metadata and abstract-level claim are verified. Public participant-level data not found. The source-grounded target is the claim that ME solves conventional scale problems and yields robust fine distinctions; stronger "privileged method" wording needs either full-text support or reception-source support.
- Sprouse 2013: public author-hosted participant-level data and materials found on Jon Sprouse's current site. Headers include an author-contact caveat for novel reuse.
- Sprouse and Almeida 2017: public author-hosted participant-level data and materials found on Jon Sprouse's current site, with the same author-contact caveat.
- Langsford 2018: Glossa supplementary PDF, author pages, and OSF/PsyArXiv record checked. Raw participant rows not found; OSF preprint storage lists only the paper PDF.
- Afterlife sources: keep CoLA, BLiMP, and SAD as construct-afterlife evidence only, not as ME-vs-Likert evidence.

## Stop conditions

- If Bard et al. participant-level data is not found, keep the project framed as a secondary-data reassessment rather than a direct replication.
- If Langsford raw participant rows remain unavailable, do not promise a full response-style/test-retest reanalysis of Langsford.
- If a dataset mixes acceptability, grammaticality, naturalness, standardness, or correction behavior, record that distinction before using it as evidence.
