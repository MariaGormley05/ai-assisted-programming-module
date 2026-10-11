"""Utilities for turning blog post titles into URL slugs."""

import re
import unicodedata


def slugify(title: str) -> str:
    """Return a lowercase, hyphen-separated slug for *title*."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    words = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_title.lower()).strip("-")
    return words
