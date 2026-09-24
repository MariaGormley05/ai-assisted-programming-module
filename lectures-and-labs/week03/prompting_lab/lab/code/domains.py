"""Task 8 Placeholder: extract_domain

Implement extract_domain(url: str) -> str in Task 8 using a tests-first approach.
Guidelines (from lab):
- Return registrable domain (strip subdomains) for simple cases.
- Accept multi-part TLDs in naive fashion (no full PSL parsing expected).
- Raise ValueError for unsupported hosts like 'localhost'.
- Keep implementation minimal; only what's needed for the provided tests.
"""
from __future__ import annotations
from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """Return the registrable domain (no subdomain) for a simple URL.

    The tests you write first in DIY 8 define the behaviour. Constraints:
    strip subdomains; handle the one multi-part TLD the tests use; raise
    ValueError for hosts that have no registrable domain, such as
    localhost. No public-suffix list is expected.
    """
    # TODO: implement in DIY 8, after the tests exist
    # Then split by '.' and take the appropriate parts
    raise NotImplementedError("Task 8: Implement extract_domain function")
