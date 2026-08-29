# LingBuzz v2 figures pass

Date: 2026-08-29
Scope: whole manuscript and both plotted figures
Verdict: **pass after one colour-accessibility repair**

## Procedure

The pass registry names `check-chart-style`, but that skill is unavailable in
this environment. I substituted a direct audit of the plotting source,
aggregate inputs, exported PDF and PNG files, captions, in-text citations, and
rendered manuscript pages, using the central figure rules and PDF visual QA.

## Findings

- Figure 1 uses the full retained aggregate inputs: 298 identifiers labelled
  `condition` in the 2013 source and 786 labelled `item` in the 2017 source.
  The caption explains that distinction and identifies each point as an
  aggregate rather than a participant row.
- Figure 2 contains all 54 endpoint, 72 prediction, and 36 decision
  specifications. The exports reproduce the source counts: one endpoint
  specification and four prediction specifications cross their displayed
  thresholds, while none of the decision specifications does. The decision
  rows consistently give 3/150 discordant 2013 pairs and 1/50 discordant 2017
  pairs.
- The plotting script validates schemas, study labels, expected row counts,
  denominators, and discordant-pair identities before plotting.
- Both figures are cited before they appear. Their captions state the data
  source, aggregation level, sample or specification counts, thresholds, and
  the meaning of colour, shape, fill, and vertical staggering.
- Shape and fill provide redundant channels, so interpretation does not depend
  on colour alone. Panel-specific legends in Figure 2 make the A/B mappings
  explicit; Panel C directly labels its denominators and discordant pair IDs.
- Both source PDFs and their final manuscript pages render cleanly without
  clipping, overlap, or illegible labels.

## Repair made

The bounded-logistic curve and the open yes/no marker outlines used the bright
coral and gold fills even though they are thin strokes. The plotting code now
uses the darker AA coral and gold variants for those strokes. Solid gold
criterion squares and the gold star remain unchanged. The figures were then
regenerated and re-inspected.

## Non-blocking technical note

Poppler reports a font-type/file mismatch while rendering the standalone
figure PDFs. The embedded EB Garamond text nevertheless renders and extracts
correctly in both the source figures and the manuscript, so this is not a
visible or publication-blocking defect.

Final assessment: **pass**. The figures are numerically faithful,
self-contained, reproducible from the aggregate outputs, visually legible, and
appropriately integrated into the paper.
