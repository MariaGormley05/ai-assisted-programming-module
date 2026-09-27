"""Validate an email address using a deliberately simple rule."""


def validate_email(address: str) -> bool:
    """Return whether address is at most 254 characters and has an @ followed by a dot."""
    if not isinstance(address, str) or len(address) > 254:
        return False

    at_position = address.find("@")
    return at_position != -1 and address.find(".", at_position + 1) != -1
