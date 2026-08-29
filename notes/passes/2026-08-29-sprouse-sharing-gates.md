# Sprouse colleague-sharing gate audit

Date: 2026-08-29
Artifact reviewed: `main.tex` and its seven included sections
Final manuscript fingerprint: `structure 44b7cfa31a00ad0f`; `prose
5e41e236db3e159a`; `numbers 31e5f9c5b63cde71`
Release decision: **green for colleague sharing; not represented as a
submission-ready package**

## Scope

This gate covers the checks most likely to matter before sending the paper to
Jon Sprouse: contribution alignment, charitable engagement, negative claims,
numbers, quotations, reader-facing clarity, terminology, explanatory levels,
projectibility, proofreading, bibliography integrity, house style, build
integrity, and PDF rendering. It deliberately omits venue formatting,
anonymization, a new external review board, and the rest of the publication
package.

## Contribution alignment

The title names the paper's actual contribution: a secondary-data reassessment
of Bard et al.'s case for magnitude estimation. The abstract reports both the
analysis-chartered primary result and the post-outcome multiverse, including the
localized 2017 qualification. The introduction identifies the problem as the
separation of formal graded measurement from a practical advantage specific to
ME. The conclusion returns to exactly that distinction and states what evidence
would change the result. The section sequence moves from target, through design
and evidence, to construct consequences and conclusion; it isn't merely a list
of topics. No promise in the abstract or introduction is left unfulfilled.

Verdict: **green**.

## Charitable engagement

| Target | Strongest version and agreement | What the paper takes from it | Criticism after the grant | Verdict |
| --- | --- | --- | --- | --- |
| Bard, Robertson, and Sorace (1996) | ME is presented as an open ratio-yielding response that can recover distinctions fixed scales censor, not as an all-purpose gold standard. | The paper credits Bard et al. with making graded acceptability measurable and methodologically serious. | Later data don't show a robust practical ME-only ordering in the sampled contrasts. | Green |
| Sprouse et al. (2013) | The original study assessed convergence between informal and formal judgments. | It supplies shared-item method-comparison rows. | The endpoint-resolution analysis is explicitly labelled a secondary use, not the original estimand. | Green |
| Sprouse and Almeida (2017) | The original study compared task sensitivity and statistical power. | It supplies an independent method-comparison dataset and decision channels. | The paper reports the localized rank/forced-choice ME increment instead of suppressing it. | Green |
| Langsford et al. (2018) | The article contributes reliability, bias, and variability evidence across methods. | It keeps reliability distinct from resolution. | The paper limits new modelling because verified public materials available to the project lack raw response rows. | Green |

The critical verbs have been cooled where necessary. The paper now distinguishes
the targets' original purposes from its own and doesn't attribute a broad ME
superiority claim to Bard et al.

## Negative claims

| Claim | Outcome | Basis |
| --- | --- | --- |
| Bard participant rows aren't available | Narrowed to “aren't available to this project”; no field-wide non-existence claim. | Project source inventory and local holdings search. |
| Public Langsford materials lack raw participant responses | Narrowed to verified public materials available to this project. | Glossa article/supplement, author page, PsyArXiv/OSF routes, and project source-verification record. |
| Rows for a full Bard--Sprouse--Langsford dimensionality model aren't available | Narrowed to availability to this project and tied to the named evidence base. | Same inventory. |

The manuscript makes no “first”, “novel”, “no one has”, or literature-wide
absence claim. Verdict: **green**.

## Numbers audit

An independent read-only Codex GPT-5-family subagent audited the final text
against the aggregate CSV outputs.

- Primary result tables were independently reproduced from fresh public inputs;
  every selected derived CSV matched the retained output byte for byte.
- Manual comparison confirms the sample sizes, correlations, component shares,
  endpoint SDs, pair-model values, and bootstrap intervals in Table 2 and its
  surrounding prose.
- Manual comparison confirms the 162-specification total, the 27/36 family
  denominators, endpoint-support counts, four localized 2017 prediction results,
  `.025`--`.049` delta range, and 3/150 and 1/50 sign-discordance counts.
- The independent audit found zero mismatches and zero unsourced substantive
  numerical claims. It separately verified all eight bootstrap endpoints, all
  four convergence estimates and sample sizes, the three component shares,
  endpoint SDs, pair-model values, all multiverse family counts, the localized
  2017 model type and target, the B/G/M exclusions, and the benchmark counts.
- One source difference isn't manuscript drift: the public 2013 ME/LS files
  yield 298 aggregate condition IDs, whereas the published article describes
  296 data points. The manuscript correctly labels 298 as pipeline aggregate
  conditions and doesn't present it as the article's participant or design
  count.

Independent verdict: **green (zero mismatches)**.

## Quotation audit

The quote checker couldn't associate `BardEtAl1996` with the differently named
local source file, so each quotation was checked manually against
`../../../literature/Bard-MagnitudeEstimationLinguistic-1996.md` and the source
page markers/PDF.

