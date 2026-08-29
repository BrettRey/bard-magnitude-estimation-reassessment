# Project agent guidance
<!-- SUMMARY: Agent guidance for Was magnitude estimation necessary? A secondary-data reassessment of Bard, Robertson, and Sorace (1996); deliberately short and routed to portfolio rules · status: active · updated: 2026-08-29 -->

Guidance for Claude Code, Codex, and other agents working in this repository.

## Project

Academic paper: **Was magnitude estimation necessary? A secondary-data
reassessment of Bard, Robertson, and Sorace (1996)**, by Brett Reynolds.

This is a no-new-data conceptual replication and secondary-data reassessment.
The analysis tests Bard et al.'s resolution claim using later method-comparison
data; it is not a direct replication of Bard et al.

## This file is deliberately short

House style, writing style, terminology, citation practice, dispatch
invocations, and submission process live in the portfolio rules. They are not
copied here.

| What you need | Where it actually lives |
|---|---|
| LaTeX house style: terms, mentions, dashes, citations | `../../../.claude/rules/latex-house-style.md` |
| Writing style, AI tics, paragraph discipline | `../../../.claude/rules/writing-style.md` |
| CGEL terminology | `../../../.claude/rules/cgel-conventions.md` |
| Source grounding | `../../../.claude/rules/source-grounding.md` |
| Bibliography workflow | `../../../.claude/rules/bibliography-workflow.md` |
| Multi-model dispatch | `../../../.claude/rules/multi-model-dispatch.md` |
| Portfolio-wide commitments | `../../../canon/` |
| Values behind the rules | `../../../constitution.md` |

Read `STATUS.md`, `DECISIONS.md`, `notes/project-brief.md`, and
`notes/source-verification.md` for project-specific state and research
constraints.

## Build

Use XeLaTeX. Avoid LuaLaTeX because it breaks the PDF text layer.

```bash
make          # bard-magnitude-estimation-reassessment.pdf
make quick    # single XeLaTeX pass
make blind    # bard-magnitude-estimation-reassessment-blind.pdf
make figures  # regenerate manuscript figures
make test     # analysis tests and Python compilation checks
make clean    # remove auxiliary files but keep PDFs
```

The canonical manuscript root is
`bard-magnitude-estimation-reassessment.tex`. Never hardcode a TeX Live path
in `\\setmainfont`.

## Layout

```text
bard-magnitude-estimation-reassessment/
├── bard-magnitude-estimation-reassessment.tex
├── sections/
├── figures/
├── analysis/
├── data/
├── references.bib
├── references-local.bib
├── .house-style/             # symlinks to the central house style
├── Makefile
├── STATUS.md
├── DECISIONS.md
└── submission/
```

This project uses the central house style strictly by symlink. Do not copy a
local snapshot into the project.

## Gates before anything goes out

Before a formal submission, create and verify:

1. `submission/venue-decision-YYYY-MM-DD.md`
2. `submission/pre-submission-checklist-YYYY-MM-DD.md`
3. `submission/paper-assurance-YYYY-MM-DD.md`

A colleague-sharing draft does not claim that every venue-specific publication
gate has run.

## Canon

This pre-existing paper has no `.canon-stamp`. Do not create one by hand or
claim reconciliation without running the canon workflow. To inspect drift:

```bash
python3 ../../../Project-Management/tools/canon_drift.py \
  --project papers/development/bard-magnitude-estimation-reassessment
```

## Log decisions as you go

Record non-trivial structural, methodological, terminological, or framing
decisions in `DECISIONS.md` when they are made. If a decision binds more than
this paper, it belongs in the portfolio canon.
