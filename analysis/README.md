# Analysis

Use this directory for reproducible analysis scripts or notebooks after the
dataset inventory is verified.

Candidate first scripts:

- `sprouse_item_signal.py`: first approved descriptive item/contrast signal
  pass for the Sprouse 2013 and 2017 data;
- `sprouse_dimensionality_gate.py`: first-pass PCA/parallel-analysis
  dimensionality gate over the derived item/contrast matrices;
- `sprouse_response_function_resolution.py`: bounded-Likert response-function
  sensitivity analysis for Bard's ME resolution claim;
- `sprouse_pair_resolution_robustness.py`: pair-level good-vs-bad contrast
  robustness check for ME-specific resolution after bounded-method prediction;
- method-comparison harmonization for any fuller response-function model;
- reliability and participant-response analysis, only where row structure
  supports it;
- item-level divergence analysis for grammaticality vs acceptability labels.

Current gate:

- `scripts/build_sprouse_crosswalks.py` writes ignored structural crosswalks and
  machine-readable pre-analysis rules under `data/derived/sprouse/`.
- `scripts/sprouse_analysis_gate.py` reads those rules and writes ignored
  readiness manifests under `data/derived/sprouse_analysis/`.
- Sprouse reuse is approved for the limited secondary methodological analysis.
  Run `scripts/sprouse_analysis_gate.py --reuse-status approved` before outcome
  scripts. The approved gate opens descriptive and model-building work within
  the permission boundary, but raw participant-level files still must not be
  redistributed.
- `analysis/sprouse_dimensionality_gate.py` should be run only after
  `analysis/sprouse_item_signal.py`, because it consumes those derived
  item/contrast matrices. Its outputs are a first-pass gate, not a final
  confirmatory response-function model.
- `analysis/sprouse_response_function_resolution.py` should also be run only
  after `analysis/sprouse_item_signal.py`. It uses raw local ME/LS files plus
  the approved readiness gate, writes ignored derived outputs under
  `data/derived/sprouse_analysis/`, and treats ME as an unbounded diagnostic
  axis rather than as the true latent acceptability scale.
- `analysis/sprouse_pair_resolution_robustness.py` should be run after
  `analysis/sprouse_item_signal.py`. It consumes the derived pair table, reads
  local raw ME/LS rows only to aggregate condition-level raw Likert contrasts,
  uses explicit compact-spacing fallback for the known 2013 `den Dikken` and
  `de Vries` spacing variants, and writes ignored pair-level diagnostics under
  `data/derived/sprouse_analysis/`.

## Local reproduction recipe

The Sprouse data are public on Jon Sprouse's author site but are not
redistributed here. To reproduce the reported diagnostics locally, download the
2013 and 2017 data/materials files from the source URLs recorded in
`notes/source-verification.md`, then unpack/place them so this layout exists:

```text
/tmp/bard-data-check/
|-- Sprouse2013/
|   `-- SSA.data/
|       |-- FC experiment/
|       |-- LS experiment/
|       `-- ME experiment/
`-- Sprouse2017/
    |-- SA2017.data/
    `-- SA2017.materials.xlsx
```

Run the pipeline from the project root:

```bash
python3 scripts/build_sprouse_crosswalks.py --raw-root /tmp/bard-data-check
python3 scripts/sprouse_analysis_gate.py --reuse-status approved
python3 analysis/sprouse_item_signal.py --raw-root /tmp/bard-data-check
python3 analysis/sprouse_dimensionality_gate.py
python3 analysis/sprouse_response_function_resolution.py --raw-root /tmp/bard-data-check
python3 analysis/sprouse_pair_resolution_robustness.py --raw-root /tmp/bard-data-check
```

All generated outputs remain under ignored `data/derived/` paths unless a later
sharing decision deliberately promotes aggregate, non-participant-level files.
