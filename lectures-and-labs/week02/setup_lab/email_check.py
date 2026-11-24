"""Run every validator you were given against the same awkward addresses.

    python email_check.py validate_a validate_b
    python email_check.py validate_a validate_b validate_c

Each name is a .py file in this folder. The harness imports it, takes the
first function whose name mentions "valid" or "email" (or else the first
function it defines), calls it with each address, and prints yes, no or
ERROR. Then it counts the rows where the validators disagree. Nothing here
is marked; it exists so you can see the decisions each prompt made without
reading regexes.
"""
from __future__ import annotations

import importlib
import os
import sys
import types

ADDRESSES = (
    ("a@b.c", "shortest thing with an @ and a dot after it"),
    ("a@b", "no dot after the @"),
    ("first.last@example.co.uk", "ordinary"),
    ("user+tag@gmail.com", "a plus sign, common in real mailboxes"),
    ("A@B.COM", "upper case"),
    ("a@b..c", "two dots in a row"),
    ('"john doe"@example.com', "quoted local part with a space: legal by the RFC"),
    ("üser@example.com", "a non-ASCII letter"),
    (" a@b.c ", "spaces around it"),
    ("a" * 242 + "@example.com", "exactly 254 characters"),
    ("a" * 243 + "@example.com", "255 characters"),
)


def validator(name: str):
    """The function in <name>.py that looks like the validator."""
    module = importlib.import_module(name)
    functions = [v for v in vars(module).values()
                 if isinstance(v, types.FunctionType) and v.__module__ == module.__name__]
    if not functions:
        sys.exit(f"{name}.py defines no function")
    for fn in functions:
        if "valid" in fn.__name__ or "email" in fn.__name__:
            return fn
    return functions[0]


def verdict(fn, address: str) -> str:
    try:
        return "yes" if fn(address) else "no"
    except Exception as exc:  # raising is a decision too
        return f"ERROR:{type(exc).__name__}"


def shown(address: str) -> str:
    if address != address.strip():
        return repr(address)
    if len(address) <= 28:
        return address
    return f"{address[:8]}...({len(address)} chars)"


def main(names: list[str]) -> int:
    if len(names) < 2:
        print(__doc__)
        return 2
    sys.path.insert(0, os.getcwd())
    fns = [validator(n) for n in names]
    width = max(len(n) for n in names)
    print(f"{'address':<32}  " + "  ".join(n.ljust(width) for n in names))
    splits = 0
    for address, note in ADDRESSES:
        results = [verdict(fn, address) for fn in fns]
        if len(set(results)) > 1:
            splits += 1
        print(f"{shown(address):<32}  " + "  ".join(r.ljust(width) for r in results)
              + f"   {note}")
    print()
    print(f"{splits} of {len(ADDRESSES)} addresses split the validators. Every one of "
          "those is a decision the prompt left open, and something decided it anyway.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
