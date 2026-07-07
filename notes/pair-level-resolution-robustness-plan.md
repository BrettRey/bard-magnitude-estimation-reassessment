# Pair-Level Resolution Robustness Plan

## Purpose

The item/condition response-function diagnostic found bounded-Likert curvature but not unusually large endpoint ME spread. A pair-level check should ask the adjacent practical question: when the analysis is reduced to the good-vs-bad contrasts used in Sprouse's method-comparison design, does ME preserve practically different pair distinctions that bounded formats blur?

This is a robustness check, not a new primary model. It should test whether the previous conclusion survives at the contrast level.

## Assumptions Checked

- `sprouse_pair_contrasts.csv` already contains aligned 2013 and 2017 pair contrasts for ME, Likert, and the available binary tasks.
- Pair IDs are condition-level in both 2013 and 2017.
- The previous response-function residual table is not sufficient for 2017 pair joining because its 2017 unit IDs are item-level token IDs.
- The pair-level script should therefore read the local raw ME/LS files and aggregate ME/LS by condition for both datasets.

## Main Diagnostics

For each dataset:

1. Aggregate raw ME z-score means and raw Likert means by condition.
2. Join bad and good conditions to `sprouse_pair_contrasts.csv`.
3. Compute condition-pair contrasts:
   - ME z-score contrast.
   - Raw Likert contrast.
   - Existing Likert z-score contrast.
   - Available binary-task contrast or expected agreement signal.
4. Fit a simple bounded-method prediction of ME contrast from non-ME signals.
5. Rank pairs by ME contrast, bounded-method contrast, and ME residual after bounded-method prediction.

## Output Files

Write ignored outputs under `data/derived/sprouse_analysis/`:

- `sprouse_pair_resolution_rows.csv`: one row per aligned pair with raw-scale contrasts, ranks, and ME residuals.
- `sprouse_pair_resolution_summary.csv`: per-dataset correlations, rank overlap, residual spread, and decision-concordance summaries.
- `sprouse_pair_resolution_extremes.csv`: the largest ME-over-bounded and bounded-over-ME residual pairs for audit.
- `sprouse_pair_resolution_manifest.csv`: output provenance and row counts.

## Interpretation Rules

- Treat large ME residuals as audit targets, not discoveries by themselves.
- A useful ME-specific resolution result would look like stable, interpretable ME-over-bounded residuals concentrated in pairs where bounded methods are compressed or ambiguous.
- If ME ranks and bounded-method ranks mostly agree, and the residual extremes are isolated rather than systematic, this reinforces the current conclusion: ME tracks the same item-level signal without a clear practical resolution advantage in these data.

## Implementation Steps

1. Add `analysis/sprouse_pair_resolution_robustness.py`.
2. Require the approved Sprouse readiness gate and the descriptive pair outputs.
3. Reuse the project CSV loader pattern for raw files.
4. Build condition-level ME/LS aggregates for 2013 and 2017.
5. Join those aggregates to the existing pair table.
6. Fit bounded-method prediction models with `numpy.linalg.lstsq`.
7. Write row, summary, extremes, and manifest outputs.
8. Update `analysis/README.md`, `STATUS.md`, and `DECISIONS.md`.
9. Run the new script, `py_compile`, `git diff --check`, and whitespace scans.
