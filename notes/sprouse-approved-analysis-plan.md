# Sprouse Permission and First Analysis Plan

Date: 2026-07-07

## Permission Boundary

Jon Sprouse replied that Brett may use the Sprouse, Schuetze, and Almeida
(2013) and Sprouse and Almeida (2017) public data files to explore the
contribution of magnitude estimation to an item-level signal. The permission is
bounded:

- use the data for the limited secondary methodological analysis;
- do not redistribute participant-level raw files;
- cite the original papers and data source clearly;
- if the project drifts away from magnitude estimation's contribution to
  item-level acceptability and toward something closer to Sprouse/Almeida's
  current interests, reach back out before proceeding.

## Immediate Updates

1. Record the permission decision in `DECISIONS.md`, `STATUS.md`,
   `notes/source-verification.md`, `data/README.md`, and `analysis/README.md`.
2. Re-run `scripts/sprouse_analysis_gate.py` with `--reuse-status approved`
   after regenerating the ignored structural files.
3. Keep raw Sprouse files outside Git. Use `/tmp/bard-data-check` as the local
   working copy unless Brett chooses a different private raw-data location.

## First Outcome Analysis

The first outcome script should be deliberately narrow. It should open the
previously gated analysis without trying to solve the full response-function
model in one pass.

Planned script:

`analysis/sprouse_item_signal.py`

Primary outputs under ignored `data/derived/sprouse_analysis/`:

- item/method aggregate tables for 2013 and 2017;
- cross-method item-level correlations for ME, Likert, forced choice, and yes/no
  where the item universe aligns;
- simple item-level disagreement summaries that identify where ME diverges from
  bounded methods;
- a manifest recording that the analysis is permitted, secondary, and bounded
  by the email permission.

The script should not commit participant-level raw data or derived tables. Any
results promoted into the manuscript should be summarized, not redistributed as
raw response rows.

## Guardrails

- Do not replace the chartered response-function/dimensionality model with this
  first descriptive pass. This is a staging analysis that checks the item-level
  signal and disagreement surface.
- Do not claim that magnitude estimation lacks any possible use. The claim under
  test is practical advantage in the available method-comparison data.
- Keep 2013 forced choice represented by `FC.signtest.csv` as primary.
- Keep 2017 yes/no item IDs `B`, `G`, and `M` excluded from item-level
  comparisons.
- If this first pass reveals that the cross-method item matrices are too sparse
  or not comparable, stop and revise the analysis route before modelling.
