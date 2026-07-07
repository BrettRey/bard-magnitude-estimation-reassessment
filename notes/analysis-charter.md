# Analysis Charter

Status: active analysis charter after Roughdraft review. This charter froze the
primary analysis choices before any new row-level modelling or visualization of
the Sprouse data. Later deviations are allowed, but they must be labelled
exploratory in the paper and in the analysis notes.

Permission update (2026-07-07): Jon Sprouse approved Brett's limited secondary
use of the public 2013 and 2017 data files after checking with Diogo Almeida.
This opens the outcome-analysis gate within the approved methodological scope;
it does not change the estimands or representation choices fixed below.

## Purpose

The paper asks whether magnitude estimation has a practical measurement
advantage over other formal acceptability-judgment methods, given a
source-grounded reading of Bard, Robertson, and Sorace (1996). The target is not
"Bard were wrong." The target is narrower: Bard's documented claim that
magnitude estimation solves conventional scale problems and yields robust
fine-grained acceptability data, plus the stronger later reading that magnitude
estimation has a privileged methodological status.

The analysis should therefore compare magnitude estimation against a serious
measurement null: formal methods observe a common item-level acceptability
signal through method-specific response functions, not merely the same signal
plus method noise. Bounded methods (Likert, forced choice, yes/no) can censor or
compress the signal at the extremes; magnitude estimation's open ratio scale
need not. The null is that one latent dimension, read through those response
functions, suffices. Magnitude estimation has to earn any method-specific term,
and the single-dimension assumption itself has to survive a falsification test
before any such term is adjudicated.

This is a deliberate correction. A plain "common signal plus method noise" null
cannot represent the specific advantage Bard et al. actually claimed, namely
that an open ratio scale recovers gradient distinctions that fixed-point scales
lose by construction (a resolution / scale-boundary claim, pp. 32, 35, 41). Under
that simpler null, any resolution that magnitude estimation recovers but bounded
scales compress is booked as magnitude-estimation noise, so the method can only
lose. The response-function and dimensionality machinery below is what keeps the
null from being rigged against the claim under test.

## Dataset Routing

### Included for row-level analysis

- Sprouse, Schuetze, and Almeida (2013): primary row-level analysis base.
  - Methods: magnitude estimation, 7-point Likert scale, forced choice.
  - Role: main test of method-specific practical advantage on a later
    acceptability-judgment dataset.
  - Constraint: reuse approved for the limited secondary methodological
    analysis. Do not redistribute participant-level raw files; reach back out
    if the project drifts from the approved scope.
- Sprouse and Almeida (2017): secondary row-level analysis base.
  - Methods: magnitude estimation, Likert scale, forced choice, yes/no.
  - Role: generalization and design-sensitivity check, not the main historical
    test of Bard's claim.
  - Constraint: same approved reuse boundary as the 2013 data.

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

0. Measurement structure (estimated first, see the gate below): whether one
   latent acceptability dimension, read through method-specific response
   functions, suffices, or whether methods load on distinct dimensions. This is
   prior to every estimand that follows; if it fails, the single-signal
   comparison is the wrong question, not just a question with a different answer.
1. Common item-level acceptability signal: the degree to which methods recover
   the same item or contrast ordering.
2. Method-specific noise or bias: the residual method contribution after
   accounting for item or contrast signal and the response function.
3. Resolution: whether magnitude estimation recovers graded item differences
   that bounded methods compress at ceiling or floor. This is Bard's actual
   claim and is not reducible to noise or bias.
4. Decision agreement: whether methods lead to the same theoretically relevant
   acceptability conclusions for contrasts.
5. Method-by-item instability: cases where method choice changes the linguistic
   conclusion. Estimate this only in row-level datasets with comparable items.

Participant response-style and test-retest estimands are not primary for this
paper unless a dataset provides the required repeated participant-level
structure. Do not infer them from published convergence rates or article-level
summaries.

## Measurement-Model Specification

The generative model is a latent item-level acceptability value for each item,
observed through a method-specific response function rather than as the same
value plus noise:

- magnitude estimation: an unbounded ratio / log-linear response (Bard et al.
  themselves work on the log of estimates);
- Likert: an ordered-threshold (ordinal) response with bounded support, which
  can compress differences near the top and bottom of the scale;
- forced choice: a binary comparison (Thurstonian) response over pairs;
- yes/no: a binary threshold response;
- Thurstonian choice: a latent-difference response.

Each method also carries a method-specific noise or bias term. The point of the
response functions is that censoring and compression at scale boundaries are
represented in the model, not absorbed into magnitude-estimation noise. A
resolution advantage for magnitude estimation can then appear as recovery of
item differences that the bounded response functions cannot express.

### Dimensionality gate (run first, before any method-specific term)

Before adjudicating whether magnitude estimation earns a method-specific term,
test the single-latent assumption itself on the cross-method item matrix:

1. Compare a one-factor model against a correlated-two-factor and a bifactor
   model (a general acceptability factor plus method or scale-type factors).
2. Inspect whether method-pair residuals carry reliable item-level structure
   beyond what one factor predicts.

Decision rule, fixed in advance:

- If one factor suffices (the multidimensional models do not improve fit by the
  prespecified criterion and residuals are unstructured), proceed to adjudicate
  any magnitude-estimation term under the single-signal null.
- If a multidimensional model fits better, or method residuals carry reliable
  item structure, the single-latent null is rejected as the wrong measurement
  model. The question then becomes which methods load on which dimensions and
  where they diverge. Magnitude estimation is not penalized as noise for
  carrying a real second dimension, and a divergence consistent with bounded-
  scale censoring counts toward, not against, the resolution claim.

This gate is the falsifier for unidimensionality. Without it, "magnitude
estimation must earn its term" presupposes the one-signal model and the method
can only lose; with it, the model that the comparison assumes is itself at risk.

The projectibility account in the manuscript predicts where this gate should
break: items where acceptability diverges from correction, register fit, or
cross-speaker stability are where a single acceptability scalar is most likely to
be insufficient. That prediction is the empirical work the projectibility framing
does here, not decoration.

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
one of the following over the response-function measurement null by enough to
change the paper's substantive conclusion:

- resolution: recovery of graded item differences that bounded methods censor or
  compress at the extremes (Bard's actual claim, pp. 32, 35, 41), or a second
  measurement dimension surviving the dimensionality gate;
- out-of-sample prediction of item or contrast acceptability;
- decision stability for theoretically relevant contrasts;
- convergence with independently published judgments;
- interpretable reduction in method-specific noise or bias.

Keep these distinct: reliability (test-retest consistency), validity
(measuring acceptability rather than an artefact), resolution (sensitivity to
fine gradience), and freedom from scale-boundary censoring are different
properties. Langsford et al. report magnitude estimation as less reliable; that
does not settle resolution, which is the dimension Bard's claim lives on.

A small numerical improvement that leaves the same linguistic conclusions in
place is not a practical advantage. A method-specific advantage that appears
only under one transformation or exclusion rule is a sensitivity result, not the
main result.

## Negative Controls

Use negative controls to detect pipeline artefacts, not as the substantive null:

- shuffle acceptability labels within constrained item sets;
- permute method labels only where the design makes the permutation meaningful;
- simulate no-method-advantage data from the response-function generative model
  (one latent dimension, method-specific links) and confirm that the analysis
  does not routinely select magnitude estimation as superior;
- simulate two-dimensional data with bounded-scale censoring and confirm that the
  dimensionality gate recovers the second dimension rather than missing it. A
  gate that cannot detect known censoring on simulated data is not trustworthy
  enough to clear magnitude estimation on real data.

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
