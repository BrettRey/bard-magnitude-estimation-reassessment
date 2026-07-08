# Roadmap with Review-Board Assessments

Date: 2026-07-08

## Current State

The paper is now a constrained secondary-data results draft, not a mere design
proposal. Sprouse reuse permission is approved within a limited methodological
scope; raw participant-level files remain outside the repository; the manuscript
reports aggregate diagnostics only.

The last shipped commit before the Stage 4 pass is `9a87700`
(`Apply roadmap reader-facing tightening`). Stage 1 was shipped as `c4eb798`
(`Record roadmap and proportional completion pass`), and Stages 2 and 3 were
shipped together as `9a87700`.

The current Stage 4 pass adds a small sensitivity check rather than a new
modelling program: aggregate-unit bootstrap intervals for the reported
cross-method correlations and pair-level bounded-predictor \(R^2\). The
generated sensitivity CSVs remain ignored under `data/derived/`; the committed
artifact is the script plus the manuscript and documentation sentences needed
to interpret it.

The current manuscript remains 10 pages. The most recent pre-Stage-4 checks
passed: style scan, `git diff --check`, `make`, and final LaTeX log scan.
Remaining warnings are the existing template-level `fancyhdr` warnings and the
existing `microtype` footnote patch warning.

## What the Boards Have Said

### June 23 Board: Design-Stage Stress Test

Verdict: unanimous Revise & Resubmit, no rejects.

The June board found the original direction promising but exposed three
structural risks:

1. The common-latent-signal null was too easy on the conclusion because it
   treated all methods as noisy readings of one scalar.
2. The Bard target needed full primary-text grounding, especially the
   ratio-scale and fixed-scale-censoring rationale.
3. The projectibility section had to generate an empirical prediction, not sit
   beside the measurement argument.

Status now:

| June board item | Current status |
|---|---|
| Re-specify the null with method-specific response functions | Addressed in design and implemented approximately in Sprouse diagnostics |
| Add dimensionality test/check before reading ME-specific terms | Addressed as a first-pass aggregate check; explicitly limited |
| Page-anchor Bard from the primary article | Addressed |
| Separate Bard's actual resolution claim from later "gold standard" reception | Addressed |
| Operationalize Type S/M as contrast-level properties | Addressed in Section 4 |
| Split CoLA/BLiMP/SAD afterlife by evidential channel | Addressed, now with a compact table |
| Make projectibility predict where a single scalar should fail | Addressed in Section 6 and conclusion, though still modest |
| Resolve B/G/M exclusion with Sprouse directly | Structurally justified; not separately author-confirmed |

Assessment: the June board's core rigor concerns are now mostly resolved. The
remaining live issue from that board is not conceptual but evidential: B/G/M is
treated by documented structural exclusion rather than by direct author
confirmation.

### July 7 Board: Results-Draft Stress Test

Verdict: unanimous Revise & Resubmit, no rejects.

The July board judged the paper fair, disciplined, and viable. Its concerns were
mostly about auditability and presentation rather than the validity of the core
move.

| July board item | Status after current pass |
|---|---|
| Empirical diagnostics too compressed | Addressed proportionally: aggregate counts are in Table `sprouse-diagnostics`, and aggregate-unit bootstrap intervals now cover the reported correlations and pair-level \(R^2\) |
| Practical ME advantage lacks decision rule | Addressed by Gelman pass in Section 4 and conclusion |
| Dimensionality language too strong | Addressed; implemented result is a check/screen, not a full participant-level gate |
| Reproducibility/provenance too thin | Mostly addressed through `analysis/README.md`, data/code availability, and internal charter wording |
| Benchmark afterlife section too compressed | Addressed with compact CoLA/BLiMP/SAD construction table |
| Projectibility payoff too late or too implicit | Partly addressed with conclusion payoff sentence; can be brought earlier if needed |

Assessment: the July board would probably still ask for a fuller methods
appendix, but that is a completeness request, not a fatal rigor objection. The
current draft is defensible as a scoped paper if it does not pretend to be the
last word on participant-level measurement modelling.

## Quality-Gate View

### Rigour

Current state is strong enough for the paper's stated scope. The null is no
longer rigged against ME; response-function curvature is allowed; dimensionality
is checked before ME-specific interpretation; practical advantage has a decision
rule; limitations are named.

Next rigor gain worth doing: add only concise formula/provenance detail where it
prevents misreading of the existing diagnostics. Avoid a sprawling appendix until
a venue or reviewer demands it.

