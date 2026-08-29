# Manuscript root and template migration
## Intended outcome
Give the manuscript a useful filename and bring the project forward to the current central paper template without changing its argument, results, figures, or bibliography.

The descriptive stem is `bard-magnitude-estimation-reassessment`.
## One decision exposed by the current template
The current central template deliberately keeps `main.tex` as its internal build root and creates a descriptively named upload PDF from the project folder name. Several portfolio tools also still treat `main.tex` as the expected root.
### Option A: current-template convention (recommended)
- Keep `main.tex` as the internal source root.

- Adopt the current template's named-output build, producing `bard-magnitude-estimation-reassessment.pdf` as the paper to read and share.

- Keep `main.pdf` only as an internal build product.

- Produce `bard-magnitude-estimation-reassessment-blind.pdf` from the existing blind-build target.

- Update live documentation so it points readers to the named PDF while still identifying `main.tex` as the source root.


This satisfies the practical problem (no one receives a file called `main.pdf`) and remains compatible with current portfolio tooling.
### Option B: literal root rename (selected)
- Rename `main.tex` to `bard-magnitude-estimation-reassessment.tex`.

- Build `bard-magnitude-estimation-reassessment.pdf` directly, with all auxiliary files using that stem.

- Rename the blind build correspondingly.

- Update every live project reference and audit the portfolio tools that currently hard-code `main.tex`.


This removes `main.*` entirely, but it changes a portfolio convention rather than merely migrating this paper to the current template. Historical audit records would remain unchanged.

**Decision:** Brett selected Option B in Roughdraft on 2026-08-29.
## Template migration common to either option
1. Move the existing AI-use statement to page 1 using the current `\aidisclosure{}` macro, immediately after the keywords. Remove the resulting empty end-of-paper acknowledgements section.

2. Adapt the current template Makefile while preserving this project's section dependencies, `references-local.bib`, blind build, and XeLaTeX/Biber sequence.

3. Refresh the template-derived agent guidance from the current central version, substitute this paper's title and directory, and keep project-specific research guidance in `notes/project-brief.md`, `STATUS.md`, and `DECISIONS.md`.

4. Preserve the project's central house-style symlinks. Do not copy a local house-style snapshot.

5. Do not fabricate a `.canon-stamp`: the current creation script gives one to new papers, but an existing paper needs an actual canon reconciliation before claiming that status.

6. Update README/build instructions and live submission-preparation notes. Preserve historical review and pass records as historical records.

7. Run full normal and blind builds, the central style checker, bibliography and analysis tests, log scans, PDF metadata checks, and rendered-page comparison.

## Reversibility
The source and Makefile changes are ordinary Git-tracked edits. The existing dirty working tree will be preserved, and no unrelated changes will be staged, committed, or pushed.

## Completion

Completed on 2026-08-29 using the selected literal-root option.

- The canonical source is `bard-magnitude-estimation-reassessment.tex`; no live `main.*` artifact remains in the project root.
- Normal and anonymous builds produce correspondingly named 13-page PDFs.
- The current-template page-one AI disclosure, adapted Makefile, and project guidance are in place.
- Normal and anonymous build logs are clean; the central style audit and four analysis tests pass.
- Manuscript fingerprinting, the pass tracker, and canon-drift scanning recognize the named root. The older portfolio distillation script still expects `main.tex` for full-body extraction, but it continues to discover the project through `STATUS.md` and `CLAUDE.md`; changing that global tool was left outside this project-scoped migration.
