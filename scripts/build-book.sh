#!/usr/bin/env bash
set -euo pipefail

BOOK="${1:-}"
if [[ -z "$BOOK" ]]; then
  echo "Uso: scripts/build-book.sh <slug>"
  echo "Ejemplo: scripts/build-book.sh estructuras-aeroespaciales"
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/books/$BOOK"

if [[ ! -f "$DIR/main.tex" ]]; then
  echo "No existe $DIR/main.tex" >&2
  exit 2
fi

cd "$DIR"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
echo "PDF generado en: $DIR/main.pdf"
