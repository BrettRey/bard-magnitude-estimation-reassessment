# Dimensionality Gate Implementation Plan

Date: 2026-07-07

## Discovery Notes

The charter calls for a dimensionality gate before any magnitude-estimation
term is adjudicated. A full confirmatory response-function model is still a
larger modelling task. The next implementable step is a defensible first
approximation that tests whether the observed cross-method item or contrast
matrices behave like one dominant dimension.

Available inputs:

- `data/derived/sprouse_analysis/sprouse_item_signal_matrix.csv`
- `data/derived/sprouse_analysis/sprouse_pair_contrasts.csv`
- `data/derived/sprouse_analysis/sprouse_signal_correlations.csv`

Available dependencies in the local environment:

- `numpy`
- `scipy`
- `pandas`

## Assumptions and Failure Conditions

1. The existing item and pair matrices are the correct inputs.
   - Fails if the matrices are stale or the approved gate is missing.
   - Response: require the approved gate and existing descriptive outputs before
     running.
2. PCA on cross-method aggregate signals is an acceptable first approximation to
   the dimensionality gate.
   - Fails if we present it as the final response-function model.
   - Response: label outputs as a dimensionality-gate approximation and keep the
     full response-function model as future work.
3. A second dimension should count only if it is larger than random-column
   structure and leaves structured one-factor residuals.
   - Fails if we rely only on informal eyeballing of correlations.
   - Response: use Horn-style parallel analysis plus one-factor residual
     diagnostics.

## Planned Script

Add:

`analysis/sprouse_dimensionality_gate.py`

Inputs:

- approved readiness manifest from `scripts/sprouse_analysis_gate.py`
- descriptive item/contrast outputs from `analysis/sprouse_item_signal.py`

Outputs under ignored `data/derived/sprouse_analysis/`:

- `sprouse_dimensionality_gate_summary.csv`
- `sprouse_dimensionality_eigenvalues.csv`
- `sprouse_dimensionality_loadings.csv`
- `sprouse_dimensionality_residuals.csv`
- `sprouse_dimensionality_manifest.csv`

## Units to Analyze

- `2013 pair`: `me_contrast`, `ls_contrast`,
  `fc_expected_agreement_rate`
- `2017 item`: `me_zscore`, `ls_zscore`, `fc_selected_rate`,
  `yn_yes_rate`
- `2017 pair`: `me_contrast`, `ls_contrast`, `fc_selected_contrast`,
  `yn_yes_contrast`

Skip `2013 condition` as a dimensionality test because it only has ME and
Likert; two columns can show agreement but cannot test a second dimension in
the intended sense.

## Decision Rule

For each analyzable matrix:

1. standardize complete cases;
2. compute the correlation matrix;
3. compute eigenvalues/eigenvectors;
4. run parallel analysis by independently permuting each method column;
5. reconstruct the correlation matrix from the first principal component and
   compute off-diagonal residuals.

Flag the matrix as `single_dimension_sufficient_first_pass` only if:

- the second observed eigenvalue is not greater than the 95th percentile second
  eigenvalue from the permuted matrices;
- one-factor off-diagonal RMS residual is at most `.10`;
- one-factor maximum absolute off-diagonal residual is at most `.20`.

Otherwise flag it as `possible_multidimensional_structure`.

These thresholds are intentionally conservative and should be treated as a
first-pass gate, not a final psychometric model.

## Verification

Run:

```bash
python3 scripts/sprouse_analysis_gate.py --reuse-status approved
python3 analysis/sprouse_item_signal.py --raw-root /tmp/bard-data-check
python3 analysis/sprouse_dimensionality_gate.py
python3 -m py_compile analysis/sprouse_dimensionality_gate.py
```

Then inspect the summary CSV and update `STATUS.md` with the first-pass result.
