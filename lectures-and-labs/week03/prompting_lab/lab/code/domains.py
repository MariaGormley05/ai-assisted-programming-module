"""extract_domain: the subject of DIY 7 (tests first).

Write the tests in lab/tests/test_extract_domain.py first; then have the
assistant implement extract_domain so that they pass.
"""
from __future__ import annotations

from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """Return the registrable domain (no subdomain) for a simple URL.

    Strip subdomains; handle the one multi-part suffix the tests use,
    .co.uk; raise ValueError for a host that has no registrable domain,
    such as localhost, and for an empty string. No public-suffix list is
    expected.
    """
    raise NotImplementedError("DIY 7: write the tests first, then implement this")
