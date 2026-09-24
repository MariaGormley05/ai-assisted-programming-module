# AIAP Automated Checking Lab

Two halves. Build a pipeline that checks code which behaves the same every
time, then build one that checks something that answers differently on
every run — because any app with an AI feature in it contains both.

## What you'll learn

- Build a GitHub Actions pipeline from nothing and read its output
- Order checks by irreversibility rather than by sophistication
- Put an AI review step in a pipeline without letting it lie to you
- Write an eval suite for a non-deterministic feature
- Use the assertion ladder, and pick the strongest rung a task allows

## Table of Contents

1. [A pipeline from nothing](#1-a-pipeline-from-nothing)
2. [The checks that matter most](#2-the-checks-that-matter-most)
3. [AI inside the pipeline](#3-ai-inside-the-pipeline)
4. [Evals: checking the unrepeatable](#4-evals-checking-the-unrepeatable)
5. [Common mistakes](#common-mistakes)
6. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab and install its dependencies:

   ```bash
   cd lectures-and-labs/week10/cicd_lab
   pip install -r requirements.txt
   ```

3. Confirm the sample app's test passes, then run the app and open the
   port the Codespace forwards:

   ```bash
   python -m pytest
   python -m flask --app startup run
   ```

`hello_app/` is a small Flask application with a working test. It is
deliberately ordinary — the lab is about what you build *around* it.

Section 3 sends a diff to a hosted model from GitHub Actions. It uses the
same free API key you got for the RAG lab, stored in your copy of the repo
as a **repository secret** named `LLM_API_KEY` — nothing in this lab costs
money. Sections 1, 2 and 4 need no key at all.

---

## 1. A pipeline from nothing

A pipeline is a script that runs on a trigger. The only thing that makes
it different from running the commands yourself is that it runs whether or
not you remembered.

### DIY 1: Make it run your tests

1. Create `.github/workflows/ci.yml` in **your own copy** of the repo.
2. Trigger it on `push`.
3. Have it check out the code, set up Python 3.12, install
   `lectures-and-labs/week10/cicd_lab/requirements.txt`, and run `pytest` from `lectures-and-labs/week10/cicd_lab`.
4. Push, and watch it in the **Actions** tab.
5. Now **break a test on purpose**, push, and confirm the run goes red.

**Expected output**

```text
Run python -m pytest
========================= test session starts =========================
collected 1 item

tests/test_app.py .                                             [100%]

========================== 1 passed in 0.4s ===========================
```

<details><summary>Hint</summary>

Step 5 matters more than step 4. A pipeline you have never seen fail is a
pipeline you have no evidence works — plenty of workflows pass because
they silently run nothing.

If the run cannot find your tests, check the working directory: Actions
starts at the repo root, not in the lab folder.

</details>

---

## 2. The checks that matter most

Most people add tests first because tests are what CI is "for". Value per
minute says otherwise.

### DIY 2: Add the cheap checks first

Add three checks to your pipeline, in this order:

1. **Secret scanning** — enable it in Settings → Code security. Confirm
   it is on.
2. **Dependency scanning** — enable Dependabot alerts.
3. **A linter** — add a `ruff` or `pylint` step to `ci.yml`.
4. For each, record in `findings.md`: what it caught, or that it caught
   nothing.
5. Answer: **which of these three could you not undo by pushing a fix?**

**What you should have**

Three checks enabled, and a written answer to step 5 with your reasoning.

<details><summary>Hint</summary>

Step 5 is the whole point of the section. A failing test costs you a red
build; push a fix and it is gone. A leaked credential is not undone by
pushing a fix — the key is out, and it must be rotated.

That asymmetry is why irreversibility, not sophistication, is the right
ordering principle for what you automate.

</details>

---

## 3. AI inside the pipeline

A linter finds style. A compiler finds type errors. Neither can tell you
that a function's name no longer describes what it does.

`review_diff.py` in this folder is the starter for this section. It reads
a diff, sends it to a model with a prompt that asks only for the things a
compiler **cannot** check, prints the findings — and exits non-zero on
*any* failure (no key, no diff, an HTTP error, an empty answer), because a
review that could not run must go red, not green.

### DIY 3: A review step that cannot lie

1. Add the free API key from the RAG lab to your copy of the repo as a
   repository secret named `LLM_API_KEY` (Settings → Secrets and
   variables → Actions).
2. Add a second workflow, `.github/workflows/review.yml`, that runs on
   pull requests, diffs the branch against its base, and runs the starter
   on that diff:

   ```yaml
   name: review
   on: [pull_request]
   jobs:
     review:
       runs-on: ubuntu-latest
       permissions:
         contents: read
         pull-requests: write
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0
         - name: Review the diff, and fail if the review could not run
           env:
             LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
           run: |
             git fetch --quiet origin ${{ github.base_ref }}
             git diff origin/${{ github.base_ref }}...HEAD > pr.diff
             python lectures-and-labs/week10/cicd_lab/review_diff.py pr.diff | tee review.md
         - name: Post the findings as a comment
           env:
             GH_TOKEN: ${{ github.token }}
           run: gh pr comment ${{ github.event.pull_request.number }} --body-file review.md
   ```

3. It posts its findings as a **comment**, not a commit — the last step
   above. Keep it that way.
4. Open a pull request with a deliberately badly-named function and
   confirm the review notices.
5. Now break the secret on purpose — rename it, or set it to nonsense —
   and confirm the job goes **red** rather than reporting a clean review.

**What you should have**

A review job that comments on pull requests, and evidence from step 5 that
a broken run goes red instead of green.

<details><summary>Hint</summary>

Step 5 is the one that separates a useful review job from a decorative
one. The failure mode is a job that catches its own exception, writes the
error text into the report, and exits zero — leaving a green tick over a
check that never ran. The starter refuses to do that; if you write your
own, keep that property. Actions runs each `run:` step with `pipefail`, so
`python review_diff.py | tee` fails the step when the script fails.

Never ask it whether the code compiles. A compiler answers that exactly;
a model guesses.

</details>

---

## 4. Evals: checking the unrepeatable

`summarise.py` in this folder wraps a small summarising feature. Same
input, different output. Everything you know about testing assumes that
cannot happen.

### DIY 4: Watch assertEqual fail on a good answer

1. In `tests/test_summary.py`, write `test_exact`: a test asserting the
   summary of `samples/article_1.txt` equals a fixed string you got from
   one run.
2. Run it. It passes.
3. Run it again. And again.
4. Record what happens and why.

**Expected output**

```text
FAILED tests/test_summary.py::test_exact
  AssertionError: assert 'Revenue rose 12% on renewals.'
                      == 'Revenue grew 12% year on year.'
```

<details><summary>Hint</summary>

Both strings are correct summaries. The test is not detecting a bug — it
is asserting something that was never true: that the output is fixed.

This is the moment the rest of the section exists to solve. Do not fix the
test yet.

</details>

### DIY 5: Climb the assertion ladder

Replace that test with property checks that are true of **any** acceptable
summary.

1. Build a set of at least **eight** cases in `evals/cases.json`, each
   with an input and the properties its output must satisfy.
2. Write `evals/run_evals.py` to score the set and print a **pass rate**,
   not pass/fail.
3. Use the strongest rung each property allows:
   - non-empty · under a length limit · mentions the key figure · says
     which way the figure moved · does not echo the prompt back
4. Run it and record the rate.

**Expected output**

```text
Running 8 cases

  case-01  PASS
  case-02  PASS
  case-03  FAIL  (missing key figure: "12%")
  ...

Pass rate: 7/8 (87.5%)
```

<details><summary>Hint</summary>

Property checks are cheap, deterministic and repeatable, and they catch
the failures that actually happen: empty output, runaway length, the
prompt echoed back, the one number that mattered dropped, "fell" where the
article said "rose". Run the set more than once — a rate from one run of
a non-deterministic feature is a single sample.

Reach for a model-as-judge only for the residue no property can express —
and if you do, ask it for the **reason** as well as the score.

</details>

### DIY 6: Prove a change helped

1. Note your current pass rate.
2. Change `PROMPT` at the top of `summarise.py` — try to improve it. The
   stand-in model understands a short list of instructions, documented at
   the top of that file: mention the figure, mention the direction, set a
   word limit, ask for two sentences. A real model understands far more,
   far less predictably — which is why you measure.
3. Re-run the whole set, more than once.
4. Record the before and after rates.
5. Answer honestly: **did it improve, get worse, or move cases around?**

**What you should have**

Two pass rates and an honest verdict, including any case that got *worse*
while others improved.

<details><summary>Hint</summary>

The interesting result is when the rate is unchanged but different cases
fail. That is exactly what tuning against two or three examples does to
you, and it is invisible without a set. A word limit is the classic case:
the figure survives and the qualifier a case wanted does not.

If your rate went to 100%, add harder cases. An eval suite everything
passes has stopped telling you anything.

</details>

---

## Common mistakes

- **Adding a test suite before secret scanning.** Order by what you cannot
  undo.
- **Never watching the pipeline fail**, so you have no evidence it works.
- **Letting a failed model call report "no findings"** — a green tick over
  a check that never ran is worse than no check.
- **Asserting equality on non-deterministic output**, then concluding the
  feature is broken.
- **Reaching for a judge** where a property check would have been exact,
  cheap and deterministic.
- Tuning a prompt against the cases you happened to look at.

## Summary

- A pipeline is a script with a trigger; the value is that it runs when
  you forget.
- Order checks by **irreversibility** — secret scanning beats a test suite
  for value per minute.
- Ask AI what a compiler **cannot** check, and make a failed call a
  **failure**.
- Non-deterministic features need a **set** and a **rate**, not an
  assertion.
- Climb the ladder: exact → contains → structural → property → judge. Use
  the strongest rung the task allows.
- Without a measured set, prompt tuning is folklore.