### Accuracy

Current state is good. Bard is page-anchored; Sprouse permission is stated;
Langsford is kept at article level; CoLA/BLiMP/SAD are not treated as ME evidence;
raw data are not redistributed.

Next accuracy gain worth doing: one final source-to-claim audit of tables and
captions before any public release or preprint.

### Reliability

Current state is honest but not exhaustive. The manuscript names aggregate
diagnostics as weaker than posterior certainty or equivalence testing, does not
claim that aggregate PCA rules out participant-level method factors, and now
adds aggregate-unit bootstrap intervals for the compact reported statistics.

Next reliability gain worth doing: only source-to-claim audit and
venue-specific reproducibility detail. A larger modelling appendix should wait
for reviewer demand or a venue that needs it.

### Originality

The original contribution remains intact: Bard's durable measurement legacy is
separated from ME's method-specific status, and acceptability judgments are
routed into a projectibility-profile account rather than treated as identical
with grammaticality.

Next originality gain worth doing: sharpen the opening paragraph so the
construct-level payoff is visible before Section 6.

## Roadmap

### Stage 1: Ship the Proportional Completion Pass

Goal: preserve the current small improvements.

Tasks:

- Re-run `make`, style scan, `git diff --check`, and final log scan.
- Commit the current uncommitted changes if clean.
- Push to `origin/main`.

Exit criterion: branch is clean and aligned; `STATUS.md` records the checkpoint.

### Stage 2: Reader-Facing Tightening

Goal: improve readability and claim visibility without adding scope.

Candidate edits:

- Add one opening sentence or short paragraph naming the paper's new payoff:
  acceptability measurement survived; ME's special status did not; the surviving
  signal licenses stable item-level contrast ordering across ordinary formal
  judgment formats.
- Make the abstract mirror the current decision-rule language: no systematic
  practical ME-only resolution advantage in the tested Sprouse contrasts.
- Check that every occurrence of "dimension", "signal", "profile", and
  "acceptability" is scoped to the right evidential level.

Exit criterion: the core contribution is visible by the end of Section 1.

### Stage 3: Minimal Auditability Additions

Goal: satisfy rigorous readers without turning the paper into a methods
appendix.

Candidate edits:

- Add a short "Diagnostics are generated by..." sentence in the Table
  `sprouse-diagnostics` caption or nearby prose, pointing to the script names.
- Confirm that `analysis/README.md` has the exact command sequence for every
  reported table row.
- Add one sentence distinguishing aggregate item/contrast counts from
  participant-level rows.

Exit criterion: a reviewer can trace each reported diagnostic to a script and
known aggregate unit without raw data redistribution.

### Stage 4: Optional Sensitivity Work

Goal: only add analysis that changes evidential strength.

Status: completed proportionally.

Completed work:

- Added `analysis/sprouse_sensitivity_summary.py`.
- Bootstrapped the aggregate correlations and pair-level \(R^2\) from existing
  derived outputs.
- Kept generated aggregate sensitivity CSVs ignored under `data/derived/`.

Deferred work:

- Transformation sensitivity for ME z-scores and bounded-logistic fits. This
  should not be added unless a reviewer specifically doubts the transformation
  choice or the current scripts can support it without broadening the paper.
- Promotion of non-participant-level aggregate outputs. This should wait for a
  deliberate data-sharing decision.

### Stage 5: Preprint or Submission Preparation

Goal: decide what the paper is being released as.

Choices:

- Working paper / public repository checkpoint: acceptable soon after Stage 2 or
  Stage 3.
- Preprint: wait until the source-to-claim audit and minimal auditability pass
  are complete.
- Journal submission: wait for venue choice and then tune length, appendix
  expectations, and data-availability language to that venue.

Exit criterion: chosen release form matches the manuscript's actual scope.

## Do Not Do Yet

- Do not expand into a general survey of acceptability benchmarks.
- Do not promise a full participant-level factor model across Bard, Sprouse, and
  Langsford unless the needed raw rows exist.
- Do not redistribute participant-level raw files or derived participant-level
  tables.
- Do not claim an external registry entry.
- Do not chase every review-board completeness request before the paper has a
  venue or release target.

## Recommended Next Move

Run the final checks for the Stage 4 sensitivity pass, then ship it. After that,
the next real move is Stage 5: choose working-paper, preprint, or journal target
and run a source-to-claim audit for that release form.
