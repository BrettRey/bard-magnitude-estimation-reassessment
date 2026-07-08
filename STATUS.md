# Status

## 2026-06-23

Created lower-case project scaffold at:

`/Users/brettreynolds/Documents/LLM-CLI-projects/papers/bard-magnitude-estimation-reassessment`

Initial framing:

- Working title: *Was magnitude estimation necessary? A secondary-data reassessment of Bard, Robertson, and Sorace (1996)*.
- Project type: no-new-data archival and secondary-data reassessment.
- Conceptual target: Bard, Robertson, and Sorace (1996).
- Empirical base to verify: Sprouse, Schuetze, and Almeida (2013); Langsford et al. (2018); later acceptability datasets and benchmarks.
- Contemporary afterlife to verify: CoLA, BLiMP, Syntactic Acceptability Dataset, and related acceptability resources.

Infrastructure:

- Uses central house-style symlinks only.
- Uses central `references.bib` symlink only.
- No local house-style snapshot.
- No datasets downloaded into the repository. Verification copies of public Sprouse data were inspected under `/tmp/bard-data-check` only.
- Local BibTeX entries added only after source verification.
- Central LaTeX style linter with strict checks passes.
- XeLaTeX/Biber/XeLaTeX/XeLaTeX build passes; final log scan found no undefined citations, no overfull boxes, and no empty bibliography warnings.

Source verification progress:

- Verified Bard, Robertson, and Sorace (1996) article metadata and DOI.
- Verified the Bard claim target at the abstract/research-paper-abstract level: ME is presented as solving conventional scale problems and yielding robust fine distinctions. Do not strengthen this into a blanket Bard superiority claim without more source grounding.
- Verified Sprouse, Schuetze, and Almeida (2013) article metadata, core design facts, public data zip, and materials workbook on Jon Sprouse's current author site.
- Verified Sprouse and Almeida (2017) public method-comparison data zip and materials workbook on Jon Sprouse's current author site.
- Verified Langsford et al. (2018) article metadata, measures compared, and stimulus/corpus/model supplement. Raw participant-response rows were not found after Glossa, author-page, and OSF/PsyArXiv API checks.
- Verified CoLA publication and public dataset README, including split sizes and copyright/fair-use warning.
- Verified BLiMP publication, repository, license, task design, and erratum note.
- Verified Syntactic Acceptability Dataset publication and repository, including the grammaticality/acceptability distinction.
- Added local BibTeX entries for verified sources missing from the central bibliography: Bard 1996, Langsford 2018, CoLA dataset, and CoLA TACL paper.

Design update:

