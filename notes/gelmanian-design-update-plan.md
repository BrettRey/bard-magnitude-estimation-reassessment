# Gelmanian Design Update Plan

## Core change

Reframe the empirical design around a measurement null rather than around a simple pro/anti magnitude-estimation contrast.

Revision after the data gate: this is a conditional analysis plan, not yet the
paper's promised empirical design. Sprouse 2013 and Sprouse and Almeida 2017
provide public row-level method-comparison data; Langsford 2018 does not
currently provide public raw rows. The full latent/response-style/test-retest
model should be described only as available if the necessary rows exist.

## Proposed null

Magnitude estimation has no practical measurement advantage once item acceptability, task noise, scoring choices, and any estimable participant or item-by-method terms are accounted for.

In other words, magnitude estimation, Likert ratings, forced choice, and Thurstonian choice are treated first as noisy observations of a common latent item-level acceptability signal where shared or comparable item data exist. The burden is on a magnitude-estimation-specific term to improve prediction, reliability, decision stability, or construct interpretation enough to matter.

## Estimands

1. Item-level acceptability signal recoverable across methods.
2. Method-specific noise or bias, especially for magnitude estimation.
3. Participant-level response-style variation, only in datasets with participant-level rows and enough repeated structure.
4. Decision agreement for theoretically relevant contrasts.
5. Method-by-item instability: cases where the method changes the linguistic conclusion.

## Negative controls

Scrambled data should not be the main null. Use it as a pipeline check:

- shuffle acceptability labels within constrained item sets;
- permute method labels where paired designs make that legitimate;
- simulate data from a no-method-advantage latent model and verify that the planned analysis does not routinely crown magnitude estimation.

## Forking-path constraints

Before modelling reusable data, fix:

- which datasets can answer which estimands;
- which methods count as the primary comparison set;
- which transformations are primary versus sensitivity checks;
- which result would count as practical measurement advantage;
- which construct claims are forbidden without participant-response data.

## Manuscript edits

1. Update `notes/project-brief.md` so the thesis names the common-latent-model null explicitly.
2. Update `notes/assumptions-and-pressure-test.md` with the Gelmanian null, estimands, negative controls, and falsification conditions.
3. Update `sections/03-secondary-data-design.tex` to say that the secondary-data design routes sources to estimands before modelling.
4. Update `sections/04-scale-and-reliability.tex` to frame the scale/reliability section around practical measurement advantage over the common-latent null.

## Stop conditions

- If no dataset supports method-level comparison on the same or comparable items, the paper should not claim to assess magnitude estimation's practical advantage.
- If raw rows are unavailable, do not fit participant response-style terms, test-retest terms, or method-by-item instability terms from published convergence rates.
- If analyses are chosen after seeing which method looks best, the paper has recreated a garden-of-forking-paths problem.
- If scrambled or permuted controls recover strong method advantages, the analysis pipeline is not trustworthy enough for the paper's main claim.
