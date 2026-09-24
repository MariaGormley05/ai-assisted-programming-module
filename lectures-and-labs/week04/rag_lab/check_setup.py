"""Confirm this lab can run before you start it.

    python check_setup.py

Checks Python, the packages from requirements.txt, the five documents in
data/, and whether a key for the generation half (sections 3 to 5) is set.
The embedding model needs no key. Prints one line per check and exits
non-zero if anything essential is missing. It never prints a key.
"""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
PACKAGES = {  # import name -> the name pip knows it by
    "sentence_transformers": "sentence-transformers",
    "chromadb": "chromadb",
    "openai": "openai",
    "dotenv": "python-dotenv",
}
DOCS = ["introduction_to_programming.txt", "data_structures_basics.txt",
        "algorithms_overview.txt", "database_fundamentals.txt",
        "web_development_intro.txt"]


def line(ok: bool, label: str, detail: str = "") -> bool:
    print(f"  [{'ok' if ok else '  '}] {label}{'  — ' + detail if detail else ''}")
    return ok


def main() -> int:
    print("RAG lab setup check\n")
    good = True

    v = sys.version_info
    good &= line(v >= (3, 10), f"Python {v.major}.{v.minor}",
                 "" if v >= (3, 10) else "3.10 or newer required")

    for module, dist in PACKAGES.items():
        try:
            importlib.import_module(module)
            present = True
        except ImportError:
            present = False
        good &= line(present, dist, "" if present else "pip install -r requirements.txt")

    for name in DOCS:
        present = (HERE / "data" / name).is_file()
        good &= line(present, f"data/{name}", "" if present else "missing")

    # Reported, not required: sections 1 and 2 (chunking, embeddings,
    # retrieval) run without any key. Sections 3 to 5 send the retrieved
    # text to a hosted model, and that is what the key is for.
    try:
        from dotenv import load_dotenv
        load_dotenv(HERE / ".env")
    except ImportError:
        pass
    has_key = bool(os.environ.get("LLM_API_KEY"))
    model = os.environ.get("LLM_MODEL", "gemini-3.5-flash-lite")
    line(has_key, "LLM_API_KEY",
         f"set (model: {model})" if has_key else
         "not set — fine for sections 1 and 2; sections 3 to 5 need one. "
         "Free at https://aistudio.google.com/apikey, then: cp .env.example .env")

    print()
    print("Ready." if good else "Something above needs fixing before you start.")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
