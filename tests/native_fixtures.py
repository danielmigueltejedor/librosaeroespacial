"""Historical manuscripts exercise native validators independently of the catalogue."""
from pathlib import Path


def native_book_dir(slug: str) -> Path:
    return Path(__file__).resolve().parent / "fixtures" / "native-v02" / slug
