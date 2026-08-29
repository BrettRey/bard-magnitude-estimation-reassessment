# LingBuzz v2 numbers audit

Date: 2026-08-29
Scope: named root and all seven included sections
Auditor: independent Codex subagent, GPT-5 family
Verdict: **pass after four direct-rounding corrections**

## Method

Every displayed statistic, interval, percentage, count, denominator, threshold,
year, page locator, and derived total was checked against the retained CSV
outputs or a primary/official source record. The auditor made no file edits. A
second pass over the corrected source found zero remaining numerical
mismatches, zero unsourced substantive values, and no cross-section
inconsistencies.

## Corrections

The audit caught four double-rounding errors introduced by the earlier
two-decimal formatting pass:

- 2017 item \(r\): `.93` → `.92` from exact `.924894`.
- 2013 upper-endpoint SD: `.18` → `.17` from exact `.174609`.
- 2017 pair CI upper bound: `.97` → `.96` from exact `.964973`.
- Supporting prediction-increment range: `.03--.05` → `.02--.05` from exact
  `.024756--.049255`.

## Derived claims

| Claim | Exact source value or record | Verdict |
|---|---|---|
| Figure points: 298 conditions, 786 items | `sprouse_item_signal_matrix.csv`: 298 and 786 rows | Exact |
| Likert scale 1–7 | Raw scale and `bounded_logistic_1_7` model | Exact |
| 95% bootstrap | `sprouse_sensitivity_summary.csv`, `ci_level=.95` | Exact |
| 2013 condition CI [.98,.99] | [.982808,.988570] | Correct |
| 2013 pair CI [.95,.97] | [.950441,.973965] | Correct |
| 2017 item CI [.92,.93] | [.915342,.933621] | Correct |
| 2017 pair CI [.92,.96] | [.917117,.964973] | Correct |
| 2013 pair-\(R^2\) CI [.90,.95] | [.900110,.945889] | Correct |
| 2017 pair-\(R^2\) CI [.86,.94] | [.862072,.940980] | Correct |
| Correlations .99, .96, .92, .94 | .985863, .963430, .924894, .944048 | Correct |
| Units 298, 150, 786, 50 | Signal, pair, and sensitivity outputs | Exact |
| First-component shares 89.4%, 80.6%, 85.9% | 89.3619%, 80.5867%, 85.8708% | Correct |
| Second eigenvalues below thresholds | .2836<1.0511; .5886<1.0507; .4075<1.1967 | Exact |
| 2013 endpoint/middle SDs .14/.17/.31 | .141828/.174609/.313067 | Correct |
| 2017 endpoint/middle SDs .25/.32/.35 | .248741/.321028/.349065 | Correct |
| Bounded logistic improves over linear | Lower AIC and higher \(R^2\) in both datasets | Exact |
| Pair \(R^2=.93,.90\) | .925539 and .901343 | Correct |
| Zero top-quartile/bottom-half pairs | Count 0 in both pair summaries | Exact |

## Multiverse claims

| Claim | Exact source | Verdict |
|---|---|---|
| 162 specifications | 54 endpoint + 72 prediction + 36 decision | Exact |
| Three ME and three Likert scores | Three unique score definitions each | Exact |
| No family clears in either dataset | All six dataset-family flags false | Exact |
| Endpoint support 3/27 and 6/27 | Endpoint CSV | Exact |
| One notable endpoint specification | One of 54; ratios 1.26087/1.55412, \(p=.00820\) | Exact |
| Thresholds 1.25 and .05 | Frozen plan and implementation | Exact |
| Prediction support 0/36 and 4/36 | Prediction CSV | Exact |
| Threshold \(\Delta R^2\ge .02\) | Frozen plan and implementation | Exact |
| Four supporting models all rank/forced-choice | All four rows use that target and mapping | Exact |
| Supporting range .02–.05 | Exact .024756–.049255 | Correct |
| Sign disagreements 3/150 and 1/50 | Decision and pair-score CSVs | Exact |
| Nine scoring combinations | \(3\times3=9\) | Exact |
| IDs 41, 83, 91, and p1 | Invariant across all nine combinations | Exact |
| No decision specification clears | 0/18 in each dataset | Exact |
| Figure panels show 54 and 72 specifications | Full endpoint and prediction row counts | Exact |

## External-source and bibliographic numbers

- Bard's four abstract claims and page locators 32, 35, 41, and 65 were checked
  directly against the primary PDF.
- Study years 1996, 2013, 2017, and 2018 match the primary Bard, Sprouse, and
  Langsford papers.
- Publication years and bibliography ranges match primary PDFs, official DOI
  metadata, or the original records: Bard 1996: 32–68; Sprouse et al. 2013:
  219–248; Sprouse and Almeida 2017: 1–32; Langsford et al. 2018: 1–34;
  Schütze 2016; Weskott and Fanselow 2011: 249–273; Gelman and Loken
  2013/2014; Gelman and Carlin 2014: 641–651; Steegen et al. 2016: 702–712;
  CoLA 2019: 625–641; BLiMP 2020: 377–392; Juzek 2024: 16113–16120; and
  Goodman 1955.
- Primary sources verify the benchmark counts: 23 CoLA publications, 67 BLiMP
  suites, and 1,000 SAD sequences.
- Internal enumeration claims also resolve: two central claims, four
  evidence-source kinds, three observation channels, two comparison studies,
  and three multiverse families are each explicitly listed.

## Caveat

Sprouse et al. report 296 published data points, whereas the public ME/LS
result files contain 298 shared condition identifiers. The manuscript correctly
attributes 298 to the public files and explicitly calls them aggregate
identifiers, so this is not a mismatch.

Final assessment: **pass**. All hard-coded quantitative claims match their
retained outputs or primary sources after the four corrections above.
