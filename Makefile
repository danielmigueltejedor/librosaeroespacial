BOOK ?= estructuras-aeroespaciales
ROLE ?= scientific
PYTHON ?= python3

.PHONY: install doctor list new sync ai-pack review-pack academic-init bootstrap coverage review-suite academic-gate release-manifest check audit book clean

install:
	$(PYTHON) -m pip install -e .

doctor:
	$(PYTHON) -m framework.aerobooks.cli doctor

list:
	$(PYTHON) -m framework.aerobooks.cli list

new:
	@echo "Uso recomendado: aerobooks new <slug> --title \"...\" --subtitle \"...\""

sync:
	$(PYTHON) -m framework.aerobooks.cli sync $(BOOK)

ai-pack:
	$(PYTHON) -m framework.aerobooks.cli ai-pack $(BOOK)

review-pack:
	$(PYTHON) -m framework.aerobooks.cli review-pack $(BOOK) $(ROLE)

academic-init:
	$(PYTHON) -m framework.aerobooks.academic init $(BOOK)

bootstrap:
	$(PYTHON) -m framework.aerobooks.academic bootstrap $(BOOK)

coverage:
	$(PYTHON) -m framework.aerobooks.academic coverage $(BOOK) --strict

review-suite:
	$(PYTHON) -m framework.aerobooks.academic review-suite $(BOOK)

academic-gate:
	$(PYTHON) -m framework.aerobooks.academic gate $(BOOK)

release-manifest:
	$(PYTHON) -m framework.aerobooks.academic release-manifest $(BOOK)

check:
	$(PYTHON) -m framework.aerobooks.cli check $(BOOK)

audit:
	$(PYTHON) -m framework.aerobooks.cli audit $(BOOK)

book:
	$(PYTHON) -m framework.aerobooks.cli build $(BOOK)

clean:
	cd books/$(BOOK) && latexmk -C
