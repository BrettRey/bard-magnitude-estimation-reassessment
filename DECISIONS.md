# Decisions

## 2026-06-23

- Use a lower-case folder name: `bard-magnitude-estimation-reassessment`.
- Treat the project as a secondary-data reassessment, not a direct replication, unless the original Bard et al. participant-level data is found.
- Use Bard, Robertson, and Sorace (1996) as the conceptual target.
- Use later method-comparison work as the empirical base after verification.
- Use contemporary acceptability datasets as the construct's afterlife, not as direct replacements for magnitude-estimation data.
- Use afterlife sources rhetorically for the survival and transformation of formal acceptability measurement, not evidentially for ME-vs-Likert.
- Keep house style strictly central by symlink. Do not copy local house-style files.
- Keep candidate sources in `notes/source-verification.md` until verified.
- Cite Bard, Robertson, and Sorace (1996) with DOI `10.2307/416793`, while noting that the Edinburgh record still reports no DOI.
- Treat CoLA labels as expert/literature acceptability-grammaticality labels, not as naive-speaker acceptability judgments.
- Treat the Syntactic Acceptability Dataset as a bridge case because it explicitly separates literature-extracted grammaticality from crowdsourced acceptability.
- Treat the source-grounded Bard target as the claim that ME solves scale problems in conventional methods and yields robust fine-grained acceptability data. Do not attribute a broader superiority claim to Bard unless the full article or a reception source is cited for that stronger reading.
- Treat Sprouse et al. (2013) and Sprouse and Almeida (2017) as sources of public row-level method-comparison data from Jon Sprouse's current author site, with the stated author-contact caveat for novel research reuse.
- Do not treat Bard or Langsford as sources of public participant-level data unless an author-controlled or publisher-linked repository is found.
- Use a Gelmanian measurement null as the empirical comparison where the available data can support it: magnitude estimation has no practical measurement advantage once item acceptability, task noise, scoring choices, and any estimable participant or item-by-method terms are accounted for.
- Treat scrambled labels, method-label permutations, and no-method-advantage simulations as negative controls for the pipeline, not as the substantive null.
- Do not model participant response style, test-retest reliability, or method-by-item instability from published rates alone. Those estimands require raw participant-level rows.
- Use `notes/analysis-charter.md` as the pre-analysis commitment device. Primary datasets, comparisons, scoring rules, practical-advantage criteria, negative controls, and forbidden claims should not change after inspecting new row-level results unless the change is labelled exploratory or a revision trigger occurs.
- Proceed with Sprouse structural data inventory while reuse is pending, but avoid method rankings, convergence estimates, model fits, or publication-ready novel results until the reuse question is resolved or the analysis is reframed as verification/reproduction.
- Preserve original Sprouse identifiers in scripts. Spacing-normalized keys may be used only as explicit candidate crosswalk fields, not as silent recoding.
- Use `FC.signtest.csv` as the primary 2013 forced-choice representation because it is already pair-level and aligns with the pair-level ME/LS crosswalk. Use `FC.logistic.csv` only as a named sensitivity representation.
- Exclude 2017 yes/no item IDs `B`, `G`, and `M` from item-level comparisons because they are absent from the materials workbook, appear at repeated early order positions, and do not align with the ME/LS/FC item universe.
