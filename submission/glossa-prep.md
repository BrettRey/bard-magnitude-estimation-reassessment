# Glossa Preparation Checklist

Target venue: *Glossa: a journal of general linguistics*.

## Fit

Glossa is the right first target if the paper is framed as a general-linguistics
measurement article with theoretical implications for what acceptability
judgments project. The fit is strongest when the introduction and conclusion
make the projectibility payoff visible: the Sprouse reanalysis suggests that
formal judgments preserve stable item-level contrast ordering across ordinary
elicitation formats, while magnitude estimation does not add a systematic
practical ordering advantage for the tested contrasts.

## Official Guidance To Verify

The Glossa pages were checked on 2026-07-08 through official search-result text,
but direct page fetches were blocked by Anubis. Before submission, verify the
full current instructions manually in the Glossa web UI.

Official pages to re-check:

- About: https://www.glossa-journal.org/site/about/
- Author guidelines: https://www.glossa-journal.org/site/author-guidelines/
- Submissions: https://www.glossa-journal.org/submissions/
- Journal policies: https://www.glossa-journal.org/site/journal-policies/
- Editorial policies: https://www.glossa-journal.org/site/editorial-policies/

Current official search-result text indicates:

- Glossa publishes general-linguistics work from all areas of linguistics when
  it has theoretical implications.
- Research articles are initially capped at 13,000 words and may extend to
  15,000 after revisions; the editorial-policy page reports that Glossa does
  not accept papers of more than 15,000 words for publication.
- The submission checklist asks authors to keep within the maximum word count
  or move material to an appendix not counted toward the maximum.
- The author guidelines require a word count under the paper title, including
  footnotes and references.
- The journal policy requires data, stimuli, and analysis scripts associated
  with a submission to be openly available at submission time.

## Project-Specific Submission Tasks

- Verify the full Glossa author guidelines and submission checklist in the
  browser before changing the manuscript title page.
- Generate a submission-grade word count that includes footnotes and references;
  `texcount -inc -sum main.tex` currently reports about 3,852 words before
  references, but also reports macro-parsing errors and should not be treated as
  the final count.
- Build the anonymous version with `make blind`, inspect `main-blind.pdf`, and
  check PDF metadata.
- Review the manuscript for author-identifying wording. The data/source
  permission boundary can name Jon Sprouse and Diogo Almeida, but acknowledgments
  and any repository self-reference may need anonymous-review handling.
- Decide whether to promote aggregate, non-participant-level outputs from
  `data/derived/` for Glossa's open-data policy. Raw participant-level Sprouse
  files must not be redistributed.
- Draft a Glossa-specific data-availability statement explaining the boundary:
  source public data are available from Jon Sprouse's site, reuse permission was
  granted for this limited secondary analysis, raw participant rows are not
  redistributed here, and the repository contains scripts plus any deliberately
  promoted aggregate outputs.
- Decide whether a compact methods appendix or supplement is needed for the
  response-function and aggregate bootstrap diagnostics.
- Re-check the abstract and Section 1 for Glossa fit: the paper should not read
  only as a narrow methods replication; the general-linguistics payoff is the
  relation between elicitation format, acceptability evidence, and projectible
  grammatical contrasts.
- Add final venue-specific AI-use wording if required by Glossa's current
  policy or the submission system.
