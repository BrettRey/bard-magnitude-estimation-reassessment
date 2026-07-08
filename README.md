# Bard Magnitude Estimation Reassessment

Working-paper repository for:

*Was magnitude estimation necessary? A secondary-data reassessment of Bard,
Robertson, and Sorace (1996)*

Current status: July 2026 Glossa-targeted working-paper repository checkpoint.
The compiled manuscript is [main.pdf](main.pdf); source lives in
[main.tex](main.tex) and [sections/](sections/). Venue-prep notes are in
[submission/](submission/).

## Current Claim

The paper separates two claims often run together in the history of magnitude
estimation:

- acceptability judgments are graded, measurable, and methodologically serious;
- magnitude estimation has a practical advantage over simpler formal judgment
  tasks.

The current Sprouse reanalysis supports the first claim more strongly than the
second. In the available aggregate Sprouse diagnostics, magnitude estimation,
Likert ratings, forced choice, and yes/no judgments preserve a strong practical
item/contrast signal. The analysis finds bounded response-function curvature,
but no systematic practical ME-only resolution advantage in the tested Sprouse
contrasts.

## Data Boundary

Raw participant-level files are not redistributed in this repository. Jon
Sprouse approved Brett Reynolds's limited secondary use of the public Sprouse,
Schuetze, and Almeida (2013) and Sprouse and Almeida (2017) data files after
checking with Diogo Almeida. The approved scope is a methodological analysis of
magnitude estimation's contribution to an item-level acceptability signal.

Generated outputs under `data/derived/` are ignored by Git. The manuscript
reports summary diagnostics, not raw participant rows or derived
participant-level tables. See [data/README.md](data/README.md) and
[notes/source-verification.md](notes/source-verification.md).

## Reproducing The Analysis

Prerequisites:

- TeX Live with XeLaTeX and Biber;
- Python 3 with `numpy`, `pandas`, and `scipy`;
- local copies of the public Sprouse 2013/2017 data and materials, placed under
  `/tmp/bard-data-check/` as described in [analysis/README.md](analysis/README.md).

Build the manuscript:

```bash
make
```

Run the full local analysis pipeline:

```bash
python3 scripts/build_sprouse_crosswalks.py --raw-root /tmp/bard-data-check
python3 scripts/sprouse_analysis_gate.py --reuse-status approved
python3 analysis/sprouse_item_signal.py --raw-root /tmp/bard-data-check
python3 analysis/sprouse_dimensionality_gate.py
python3 analysis/sprouse_response_function_resolution.py --raw-root /tmp/bard-data-check
python3 analysis/sprouse_pair_resolution_robustness.py --raw-root /tmp/bard-data-check
python3 analysis/sprouse_sensitivity_summary.py
```

All analysis products are written to ignored `data/derived/` paths unless a
later sharing decision deliberately promotes aggregate, non-participant-level
outputs.

## Repository Map

- [main.tex](main.tex): manuscript driver.
- [sections/](sections/): section-level manuscript source.
- [analysis/](analysis/): reproducible analysis scripts and local reproduction
  recipe.
- [scripts/](scripts/): structural crosswalk and analysis-gate scripts.
- [data/README.md](data/README.md): data-handling and permission boundary.
- [notes/source-verification.md](notes/source-verification.md): source and
  dataset verification trail.
- [notes/analysis-charter.md](notes/analysis-charter.md): internal
  pre-outcome analysis charter.
- [reviews/](reviews/): simulated review-board reports.
- [submission/](submission/): release and submission planning notes.

## House Style

This project uses Brett Reynolds's central house style strictly by symlink:

- `.house-style/preamble.tex -> ../../../../.house-style/preamble.tex`
- `.house-style/style-rules.yaml -> ../../../../.house-style/style-rules.yaml`
- `references.bib -> ../../../.house-style/references.bib`

Do not copy house-style files into this project.
