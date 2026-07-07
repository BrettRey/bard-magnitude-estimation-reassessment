# Response-Function Resolution Plan

## Purpose

The dimensionality gate did not reject a one-dimension structure in the available aggregate Sprouse matrices. The next question is narrower: whether magnitude estimation (ME) shows evidence of the resolution advantage Bard et al. argued for, especially where a bounded Likert response function might compress distinctions.

This is not the final mixed or ordinal measurement model. It is a targeted sensitivity analysis that asks whether the raw Sprouse Likert scale behaves as if it is saturating relative to ME, and whether ME retains extra separation where the bounded scale is near its limits.

## Assumptions Checked

- Raw Sprouse result files are available only in the local working copy under `/tmp/bard-data-check`, not in Git.
- The existing approved gate and descriptive script already read these files without redistributing participant-level rows.
- The relevant raw columns exist in both datasets:
  - ME: unbounded `judgment` plus supplied `zscores`.
  - Likert: bounded 1-7 `judgment` plus supplied `zscores`.
- The 2013 files need the project loader's encoding/header handling rather than plain `pandas.read_csv(skiprows=5)`.

## Main Diagnostic

Treat ME aggregate z-score as the working unbounded axis and raw Likert mean as the bounded response. Fit two item/condition-level response functions separately for:

- 2013 condition means.
- 2017 item means.

Models:

1. Linear response: raw Likert mean as a linear function of ME z-score.
2. Saturating bounded response: raw Likert mean as a logistic curve constrained to the 1-7 scale.

If the saturating model clearly improves fit and the residual/within-bin diagnostics show large ME spread near Likert endpoints, that supports the possibility that ME preserved distinctions compressed by the bounded scale. If the linear model is essentially as good and endpoint ME spread is not exceptional, the response-function route gives little support to a practical ME resolution advantage in these datasets.

## Resolution Diagnostics

Write three ignored output files under `data/derived/sprouse_analysis/`:

- `sprouse_response_function_model_fits.csv`: dataset, unit, model, sample size, RSS, AIC, R-squared, and fitted parameters.
- `sprouse_response_function_bins.csv`: Likert quantile bands with ME spread, raw Likert spread, and model residual spread.
- `sprouse_response_function_residuals.csv`: per item/condition fitted values and residuals for audit and later plotting.

The bins should distinguish lower endpoint, lower-middle, middle, upper-middle, and upper endpoint regions. The endpoint labels are diagnostic labels, not claims that the aggregate means literally equal 1 or 7.

## Interpretation Rules

- Do not treat ME as the true latent acceptability scale. It is only the unbounded proxy in this diagnostic.
- Do not claim that a better bounded logistic fit proves ME superiority. It only shows that a bounded response-function story is plausible.
- Do not claim that a weak logistic result proves ME is useless. It only weakens the Bard-style practical resolution claim in these datasets.
- Keep the Gelmanian discipline: state the estimand, make the falsification condition visible, avoid post-hoc method shopping, and report the sensitivity result even if it is dull.

## Implementation Steps

1. Add `analysis/sprouse_response_function_resolution.py`.
2. Reuse the project CSV loader pattern so legacy encodings are handled consistently.
3. Require the approved Sprouse readiness gate and the first descriptive outputs.
4. Aggregate raw Likert means and ME z-score means for the 2013 and 2017 ME/LS files.
5. Fit linear and bounded-logistic response functions with `numpy` and `scipy`.
6. Write model-fit, bin, residual, and manifest outputs under the ignored derived directory.
7. Update `analysis/README.md`, `STATUS.md`, and `DECISIONS.md` with the scope and result.
8. Run the script, `py_compile`, and `git diff --check`.
