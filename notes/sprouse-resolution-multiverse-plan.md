# Sprouse resolution multiverse plan

Status: frozen before execution. This is a post-outcome robustness analysis, not
part of the original analysis charter and not an external preregistration.

## Question

Does the manuscript's conclusion--that the available Sprouse comparisons show
no systematic practical resolution advantage unique to magnitude estimation
(ME)--survive the defensible scoring and modelling choices that the existing
pipeline fixed to one primary route?

The multiverse does not treat unexplained ME variance as evidence of validity.
ME-specific variation counts toward a practical advantage only when it has the
scale-boundary pattern Bard et al. predicted, improves out-of-sample prediction
of an independent judgment channel, or wins when an independent channel
adjudicates an ME--Likert decision disagreement.

## Fixed data boundary

- Sprouse, Schuetze, and Almeida (2013): 298 aligned ME/Likert conditions and
  150 published good--bad pairs.
- Sprouse and Almeida (2017): 786 aligned ME/Likert/forced-choice/yes-no items
  after the structural exclusion of `B`, `G`, and `M`, and 50 published pairs.
- Participant-level rows are read locally but never written to the repository.
- Fresh downloads are identified by SHA-256 in the output manifest.

## Score specifications

ME is scored three ways, all fixed before the multiverse is run:

1. `provided_z`: the z-scores supplied in the public files;
2. `log_subject_z`: log raw ME judgments, z-standardized within participant or
   subject, then aggregated by condition/item;
3. `subject_percentile`: within-participant or within-subject midranks, scaled to
   the unit interval, then aggregated by condition/item.

Likert is scored three ways:

1. `provided_z`: supplied z-scores;
2. `raw_mean`: raw 1--7 judgments;
3. `subject_percentile`: within-participant or within-subject midranks, scaled to
   the unit interval.

All pair scores are good-condition minus bad-condition. Transformations are
performed before condition/item aggregation. No trimming or outcome-dependent
exclusion branch is admitted.

Pre-execution implementation note: the public ME files contain some zero raw
responses, for which a literal logarithm is undefined. Non-positive responses
are treated as unavailable only in the `log_subject_z` branch; they remain in
the supplied-z and percentile branches. The manifest records the affected row
counts. This rule was added during the smoke test, before any multiverse outcome
was generated.

A second branch-specific missingness rule was fixed during verification: where
the public file supplies a z-score but records the raw judgment as `NA`, the
`provided_z` branch retains the row, while branches computed from raw judgments
treat it as unavailable. This reproduces the primary pipeline exactly and does
not use outcome values to choose rows.

## Family 1: endpoint-resolution multiverse

This family asks whether ME spreads out where the raw Likert scale is most
compressed.

- ME score: three specifications above.
- Endpoint definition:
  - `fixed`: Likert mean <=2.5, 3.5--4.5, and >=5.5;
  - `quintile`: bottom 20%, central 20%, and top 20%;
  - `quartile`: bottom 25%, central 25%, and top 25%.
- Spread statistic: sample SD, IQR, or median absolute deviation.

For every admissible cell, report lower/middle and upper/middle ME-spread ratios.
Use 5,000 fixed-seed permutations of ME scores over units to calibrate the
one-sided probability of obtaining a minimum endpoint ratio at least as large.

Specification-level support requires both endpoint ratios to exceed 1.0;
practically notable support requires both to reach 1.25 and the permutation
probability to be below .05. Family-level robustness requires at least 80% of
admissible specifications to show ordinary support and at least 50% to show
practically notable support in each dataset.

## Family 2: incremental-prediction multiverse

This family asks whether ME contributes out-of-sample information about an
independent response channel beyond Likert, and whether that increment exceeds
the reciprocal increment contributed by Likert beyond ME.

- ME score: three specifications.
- Likert score: three specifications.
- Validation target:
  - 2013: forced-choice expected-agreement margin from `FC.signtest.csv`, and
    the good-minus-bad selection contrast from `FC.logistic.csv`;
  - 2017: forced-choice good-minus-bad selection contrast, and yes/no
    good-minus-bad contrast.
- Mapping: ordinary least squares on standardized predictors, and ordinary
  least squares on percentile-rank-transformed variables.

Use 50 repeats of five-fold cross-validation with seed `20260829`. For every
specification report:

- the change in cross-validated R-squared from Likert alone to Likert plus ME;
- the reciprocal change from ME alone to ME plus Likert; and
- their difference.

Specification-level support requires an ME increment of at least .02 and a
larger ME increment than reciprocal Likert increment. Family-level robustness
requires at least 80% of admissible specifications to support ME and a median ME
increment of at least .02 in each dataset.

## Family 3: decision-adjudication multiverse

This family isolates pairs on which ME and Likert disagree about the sign of the
published good--bad contrast.

- ME score: three specifications.
- Likert score: three specifications.
- Independent adjudicator: the two dataset-specific targets listed above.

For every specification report the number of sign-discordant pairs, how often
the independent channel agrees with ME, how often it agrees with Likert, and
ties. Specification-level support requires at least five adjudicable
disagreements and ME agreement of at least 70%. Family-level robustness requires
at least 80% of admissible specifications to support ME in each dataset.

## Interpretation rule

The manuscript's primary conclusion changes to a robust practical ME advantage
only if at least two of the three families clear their family-level criteria in
both datasets. A family that clears its criterion in only one dataset or under a
minority of specifications is reported as a scoped sensitivity result. If no
family clears, the existing conclusion is retained and strengthened from a
small set of diagnostics to a bounded multiverse result.

Because the multiverse was designed after the primary results were known, it
can test robustness but cannot erase the exploratory status of the added
specifications.

## Outputs

All outputs remain ignored under `data/derived/sprouse_multiverse/`:

- `sprouse_multiverse_unit_scores.csv`;
- `sprouse_multiverse_pair_scores.csv`;
- `sprouse_endpoint_multiverse.csv`;
- `sprouse_prediction_multiverse.csv`;
- `sprouse_decision_multiverse.csv`;
- `sprouse_multiverse_summary.csv`;
- `sprouse_multiverse_manifest.csv`.

No participant identifier or participant-level row is written.
