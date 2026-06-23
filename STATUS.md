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

Next steps:

1. Wait for Sprouse's reply before treating novel secondary results as publication-ready.
2. If reuse is approved or the analysis is explicitly verification-only, add the first substantive analysis script after the gate reads as open.
3. Search one more time for Langsford raw data only if the paper needs participant-level test-retest/response-style modelling; otherwise treat Langsford as article-level evidence.
4. Move project-specific BibTeX entries to the central bibliography later if they become reusable outside this project.

## Literature Hooks

### 2026-06-23 - Cai et al. 2026 Nature

- Central note: `../../literature/cai_etal_2026_neuronal_language_models.notes.md`.
- Use only as a guardrail if the paper discusses the contemporary afterlife of acceptability as a benchmark or neural target. Neural encoding of parser-derived features during speech production does not settle acceptability, grammaticality, or the measurement status of magnitude estimation.
