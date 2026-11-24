"""The eval for summarise.py: run every test case, check every summary, and print the pass rate.

Run it from the lab folder:   python evals/run_evals.py

Each case in evals/cases.json is an article and the rules a good summary of it must follow. check() tests one
summary in this order, each check on the highest rung of the assertion ladder that still passes every good summary:

  1. property   the summary is not empty
  2. property   the summary has at most max_words words
  3. contains   the summary contains the case's key figure
  4. property   the summary has no word for the opposite direction, such as "fell" for a rise
  5. property   the summary does not repeat the prompt

DIY 7 sets the two numbers below. With RUNS = 1 the script prints one line per case, then the pass rate. With more
runs it prints each run's pass rate, then the average. The script then ends with an exit code: 1 if the average pass
rate is below MIN_PASS_RATE, so that a CI step running this script goes red, and 0 otherwise.
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB))  # lets "import summarise" work when this file is run as python evals/run_evals.py
from summarise import PROMPT, summarise  # noqa: E402  (this import must come after the line above)

RUNS = 1             # DIY 7: how many times to run the whole set
MIN_PASS_RATE = 0.0  # DIY 7: the lowest average pass rate that keeps the build green (0.0 never fails)

WRONG_WAY = {"up": ("fell", "dropped", "was down"), "down": ("rose", "grew", "increased", "was up")}


def check(case, summary):
    """Return None if the summary passes every check, or the reason it fails the first check it fails."""
    if not summary.strip():
        return "empty"
    words = len(summary.split())
    if words > case["max_words"]:
        return f"too long: {words} words"
    if case["figure"] not in summary:
        return f'missing key figure: "{case["figure"]}"'
    for word in WRONG_WAY[case["direction"]]:
        if word in summary:
            return f'wrong direction: "{word}"'
    if PROMPT in summary:
        return "echoed the prompt"
    return None


def run_once(cases, show_each_case):
    """Summarise every case once and return how many summaries passed every check."""
    passed = 0
    for case in cases:
        text = case["input"] if "input" in case else (LAB / case["input_file"]).read_text(encoding="utf-8")
        reason = check(case, summarise(text))
        if reason is None:
            passed += 1
        if show_each_case:
            print(f"  {case['id']}  PASS" if reason is None else f"  {case['id']}  FAIL  ({reason})")
    return passed


def main():
    cases = json.loads((LAB / "evals" / "cases.json").read_text(encoding="utf-8"))
    rates = []
    for run in range(1, RUNS + 1):
        passed = run_once(cases, show_each_case=(RUNS == 1))
        rates.append(passed / len(cases))
        label = "Pass rate" if RUNS == 1 else f"Run {run} pass rate"
        print(f"{label}: {passed}/{len(cases)} ({passed / len(cases):.1%})")
    average = sum(rates) / len(rates)
    if RUNS > 1:
        print(f"Average pass rate: {average:.1%}. The minimum is {MIN_PASS_RATE:.0%}.")
    if average < MIN_PASS_RATE:
        print("Below the minimum: this step fails, so the build goes red.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
