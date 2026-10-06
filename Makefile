BOOK ?= estructuras-aeroespaciales
PYTHON ?= python3

.PHONY: install doctor list new sync ai-pack check audit book clean

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

check:
	$(PYTHON) -m framework.aerobooks.cli check $(BOOK)

audit:
	$(PYTHON) -m framework.aerobooks.cli audit $(BOOK)

book:
	$(PYTHON) -m framework.aerobooks.cli build $(BOOK)

clean:
	cd books/$(BOOK) && latexmk -C
