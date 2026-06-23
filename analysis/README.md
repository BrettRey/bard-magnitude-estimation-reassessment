# Analysis

Use this directory for reproducible analysis scripts or notebooks after the
dataset inventory is verified.

Candidate first scripts:

- dataset inventory and metadata table;
- method-comparison harmonization;
- reliability and participant-response analysis;
- item-level divergence analysis for grammaticality vs acceptability labels.

Current gate:

- `scripts/build_sprouse_crosswalks.py` writes ignored structural crosswalks and
  machine-readable pre-analysis rules under `data/derived/sprouse/`.
- `scripts/sprouse_analysis_gate.py` reads those rules and writes ignored
  readiness manifests under `data/derived/sprouse_analysis/`.
- With Sprouse reuse still pending, outcome summaries remain gated. The gate
  script may be run to verify analysis inputs, but it does not compute method
  rankings, convergence rates, means, or model fits.
