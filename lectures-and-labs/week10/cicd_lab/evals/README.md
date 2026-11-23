# The eval for `summarise.py`

- `cases.json`: the test cases. Each case is an article, and the rules a
  good summary of it must follow: the key figure, the direction (a rise or
  a fall), and the most words. DIY 5 asks you to add one case of your own.
- `run_evals.py`: the eval script. It runs `summarise.py` on every case,
  checks every summary against the case's rules, and prints the pass rate.
  DIY 7 sets its two numbers, `RUNS` and `MIN_PASS_RATE`, and runs it in
  your CI pipeline.

Run it from the lab folder:

```bash
python evals/run_evals.py
```
