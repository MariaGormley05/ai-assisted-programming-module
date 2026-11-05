"""Run calc() from messy_code.py on four lists and compare each answer with
the one the file gave before anyone refactored it.

    python check_refactor.py

Run it before you refactor (four lines of "same") and again after.
"""
import importlib

LISTS = [[10, 20, 30, 40, 50], [-5, -3], [5, 0, 3], []]
BEFORE = [
    "{'avg': 30.0, 'max': 50, 'min': 10, 'sum': 150}",
    "{'avg': -4.0, 'max': 0, 'min': -5, 'sum': -8}",
    "{'avg': 2.6666666666666665, 'max': 5, 'min': 3, 'sum': 8}",
    "ZeroDivisionError",
]


def answer(calc, numbers):
    try:
        return repr(calc(list(numbers)))
    except Exception as e:  # an error is an answer too: compare its name
        return type(e).__name__


def main():
    try:
        module = importlib.import_module("messy_code")
    except Exception as e:
        print(f"messy_code.py does not run: {type(e).__name__}: {e}")
        return
    calc = getattr(module, "calc", None)
    if calc is None:
        print("messy_code.py has no calc() any more: the refactor renamed it.")
        print("Put the file back with  git restore messy_code.py  and ask again.")
        return
    print("calc() on four lists, before the refactor and now:\n")
    changed = 0
    for numbers, before in zip(LISTS, BEFORE):
        now = answer(calc, numbers)
        label = str(numbers)
        if now == before:
            print(f"  {label:22} same")
        else:
            changed += 1
            print(f"  {label:22} CHANGED  before: {before}")
            print(f"  {'':22}          now:    {now}")
    print()
    print("No behaviour change." if not changed else f"Behaviour changed on {changed} of {len(LISTS)} lists.")


if __name__ == "__main__":
    main()
