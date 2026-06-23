# Dataset Inventory

Status: structural inventory only. This file records data availability, file
structure, identifiers, and comparability checks before substantive modelling.
It should not be used to choose methods, transformations, exclusions, or claims
based on observed performance.

## Raw Data Handling

No raw participant-level data are committed to the repository. Public Sprouse
verification copies were inspected locally under `/tmp/bard-data-check`.

The Sprouse CSV result files include this caveat in their header block: the data
are provided in the spirit of open science so that researchers can verify the
analyses, and researchers are asked to contact Jon Sprouse about possible use
for novel research. Until that reuse question is resolved, structural inventory,
script drafting, and reproduction-oriented checks are acceptable; publication of
novel secondary results should remain conditional.

The result CSVs include five non-data lines before the real header. Their own
metadata note says that R users should try `skip=5`. Analysis scripts should use
the same rule for result files and should not apply it to condition or materials
files that already start with headers.

`scripts/build_sprouse_crosswalks.py` implements this import rule and writes
ignored structural outputs to `data/derived/sprouse/`. The generated files are
local derivatives only: `schema_summary.csv`, `2013_condition_crosswalk.csv`,
`2013_condition_presence.csv`, `2017_label_crosswalk.csv`,
`2017_material_items.csv`, `2017_method_item_presence.csv`, and
`2017_yn_only_items.csv`.
The script also writes `analysis_rules.csv` and `2017_yn_item_inclusion.csv` so
future analysis code can read the pre-analysis representation and inclusion
rules directly.

## Sprouse, Schuetze, and Almeida 2013

Source files inspected:

- `SSA.data/FC experiment/FC.logistic.csv`
- `SSA.data/FC experiment/FC.signtest.csv`
- `SSA.data/FC experiment/conditions.csv`
- `SSA.data/ME experiment/LI.me.results.csv`
- `SSA.data/ME experiment/LI.conditions.csv`
- `SSA.data/LS experiment/LI.ls.results.csv`
- `SSA.data/LS experiment/LI.conditions.csv`
- `SSA.Materials.xlsx`

### Result Files

| File | Rows | Columns | Key counts |
| --- | ---: | --- | --- |
| `FC.logistic.csv` | 30,700 | `participant`, `survey`, `order`, `item`, `condition`, `judgment` | 307 participants; 24 surveys; 2,386 items; 300 conditions; 50 order positions |
| `FC.signtest.csv` | 15,350 | `participant`, `survey`, `order`, `judgment`, `item`, `condition`, `expected`, `pattern` | 307 participants; 24 surveys; 1,200 items; 150 conditions; 50 order positions |
| `LI.me.results.csv` | 30,400 | `participant`, `survey`, `order`, `judgment`, `item`, `condition`, `zscores` | 304 participants; 24 surveys; 2,384 items; 298 conditions; 100 order positions |
| `LI.ls.results.csv` | 30,400 | `participant`, `survey`, `order`, `judgment`, `item`, `condition`, `zscores` | 304 participants; 24 surveys; 2,384 items; 298 conditions; 100 order positions |

### Condition And Materials Files

| File | Rows | Columns | Notes |
| --- | ---: | --- | --- |
| `FC experiment/conditions.csv` | 150 | `bad`, `good` | Pair-level crosswalk for forced choice. |
| `ME experiment/LI.conditions.csv` | 150 | `bad`, `good`, `list` | Pair/list crosswalk for magnitude estimation. |
| `LS experiment/LI.conditions.csv` | 150 | `bad`, `good`, `list` | Pair/list crosswalk for Likert ratings. |
| `SSA.Materials.xlsx` | 1 sheet; 1,203 non-empty rows | bad item, bad sentence, notes, plausibility flag, good item, good sentence, key | Header row begins at row 4. |

### Structural Alignment

- Magnitude estimation and Likert have identical item sets: 2,384 common items
  out of 2,384 in the union.
- Magnitude estimation and Likert have identical condition sets: 298 common
  conditions out of 298 in the union.
- Forced-choice sign-test conditions overlap only partly with the ME/LS
  condition fields as named in the result files: 144 common conditions out of
  304 in the union. The forced-choice condition file should be treated as the
  authoritative pair-level crosswalk before modelling FC against ME/LS.
- The FC logistic file has 300 conditions and the FC sign-test file has 150
  conditions, so scripts must state which FC representation is being used for
  each estimand.
- The scripted pair-level crosswalk finds 144 exact FC-to-ME/LS pair matches by
  bad-condition key and 150 matches after a compact spacing key is applied. The
  six non-exact cases are ID spacing variants:
  `33.1.den Dikken.58a.*`, `33.1.den Dikken.5b.*`,
  `33.1.den Dikken.62b.*`, `33.1.den Dikken.71a.*`,
  `36.4.den Dikken.45.*`, and `37.2.de Vries.39a.*`. These correspond to
  `denDikken`/`deVries` forms in the ME/LS condition files. The script preserves
  original IDs and records the compact key as a candidate match basis rather
  than silently rewriting identifiers.

