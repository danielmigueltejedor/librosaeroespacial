#!/usr/bin/env bash
set -euo pipefail

BOOK="${1:-estructuras-aeroespaciales}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"
python3 -m framework.aerobooks.cli build "$BOOK"