- Reframed the empirical design around a common-latent-signal null rather than a scrambled-data null, but made the latent/response-style/test-retest apparatus conditional on data that can actually support those estimands.
- Added Gelmanian estimands and forking-path constraints to `notes/project-brief.md` and `notes/assumptions-and-pressure-test.md`.
- Replaced the placeholder prose in `sections/03-secondary-data-design.tex` and `sections/04-scale-and-reliability.tex` with the measurement-null and reliability framing.
- Added the genre gate: current feasible paper is a constrained secondary reanalysis of Sprouse row-level data plus article-grounded synthesis of Langsford, not a full re-fit of all method-comparison evidence.
- Added `notes/analysis-charter.md` as the pre-analysis commitment device. It fixes dataset routing, primary comparisons, primary scoring rules, practical-advantage criteria, negative controls, forbidden claims, and revision triggers before any new row-level modelling or visualization.
- Opened the analysis charter in Roughdraft; the review completed with no CriticMarkup changes to resolve.
- Drafted `notes/sprouse-data-reuse-email.md`, a short request to Jon Sprouse about novel secondary reuse of the public 2013/2017 data files.
- Sent the reuse request to Jon Sprouse at `jon.sprouse@nyu.edu`.
- Added `notes/dataset-inventory.md`, a structural-only inventory of the public Sprouse verification copies. It records files, columns, row counts, key counts, crosswalk needs, and charter mapping without computing method rankings or outcome summaries.
- Added `data/README.md` documenting that raw data and derived outputs are not committed while reuse and analysis scope remain unsettled.
- Added `scripts/build_sprouse_crosswalks.py`, which imports Sprouse result CSVs with the documented `skip=5` rule, preserves original identifiers, and writes ignored structural outputs under `data/derived/sprouse/`.
- Ran the crosswalk script against `/tmp/bard-data-check`. It produced schema and crosswalk files locally under ignored `data/derived/sprouse/`.
- Scripted structural check: the 2013 FC-to-ME/LS pair crosswalk has 144 exact matches and all 150 pairs after explicit compact spacing-key matching; the six non-exact cases are `den Dikken`/`denDikken` and `de Vries`/`deVries` ID-spacing variants.
- Scripted structural check: the 2017 yes/no-only IDs are `B`, `G`, and `M`, each absent from the materials workbook and appearing as repeated early-order rows rather than linguistic item IDs.
- Fixed pre-analysis representation rules: `FC.signtest.csv` is the primary 2013 forced-choice representation; `FC.logistic.csv` is a named sensitivity representation.
- Fixed pre-analysis 2017 YN inclusion rule: exclude `B`, `G`, and `M` from item-level comparisons, leaving 786 yes/no items aligned with the ME/LS/FC item universe.
- Updated `scripts/build_sprouse_crosswalks.py` to write ignored machine-readable rules in `data/derived/sprouse/analysis_rules.csv` and `data/derived/sprouse/2017_yn_item_inclusion.csv`.
- Added `scripts/sprouse_analysis_gate.py`, the first outcome-analysis scaffold. It reads the generated machine-readable rules and structural crosswalks, writes ignored readiness manifests, and keeps outcome analysis gated while Sprouse reuse is pending.
- Ran `scripts/sprouse_analysis_gate.py` with `--reuse-status pending`. It passed the structural checks and failed only the intended `sprouse_reuse_status` gate.
- Updated the manuscript methods prose in `sections/03-secondary-data-design.tex` and `sections/04-scale-and-reliability.tex` to reflect the fixed 2013 forced-choice representation choice and 2017 yes/no exclusion rule.
- Replaced the placeholder abstract, opening problem section, and Bard-target section with source-gated framing prose.
- Added an evidence-routing table to `sections/03-secondary-data-design.tex` distinguishing Bard article evidence, Sprouse row-level comparison data, Langsford article-level reliability evidence, and benchmark afterlife evidence.
- Rebuilt `main.pdf`; the final log scan found no undefined citations, no overfull boxes, no underfull boxes, and only the existing template-level `fancyhdr`/`microtype` warnings.
- Replaced the remaining section placeholders in `sections/05-contemporary-afterlife.tex`, `sections/06-grammaticality-and-acceptability.tex`, and `sections/07-conclusion.tex`.
- Current manuscript now has prose in all substantive sections; the only remaining `TODO` is the final AI-use disclosure in acknowledgements.
- Rebuilt `main.pdf` again; the final log scan found no undefined citations, no overfull boxes, no underfull boxes, and only the existing template-level `fancyhdr`/`microtype` warnings.
- Reframed the grammar/acceptability discussion around grammar as a system of projectibility profiles: acceptability judgments are now treated as one evidential route into grammaticality rather than as the whole target.
- Updated `notes/project-brief.md` and `notes/assumptions-and-pressure-test.md` so the projectibility-profile theory is part of the project route and pressure-test surface.

Evaluation pass (post-draft):

- Read the full built manuscript and evaluated it as an artifact, not just the plans.
- Added a prior-art and marginal-contribution beat to `sections/01-problem.tex`: the methodology literature has already deflated ME's special status (Schütze 2016: 208, citing Weskott & Fanselow 2011 and Sprouse et al. 2013; plus Sprouse & Almeida 2017 on power and Langsford et al. 2018 on reliability), so the contribution is the construct-level reframing and prespecified estimand routing, not the bare verdict.
- Added `weskott2011` to `references-local.bib` with metadata from Schütze (2016) and a verification-pending comment; logged it in `notes/source-verification.md`.
- Reframed the abstract so the Sprouse analysis reads as prespecified and gated on reuse permission rather than already performed.
- Tightened `sections/04-scale-and-reliability.tex` so it inherits the unit-of-analysis charter from section 3 instead of restating the 2013/2017 representation rules.
- Added the Goodman (1955) citation at the first mention of projectibility in `sections/06-grammaticality-and-acceptability.tex`.
- Added a `% TODO` in `sections/02-bard-target.tex` to page-anchor the Bard characterization once the article PDF is in the literature folder (currently reconstructed; no primary page citation).
- Confirmed TESL framing is dropped by decision.
- Rebuilt `main.pdf` (7 pages); log scan shows no undefined citations; `weskott2011`, `Goodman1955`, `schutze2016`, and `sprouse2017` all resolve in the bibliography.

