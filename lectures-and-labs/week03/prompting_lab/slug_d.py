"""Utilities for turning blog post titles into URL slugs."""

import re
import unicodedata


def slugify(title: str) -> str:
    """Return a lowercase, hyphen-separated slug for *title*."""
    normalized = unicodedata.normalize("NFKD", title.lower())
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_title = ascii_title.replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
