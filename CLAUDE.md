# CLAUDE.md

This file provides project-specific guidance for Brett Reynolds's paper:

**Was magnitude estimation necessary? A secondary-data reassessment of Bard, Robertson, and Sorace (1996)**

## Project Role

This is a no-new-data reassessment project. The contribution is not a direct
replication of Bard et al. unless the original participant-level data is found.
The contribution is to test the methodological claims through later datasets
and to ask what survived: formal acceptability measurement, magnitude
estimation as a tool, or a broader construct of acceptability.

## Local Questions

1. Which claim is being tested: scale resolution, reliability, decision
   convergence, or construct validity?
2. What is the evidence type: original published numbers, later participant
   responses, expert labels, or benchmark metadata?
3. Does a dataset measure acceptability, grammaticality, naturalness,
   standardness, correction behaviour, or a mixture?
4. Are Bard et al. being used as a target of reassessment rather than a straw
   target?
5. Does the paper need new human judgments to answer the TESL-facing questions?

## Build System

Use XeLaTeX, not pdfLaTeX or LuaLaTeX.

```bash
make
make quick
make clean
```

Manual full build:

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

## File Structure

```text
bard-magnitude-estimation-reassessment/
|-- main.tex
|-- sections/
|-- notes/
|-- data/
|-- analysis/
|-- submission/
|-- STATUS.md
|-- DECISIONS.md
|-- README.md
|-- references.bib          # symlink to ../../.house-style/references.bib
|-- references-local.bib    # verified project-specific additions only
`-- .house-style/           # symlinks to central house-style files
```

## House Style

This project uses Brett's central house style strictly by symlink. Do not copy
local house-style files into the project.

## Citation and Data Discipline

- Use the central bibliography when the key already exists.
- Add to `references-local.bib` only after source verification.
- Keep candidate sources in `notes/source-verification.md` until verified.
- Do not download, transform, or summarize datasets before reading the dataset
  documentation.
- Keep participant response data, expert labels, benchmark labels, and
  theoretical grammaticality at separate explanatory levels unless the bridge
  is argued.

## Current State

Read `STATUS.md`, `DECISIONS.md`, `notes/project-brief.md`, and
`notes/source-verification.md` at the start of a session. Log durable decisions
to `DECISIONS.md` as they happen.
