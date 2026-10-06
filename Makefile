BOOK ?= estructuras-aeroespaciales

.PHONY: book clean

book:
	./scripts/build-book.sh $(BOOK)

clean:
	cd books/$(BOOK) && latexmk -C
