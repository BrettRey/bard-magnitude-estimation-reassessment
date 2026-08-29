# Manuscript figure plan

## Recommendation

Add two figures. Together they should let a reader see the paper's empirical argument before reading the numerical table: the methods largely share a signal, bounded Likert responses curve at the ends, and the apparent magnitude-estimation advantages do not recur broadly across defensible specifications.

## Figure 1: Shared signal and bounded response

Two panels, one for each source dataset:

- horizontal axis: aggregate magnitude-estimation mean (standardized);
- vertical axis: aggregate raw Likert mean on the 1–7 scale;
- translucent points: conditions in Sprouse, Schütze, and Almeida (2013), and items in Sprouse and Almeida (2017);
- dashed line: linear fit;
- solid line: bounded logistic fit.

This figure should make the paper's fair measurement null visible. The high convergence is obvious from the point cloud, while the solid curve shows why bounded tasks shouldn't be treated as linear noisy copies of magnitude estimation. The caption will state that magnitude estimation is a diagnostic axis, not the latent true scale.

Placement: Section 4, immediately after the paragraph reporting the common signal and bounded curvature.

## Figure 2: Multiverse landscape

Three compact panels:

1. Endpoint specifications: all admissible minimum endpoint-to-middle spread ratios, separated by dataset, with a reference line at 1.0 and the sole notable specification highlighted.
2. Incremental prediction: cross-validated change in R-squared from adding magnitude estimation to Likert, with a reference line at .02. Colour distinguishes forced-choice from yes/no targets; marker shape distinguishes raw- from rank-scale mappings. This panel makes the four localized 2017 rank/forced-choice results visible without hiding the rest of the specification distribution.
3. Decision consequences: proportion of ME–Likert contrast-sign disagreements, annotated as 3/150 for 2013 and 1/50 for 2017. The caption will note that no decision specification clears its family rule.

Placement: Section 4, after the paragraph giving the disaggregated multiverse result.

## Production and verification

- Add one deterministic script: `analysis/make_manuscript_figures.py`.
- Read only the existing aggregate products under `data/derived/sprouse_analysis/` and `data/derived/sprouse_multiverse/`.
- Write vector PDFs for LaTeX and PNG previews under `figures/`.
- Use the central plotting palette and EB Garamond styling, but retain differences in line style and marker shape so the plots work in greyscale.
- Add source-data and expected-row checks so a stale or incomplete analysis output fails loudly.
- Keep the existing numerical table. It supplies exact values that the figures shouldn't try to duplicate.
- Rebuild, inspect every new figure at full resolution and in the manuscript, and rerun house-style/build checks.

## Deliberate omission

Do not add a separate PCA scree plot. It would visually promote a deliberately weak first-pass dimensionality check and compete with the paper's actual claim. The numerical table is the right level of emphasis for that diagnostic.
