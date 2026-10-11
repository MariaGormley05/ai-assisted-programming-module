"""Utilities for turning blog post titles into URL slugs."""

import re
import unicodedata


def slugify(title: str) -> str:
    """Return a lowercase, hyphen-separated slug for *title*."""
    title = title.lower().replace("ß", "ss")
    title = title.replace("'", "").replace("’", "")
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
    if not slug:
        raise ValueError("title contains no letters or digits")
    return slug