### Charter Mapping

- Common item-level acceptability signal: supported for ME versus Likert
  directly; supported for FC through the pair-level `FC.signtest.csv`
  representation as primary.
- Method-specific noise or bias: supported for ME versus Likert; possible for FC
  through `FC.signtest.csv` as primary and `FC.logistic.csv` only as a named
  sensitivity representation.
- Decision agreement: supported, but the unit of decision must be fixed before
  analysis.
- Method-by-item instability: possible for ME versus Likert; FC comparisons must
  use the explicit pair-level crosswalk or be labelled as the logistic
  sensitivity representation.

## Sprouse And Almeida 2017

Source files inspected:

- `SA2017.data/ME.results.csv`
- `SA2017.data/LS.results.csv`
- `SA2017.data/FC.results.csv`
- `SA2017.data/YN.results.csv`
- `SA2017.materials.xlsx`

### Result Files

| File | Rows | Columns | Key counts |
| --- | ---: | --- | --- |
| `ME.results.csv` | 14,100 | `subject`, `survey`, `order`, `judgment`, `item`, `condition`, `zscores` | 141 subjects; 8 surveys; 786 items; 100 conditions; 100 order positions |
| `LS.results.csv` | 14,100 | `subject`, `survey`, `order`, `judgment`, `item`, `condition`, `zscores` | 141 subjects; 8 surveys; 786 items; 100 conditions; 100 order positions |
| `FC.results.csv` | 6,950 | `subject`, `survey`, `order`, `judgment`, `condition`, `label`, `expected`, `pattern` | 139 subjects; 16 surveys; 786 condition values; 50 order positions |
| `YN.results.csv` | 14,734 | `subject`, `survey`, `order`, `judgment`, `item`, `condition` | 139 subjects; 8 surveys; 789 items; 103 conditions; 106 order positions |

### Materials Files

| Sheet | Non-empty rows | Columns observed | Notes |
| --- | ---: | --- | --- |
| `LI phenomena labels` | 51 | `label`, `bad condition`, `good condition` | Maps `p1`--style labels to bad/good condition IDs. |
| `materials` | 801 | `item`, `sentence` | Item-to-sentence lookup. |

### Structural Alignment

- Magnitude estimation and Likert have identical item sets: 786 common items out
  of 786 in the union.
- Magnitude estimation and Likert have identical condition sets: 100 common
  conditions out of 100 in the union.
- Forced-choice `condition` values align with the ME/LS `item` fields: 786
  common values out of 786 in the union.
- Yes/no overlaps with the ME item set on 786 items out of 789 in the union, so
  the three YN-only items need inspection before any direct comparison.
- The scripted YN-only check identifies the three non-material item IDs as `B`,
  `G`, and `M`. Each appears for 139 subjects twice, giving 278 rows per ID:
  `M` at order positions 1 and 5, `B` at positions 2 and 4, and `G` at
  positions 3 and 6. They are not present in the materials workbook.
- The FC file does not have an `item` column. Its `condition` field appears to
  carry item IDs, while `label` carries the phenomenon-pair label. Scripts
  should preserve that distinction.

### Charter Mapping

- Common item-level acceptability signal: supported for ME, Likert, FC, and most
  YN rows after excluding the non-material yes/no IDs `B`, `G`, and `M`.
- Method-specific noise or bias: supported for ME versus Likert directly;
  possible for FC and YN with explicit unit handling.
- Decision agreement: supported if labels/conditions are mapped through the
  workbook before analysis.
- Method-by-item instability: possible, but should be secondary because the
  charter treats 2017 as a generalization/design-sensitivity check.

## Immediate Script Requirements

- Done in `scripts/build_sprouse_crosswalks.py`: define a single import
  function that skips five header lines only for Sprouse result CSVs.
- Done in `scripts/build_sprouse_crosswalks.py`: preserve original identifiers
  and report spacing-normalized candidate keys separately.
- Done in `scripts/build_sprouse_crosswalks.py`: build explicit crosswalk
  tables from the condition CSVs and materials workbook before joining methods.
- Done in `scripts/build_sprouse_crosswalks.py`: write `analysis_rules.csv`
  with the primary 2013 FC representation, the 2013 FC sensitivity
  representation, and the 2017 YN item-level exclusion rule.
- Done in `scripts/build_sprouse_crosswalks.py`: write
  `2017_yn_item_inclusion.csv`, with 786 YN items included and `B`, `G`, and
  `M` excluded from item-level comparisons.
- Done locally: generated crosswalks and summaries are written under ignored
  `data/derived/sprouse/`, not `data/raw/`.
- Keep all first-pass summaries structural. Do not compute method rankings,
  convergence rates, means, or model fits until this inventory is accepted.
