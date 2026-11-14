# AIAP CI/CD & Evals Lab

This lab has two halves. In the first you build **CI**: checks that GitHub
runs by itself on every change you push, for code that behaves the same on
every run. In the second you build an **eval**: a way to test a feature
that answers differently on every run, as anything built on an AI model
does. An app with an AI feature in it needs both.

## What you'll learn

- Build a GitHub Actions workflow that runs your tests on every push, and
  watch it fail on purpose
- Put first the checks that catch a mistake a later push cannot undo, such
  as a leaked key
- Add an AI review to pull requests that goes red when the review could
  not run
- Test a feature whose output changes on every run with an eval: a set of
  cases, scored as a pass rate
- Pick the most exact check that still accepts every good answer, using
  the assertion ladder (a ranking of checks from exact match to asking
  another model)

## Table of Contents

1. [A pipeline from nothing](#1-a-pipeline-from-nothing)
2. [The checks that matter most](#2-the-checks-that-matter-most)
3. [AI inside the pipeline](#3-ai-inside-the-pipeline)
4. [Evals: testing output that changes every run](#4-evals-testing-output-that-changes-every-run)
5. [Common mistakes](#common-mistakes)
6. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab and install its dependencies:

   ```bash
   cd lectures-and-labs/week10/cicd_lab
   pip install -r requirements.txt
   ```

3. Confirm the sample app's test passes, then run the app:

   ```bash
   python -m pytest
   python -m flask --app startup run
   ```

   To see the app, open the **PORTS** tab next to the terminal and click
   the globe icon beside port 5000. Press `Ctrl+C` in the terminal to stop
   the app.

4. Open the chat panel with `Ctrl+Alt+I` (`Ctrl+Cmd+I` on a Mac) and
   choose **Copilot** as the session. Every step that uses the assistant
   names the role to pick in the agent picker: **Ask** reads your files
   and answers, but cannot edit a file or run a command that changes
   anything; **Agent** edits files straight away and asks before it runs a
   command. Leave the mode and permissions controls on their defaults,
   **Interactive** and **Manual permissions**. If your picker uses other
   names, look for the read-only one and the one that asks first.

*Fresh conversation* means press the `+` at the top of the chat panel
first.

`hello_app/` is a small Flask application with a working test. It is
deliberately ordinary: the lab is about what you build *around* it.

Section 3 sends a diff (the lines a change adds and removes) to a hosted AI
model from GitHub Actions. That section needs a free Gemini API key, stored
in your copy of the repo as a **repository secret** named `LLM_API_KEY`;
DIY 3 shows how. Nothing in this lab costs money, but on the free tier
Google may use what you send to improve its products, so send it nothing
personal. Sections 1, 2 and 4 need no key.

---

## 1. A pipeline from nothing

A **pipeline** is a list of checks that runs by itself whenever something
happens, such as a push. You could run the same commands yourself; the
pipeline runs them every time, whether or not you remember.

Running a pipeline on every change is **CI**, continuous integration.
**CD**, continuous delivery, also ships the change once the checks pass;
this lab builds the checking half. On GitHub, **GitHub Actions** runs
pipelines. You describe one in a **workflow**: a YAML file (plain text,
indented `key: value` lines) in `.github/workflows/` at the top of your
repository. A workflow holds **jobs**. GitHub runs each job on a fresh
Linux machine with nothing on it, not even your code, and the job works
through its **steps** in order. A step runs a command (`run:`) or a
ready-made action that someone has published (`uses:`); the action
`actions/checkout`, for example, copies your code onto the machine. When a
step fails, the job turns red and the later steps do not run.

### DIY 1: Make it run your tests

1. Fresh conversation, **Agent**. Type:

   ```text
   Create .github/workflows/ci.yml at the root of this repository: a GitHub
   Actions workflow that runs on every push, checks out the code, sets up
   Python 3.12, installs lectures-and-labs/week10/cicd_lab/requirements.txt
   and runs python -m pytest in lectures-and-labs/week10/cicd_lab.
   ```

2. Open the file Agent made. Check that it is in `.github/workflows/` at
   the top of the repo, not inside the lab folder, and that it has the four
   steps the prompt asked for; the hint has a version to compare it with.
3. Commit and push the workflow. These commands work from any folder in the
   repo (`:/` means "from the top of the repo"):

   ```bash
   git add :/.github
   git commit -m "Add a CI workflow"
   git push
   ```

4. On GitHub, open your repo's **Actions** tab and the newest run named
   **ci**. Click its job, then the `python -m pytest` step, to read the
   log.
5. Break the test on purpose: in `tests/test_app.py`, change `200` to
   `404`, then commit and push the change:

   ```bash
   git commit -am "Break the test on purpose"
   git push
   ```

   Confirm that the new **ci** run goes red and that its log names the
   failing line.
6. Change `404` back to `200`, commit and push the same way, and confirm
   the next **ci** run is green again.

**Expected output**

The `python -m pytest` step of a green run:

```text
Run python -m pytest
============================= test session starts ==============================
platform linux -- Python 3.12.x, pytest-9.x.x, pluggy-1.x.x
rootdir: /home/runner/work/<your-repo>/<your-repo>/lectures-and-labs/week10/cicd_lab
collected 1 item

tests/test_app.py .                                                      [100%]

============================== 1 passed in 0.4s ===============================
```

<details><summary>Hint</summary>

Step 5 matters more than step 4. A pipeline you have never seen fail gives
you no evidence that it works: plenty of workflows pass because they
quietly run nothing.

A working `ci.yml` looks like this. Agent's version may use other names or
versions and still be right:

```yaml
name: ci
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - run: pip install -r lectures-and-labs/week10/cicd_lab/requirements.txt
      - run: python -m pytest
        working-directory: lectures-and-labs/week10/cicd_lab
```

No run in the Actions tab at all? GitHub reads workflows only from
`.github/workflows/` at the top of the repo, so the file is in the wrong
folder.

If the run fails with `No module named 'hello_app'`, check the step's
working directory (the folder it runs in), and that it runs
`python -m pytest` rather than `pytest`. GitHub Actions starts in the repo
root, not in the lab folder, and only `python -m` puts the current folder
on the import path, where the test finds `hello_app`.

Other runs in the Actions tab are not yours: the course's **marp** runs
show as skipped, and a **security** workflow from an earlier lab may end
red. Read the run named **ci**.

If `git push` is refused with a message about `workflows` permission, make
the change on GitHub's website instead (**Add file → Create new file**, or
the pencil icon on a file), then run `git pull` in the Codespace.

</details>

---

## 2. The checks that matter most

Most people add tests first. Some checks take minutes to add, though, and
catch mistakes that pushing a fix cannot undo, so they come first:

- **Secret scanning** looks through your commits for anything shaped like
  a password or an API key.
- A **linter** reads code without running it and reports likely mistakes,
  such as an import that nothing uses.
- **Dependency scanning** compares the packages your requirements files
  name with security advisories: published notices that a version of a
  package has a known flaw.

### DIY 2: Add the cheap checks first

1. **Secret scanning.** GitHub's own scanner is for public repos and paid
   plans, and your copy is private, so add **gitleaks** to `ci.yml`
   instead. Give the checkout step `fetch-depth: 0`, and put the gitleaks
   step straight after it:

   ```yaml
         - uses: actions/checkout@v7
           with:
             fetch-depth: 0
         - uses: gitleaks/gitleaks-action@v3
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
   ```

2. **A linter.** Add this step after the step that sets up Python:

   ```yaml
         - name: Lint the lab with ruff
           run: pip install ruff==0.15.1 && ruff check lectures-and-labs/week10/cicd_lab
   ```

3. Commit and push (`git commit -am "Add gitleaks and ruff"`, then
   `git push`). In the new **ci** run, the gitleaks step should be green
   and the ruff step red: ruff reports `F401` findings, its code for an
   import that nothing uses.
4. Fresh conversation, **Ask**. Paste the ruff step's log and type:
   *"Explain this log from my GitHub Actions run. Which of these unused
   imports can I delete without breaking the app?"*
5. Fix the findings. Delete the unused `Flask` import in
   `hello_app/views.py` and the line `import pytest` in
   `tests/test_app.py`. Add `# noqa: F401`, a comment that tells ruff to
   skip that finding on that line, to the end of the other three import
   lines: two in `hello_app/webapp.py`, one in `startup.py`. The app needs
   those three (the hint says why). Did Ask agree? Run `python -m pytest`,
   then commit and push: every step of the **ci** run should now be green.
6. **Dependency scanning.** On GitHub, open **Settings → Advanced Security**
   and click **Enable** next to **Dependabot alerts** (Dependabot is
   GitHub's dependency scanner). After a few minutes, open the **Security**
   tab, then **Dependabot**.
7. **Which of these three checks catches something you could not undo by
   pushing a fix?** Decide, then open the hint.

**What you should have**

A **ci** run with every step green: gitleaks says `No leaks detected`, ruff
says `All checks passed!` and pytest says `1 passed`. Also Dependabot's
alerts page, with whatever it found; finding nothing is a result too.

<details><summary>Hint</summary>

Step 7 is the point of the section. A failing test costs you a red run;
push a fix and it is gone. A leaked key is not undone by pushing a fix: the
key is already out, in the history and possibly copied, so it must be
**rotated**: cancelled and replaced with a new one. That is why checks are
ordered by what cannot be undone, not by how sophisticated they are.

`fetch-depth: 0` matters: gitleaks scans every commit in the push, so it
needs the history. Without it, a push of more than one commit turns the
step red and its log says `unknown revision`.

The three imports in step 5 look unused, but each does a job.
`from . import views` in `webapp.py` loads `views.py`, which registers the
app's pages; the two `import app` lines make `app` available to the test
and to `flask --app startup run`. So do not clear the findings with
`ruff check --fix`: it deletes all five imports, and the test then fails.
Assistants often miss this too. Point ruff at the lab folder, as in step 2:
`ruff check .` from the repo root lints every other lab as well.

The step pins ruff's version with `==0.15.1`. Newer versions also check the
order of imports and report `I001` findings, so a tool left to update
itself can turn a pipeline red with no change to your code. Pin the version
of every tool a pipeline installs.

Your `ci.yml` should now look like this:

```yaml
name: ci
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Lint the lab with ruff
        run: pip install ruff==0.15.1 && ruff check lectures-and-labs/week10/cicd_lab
      - run: pip install -r lectures-and-labs/week10/cicd_lab/requirements.txt
      - run: python -m pytest
        working-directory: lectures-and-labs/week10/cicd_lab
```

The workflow runs on `push` only. If you add `pull_request` to its
triggers, also give the job `permissions:` with `contents: read` and
`pull-requests: read`: on a pull request, gitleaks lists the request's
commits, which needs the `GITHUB_TOKEN` line above and a token allowed to
read pull requests, which the default token of a private repo is not.

gitleaks needs no licence key in a copy under your own account. In a copy
that belongs to an organisation it asks for a free one, passed to the step
as `GITLEAKS_LICENSE`.

Most of Dependabot's alerts are likely to be about `mcp==1.26.0`, which the
MCP lab pins on purpose. If Dependabot opens a pull request to update it,
do not merge that pull request.

</details>

---

## 3. AI inside the pipeline

A linter finds style problems and some mistakes, and a compiler (for
Python, the interpreter) rejects code that cannot run. Neither can tell you
that a function's name no longer describes what the function does.

A **pull request** asks to merge the commits on one branch into another,
and GitHub shows its diff for review. `review_diff.py` in this folder reads
a diff, sends it to a model with a prompt that asks only for what a
compiler **cannot** check, and prints the findings. The script ends with a
non-zero exit code (the number a program returns to say it failed) on
*any* failure: no key, no diff, an HTTP error, an empty answer. A review
that could not run must go red, not green.

### DIY 3: A review step that cannot lie

1. Get a free Gemini API key at
   [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   signed in with a Google account, or reuse one from an earlier lab's
   `.env` file. On GitHub, open
   **Settings → Secrets and variables → Actions**, click
   **New repository secret**, name it `LLM_API_KEY` and paste the key.
   GitHub keeps a repository secret encrypted and gives it only to a
   workflow that asks for it by name.
2. Add a second workflow, `.github/workflows/review.yml`, next to
   `ci.yml`, and commit and push it as in DIY 1, step 3. On every pull
   request it diffs the branch against the branch it would merge into,
   runs the starter on that diff, and posts the findings as a comment,
   never as a commit: a review should not change your code.

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
         - uses: actions/checkout@v7
           with:
             fetch-depth: 0
         - name: Review the diff, and fail if the review could not run
           env:
             LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
           shell: bash
           run: |
             git fetch --quiet origin ${{ github.base_ref }}
             git diff origin/${{ github.base_ref }}...HEAD > pr.diff
             python lectures-and-labs/week10/cicd_lab/review_diff.py pr.diff | tee review.md
         - name: Post the findings as a comment
           env:
             GH_TOKEN: ${{ github.token }}
           run: gh pr comment ${{ github.event.pull_request.number }} --body-file review.md
   ```

3. Open a pull request with a deliberately badly named function. Start a
   branch:

   ```bash
   git switch -c bad-name
   ```

   In `hello_app/views.py`, rename the function `get_data` to
   `delete_all_users`. The function still only returns data, so its name
   now lies. Then commit and push the branch:

   ```bash
   git commit -am "Rename get_data"
   git push -u origin bad-name
   ```

   `git push` prints a link ending in `/pull/new/bad-name`. Open it and
   click **Create pull request**.
4. Wait for the **review** check to finish, then read its comment on the
   pull request's **Conversation** tab. Does the review name
   `delete_all_users`?
5. Now break the secret on purpose. In
   **Settings → Secrets and variables → Actions**, edit `LLM_API_KEY` and
   replace the key with nonsense. Then make the review run again with an
   empty commit:

   ```bash
   git commit --allow-empty -m "Run the review again"
   git push
   ```

   Confirm that the **review** check goes **red** instead of posting a
   clean review, and that its log ends with a line starting `review_diff:`.
6. Put the real key back in the secret. Close the pull request without
   merging it, and go back to your main branch with `git switch main`.

**What you should have**

A review comment on the pull request and, after step 5, a red **review**
check whose log ends with a `review_diff:` line that says why the review
could not run.

<details><summary>Hint</summary>

Step 5 separates a useful review job from a decorative one. The failure to
avoid is a job that catches its own error, writes the error text into the
report and exits with 0, leaving a green tick over a check that never ran.
The starter refuses to do that; if you write your own, keep that property.

That is why the review step says `shell: bash`. GitHub Actions turns on
`pipefail`, which makes a chain of commands joined by `|` fail when any of
them fails, only for a step that says `shell: bash`. Without it,
`python review_diff.py | tee review.md` (`tee` copies the output to a file
as well as to the screen) ends with `tee`'s exit code, 0, and the step
stays green when the script fails.

If the review missed the bad name in step 4, run it again with the empty
commit from step 5, before you break the key. A review is a sample too:
the same diff can get a different answer.

Never ask the model whether the code compiles. A compiler answers that
exactly; a model guesses.

If you use a provider other than Gemini, add `LLM_BASE_URL` and
`LLM_MODEL` as repository secrets too, and pass them in the `env:` block
next to the key. A secret you never created reaches the script as an empty
string, and the script then uses its Gemini default.

Pull requests that Dependabot opens cannot read your repository secrets,
so the review check goes red on them: the step 5 behaviour, working as
intended.

</details>

---

## 4. Evals: testing output that changes every run

`summarise.py` in this folder is a small summarising feature with a
stand-in model: a short program that behaves like an AI model, so the same
article gets a different summary on each run. Every test you have written
so far assumes that the same input gives the same output.

An **eval** (short for evaluation) runs a set of test cases against a
feature like this, many times, and scores it as a **pass rate**: the share
of cases whose output passed every check, such as 5/6. The **assertion
ladder** says which check to use. Its rungs run from the most exact, at the
top, to the least:

| Rung | What it checks | Example for a summary |
|---|---|---|
| Exact match | The output equals one fixed string | `summary == "Revenue grew 12%."` |
| Contains | A key fact appears in the output | `"12%" in summary` |
| Structural | The output has the right shape | one sentence; valid JSON |
| Property | Something true of every good answer | at most 25 words; no "fell" when the article says rose |
| Model-as-judge | Another model scores the output and gives a reason | "Is every claim supported by the article?" |

Use the highest rung that still accepts every good answer. A summary rules
out exact match, so the figure is a contains check, the length and the
direction are properties, and a judge is kept for what no rule can
express.

### DIY 4: Watch an equality test fail a good answer

1. Run the summariser on the first sample three times:

   ```bash
   python summarise.py samples/article_1.txt
   ```

2. Create `tests/test_summary.py` with this test, and paste one of the
   lines you got between the quotes:

   ```python
   from pathlib import Path

   from summarise import summarise


   def test_exact():
       text = Path("samples/article_1.txt").read_text(encoding="utf-8")
       assert summarise(text) == "PASTE ONE LINE FROM STEP 1 HERE"
   ```

3. Run the test four or five times with `python -m pytest tests/test_summary.py`.
   The test almost always fails; a pass is luck.
4. In each failure, the line starting `-` is your fixed string and the line
   starting `+` is what this run wrote; a line starting `?` only marks
   where the two differ. Is either of them a wrong summary?

**Expected output**

```text
>       assert summarise(text) == "Revenue was up 12% year on year."
E       AssertionError: assert 'Revenue grew 12%.' == 'Revenue was ...year on year.'
E
E         - Revenue was up 12% year on year.
E         + Revenue grew 12%.

tests/test_summary.py:8: AssertionError
```

<details><summary>Hint</summary>

Usually both strings are good summaries, worded differently. Then the test
is not detecting a bug: it asserts something that was never true, that the
output is fixed.

Sometimes one of them really is wrong: no 12%, or "fell" or "dropped" for a
rise. The stand-in does that on purpose, a little more than one run in
three with the prompt as shipped. An equality test fails both kinds the
same way, so it cannot tell you which one you got. DIY 5 can.

Do not fix this test; DIY 5 replaces it.

</details>

### DIY 5: Climb the assertion ladder

Replace the equality test with checks that are true of **every** acceptable
summary.

1. Delete `tests/test_summary.py`. The test has done its job, and left in
   place it would turn your **ci** run red on most pushes.
2. Create `evals/cases.json` with six cases: `samples/article_1.txt`,
   `samples/article_2.txt`, and four short articles of your own about
   something that rose. Start from this case:

   ```json
   [
     {
       "id": "case-01",
       "input_file": "samples/article_1.txt",
       "figure": "12%",
       "direction": "up",
       "max_words": 25
     }
   ]
   ```

   For your own articles, put the text itself in `"input"` instead of
   `"input_file"`. Write them so the stand-in can read them: the thing that
   changed as the first word, and the figure that matters as the first
   number, as in *"Signups rose 30% after the redesign."*
3. Fresh conversation, **Agent**. Type:

   ```text
   Write evals/run_evals.py. It reads evals/cases.json, calls summarise()
   from summarise.py once for each case, and checks the summary in this
   order: it is not empty; it has at most max_words words; it contains the
   case's figure; if direction is "up" it contains none of fell, dropped,
   was down, and if "down" none of rose, grew, increased, was up; it does
   not contain PROMPT from summarise.py. Print one line per case, such as
   "case-01  PASS" or "case-02  FAIL  (missing key figure: "40%")", then a
   last line such as "Pass rate: 5/6 (83.3%)". It must run from the lab
   folder with: python evals/run_evals.py
   ```

4. Run the set from the lab folder three times. Does the rate stay the
   same?

   ```bash
   python evals/run_evals.py
   ```

**Expected output**

Your lines and your rate will differ, and they change from run to run:

```text
  case-01  PASS
  case-02  FAIL  (missing key figure: "40%")
  case-03  PASS
  case-04  FAIL  (wrong direction: "fell")
  case-05  PASS
  case-06  PASS

Pass rate: 4/6 (66.7%)
```

<details><summary>Hint</summary>

Each check sits on the highest rung that still passes every good summary:
the figure is a contains check, and empty output, the length, the
direction words and an echoed prompt are properties. Property checks are
cheap, give the same verdict on the same output every time, and catch the
failures that actually happen: empty output, runaway length, the prompt
echoed back, the one number that mattered dropped, "fell" where the
article said "rose".

The stand-in is simple on purpose. It takes the first word of the article
as the subject and the first number as the key figure, and it writes every
change as a rise; when it slips, it writes fell, dropped or was down
instead. That is why your own articles start with the thing that changed,
put the figure first, and rose.

With the prompt as shipped, each case passes about five runs in eight, so
most runs land between 3/6 and 5/6. A rate from one run is a single
sample.

If `python evals/run_evals.py` stops with
`ModuleNotFoundError: No module named 'summarise'`, the runner is looking
in the wrong folder: Python puts the script's own folder, `evals/`, on the
import path, not the lab folder. These lines at the top of `run_evals.py`
fix it:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```

Now run the stand-in on `samples/article_3.txt` a few times. You will see
summaries such as *"The main point is that The increased by 23 across all
regions."* The summary mentions 23 and it is short, so the property checks
pass it, yet it makes no sense: "The" is not a subject, the 23 services
were removed rather than added, and the article never mentions regions.
That is the kind of failure a model-as-judge is for: give the judge the
article, ask whether every claim in the summary is supported by it, and ask
for its **reason** as well as its score.

</details>

### DIY 6: Prove a change helped

1. Run the whole set five times and keep the output:

   ```bash
   for run in 1 2 3 4 5; do python evals/run_evals.py; done > before.txt
   ```

2. Change `PROMPT` at the top of `summarise.py` to try to improve it. The
   stand-in understands only the instructions listed at the top of that
   file: mention the figure, mention the direction, set a word limit
   ("under 10 words"), ask for two sentences. A real model understands far
   more, far less predictably, which is why you measure.
3. Run the set five times again, into a second file:

   ```bash
   for run in 1 2 3 4 5; do python evals/run_evals.py; done > after.txt
   ```

4. Put the two side by side: the ten pass rates, then how often each case
   failed, and why, before and after. Each line of the counts is one case
   and one reason, so a case that failed for two reasons appears twice.

   ```bash
   grep "Pass rate" before.txt after.txt
   grep -h FAIL before.txt | sort | uniq -c
   grep -h FAIL after.txt | sort | uniq -c
   ```

5. Did the change improve the set, make it worse, or move the failures to
   other cases or other reasons?
6. Put the prompt back as it was shipped:

   ```bash
   git restore summarise.py
   ```

**What you should have**

Five pass rates from before the change and five from after, and each
case's failures counted on both sides, including any case that got *worse*
while others improved.

<details><summary>Hint</summary>

The counts tell you more than the rate. Mention only the figure in the
prompt, for example, and the "missing key figure" lines disappear while
the "wrong direction" lines stay. Two or three examples checked by eye
would never show you that.

A word limit cuts the summary from the end, so it can cut the figure off
too: with "under 6 words", about half the summaries of `article_1.txt` lose
the 12%.

If your rate reached 100%, add a case about something that fell, with
`"direction": "down"`, such as *"Costs fell 8% after the switch to a new
supplier."* The stand-in writes a rise for every article, so that case
fails nearly every run, and every run once the prompt mentions the
direction: a case that got worse while the others improved. Finding a
failure that no prompt fixes is what an eval set is for. A set that every
case passes has stopped telling you anything.

Five runs of six cases is a small sample. If before and after look close,
run 20 of each:
`for run in $(seq 20); do python evals/run_evals.py; done > before.txt`.

</details>

---

## Common mistakes

- **Adding a test suite before secret scanning.** A failing test is fixed
  by the next push; a leaked key is not.
- **Never watching the pipeline fail**, so you have no evidence that it
  works.
- **Letting a failed model call report "no findings".** A green tick over
  a check that never ran is worse than no check.
- **Asserting equality on output that changes every run**, then deciding
  the feature is broken.
- **Reaching for a model-as-judge** where a property check would have been
  exact, cheap and repeatable.
- Tuning a prompt against the few cases you happened to look at.

## Summary

- A pipeline runs your checks on every push, whether or not you remember.
  GitHub Actions runs one from a workflow file in `.github/workflows/`.
- Put first the checks that catch what a later push cannot undo: secret
  scanning before a test suite.
- Ask an AI reviewer only what a compiler **cannot** check, and make a
  review that could not run go **red**.
- A feature whose output changes on every run needs a **set** of cases and
  a **pass rate**, not one equality test.
- Use the highest rung of the assertion ladder that still accepts every
  good answer: exact match, contains, structural, property, then a
  model-as-judge.
- Without a measured set, you cannot tell whether a prompt change helped.
