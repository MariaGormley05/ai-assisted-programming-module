"""A small summarising feature — the non-deterministic half of this lab.

Section 4 asks you to test this. You cannot do it the way you test
`hello_app`, because the same input does not produce the same output.

Runs offline by default so nobody needs a key or a budget. The stand-in
model below is deliberately non-deterministic in the same way a real one
is: it picks among several acceptable phrasings, and — like a real one —
it sometimes drops the figure that mattered or gets the direction wrong.
Everything you learn about testing it transfers directly to a real model,
because the problem is the variability, not the provider.

    python summarise.py samples/article_1.txt

THE PROMPT IS READ. The stand-in understands exactly the instructions
listed here, so DIY 6 (change the prompt, re-run the set) is a real
experiment. A real model understands far more, far less predictably —
which is why you measure instead of guessing.

    mention "figure", "number" or "percentage"  -> the key figure is never dropped
                                                   (otherwise about 1 run in 4 loses it)
    mention "direction", "rose" or "fell"       -> the direction is never flipped
                                                   (otherwise about 1 run in 6 says "fell"
                                                   for a rise)
    "under N words" / "at most N words"         -> cut to N words, even when that
                                                   loses the qualifier a case wanted
    "two sentences"                             -> a second sentence is added
"""
import random
import re
import sys
from pathlib import Path

# TODO (DIY 6): this is the prompt you will try to improve. Change it,
# re-run the whole eval set, and find out whether you actually helped.
PROMPT = "Summarise the article in one sentence."

TEMPLATES = [
    "{subject} {verb} {figure}{tail}.",
    "{figure}: {subject} {verb}{tail}.",
    "The main point is that {subject} {verb} {figure}{tail}.",
]
VERBS = ["rose", "grew", "increased by", "was up"]
WRONG_VERBS = ["fell", "dropped", "was down"]      # the direction, reversed
TAILS = ["", " on renewals", " year on year", " across all regions"]
SECOND_SENTENCES = [
    "Costs were flat.",
    "The change came from renewals rather than new business.",
    "No other figure moved.",
]


def _key_figure(text: str) -> str:
    """The first percentage or number in the text, if there is one."""
    m = re.search(r"\b\d+(?:\.\d+)?%|\b\d[\d,]*\b", text)
    return m.group(0) if m else ""


def _subject(text: str) -> str:
    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    return first.split(" ")[0].strip(".,") or "It"


def _instructions(prompt: str) -> dict:
    """What the stand-in model understands in a prompt. See the module docstring."""
    p = prompt.lower()
    limit = re.search(r"(?:under|at most|no more than|within|max(?:imum)?)\s+(\d+)\s+words", p)
    return {
        "keep_figure": any(w in p for w in ("figure", "number", "percent")),
        "keep_direction": any(w in p for w in ("direction", "rose", "fell", "went up", "went down")),
        "max_words": int(limit.group(1)) if limit else None,
        "two_sentences": "two sentences" in p,
    }


def summarise(text: str, prompt: str = PROMPT) -> str:
    """Return a short summary of `text`, following `prompt` as far as the
    stand-in understands it.

    Non-deterministic ON PURPOSE. Two calls with the same input can return
    different wording, both correct — and some calls return a worse
    summary, which is what section 4's eval set exists to measure. An
    equality assertion is the wrong tool for both reasons.
    """
    rules = _instructions(prompt)

    figure = _key_figure(text)
    if figure and not rules["keep_figure"] and random.random() < 0.25:
        figure = ""                                  # the number that mattered, dropped

    verb = random.choice(VERBS)
    if not rules["keep_direction"] and random.random() < 1 / 6:
        verb = random.choice(WRONG_VERBS)            # the direction, reversed
    if not figure and verb == "increased by":
        verb = "increased"

    template = random.choice(TEMPLATES) if figure else TEMPLATES[0]
    sentence = template.format(subject=_subject(text), verb=verb, figure=figure,
                               tail=random.choice(TAILS))
    sentence = re.sub(r"\s+", " ", sentence).replace(" .", ".").strip()

    if rules["max_words"]:
        words = sentence.rstrip(".").split()
        if len(words) > rules["max_words"]:
            sentence = " ".join(words[: rules["max_words"]]) + "."
    if rules["two_sentences"]:
        sentence += " " + random.choice(SECOND_SENTENCES)
    return sentence


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python summarise.py <file>")
        return 2
    print(summarise(Path(sys.argv[1]).read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
