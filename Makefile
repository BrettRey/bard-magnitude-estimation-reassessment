# Makefile for LaTeX paper compilation

# Configuration
LATEX = xelatex
BIBER = biber
MAIN = bard-magnitude-estimation-reassessment
BLIND = $(MAIN)-blind
OUTDIR = .
MANUSCRIPT_DEPS = $(MAIN).tex sections/*.tex figures/*.pdf references.bib references-local.bib

# Targets
.PHONY: all quick blind figures test lualatex clean distclean view help

all: $(MAIN).pdf

# Full build sequence with bibliography
$(MAIN).pdf: $(MANUSCRIPT_DEPS)
	@echo "==> First LaTeX pass..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex
	@echo "==> Running Biber..."
	$(BIBER) $(MAIN)
	@echo "==> Second LaTeX pass..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex
	@echo "==> Third LaTeX pass (finalizing)..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex
	@echo "==> Build complete: $(MAIN).pdf"

# Quick build (single pass, no bibliography update)
quick: $(MAIN).tex
	@echo "==> Quick build (single pass)..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex

# Double-anonymous build
blind: $(MANUSCRIPT_DEPS)
	@echo "==> Blinded build (anonymized)..."
	$(LATEX) -output-directory=$(OUTDIR) -jobname=$(BLIND) "\def\blindbuild{}\input{$(MAIN).tex}"
	$(BIBER) $(BLIND)
	$(LATEX) -output-directory=$(OUTDIR) -jobname=$(BLIND) "\def\blindbuild{}\input{$(MAIN).tex}"
	$(LATEX) -output-directory=$(OUTDIR) -jobname=$(BLIND) "\def\blindbuild{}\input{$(MAIN).tex}"
	@echo "==> Blinded build complete: $(BLIND).pdf"

figures:
	python3 analysis/make_manuscript_figures.py

test:
	python3 -m unittest discover -s analysis -p 'test_*.py'
	python3 -m py_compile analysis/*.py

# Use LuaLaTeX instead of XeLaTeX (not recommended: it breaks the PDF text layer)
lualatex: LATEX = lualatex
lualatex: all

# Clean build artifacts (keep PDFs)
clean:
	@echo "==> Cleaning build artifacts..."
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg $(MAIN).log
	rm -f $(MAIN).out $(MAIN).run.xml $(MAIN).toc $(MAIN).fdb_latexmk
	rm -f $(MAIN).fls $(MAIN).synctex.gz
	rm -f $(BLIND).aux $(BLIND).bbl $(BLIND).bcf $(BLIND).blg $(BLIND).log
	rm -f $(BLIND).out $(BLIND).run.xml $(BLIND).toc $(BLIND).fdb_latexmk
	rm -f $(BLIND).fls $(BLIND).synctex.gz
	@echo "==> Clean complete"

# Clean everything including PDFs
distclean: clean
	@echo "==> Removing PDFs..."
	rm -f $(MAIN).pdf $(BLIND).pdf
	@echo "==> Deep clean complete"

view: $(MAIN).pdf
	@echo "==> Opening $(MAIN).pdf..."
	open $(MAIN).pdf

help:
	@echo "Available targets:"
	@echo "  make          - Build $(MAIN).pdf with the full bibliography"
	@echo "  make quick    - Run one XeLaTeX pass"
	@echo "  make blind    - Build $(BLIND).pdf"
	@echo "  make figures  - Regenerate manuscript figures"
	@echo "  make test     - Run analysis tests and Python compilation checks"
	@echo "  make clean    - Remove build artifacts but keep PDFs"
	@echo "  make distclean- Remove build artifacts and PDFs"
	@echo "  make view     - Open $(MAIN).pdf"