Review board + Bard ingestion (2026-06-23):

- Ran a six-reviewer simulated board (Sprouse, Sorace, Featherston, Navarro, Schütze, plus the mandatory projectibility reviewer). Unanimous Revise & Resubmit. Full reviews and synthesis in `reviews/review-board-2026-06-23.md`.
- Headline finding: five of six independently flagged the common-latent-signal null as begging the question / rigged against ME (it assumes one latent scalar; bounded scales may censor gradience, not just add noise). The convergent fix (method-specific response functions + a prespecified dimensionality test that can falsify unidimensionality) also makes §6 projectibility load-bearing and supplies a genuinely new estimand. This null re-specification is the main open task, not yet started.
- Obtained the full Bard (1996) article (Brett supplied the JSTOR scan); moved PDF + markdown + images into `literature/Bard-MagnitudeEstimationLinguistic-1996.*`. The markdown preserves journal page numbers.
- Rewrote §2 from the primary text, page-anchored: abstract four-part claim (p. 32), the scale-type diagnosis ("wrong kind of measurement scale," p. 32; fixed scales "predetermine the number of distinctions," p. 35), the open-ended ratio rationale (p. 41), and Bard's own hedges ("considerable empirical cost"; "the data currently do not decide between them," p. 65). Corrected the framing: Bard's claim is a specific resolution-over-fixed-scales argument, not the broad "privileged formal method" reception. Added p. 32 anchors to §4 and §7; resolved the §2 TODO.
- Verified Weskott & Fanselow (2011) via Crossref: *Language* 87(2), 249--273, DOI 10.1353/lan.2011.0041; `weskott2011` updated and `/push-bib`-ready.
- Build clean throughout (7 pages, no undefined citations); style check clean apart from a now-fixed `\citep`->`\parencite`.