| Page | Quoted material | Verdict |
| --- | --- | --- |
| 32 | Four abstract claims: solving scale problems, fine distinctions, naive-speaker use, replication | Exact |
| 32 | “the use of the wrong kind of measurement scale” | Exact |
| 35 | Fixed scales “predetermine[] the number of distinctions subjects may use” | Exact; manuscript inflection matches source wording |
| 41 | No restriction on number of values; complete freedom over numbers | Exact |
| 65 | “considerable empirical cost”; data don't decide between models | Exact |

All sourced quotations carry resolved page citations. Verdict: **green**.

## Reader, terminology, and explanatory level

The manuscript was read in order in source and as extracted from the final PDF.
The unavailable registered `reader-pass` skill was replaced, as disclosed, by
the manuscript-clarity procedure. The main reader-facing repairs were to state
Sprouse's original aims, define the multiverse's timing and decision rule,
surface the localized 2017 result, and clarify the profile/channel distinction.

The paper's local contrasts remain stable:

- graded/formal acceptability measurement vs an advantage specific to ME;
- resolution vs convergence and reliability;
- source type vs observation channel;
- observation channel vs projectibility profile;
- aggregate task-format evidence vs participant-level or cross-channel claims;
- analysis-chartered primary work vs post-outcome multiverse robustness.

The behavioural response level, aggregate analytical level, benchmark-
construction level, and grammatical-inference level are now marked rather than
slid between. No causal mechanism, latent truth scale, or participant-level
factor structure is inferred from the aggregate matrices. Verdict: **green**.

## Projectibility audit

| Check | Finding | Verdict |
| --- | --- | --- |
| Projection target | Observing relative ordering under one sampled formal task warrants expecting similar aggregate ordering under another. | Green |
| Non-triviality | The target is cross-task ordering, not the tautology that a score predicts itself. | Green |
| Purpose | The purpose is method comparison for linguistic contrasts; purpose selects the inference but doesn't make it true. | Green |
| Warrant | Cross-method convergence, pair robustness, aggregate bootstrap intervals, and the multiverse provide the warrant. | Green |
| World-side commitment | The paper claims limited stability of aggregate contrast ordering in these materials. | Green |
| Mechanism separation | No stabilizer, controller, causal-order, or homeostatic claim is made. | Green |
| Level discipline | Task responses, expert labels, benchmark labels, and profiles are distinguished. | Green |
| Scope | The result is limited to the sampled Sprouse contrasts and task formats. | Green |
| Revision condition | Clear endpoint spread, bounded-method misses, stable ME residual structure, or lower sign/exaggeration risk would change the conclusion. | Green |
| Positioning | Projectibility is load-bearing but not used to relabel a merely stable pattern as a natural kind. | Green |

Strongest world-side commitment: the sampled contrasts preserve a similar
aggregate ordering across ordinary formal elicitation formats. The paper makes
no stronger causal or homeostatic commitment.

## Unearned-therefore check

| True premise | Unearned therefore | Hidden bridge premise | Better reading now in the manuscript |
| --- | --- | --- | --- |
| Four 2017 rank-scale forced-choice specifications show a positive ME increment. | Therefore ME supplies a general extra information channel, or the result conclusively refutes every no-information hypothesis. | A positive cross-validated increment in this specification cluster is a stable, target-general property rather than a local modelling result. | A blanket no-information claim is too strong for those specifications; the result doesn't establish a systematic practical advantage. |

The overreach was evidential, and the revised sentence keeps the exception local.

## Proofread, bibliography, and house style

- No unresolved TODO, FIXME, placeholder, `??`, missing citation, or missing
  reference appears in the manuscript or extracted PDF.
- The house-style checker passes on `main.tex` and every included section.
- The terminology checker reports zero flags; `projectibility` and `profile` are
  glossed at first use.
- Parenthetical citations use `\citep`; no `\parencite` remains. Keywords and
  PDF keywords match, and `\clearpage` precedes the bibliography.
- Fourteen unique citation keys are used. All resolve once in the central
  bibliography; there are no duplicate cited keys or unused local entries.
  `references.bib` is the expected symlink to the central bibliography, and
  Biber reports all 14 keys without warnings.

Verdict: **green**.

## Build and render integrity

- The manuscript fingerprint resolves all nine TeX files and all 14 citation
  keys.
- No TeX Live path is hard-coded.
- A forced full XeLaTeX/Biber/XeLaTeX/XeLaTeX build succeeds.
- The final log has no missing files, unresolved citations/references,
  overfull/underfull boxes, or package errors. Remaining warnings come from the
  central template's unused two-sided `fancyhdr` options and the harmless
  `microtype` footnote patch.
- `git diff --check` passes.
- The final PDF is 13 letter-size pages; all fonts are embedded.
- Two aggregate-data figures now visualize the shared signal/bounded response
  and the full endpoint, prediction, and decision multiverse. Their vector PDFs
  and PNG previews reproduce byte for byte from the checked aggregate outputs.
- Every page was rendered at 144 dpi and inspected. Tables are readable and are
  held at their source positions; no clipping, overlap, broken glyph, or orphaned
  heading was found.

Verdict: **green**.

## Overall judgment

The paper is ready to share with Jon Sprouse as a strong working-paper draft.
The multiverse was worth adding: it materially improves robustness and
transparency without changing the thesis. The draft should not be described as
fully submission-gated, preregistered, or participant-level modelling.
