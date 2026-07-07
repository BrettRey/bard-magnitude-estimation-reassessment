# Source and Dataset Verification

This file tracks sources mentioned in the setup prompt. Do not cite, download,
or analyse a source until it has been verified against an authoritative page.

## Conceptual target

- [x] Bard, Robertson, and Sorace (1996), "Magnitude estimation of linguistic acceptability."
  - Verified metadata:
    - Ellen Gurman Bard, Dan Robertson, and Antonella Sorace.
    - *Language* 72(1), 32--68.
    - DOI: <https://doi.org/10.2307/416793>.
    - Publisher page: <https://www.cambridge.org/core/journals/language/article/abs/magnitude-estimation-of-linguistic-acceptability/BD0BBEF8A2F8F2802FF5676B86F29B5B>.
    - Edinburgh record: <https://www.research.ed.ac.uk/en/publications/magnitude-estimation-of-linguistic-acceptability/>.
  - Verification note:
    - Cambridge/Crossref now supply DOI `10.2307/416793`; the Edinburgh record still says "No DOI for article", so cite the DOI but preserve the discrepancy in notes if needed.
  - Public participant-level data:
    - Not found on Cambridge, Edinburgh, JSTOR, or Crossref-linked records. No open-access full text exists (Edinburgh record: "content not online, for subscribers only").
  - Full text obtained and read (2026-06-23):
    - PDF, markdown conversion, and image folder now in `literature/Bard-MagnitudeEstimationLinguistic-1996.{pdf,md}` (+ `_images`). The markdown preserves journal page numbers, so quotations are page-anchorable directly.
    - Brett supplied the JSTOR scan (Stable URL <https://www.jstor.org/stable/416793>); not committed to this repo.
  - Source-grounded claim target (now page-anchored):
    - Abstract (p. 32): ME "solve[s] the measurement scale problems which plague conventional techniques," provides "data which make fine distinctions robustly enough to yield statistically significant results of linguistic interest," is "usable in a consistent way by linguistically naive speaker-hearers," and allows "replication across groups of subjects."
    - The case is a scale-type / resolution argument: the problem is "the use of the wrong kind of measurement scale" (p. 32); fixed-point scales "predetermine[] the number of distinctions subjects may use" and censor finer ones (p. 35); ME "does not restrict the number of values" and gives "complete freedom about which of the infinite set of numbers to use," yielding interval/ratio data (p. 41).
    - Comparison class is informal asterisk annotation and fixed-point scales, NOT the later Likert/forced-choice/yes-no/Thurstonian inventory. So Bard's superiority claim is specifically resolution-over-fixed-scales; the broader "ME is the privileged formal method in general" is a reception extrapolation.
    - Bard et al. are tentative: advantages "are garnered at considerable empirical cost" (p. 65); the underlying psychological model is left open ("the data currently do not decide between them," p. 65).
    - §2 now page-anchors these (pp. 32, 35, 41, 65); §4 and §7 cite p. 32 for the four-part claim. The §2 page-anchor TODO is resolved.
  - Current role: conceptual target and historical claim source, now read in full; still not a raw-data source.

## Later method-comparison base

- [x] Sprouse, Schuetze, and Almeida (2013), "A comparison of informal and formal acceptability judgments using a random sample from Linguistic Inquiry 2001-2010."
  - Central bib key found: `sprouse2013`.
  - Verified metadata:
    - Jon Sprouse, Carson T. Schütze, and Diogo Almeida.
    - *Lingua* 134, 219--248.
    - DOI: <https://doi.org/10.1016/j.lingua.2013.07.002>.
    - Elsevier DOI target: <https://linkinghub.elsevier.com/retrieve/pii/S0024384113001526>.
    - Author-hosted PDF: <https://www.jonsprouse.com/papers/Sprouse%20et%20al.%202013.pdf>.
  - Verified design facts from the author-hosted PDF:
    - Tested 296 data points drawn from approximately 1743 English standard acceptability data points in *Linguistic Inquiry* 2001--2010.
    - Used 936 naive participants.
    - Compared magnitude estimation, 7-point Likert ratings, and two-alternative forced choice against informal published judgments.
    - Reported a 95% convergence estimate with a 5.3--5.8% margin of error.
  - Public participant-level data:
    - Found on Jon Sprouse's current author site, which lists `pdf`, `data`, and `materials` links for the article: <https://www.jonsprouse.com/research.html>.
    - Data zip: <https://www.jonsprouse.com/data/Lingua2013/SSA.data.zip>.
    - Materials workbook: <https://www.jonsprouse.com/data/Lingua2013/SSA.Materials.xlsx>.
    - Verified zip contents include forced-choice, Likert-scale, and magnitude-estimation CSVs plus condition files:
      - `FC experiment/FC.logistic.csv`: `participant,survey,order,item,condition,judgment`.
      - `FC experiment/FC.signtest.csv`: `participant,survey,order,judgment,item,condition,expected,pattern`.
      - `LS experiment/LI.ls.results.csv`: `participant,survey,order,judgment,item,condition,zscores`.
      - `ME experiment/LI.me.results.csv`: `participant,survey,order,judgment,item,condition,zscores`.
    - File headers say the data are provided for verification and ask researchers to contact Jon Sprouse about novel research reuse.
    - Reuse permission: approved by Jon Sprouse in correspondence reported by Brett on 2026-07-07, after Sprouse checked with Diogo Almeida. Boundary: limited secondary methodological analysis of magnitude estimation's contribution to an item-level signal; do not redistribute participant-level raw files; cite the original papers and data source clearly; reach back out if the project drifts toward a different topic closer to Sprouse/Almeida's current interests.
  - Current role: empirical base for method convergence across magnitude estimation, Likert ratings, and forced choice.

- [x] Sprouse and Almeida (2017), "Design sensitivity and statistical power in acceptability judgment experiments."
  - Verified metadata:
    - Jon Sprouse and Diogo Almeida.
    - *Glossa: a journal of general linguistics* 2(1), article 14.
    - Author site entry: <https://www.jonsprouse.com/research.html>.
  - Public participant-level data:
    - Found on Jon Sprouse's current author site.
    - Data zip: <https://www.jonsprouse.com/data/Glossa2017/SA2017.data.zip>.
    - Materials workbook: <https://www.jonsprouse.com/data/Glossa2017/SA2017.materials.xlsx>.
    - Verified zip contents include `FC.results.csv`, `LS.results.csv`, `ME.results.csv`, and `YN.results.csv`.
    - CSV headers use subject-level rows (`subject,survey,order,...`) for forced choice, Likert, magnitude estimation, and yes/no tasks.
    - File headers carry the same verification-purpose and author-contact caveat as the 2013 data.
    - Reuse permission: approved by Jon Sprouse in correspondence reported by Brett on 2026-07-07, after Sprouse checked with Diogo Almeida. Same boundary as the 2013 data: limited secondary methodological analysis, no redistribution of participant-level raw files, clear citation, and renewed contact if the project drifts from the approved scope.
  - Current role: public row-level method-comparison data that can support a constrained secondary reanalysis within the approved permission boundary.

- [x] Langsford et al. (2018), "Quantifying sentence acceptability measures: Reliability, bias, and variability."
  - Verified metadata:
    - Steven Langsford, Amy Perfors, Andrew T. Hendrickson, Lauren A. Kennedy, and Danielle J. Navarro.
    - *Glossa: a journal of general linguistics* 3(1), article 37.
    - DOI: <https://doi.org/10.5334/gjgl.396>.
    - Article page: <https://www.glossa-journal.org/article/id/5005/>.
    - Supplement DOI: <https://doi.org/10.5334/gjgl.396.s1>.
    - PsyArXiv/preprint DOI: <https://doi.org/10.31234/osf.io/vrfxn>.
  - Verified design facts:
    - Compared Likert, magnitude estimation, target-pair forced choice, random-pair forced choice, and a Thurstonian model.
    - Focused on within- and between-participant test-retest reliability, response-style variability, item effects, and sample-size sensitivity.
    - Reported Likert and Thurstonian approaches as the most stable/reliable measures in their data.
    - Found magnitude-estimation scores broadly consistent with other measures but less reliable, with extra variability linked to participant response styles.
  - Public data/materials:
    - Glossa lists supplementary file `gjgl-3-396-s1.pdf`; this file contains corpus details and stimulus lists, not an obvious raw participant-response repository.
    - Glossa article page lists one supplementary PDF, with Appendix A "Corpus details" and Appendix B "Details of the Thurstone model."
    - OSF/PsyArXiv API record `vrfxn_v1` has `has_data_links: null`, `data_links: null`, and no associated OSF node.
    - OSF storage for the preprint contains only `2018_grammaticality.pdf` in the root listing on this pass.
    - Andrew Perfors's publication page links PDF, project page, PsyArXiv, and the published article, but no dataset/code button. Danielle Navarro's publication page likewise links PDF, DOI, and PsyArXiv, but not OSF/GitHub/data for this paper.
    - Final targeted pass on 2026-07-07 rechecked the Glossa article page, article PDF/XML, supplementary file `gjgl-3-396-s1.pdf`, Danielle Navarro's publication page, and OSF/PsyArXiv node/registration routes for `vrfxn`; no public raw participant-response rows or analysis code were located. The supplement remains corpus and Thurstonian-model documentation only.
    - Raw participant-response data not found after this targeted pass. Treat availability as not public unless an author-controlled repository or author reply surfaces.
  - Current role: article-level empirical base for reliability, response-style analysis, and the non-privileged status of magnitude estimation. Do not plan participant-level reanalysis, response-style modelling, or test-retest modelling from this paper unless raw rows are obtained.

- [x] Weskott and Fanselow (2011), "On the informativity of different measures of linguistic acceptability."
  - Metadata first sourced from Schütze (2016), in-text at p. 208 and full reference at p. 268 of `literature/schutze2016.md`.
  - Verified against Crossref (DOI registration authority) on 2026-06-23:
    - Thomas Weskott and Gisbert Fanselow.
    - *Language* 87(2), 249--273 (June 2011).
    - DOI: <https://doi.org/10.1353/lan.2011.0041>.
    - `references-local.bib` entry `weskott2011` updated with issue 2 and the verified DOI; ready for `/push-bib`.
  - Why it matters: Schütze (2016: 208) states that magnitude estimation's touted advantages over the Likert task have "most or all" been "subsequently refuted," citing this paper and Sprouse, Schütze, and Almeida (2013). This is the canonical anti-ME empirical result the reassessment must engage.
  - Added to `references-local.bib` as `weskott2011` with a verification-pending comment.
  - Current role: prior-art anchor for the marginal-contribution claim. Verify primary metadata and, ideally, read the paper before relying on any specific finding beyond Schütze's characterization.

## Contemporary afterlife

- [x] CoLA.
  - Verified publication metadata:
    - Alex Warstadt, Amanpreet Singh, and Samuel R. Bowman (2019), "Neural Network Acceptability Judgments."
    - *Transactions of the Association for Computational Linguistics* 7, 625--641.
    - DOI: <https://doi.org/10.1162/tacl_a_00290>.
    - ACL Anthology page: <https://aclanthology.org/Q19-1040/>.
  - Verified dataset metadata:
    - Dataset page: <https://nyu-mll.github.io/CoLA/>.
    - README: <https://github.com/nyu-mll/CoLA-baselines/blob/master/acceptability_corpus/cola_public/README>.
    - Full corpus: 10,657 sentences from 23 linguistics publications.
    - Public corpus: 9,594 train/development sentences; 1,063 held-out test sentences excluded.
    - Public split files: `raw/in_domain_train.tsv` (8551), `raw/in_domain_dev.tsv` (527), and `raw/out_of_domain_dev.tsv` (516), plus tokenized equivalents.
    - Format: source code, binary acceptability label (`0=unacceptable`, `1=acceptable`), original judgment notation, sentence.
  - Licensing/copyright note:
    - The README says the text is excerpted from published works, copyright remains with original authors/publishers where applicable, and the authors expect US research use to be fair use but make no guarantee.
  - Construct note:
    - Labels are expert/literature labels described as "acceptability (grammaticality)" in the README and "grammatical or ungrammatical" in the TACL abstract. Do not treat CoLA as naive-speaker acceptability data.
  - Current role: benchmark afterlife, not direct magnitude-estimation evidence. Use rhetorically to show that formal acceptability measurement survived as a construct, not evidentially for ME-vs-Likert.

- [x] BLiMP.
  - Central bib key found: `WarstadtEtAl2020`.
  - Verified metadata:
    - Alex Warstadt, Alicia Parrish, Haokun Liu, Anhad Mohananey, Wei Peng, Sheng-Fu Wang, and Samuel R. Bowman (2020).
    - *Transactions of the Association for Computational Linguistics* 8, 377--392.
    - DOI: <https://doi.org/10.1162/tacl_a_00321>.
    - ACL Anthology page: <https://aclanthology.org/2020.tacl-1.25/>.
    - Repository: <https://github.com/alexwarstadt/blimp>.
  - Verified dataset facts:
    - 67 sub-datasets, each with 1000 minimal pairs.
    - Automatically generated from expert-crafted grammars.
    - Pairs contrast grammatical acceptability in syntax, morphology, or semantics.
    - Repository reports aggregate human agreement with labels of 96.4%.
    - Repository states BLiMP is distributed under CC-BY.
    - Repository notes an August 16, 2021 erratum for some misreported published TACL results; cite corrected files/repo if using those specific numbers.
  - Current role: benchmark afterlife for acceptability-style model evaluation, not direct human magnitude-estimation evidence. Use rhetorically to show that formal acceptability measurement survived as a construct, not evidentially for ME-vs-Likert.

- [x] Syntactic Acceptability Dataset.
  - Central bib key found: `juzek2024`.
  - Verified publication metadata:
    - Tom S. Juzek (2024), "The Syntactic Acceptability Dataset (Preview): A Resource for Machine Learning and Linguistic Analysis of English."
    - LREC-COLING 2024, pages 16113--16120.
    - ACL Anthology page: <https://aclanthology.org/2024.lrec-main.1401/>.
  - Verified dataset metadata:
    - Repository: <https://github.com/tjuzek/sad>.
    - Dataset file listed in README: `Syntactic_acceptability_dataset_preview.tsv`.
    - Paper describes a preview of 1000 English sequences, half from textbooks and half from *Linguistic Inquiry*.
    - Entries include grammatical status from the literature and acceptability status from native-speaker crowdsourcing.
    - Paper reports grammaticality/acceptability convergence around 83%.
    - Repository states dataset license is CC0 1.0 Universal, while quoted source sentences remain subject to their original authors/publishers.
  - Construct note:
    - This is a useful bridge source because it explicitly separates extracted grammaticality labels from crowd acceptability judgments.
  - Current role: candidate bridge between grammaticality labels and acceptability judgments, not direct evidence about magnitude estimation.

## Search targets

- Bard et al. original raw or summarized data remains unresolved. The source-grounded Bard target is the abstract-level claim that magnitude estimation solves scale problems and yields robust fine distinctions.
- Sprouse et al. 2013 public participant-level data is verified on Jon Sprouse's current author site; limited secondary reuse was approved by Jon Sprouse on 2026-07-07 after checking with Diogo Almeida.
- Sprouse and Almeida 2017 public participant-level data is verified on Jon Sprouse's current author site; limited secondary reuse was approved by Jon Sprouse on 2026-07-07 after checking with Diogo Almeida.
- Langsford et al. raw participant-response data was not found after Glossa, supplement, author pages, and OSF/PsyArXiv API checks, including the final targeted pass on 2026-07-07; stimulus/corpus/model supplement is verified.
- CoLA publication and dataset citation are verified; license/fair-use limits must be stated if reused.
- Any later datasets that directly compare magnitude estimation, Likert, forced-choice, and Thurstonian measures.
