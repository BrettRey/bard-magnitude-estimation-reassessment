# Bard Magnitude Estimation Reassessment

Working title:

*Was magnitude estimation necessary? A secondary-data reassessment of Bard, Robertson, and Sorace (1996)*

## Aim

Set up a no-new-data methods-and-theory paper around Bard, Robertson, and
Sorace's 1996 magnitude-estimation article. The project treats Bard et al. as
the conceptual target, later method-comparison datasets as the empirical base,
and contemporary acceptability resources as the afterlife of the construct.

The paper should not claim to be a direct replication unless the original
participant-level data can be located. Its stronger form is an archival and
secondary-data reassessment of what survived: the measurement program for
acceptability, the documented ME scale-resolution claim, and the later stronger
reading of ME as a privileged measurement tool.

## Build

```bash
make
```

Manual build:

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

## Structure

- `main.tex` orchestrates the paper.
- `sections/` holds section-level source files.
- `notes/source-verification.md` tracks sources and datasets to verify before citation.
- `notes/assumptions-and-pressure-test.md` records early falsification conditions.
- `data/` is for scripts or pointers to reusable public datasets, not raw downloads by default.
- `analysis/` is for reproducible analysis notebooks/scripts.
- `references.bib` is a symlink to the central bibliography.
- `references-local.bib` is for verified project-specific additions only.

## House Style

This project uses the central house style strictly by symlink:

- `.house-style/preamble.tex -> ../../../.house-style/preamble.tex`
- `.house-style/style-rules.yaml -> ../../../.house-style/style-rules.yaml`
- `references.bib -> ../../.house-style/references.bib`

Do not copy house-style files into this project.
