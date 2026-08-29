# LingBuzz v2 proofreading audit

Date: 2026-08-29
Scope: whole manuscript
Mode: read-only
Verdict: **pass with minor non-blocking polish notes**

## Checks completed

- Read the named root and every included section in source order.
- Ran the central house-style checker: no violations were reported.
- Ran the terminology checker with included files followed: no first-use or
  terminology flags were reported.
- Scanned the final LaTeX logs for errors, undefined citations/references,
  overfull or underfull boxes, and missing characters: none were found.
- Checked labels and cross-references, intentional placeholders, bibliography
  calls, PDF metadata, and rendered page layout. The only placeholder is the
  deliberate author placeholder in the blind build.
- Checked the projectibility passage against the projectibility-first audit.
  It fixes a narrow projection target (aggregate ordering across formal task
  formats), identifies its sampled population and change conditions, and does
  not infer causal order or homeostasis from stability. Its tolerance is
  qualitative rather than numerical, but the claim is correspondingly narrow.

## Findings by severity

### Critical

None.

### Major

None.

### Minor

Four self-references use *present* where the house style prefers a direct
demonstrative:

- `sections/03-secondary-data-design.tex:41`: “The present resolution
  analysis” could be “This resolution analysis.”
- `sections/03-secondary-data-design.tex:83`: “In the present reanalysis”
  could be “In this reanalysis.”
- `sections/06-grammaticality-and-acceptability.tex:55`: “The present
  comparison matrices” could be “These comparison matrices.”
- `sections/07-conclusion.tex:56`: “the present diagnostics” could be “these
  diagnostics.”

Figure 1's caption phrase “Each point averages participant judgments” is
grammatical, but “Each point is the mean of participant judgments” would be
slightly more immediate.

Section 4's sentence-length profile is somewhat narrow: 64% of sentences fall
between 12 and 26 words. This is an advisory rhythm note, not a clarity defect.

Final assessment: **pass for LingBuzz v1**. No proofreading, LaTeX, citation,
source-grounding, or projectibility issue blocks posting. The listed items are
optional micro-polish and were not changed in this read-only pass.