Null re-specification (2026-06-23, the board's headline fix):

- Replaced the "common signal plus method noise" null with a response-function measurement model (ME = unbounded ratio link; bounded tasks = ordered-threshold/Thurstonian/binary links), so scale-boundary censoring registers as a resolution advantage instead of being absorbed as ME noise.
- Added a prespecified dimensionality gate (one-factor vs correlated-two-factor/bifactor; method-residual structure) run before any ME-specific term, with the decision rule in `notes/analysis-charter.md`. This is the falsifier for unidimensionality the reviewers demanded.
- Made resolution a first-class estimand and advantage criterion (distinct from reliability); fixed the Type S/M framing in §4 (property of estimating a named contrast at a given N, not of a format).
- Made §6 projectibility predict where the single-scalar model breaks (the same dimensionality gate), added Boyd's "for a purpose" clause; this unifies the theory and empirical halves and answers the "delete §6 and nothing changes" critique.
- Propagated to §3, §4, §6, §7, `notes/project-brief.md`, `notes/assumptions-and-pressure-test.md`, `notes/analysis-charter.md`. Build clean (8 pages, no undefined citations, no overfull boxes). Analysis remains gated on Sprouse permission; this is design/charter prose only.
- Did §5 afterlife channel split (portability via expert channel survived into CoLA/BLiMP; graded naive-participant measurement migrated only into crowdsourced SAD).
- Did §6 profile identity conditions (profile = structure of licensed inferences, not the average of channels; disagreement adjudicated by which inferences hold) and disambiguated the §3 "sources" vs §6 "channels" wording with a cross-reference.
- House-style: "data" now singular in main.tex and §3.
- Build clean (8 pages, no undefined cites/refs, no overfull boxes).
- Genre lane: Brett chose to HOLD the hybrid until Sprouse replies (permission pending, not denied). Revisit RR-Stage-1 vs theory-note when the reuse answer lands. Do not submit in hybrid state.
- B/G/M confirmation also blocked on Sprouse's reply. With genre held and B/G/M blocked, the paper is at a clean pause point: every review-board item is either resolved or waiting on Sprouse.

Shutdown resync (Codex, 2026-06-23 19:55 EDT):

- Confirmed the pre-shutdown source state was clean and aligned with `origin/main` at `680bea0`.
- No new manuscript or methodological decisions were made in the resync session.
- Current state remains a clean pause point: wait for Sprouse's data-reuse reply before novel outcome analysis, B/G/M confirmation, or a final genre-lane choice.

Sprouse permission and gate opening (2026-07-07):

- Brett received Jon Sprouse's reply approving use of the public Sprouse,
  Schuetze, and Almeida (2013) and Sprouse and Almeida (2017) data files for the
  limited secondary analysis of magnitude estimation's contribution to an
  item-level signal, after Sprouse checked with Diogo Almeida.
- Permission boundary logged: do not redistribute participant-level raw files;
  cite the original papers and data source clearly; reach back out if the
  project drifts away from the ME/item-level-signal question toward a topic
  closer to Sprouse or Almeida's current interests.
- Created and Roughdraft-reviewed
  `notes/sprouse-approved-analysis-plan.md`; review completed with no
  CriticMarkup changes to resolve.
- Refreshed the public Sprouse working copies under `/tmp/bard-data-check` from
  Jon Sprouse's author-site links. Raw files remain outside Git.
- Re-ran `scripts/build_sprouse_crosswalks.py` against the fresh downloads. The
  structural checks reproduced the previous state: 150 2013 condition pairs, all
  matched after compact spacing-key handling; 2017 yes/no-only IDs remain `B`,
  `G`, and `M`, leaving 786 aligned yes/no items.
- Re-ran `scripts/sprouse_analysis_gate.py --reuse-status approved`; all
  readiness gates passed.
- Added `analysis/sprouse_item_signal.py`, the first approved descriptive
  item/contrast signal script. It requires the approved readiness gate, reads
  the fresh `/tmp/bard-data-check` working copies, and writes only ignored
  derived outputs under `data/derived/sprouse_analysis/`.
- Ran `analysis/sprouse_item_signal.py --raw-root /tmp/bard-data-check`. It
  wrote `sprouse_item_method_aggregates.csv`, `sprouse_item_signal_matrix.csv`,
  `sprouse_pair_contrasts.csv`, `sprouse_signal_correlations.csv`,
  `sprouse_me_disagreements.csv`, and `sprouse_analysis_manifest.csv` under the
  ignored derived directory.
- First descriptive signal check: 2013 ME-Likert condition correlation is
  `r = .986` over 298 conditions; 2013 pair contrasts correlate `r = .963`
  between ME and Likert and `r = .763` between ME contrast and forced-choice
  expected agreement over 150 pairs.
- First descriptive signal check: 2017 item correlations are ME-Likert
  `r = .925`, ME-yes/no `r = .883`, and ME-forced-choice-selected-rate
  `r = .557` over 786 aligned items; 2017 pair contrasts are ME-Likert
  `r = .944`, ME-yes/no `r = .889`, and ME-forced-choice-selected-contrast
  `r = .715` over 50 pairs.
- Interpretation for next work: the item matrices are comparable enough to move
  to the chartered response-function/dimensionality models. Forced choice is
  aligned but visibly weaker than Likert and yes/no in this descriptive pass.
  These are staging outputs, not the final measurement model.
- Created and Roughdraft-reviewed
  `notes/dimensionality-gate-implementation-plan.md`; review completed with no
  CriticMarkup changes to resolve.
- Added `analysis/sprouse_dimensionality_gate.py`, a first-pass approximation
  to the chartered dimensionality gate. It requires the approved readiness
  manifest and the descriptive Sprouse outputs, then writes ignored diagnostics
  under `data/derived/sprouse_analysis/`.
- Ran the dimensionality-gate pipeline after the approved gate and descriptive
  item-signal script. Outputs written locally: `sprouse_dimensionality_gate_summary.csv`,
  `sprouse_dimensionality_eigenvalues.csv`, `sprouse_dimensionality_loadings.csv`,
  `sprouse_dimensionality_residuals.csv`, and `sprouse_dimensionality_manifest.csv`.
- First-pass gate result: all three analyzable matrices passed the
  `single_dimension_sufficient_first_pass` rule. The 2013 pair matrix has first
  eigenvalue `2.681` (89.4% variance), second eigenvalue `0.284`, parallel-analysis
  second-eigenvalue 95th percentile `1.051`, RMS residual `.076`, max residual
  `.101`. The 2017 item matrix has first eigenvalue `3.223` (80.6%), second
  eigenvalue `0.589`, parallel 95th percentile `1.051`, RMS residual `.088`,
  max residual `.131`. The 2017 pair matrix has first eigenvalue `3.435`
  (85.9%), second eigenvalue `0.407`, parallel 95th percentile `1.197`, RMS
  residual `.067`, max residual `.107`.
- Interpretation: this first-pass PCA/parallel-analysis gate does not reject a
  one-dimension measurement structure for the available aggregate Sprouse
  matrices. It is not the final response-function model. It does make a
  strong multidimensional rescue for magnitude estimation less likely in these
  aggregate outputs, while leaving response-function/scaling-specific analysis
  as the next modelling task.
- Created and Roughdraft-reviewed
  `notes/response-function-resolution-plan.md`; review completed with no
  CriticMarkup changes to resolve.
- Added `analysis/sprouse_response_function_resolution.py`, a targeted
  sensitivity diagnostic for Bard's resolution claim. It requires the approved
  readiness gate and the first descriptive Sprouse outputs, reads the local raw
  ME/LS files under `/tmp/bard-data-check`, and writes only ignored derived
  outputs under `data/derived/sprouse_analysis/`.
- Ran the response-function diagnostic. Outputs written locally:
  `sprouse_response_function_model_fits.csv`,
  `sprouse_response_function_bins.csv`,
  `sprouse_response_function_residuals.csv`, and
  `sprouse_response_function_manifest.csv`.
- Response-function result: raw bounded Likert means are better fit as a
  1--7 bounded-logistic response to ME aggregate z-scores than as a linear
  response. For 2013 condition means, bounded logistic improves from
  `R2 = .969` to `.977` with delta AIC `92.0` in its favour. For 2017 item
  means, bounded logistic improves from `R2 = .845` to `.853` with delta AIC
  `41.4` in its favour.
- Resolution diagnostic result: the endpoint bins do not show unusually large
  ME spread. In 2013, ME z-score SD is `.142` in the lower endpoint bin and
  `.175` in the upper endpoint bin, versus `.313` in the middle bin. In 2017,
  ME z-score SD is `.249` lower endpoint and `.321` upper endpoint, versus
  `.349` in the middle bin. Interpretation: the data support a bounded
  response-function shape, but do not yet show the practical endpoint
  resolution advantage Bard's strongest fixed-scale critique would predict.
- Created `notes/pair-level-resolution-robustness-plan.md` and attempted a
  Roughdraft checkpoint. Roughdraft opened the file but the CLI watch process
  exited with a fetch timeout rather than a normal Done Reviewing signal; no
  CriticMarkup comments were present when the file was read back from disk.
- Added `analysis/sprouse_pair_resolution_robustness.py`, a pair-level
  good-vs-bad contrast robustness check. It requires the approved readiness
  gate and the descriptive pair outputs, reads local raw ME/LS files only to
  build condition-level aggregates, and writes ignored diagnostics under
  `data/derived/sprouse_analysis/`.
- Ran the pair-level robustness diagnostic. Outputs written locally:
  `sprouse_pair_resolution_rows.csv`,
  `sprouse_pair_resolution_summary.csv`,
  `sprouse_pair_resolution_extremes.csv`, and
  `sprouse_pair_resolution_manifest.csv`.
- Pair-level result: bounded-method predictors explain most ME contrast
  variance: `R2 = .926` for 2013 pairs and `.901` for 2017 pairs. ME contrast
  correlates strongly with raw Likert contrast (`r = .962` in 2013 and `.946`
  in 2017) and with the bounded-method prediction (`r = .962` and `.949`).
  Top-quartile overlap is high: 33 of 38 2013 top-quartile ME pairs and 12 of
  13 2017 top-quartile ME pairs are also top-quartile by bounded prediction.
  No ME top-quartile pair falls into the bounded-model bottom half in either
  dataset. Interpretation: the pair-level check reinforces the conclusion that
  ME tracks the same practical contrast signal without a clear systematic
  ME-only resolution advantage in these Sprouse data.
- Integrated the Sprouse results into the manuscript. The abstract now reports
  the constrained secondary analysis and its result; Section 4 now includes
  Table `sprouse-diagnostics` summarising convergence, dimensionality,
  response-function, and pair-level robustness diagnostics; the conclusion now
  states the bounded-curvature/no-practical-ME-only-resolution distinction.
- Ran a house-style pass over the edited LaTeX. Paragraph-length warnings
  introduced or exposed by the edit were split in Sections 4 and 6. The project
  has only `.house-style/style-rules.yaml` symlinked, not a local
  `style-guide.md`; the style pass used the available YAML rules and the
  check-style skill checklist.
- Rebuilt `main.pdf` with XeLaTeX/Biber/XeLaTeX/XeLaTeX. The build succeeded
  at 9 pages. Final log scan found no undefined citations, no undefined
  references, no overfull boxes, and no underfull boxes. Remaining warnings are
  the existing template-level `fancyhdr` headheight/E-option warnings and the
  existing `microtype` footnote patch warning.
- Editorial display decision: keep Table `sprouse-diagnostics` for now rather
  than adding a compact figure. The table already states the convergence,
  dimensionality, response-function, and pair-robustness pattern; a figure would
  mostly repeat the same result at a page cost.
- Langsford final raw-data check (2026-07-07): rechecked the Glossa article
  page/PDF/XML, supplementary file `gjgl-3-396-s1.pdf`, Danielle Navarro's
  publication page, and OSF/PsyArXiv routes for `vrfxn`. No public raw
  participant-response rows or analysis code were found. The supplement remains
  corpus and Thurstonian-model documentation only, so Langsford stays
  article-level evidence in this paper.
- Focused review pass completed after the post-ship checkpoint. The abstract,
  Section 4, conclusion, and data/code availability language now make the
  Sprouse result more explicitly scoped: no systematic practical ME resolution
  advantage in these data, and the dimensionality result is a first-pass
  aggregate diagnostic rather than a full participant-level factor model.
- Added the final AI-use disclosure in the acknowledgements, naming OpenAI Codex
  (GPT-5) and Claude Opus for the recorded project uses. The manuscript no
  longer has a TODO marker.
- Rebuilt `main.pdf` after the review edits. The build remains 9 pages. Final
  scans found no TODO/FIXME markers, no undefined citations or references, no
  overfull boxes, and no underfull boxes. Remaining warnings are the existing
  template-level `fancyhdr` headheight/E-option warnings and the existing
  `microtype` footnote patch warning.
- Ran a six-role independent Codex/GPT review board and saved the report at
  `reviews/review-board-20260707-194612.md`. Verdict was unanimous Revise &
  Resubmit, with no rejects. Consensus strengths: fair Bard target, disciplined
  evidential routing, fair response-function null, useful data/AI disclosures,
  and a non-decorative projectibility section. Consensus next-round revisions:
  add empirical diagnostic detail and operational thresholds, keep
  dimensionality language soft, add stronger reproducibility/provenance detail,
  expand benchmark construction detail, and cash out the projectibility payoff
  earlier and in the conclusion.
- Applied two low-risk board-driven patches before shipping: replaced
  "prespecified" manuscript wording with analysis-charter wording and named Jon
  Sprouse/Diogo Almeida in the reuse-permission disclosure; softened the SAD
  afterlife sentence to avoid implying a direct historical migration from Bard.
- Added a local reproduction recipe to `analysis/README.md`, including the
  expected `/tmp/bard-data-check` layout and the analysis command sequence. Raw
  participant-level data remains uncommitted and non-redistributed.
- Created and Roughdraft-reviewed `notes/gelman-satisfaction-plan.md`; review
  completed with no CriticMarkup changes to resolve.
- Applied the Gelman-style hardening pass to the manuscript. Section 4 now
  defines a practical ME advantage as an inferential-decision change rather
  than a summary-statistic improvement alone; the conclusion states the ME-only
  patterns that would change the interpretation; the aggregate diagnostics are
  explicitly weaker than posterior certainty statements or formal equivalence
  tests; implemented dimensionality language is consistently softened from
  "gate" to "check" where appropriate.
- Split and tightened the data/code availability note: it now records Sprouse's
  permission boundary, the non-redistribution of participant-level rows and
  derived participant-level tables, the local reproduction recipe, and the
  Git-versioned internal charter as an internal analysis record rather than an
  external registry entry.
- Rebuilt `main.pdf` after the Gelman pass. The manuscript is now 10 pages.
  House-style scans found no flagged prose patterns in `main.tex` or
  `sections/*.tex`, apart from table-environment false positives in the
  paragraph-length helper. `git diff --check`, `make`, and
  `python3 -m py_compile scripts/*.py analysis/*.py` all passed. Final log scan
  found no undefined citations, no undefined references, no overfull boxes, and
  no underfull boxes. Remaining warnings are the existing template-level
  `fancyhdr` warnings and the existing `microtype` footnote patch warning.
- Proportional completion pass (2026-07-08): added Table
  `benchmark-afterlife` to Section 5, comparing CoLA, BLiMP, and SAD by item
  source, label channel, and evaluation target. This addresses benchmark
  construction accuracy without expanding the paper into a benchmark survey.
- Added a conclusion sentence cashing out the projectibility payoff supported
  by the Sprouse reanalysis: formal judgments project stable item-level contrast
  ordering across ordinary elicitation formats in the available data, while
  magnitude estimation alone does not project an additional practical ordering
  for the tested contrasts.
- Added aggregate counts to Table `sprouse-diagnostics`: 2013 condition means
  `n=298`, 2013 pairs `n=150`, 2017 aligned items `n=786`, and 2017 pairs
  `n=50`. This makes the compact empirical display more auditable without
  adding a methods appendix.
- Created and Roughdraft-reviewed `notes/roadmap-review-board-20260708.md`,
  which summarizes the June and July review-board assessments, current quality
  gates, and the staged roadmap from shipping through possible preprint or
  submission preparation. Review completed with no CriticMarkup changes to
  resolve.
- Rebuilt `main.pdf` after the Section 5/conclusion pass. The manuscript remains
  10 pages. Style scans and `git diff --check` passed; final log scan found no
  undefined citations, no undefined references, no overfull boxes, and no
  underfull boxes. Remaining warnings are the existing template-level
  `fancyhdr` warnings and the existing `microtype` footnote patch warning.
- Shipped Stage 1 of the roadmap as commit `c4eb798`:
  `Record roadmap and proportional completion pass`.
- Applied Stage 2 reader-facing tightening: the abstract now names "no
  systematic practical ME-only resolution advantage in the tested Sprouse
  contrasts"; Section 1 now states the paper's routing/projectibility payoff by
  the end of the problem section; "signal", "dimension", and "acceptability"
  language in Sections 4, 6, and 7 is scoped more clearly to aggregate Sprouse
  evidence and task-conditioned acceptability.
- Applied Stage 3 minimal auditability: Section 4 now says Table
  `sprouse-diagnostics` comes from the approved pipeline documented in
  `analysis/README.md` and clarifies that reported `n` values are aggregate
  condition, item, or pair units rather than participant-level rows.

Next steps:

1. Move project-specific BibTeX entries to the central bibliography later if
   they become reusable outside this project.
2. Next manuscript revision: address the review-board R&R items, especially
   operational practical-advantage thresholds and reproducibility/provenance
   detail.

## Literature Hooks

### 2026-06-23 - Cai et al. 2026 Nature

- Central note: `../../literature/cai_etal_2026_neuronal_language_models.notes.md`.
- Use only as a guardrail if the paper discusses the contemporary afterlife of acceptability as a benchmark or neural target. Neural encoding of parser-derived features during speech production does not settle acceptability, grammaticality, or the measurement status of magnitude estimation.
