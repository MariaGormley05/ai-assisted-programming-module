"""Validate the syntax of a common ASCII email address."""
import re

_LOCAL_ATOM = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
_DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
_EMAIL_PATTERN = re.compile(
    rf"{_LOCAL_ATOM}(?:\.{_LOCAL_ATOM})*@(?:{_DOMAIN_LABEL}\.)+{_DOMAIN_LABEL}"
)


def validate_email(address: str) -> bool:
    """Return whether address has common ASCII email syntax.

    This checks syntax only; it does not verify that the mailbox exists or
    accept every address permitted by the email RFCs.
    """
    if not isinstance(address, str) or len(address) > 254:
        return False

    local_part, separator, _ = address.partition("@")
    return bool(
        separator
        and len(local_part) <= 64
        and _EMAIL_PATTERN.fullmatch(address)
    )
