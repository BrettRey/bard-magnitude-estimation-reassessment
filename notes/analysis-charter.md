# Analysis Charter

Status: active pre-analysis checkpoint after Roughdraft review. This charter
freezes the primary analysis choices before any new row-level modelling or
visualization of the Sprouse data. Later deviations are allowed, but they must
be labelled exploratory in the paper and in the analysis notes.

## Purpose

The paper asks whether magnitude estimation has a practical measurement
advantage over other formal acceptability-judgment methods, given a
source-grounded reading of Bard, Robertson, and Sorace (1996). The target is not
"Bard were wrong." The target is narrower: Bard's documented claim that
magnitude estimation solves conventional scale problems and yields robust
fine-grained acceptability data, plus the stronger later reading that magnitude
estimation has a privileged methodological status.

The analysis should therefore compare magnitude estimation against a serious
measurement null: formal methods are noisy observations of a common item-level
acceptability signal. Magnitude estimation has to earn any method-specific term.

## Dataset Routing

### Included for row-level analysis

- Sprouse, Schuetze, and Almeida (2013): primary row-level analysis base.
  - Methods: magnitude estimation, 7-point Likert scale, forced choice.
  - Role: main test of method-specific practical advantage on a later
    acceptability-judgment dataset.
  - Constraint: data files ask researchers to contact Jon Sprouse about novel
    reuse. Treat downloaded files as verification copies until reuse is
    resolved.
- Sprouse and Almeida (2017): secondary row-level analysis base.
  - Methods: magnitude estimation, Likert scale, forced choice, yes/no.
  - Role: generalization and design-sensitivity check, not the main historical
    test of Bard's claim.
  - Constraint: same author-contact caveat.

### Included without row-level reanalysis

- Bard, Robertson, and Sorace (1996): conceptual target and source-grounding
  source. No public participant-level rows have been found.
- Langsford et al. (2018): article-level evidence about reliability, bias,
  response-style variability, and the relative stability of Likert and
  Thurstonian measures. No public raw participant-response rows have been found.
- CoLA, BLiMP, and the Syntactic Acceptability Dataset: afterlife evidence for
  the persistence of formal acceptability measurement. They are not evidence
  about magnitude estimation versus Likert, forced choice, or Thurstonian
  methods.

## Primary Estimands

1. Common item-level acceptability signal: the degree to which methods recover
   the same item or contrast ordering.
2. Method-specific noise or bias: the residual method contribution after
   accounting for item or contrast signal.
3. Decision agreement: whether methods lead to the same theoretically relevant
   acceptability conclusions for contrasts.
4. Method-by-item instability: cases where method choice changes the linguistic
   conclusion. Estimate this only in row-level datasets with comparable items.

Participant response-style and test-retest estimands are not primary for this
paper unless a dataset provides the required repeated participant-level
structure. Do not infer them from published convergence rates or article-level
summaries.

## Primary Comparisons

For Sprouse et al. (2013), the primary comparison set is:

- magnitude estimation versus 7-point Likert;
- magnitude estimation versus forced choice, using the pair-level
  `FC.signtest.csv` representation as primary;
- all three formal methods versus the published informal judgment labels, where
  the original dataset supports that comparison.

The 2013 `FC.logistic.csv` representation is a named sensitivity analysis, not
the primary forced-choice comparison. It preserves individual item-level binary
rows, but it changes the forced-choice unit from pair-level decisions to
item-level rows.

For Sprouse and Almeida (2017), the secondary comparison set is:

- magnitude estimation versus Likert;
- magnitude estimation versus forced choice;
- yes/no as a design-sensitivity comparison, not as a direct replacement for
  Bard's magnitude-estimation claim.

For 2017 yes/no item-level comparisons, exclude item IDs `B`, `G`, and `M`.
They are not in the materials workbook, appear at repeated early order positions
for every subject, and do not align with the ME/LS/FC item universe.

No method may be promoted to "primary" after seeing which method looks best.

## Primary Scoring Rules

Use the scoring conventions already present in the verified data files as the
primary analysis inputs:

- magnitude-estimation and Likert `zscores` where supplied;
- forced-choice binary judgments and the dataset's published expected-pattern
  or convergence fields where supplied;
- item, condition, participant or subject, survey, and order fields as
  design-level variables, not as optional post-hoc filters.
- the generated `analysis_rules.csv` file as the machine-readable record of
  forced-choice representation and yes/no inclusion decisions.

Any alternative transformation, trimming rule, normalization, exclusion rule, or
aggregation level must be listed as a sensitivity analysis before it is run.

## Practical Measurement Advantage

Magnitude estimation counts as having a practical advantage only if it improves
one of the following over the common-latent-signal null by enough to change the
paper's substantive conclusion:

- out-of-sample prediction of item or contrast acceptability;
- decision stability for theoretically relevant contrasts;
- convergence with independently published judgments;
- interpretable reduction in method-specific noise or bias.

A small numerical improvement that leaves the same linguistic conclusions in
place is not a practical advantage. A method-specific advantage that appears
only under one transformation or exclusion rule is a sensitivity result, not the
main result.

## Negative Controls

Use negative controls to detect pipeline artefacts, not as the substantive null:

- shuffle acceptability labels within constrained item sets;
- permute method labels only where the design makes the permutation meaningful;
- simulate no-method-advantage data from a common-signal structure and confirm
  that the analysis does not routinely select magnitude estimation as superior.

If negative controls produce a strong magnitude-estimation advantage, the
analysis pipeline is not trustworthy enough to support the paper's main claim.

## Forbidden Claims

The paper should not claim:

- to directly replicate Bard et al. without Bard participant-level data;
- to reanalyse Langsford response styles or test-retest reliability without
  Langsford raw participant-response rows;
- that CoLA, BLiMP, or SAD adjudicate magnitude estimation against other human
  judgment methods;
- that expert asterisks, naive participant responses, and benchmark labels are
  interchangeable evidence;
- that magnitude estimation lacks any possible use, rather than lacking a
  demonstrated practical advantage in the available comparison data.

## Allowed Exploratory Work

Exploratory work is allowed if labelled as such:

- additional transformations of magnitude-estimation scores;
- alternative aggregation levels;
- post-hoc inspection of item classes where methods disagree;
- expanded searches for Bard or Langsford raw data;
- author correspondence about data reuse or missing repositories.

Exploratory results can motivate future work, but they should not replace the
primary result unless the paper is explicitly reframed.

## Revision Triggers

Revise this charter before analysis only if one of the following occurs:

- Bard participant-level rows are found;
- Langsford raw participant-response rows are found;
- Sprouse data reuse is denied or restricted in a way that prevents novel
  analysis;
- inspection of dataset documentation shows that the assumed method comparisons
  are not actually comparable;
- the paper changes genre from constrained secondary-data reassessment to
  historiography, literature synthesis, or a new human-judgment study.
