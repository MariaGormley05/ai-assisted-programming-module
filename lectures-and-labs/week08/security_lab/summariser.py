"""A document summariser with a prompt-injection hole. DIY 5.

This stands in for the AI feature in your own project: it takes text a
user supplied and puts it in front of a model. Any text a user supplies
can contain instructions.

Run it on a clean document and it behaves. Run it on the poisoned one and
watch what the document tells it to do:

    python summariser.py documents/clean.txt
    python summariser.py documents/poisoned.txt

Your job in DIY 5 is to change SYSTEM_PROMPT and build_messages() so the
document is treated as data and not as orders -- then to try to defeat
your own fix.

No API key is needed. The stand-in model below is deliberately naive so
the injection is visible without anyone paying for tokens. It is also
deliberately SMALL: it understands exactly the things listed in
naive_model()'s docstring and nothing else, so you can reason about it.
A real model understands far more, less predictably -- and still falls
for well-built injections.
"""
import os
import sys

# TODO (DIY 5, step 4): this instruction is too weak. It says what to do
# but never says that the document is untrusted, never marks where the
# document starts and ends, and never tells the model what to do when the
# document tries to give it orders.
SYSTEM_PROMPT = "Summarise the document the user gives you in one sentence."

# The delimiters the stand-in model recognises when the system prompt tells
# it the document is data. Real prompts use shapes like these too.
DELIMITERS = (
    ("<document>", "</document>"),
    ("---BEGIN DOCUMENT---", "---END DOCUMENT---"),
    ('"""', '"""'),
)

# Phrases that tell the stand-in model the document is data, not orders.
DATA_WORDS = ("untrusted", "as data", "is data", "not instructions",
              "never instructions", "not an instruction", "never an instruction",
              "do not follow", "never follow", "ignore any instruction")

INJECTION_MARKERS = ("ignore all previous instructions",
                     "ignore your previous instructions",
                     "disregard the above")


def build_messages(document: str) -> list[dict]:
    """Assemble what gets sent to the model.

    Note what is wrong here: the document is concatenated straight into
    the user turn, so from the model's side there is nothing separating
    'the thing to summarise' from 'an instruction to follow'. Everything
    arrives as one undifferentiated stream of text.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": document},
    ]


def naive_model(messages: list[dict]) -> str:
    """A stand-in that mimics an instruction-following model.

    What it understands, in full:

    1. It scans the user turn for an injected instruction (one of
       INJECTION_MARKERS) and obeys the LAST one it finds. Otherwise it
       "summarises": it returns the document's first non-empty line.
    2. If the system prompt says the document is data (any phrase in
       DATA_WORDS) AND the user turn wraps the document in one of the
       DELIMITERS, it treats everything INSIDE the delimiters as data: an
       instruction in there is ignored.
    3. Anything OUTSIDE the delimiters is still read as instructions. That
       is where a bypass lives: a document that contains the closing
       delimiter itself steps outside the fence, exactly as real
       injections do to real prompts.

    Real models are far better than this, and still fall for well-built
    injections. This one is exaggerated on purpose so the failure -- and
    the shape of the fix, and the shape of the bypass -- are all visible.
    """
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    user = messages[-1]["content"]

    document = user            # what gets summarised
    instructions_from = user   # what the model takes orders from
    if any(word in system.lower() for word in DATA_WORDS):
        for opener, closer in DELIMITERS:
            start = user.find(opener)
            if start < 0:
                continue
            start += len(opener)
            end = user.find(closer, start)
            if end < 0:
                continue
            document = user[start:end]
            instructions_from = user[:start] + user[end + len(closer):]
            break

    lowered = instructions_from.lower()
    hits = [(lowered.rfind(marker), marker) for marker in INJECTION_MARKERS
            if marker in lowered]
    if hits:
        position, marker = max(hits)
        after = instructions_from[position + len(marker):].strip()
        first_line = after.splitlines()[0] if after else ""
        return f"[model obeyed the document] {first_line[:120]}"

    first = next((ln for ln in document.splitlines() if ln.strip()), "")
    return f"[summary] {first.strip()[:120]}"


def summarise(document: str) -> str:
    if os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"):
        # Left for you if you want to try it against a real model. The
        # injection behaves the same way; it is just less obvious.
        print("(a real key is set, but this lab runs offline by design)",
              file=sys.stderr)
    return naive_model(build_messages(document))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python summariser.py <document>")
        return 2
    document = open(sys.argv[1], encoding="utf-8").read()
    print(summarise(document))
    return 0


if __name__ == "__main__":
    sys.exit(main())
