# Makefile for LaTeX paper compilation

LATEX = xelatex
BIBER = biber
MAIN = main
OUTDIR = .

.PHONY: all quick blind lualatex clean distclean view help

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex sections/*.tex references.bib references-local.bib
	@echo "==> First LaTeX pass..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex
	@echo "==> Running Biber..."
	$(BIBER) $(MAIN)
	@echo "==> Second LaTeX pass..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex
	@echo "==> Third LaTeX pass (finalizing)..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex
	@echo "==> Build complete: $(MAIN).pdf"

quick: $(MAIN).tex
	@echo "==> Quick build (single pass)..."
	$(LATEX) -output-directory=$(OUTDIR) $(MAIN).tex

blind: $(MAIN).tex sections/*.tex references.bib references-local.bib
	@echo "==> Blinded build (anonymized)..."
	$(LATEX) -output-directory=$(OUTDIR) -jobname=$(MAIN)-blind "\def\blindbuild{}\input{$(MAIN).tex}"
	$(BIBER) $(MAIN)-blind
	$(LATEX) -output-directory=$(OUTDIR) -jobname=$(MAIN)-blind "\def\blindbuild{}\input{$(MAIN).tex}"
	$(LATEX) -output-directory=$(OUTDIR) -jobname=$(MAIN)-blind "\def\blindbuild{}\input{$(MAIN).tex}"
	@echo "==> Blinded build complete: $(MAIN)-blind.pdf"

lualatex: LATEX = lualatex
lualatex: all

clean:
	@echo "==> Cleaning build artifacts..."
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg $(MAIN).log
	rm -f $(MAIN).out $(MAIN).run.xml $(MAIN).toc $(MAIN).fdb_latexmk
	rm -f $(MAIN).fls $(MAIN).synctex.gz
	rm -f $(MAIN)-blind.aux $(MAIN)-blind.bbl $(MAIN)-blind.bcf $(MAIN)-blind.blg $(MAIN)-blind.log
	rm -f $(MAIN)-blind.out $(MAIN)-blind.run.xml $(MAIN)-blind.toc
	@echo "==> Clean complete"

distclean: clean
	@echo "==> Removing PDFs..."
	rm -f $(MAIN).pdf $(MAIN)-blind.pdf
	@echo "==> Deep clean complete"

view: $(MAIN).pdf
	@echo "==> Opening PDF..."
	open $(MAIN).pdf

help:
	@echo "Available targets:"
	@echo "  make          - Build PDF with full bibliography"
	@echo "  make quick    - Quick build"
	@echo "  make blind    - Blinded PDF for double-blind review"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make distclean- Remove build artifacts and PDFs"
	@echo "  make view     - Open PDF"
	@echo "  make help     - Show this help"
