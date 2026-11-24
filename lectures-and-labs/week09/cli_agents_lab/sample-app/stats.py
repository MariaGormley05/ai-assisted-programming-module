"""Small statistics helpers.

This is the project the coding agent works on in the CLI agents lab. It is
deliberately small, so that you can read every change an agent makes to it.
"""


def mean(values):
    """Return the arithmetic mean of a non-empty list of numbers."""
    if not values:
        raise ValueError("mean() of an empty list")
    return sum(values) / len(values)


def median(values):
    """Return the middle value of a non-empty list of numbers."""
    if not values:
        raise ValueError("median() of an empty list")
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def mode(values):
    """Return the most common value; a tie goes to the value seen first."""
    if not values:
        raise ValueError("mode() of an empty list")
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    best = max(counts.values())
    for value in values:
        if counts[value] == best:
            return value


def spread(values):
    """Return the difference between the largest and smallest value."""
    return max(values) - min(values)
