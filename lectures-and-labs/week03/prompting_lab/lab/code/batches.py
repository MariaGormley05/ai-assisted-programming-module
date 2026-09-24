"""A helper with a subtle bug — the subject of DIY 6 (chain-of-thought
debugging).

`batches(items, size)` is meant to split a list into consecutive batches of
`size`, with the last batch shorter when the list does not divide evenly.
It is wrong, but not for every input: it passes the obvious example below.
Do not fix it here first — follow DIY 6 and let the reasoning find it.

    >>> batches([1, 2, 3, 4, 5, 6], 3)
    [[1, 2, 3], [4, 5, 6]]
"""
from __future__ import annotations


def batches(items: list, size: int) -> list[list]:
    """Split `items` into consecutive batches of `size`; the last one may be shorter."""
    if size <= 0:
        raise ValueError("size must be positive")
    return [items[i:i + size] for i in range(0, len(items) - size + 1, size)]
