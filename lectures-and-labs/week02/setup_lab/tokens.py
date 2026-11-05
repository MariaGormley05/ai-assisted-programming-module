"""See the pieces a model actually reads.

    python tokens.py
    python tokens.py "any text you like"

Needs tiktoken (pip install tiktoken); the first run downloads a
tokeniser. This is one tool's split -- others cut text differently, and
the exact boundaries are not the point. The point is that it is pieces,
not letters.
"""
import sys

try:
    import tiktoken
except ImportError:
    sys.exit("This needs tiktoken:  pip install tiktoken   (then run it again)")

SAMPLES = (
    "def calculate_median(numbers):",
    "strawberry",
    "supercalifragilisticexpialidocious",
    "48391 * 7263",
)


def main(texts) -> None:
    enc = tiktoken.get_encoding("o200k_base")
    for text in texts:
        pieces = [enc.decode([token]) for token in enc.encode(text)]
        print(f"{len(pieces):>3} pieces  " + " ".join(repr(p) for p in pieces))


if __name__ == "__main__":
    main(sys.argv[1:] or SAMPLES)
