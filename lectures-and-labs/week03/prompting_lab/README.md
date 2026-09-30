# AIAP Prompting Lab

Nine short tasks with the assistant. In each one you change how you ask, or
what it can see, and something other than your eyes shows you what that
changed: a checker, a test, or `git diff`. Nothing is written down and
nothing is handed in.

## What you'll learn

- Make the decisions in a prompt yourself, and see which ones a vague prompt made for you
- Keep a change small with non-goals, and measure how small it was
- Get the model's questions before its code, and answer them with facts only you have
- Find out what a persona, "step by step" and examples really change, with a checker
- Tell a wording problem from a knowledge problem, and put the right things in front of the model
- Write context once: a test before the code, and an instructions file every conversation reads

## Table of Contents

1. [Say what you want](#1-say-what-you-want)
2. [Let it ask](#2-let-it-ask)
3. [Three techniques, tested](#3-three-techniques-tested)
4. [What it can see](#4-what-it-can-see)
5. [Common mistakes](#common-mistakes)
6. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo. If VS Code
   asks whether you trust the authors of the files, choose **Yes**.
2. Move into this lab:

   ```bash
   cd lectures-and-labs/week03/prompting_lab
   pip install -r requirements.txt
   ```

3. See where you are. This runs every check in the lab and changes
   nothing, so run it whenever you like:

   ```bash
   python check.py
   ```

4. Open the chat panel with `Ctrl+Alt+I` (`Ctrl+Cmd+I` on a Mac). Every
   step that talks to the assistant names a **mode**: **Interactive** reads
   your files and asks before it runs a command or changes a file;
   **Plan** reads and thinks but changes nothing. This lab never needs
   **Autopilot**.

*Fresh conversation* means press the `+` at the top of the chat panel
first. The files the tasks change are in `lab/code/`, and any of them can
be put back as you received it with `git restore`, which the steps use.
Several tasks end with a **hunt**: the same prompt on two or three other
models from the model picker, to see which one you can catch out.

---

## 1. Say what you want

### DIY 1: Slugify on a trap

A slug is the part of a web address made from a title: `Ireland's Best`
becomes something like `irelands-best`. Simple, until you look closely.

1. Fresh conversation, **Interactive**:

   > Write a Python function slugify(title) that turns a blog post title
   > into a URL-safe slug. Put it in a new file called slug_a.py in the
   > prompting_lab folder.

   Allow it to create the file.
2. Now make the decisions yourself. Fresh conversation, **Interactive**.
   Fill in the three blanks before you send it:

   > Write a Python function slugify(title: str) -> str in a new file
   > called slug_b.py in the prompting_lab folder. Lower case, words joined
   > by single hyphens, no hyphen at either end, no external libraries.
   > Apostrophes, straight or curly: ___. Accented letters and ß: ___.
   > If no letters or digits are left: ___.

   For example: *dropped, so Ireland's becomes irelands*, then *turned
   into plain letters, so é becomes e and ß becomes ss*, then *raise
   ValueError*. Your choices, not these, are the point.
3. Let the checker put both on twelve awkward titles:

   ```bash
   python check.py slug slug_a slug_b
   ```

4. Read the rows where the two disagree: each is a decision the first
   prompt left open that something made anyway. Then read the rows where
   they agree. Is every one of those what you would have chosen?
5. **The hunt.** Switch model and, in a fresh conversation in
   **Interactive**, send the step 1 prompt again into `slug_c.py`; then a
   third model into `slug_d.py`, and run the checker
   on all four; it takes any number of names. Which model would you trust
   to name your blog posts?

**What you should have**

A table like this one, a column per file. Yours will differ, and the
differences are the point:

```text
title                     slug_a                  slug_b
Ireland's Best            irelands-best           irelands-best           an apostrophe: dropped, or a word break?
Tom & Jerry               tom-jerry               tom-and-jerry           is & dropped, or spelt 'and'?
Über Straße               uber-strae              uber-strasse            ß: 'ss', or dropped?
!!!                       (empty)                 ERROR:ValueError        nothing survives
...
6 of 12 titles split them. Each split is a decision one prompt made and another left open.
```

<details><summary>Hint</summary>

Tested in September 2026, five current models given the step 1 prompt
agreed on most titles and split on three: the apostrophe (`irelands-best`
against `ireland-s-best`) and two titles with accents, where one model
lost the accented letters altogether (`caf-au-lait`). None of the five
turned `ß` into `ss`, and all five turned `!!!` into an empty slug. Agreement is not correctness: when every model
makes the same choice, the choice was still made by nobody.

The blanks in step 2 are what make it a better prompt. It is not better
because it is longer; it is better because it makes the decisions, and
every blank you fill is one the model no longer makes for you.

</details>

### DIY 2: Count the lines it changed

`lab/code/receipt.py` has a one-line bug: `calculate_total` stops one item
early. Fixing it needs one changed line.

1. See the bug:

   ```bash
   python check.py receipt
   ```

2. Open `lab/code/receipt.py` in the editor. Fresh conversation,
   **Interactive**, exactly this:

   > here's my file, fix the bug in calculate_total

   Allow the edit.
3. Run the checker again. It now also counts the lines changed since your
   last commit. Then read every one of them:

   ```bash
   python check.py receipt
   git diff lab/code/receipt.py
   ```

4. Put the file back as it was, and ask narrowly this time:

   ```bash
   git restore lab/code/receipt.py
   ```

   Fresh conversation, **Interactive**:

   > Fix only the off-by-one in calculate_total in receipt.py. Change
   > nothing else: no formatting, no type hints, no error handling, no
   > comments.

   Run the two commands from step 3 again.
5. **The hunt.** `git restore` the file and give the step 2 prompt to two
   other models, each in a fresh conversation in **Interactive**,
   restoring between them. Which one changed the most, and
   what did it change that you never asked for?

**Expected output**

After the narrow prompt:

```text
calculate_total, with 23% tax:
  two items  ok
  one item   ok
  no items   ok

lines changed in receipt.py since your last commit: +1 -1

Every item counted.
```

<details><summary>Hint</summary>

Measured in September 2026 through three vendors' APIs, the vague prompt
changed 1 line with one model, 3 with another, and 11 then 4 with a third
on two runs: a rewritten loop, new comments, the whole file sent back.
Through five models from the Copilot picker it changed 1 to 4 lines. The
narrow prompt changed exactly one line every time it was tried. None of
them added type hints or error handling; the old warning that assistants
rewrite everything is folklore. The real point is smaller and sharper:
without non-goals, the size of the change is not yours to decide.

It matters because of review. You will read a one-line diff; you will
skim an eleven-line one, and the change you did not ask for is the one
nobody reads.

</details>

---

## 2. Let it ask

### DIY 3: Make it ask first

`lab/code/rates.py` gets exchange rates from a slow service: every call
takes a second. A cache sounds like one line of work. It is several
decisions, and some of them depend on facts that are not in the code.

1. See it:

   ```bash
   python check.py rates
   ```

2. Open `lab/code/rates.py`. Fresh conversation, **Plan**:

   > I want to add caching to get_rate in rates.py. Do not write any code
   > yet. List the questions you would need answered first, most important
   > first.

3. Read its questions. Which of them would you not have thought to answer?
4. Here are the facts it cannot find in the code. Switch the mode to
   **Interactive**, stay in the same conversation, and answer:

   > Past days never change, so cache them for good. Today's rate is
   > revised during the day, so never keep it for more than an hour. Keep
   > at most 1,000 rates. Take the time from now() in the same file. Now
   > add the cache, and change nothing else.

5. Check it:

   ```bash
   python check.py rates
   ```

6. **The contrast.** Put the file back, and ask the way most people do:

   ```bash
   git restore lab/code/rates.py
   ```

   Fresh conversation, **Interactive**:

   > Add caching to get_rate in rates.py.

   Run `python check.py rates` again. Did it ask you anything first? If
   it got today's rate right without asking, look at the list above its
   answer: what did it open to find out what you wanted?
7. **The hunt.** Step 6 with two other models, each in a fresh
   conversation in **Interactive**, restoring between them. Does any of
   them ask a question before it caches?

**Expected output**

After step 5:

```text
rates check (a call to the stand-in service takes a second; this counts the calls)

  EUR/USD for a past day, asked 3 times      1 service call       cached
  EUR/GBP for that day                       a different rate     kept apart
  that past day, 5 hours later               0 service calls      still cached
  today's rate, asked again 90 min later     1 service call       asked the service again

Cached, and today's rate is fetched again once it is over an hour old.
```

After step 6, compare the last two rows with these: they are the two
decisions your answers settled.

<details><summary>Hint</summary>

Given "add caching", an assistant does not stop to ask: it fills the gaps
and carries on. In a September 2026 test, five models from the Copilot
picker were given the step 6 prompt, and all five built a cache that keeps
every answer forever (`lru_cache`, `functools.cache`, or a plain
dictionary), so today's rate stayed at its first value all evening. Given
the answers from step 4, all three models tried built the cache the
checker wants. Nothing in the code said the forever-cache was wrong. The
fact that makes it wrong, that today's rate changes, was in your head,
and asking for the questions first is how it gets onto the screen while
the design is still free to change.

If yours got it right without being told, look at what it read first. An
agent that opens `check.py`, or this README, finds the facts there, just
as it would find them in a test. Either way, notice which questions you
could answer and the model could not: that is the difference between a
wording problem and a knowledge problem, which section 4 is about.

</details>

---

## 3. Three techniques, tested

Three techniques every prompting guide teaches. Each task puts one to the
test instead of taking it on trust.

### DIY 4: Test the persona

`lab/code/uploads.py` saves files that users upload. It has one serious
flaw, and some ordinary untidiness.

1. Open `lab/code/uploads.py`. Fresh conversation, **Plan**:

   > Review this code.

2. Fresh conversation, **Plan**:

   > You are a senior security engineer reviewing this code before it
   > goes to production. Review uploads.py.

3. Now find out what is actually wrong:

   ```bash
   python check.py uploads
   ```

4. Did the plain review name what the checker found? Did the persona?
   Did the persona find anything real that the plain one missed, or say
   the same things more sternly?
5. Switch to **Interactive**, in either conversation:

   > Fix the flaw that lets a file be saved outside the upload folder.
   > Change nothing else.

   Then run `python check.py uploads` again.
6. **The hunt.** The step 1 prompt, fresh conversation, **Plan**, on the
   smallest model in the picker. Does it find the flaw without a persona?

**What you should have**

Before the fix, two rows the checker marks as the flaw; after it, none:

```text
uploads check (each name is tried in a fresh, empty folder)

  'report.pdf'                          saved inside uploads/     ok
  '../escaped.txt'                      saved OUTSIDE uploads/    the flaw
  '/tmp/tmpq3v8x1ab/absolute.txt'       saved OUTSIDE uploads/    the flaw

A file name chosen by a user decides where the file lands.
```

<details><summary>Hint</summary>

The flaw is called path traversal. The file name comes from the user, so
`../escaped.txt` climbs out of the folder, and a name that is a whole path
throws the folder away entirely: `os.path.join` keeps only the last
absolute part.

A persona sets what the model attends to and how it talks, not what it
knows. In a September 2026 test, five models from the Copilot picker all
named the flaw in the plain review, and all five again with the persona.
If yours did the same, the persona changed the tone; if only the persona
found it, it changed where the model looked. Either way the model learned
nothing new about security from being told it was an expert, and the
checker, not the review, is what showed you the flaw was real.

</details>

### DIY 5: Does "step by step" still help?

`lab/code/batches.py` splits a list into batches, and loses items for some
lists. It passes the example in its own docstring.

1. Fresh conversation, **Plan**:

   > Is there a bug in batches.py? If there is, what is the minimal fix?

2. Fresh conversation, **Plan**:

   > Think step by step: what batches in batches.py does, what it should
   > do, and where the two differ. Then give the minimal fix.

3. Did the second answer find anything the first missed?
4. Switch to **Interactive**:

   > Apply the minimal fix to batches in batches.py. Change nothing else.

   Then check it:

   ```bash
   python check.py batches
   ```

5. **The hunt.** The step 1 prompt on the smallest model in the picker,
   fresh conversation, **Plan**. Does it still find the bug without being
   told to reason?

**Expected output**

```text
  batches([1, 2, 3, 4, 5, 6], 3) [[1, 2, 3], [4, 5, 6]]       ok
  batches([1, 2, 3, 4, 5], 2)    [[1, 2], [3, 4], [5]]        ok
  batches([1, 2], 3)             [[1, 2]]                     ok
  batches([], 2)                 []                           ok

Every item kept.
```

<details><summary>Hint</summary>

In September 2026, six current models were asked the plain question from
step 1, and all six named the lost last batch and gave the one-line fix.
"Let's think step by step" was a 2022 discovery: asking a model to write
out its intermediate steps got more answers right. Current models reason
before they answer whether you ask or not, so the phrase now adds length
more often than accuracy.

Asking for the reasoning is still worth something, for a different
reason: it gives you steps you can check, and a wrong step is easier to
spot than a wrong conclusion.

</details>

### DIY 6: Show the format

`lab/data/people.txt` holds four people, one per line, fields separated by
`|`. Two of them live somewhere with a comma in its name.

1. Fresh conversation, **Interactive**, describing the format:

   > Convert people.txt to CSV with the header name,email,city and the
   > columns in that order. Save it as people_prose.csv next to it.
   > Nothing but the CSV in the file.

2. Fresh conversation, **Interactive**, showing it instead:

   > Convert people.txt to CSV and save it as people_shown.csv next to
   > it. Start with the header line name,email,city, then follow these
   > two examples exactly:
   >
   > Tom Walsh | tom@example.ie | Sligo becomes Tom Walsh,tom@example.ie,Sligo
   >
   > Ann Roe |  | Ennis, Clare becomes Ann Roe,,"Ennis, Clare"

3. Let the checker read both, the way any program reading a CSV would:

   ```bash
   python check.py csv lab/data/people_prose.csv lab/data/people_shown.csv
   ```

4. **The hunt.** The step 1 prompt on two other models, fresh
   conversations in **Interactive**, into `people_prose2.csv` and
   `people_prose3.csv`. Check
   them all. Which model breaks a row?

**What you should have**

```text
lab/data/people_prose.csv          5 of 5 rows right
lab/data/people_shown.csv          5 of 5 rows right
```

or a line naming the row that broke, and why.

<details><summary>Hint</summary>

The trap is the comma in `Dublin, Ireland`: a CSV value that contains a
comma must be wrapped in quotes, or every program that reads the file sees
four columns. In a September 2026 test, asked in chat, five of six models
got the CSV right from the description, and the same five from the
examples. The sixth left the comma bare both times, and a parser caught
it both times, where a quick read would not.

So examples did not beat a clear description here. They still win when a
format is unusual or has no name, and the example that carries the rule
is the one with the comma in it: two near-identical examples teach
nothing about the awkward case.

</details>

---

## 4. What it can see

Everything so far was about how you ask. This section is about what the
model can see, which matters more.

### DIY 7: Tests first

1. Run the tests for `extract_domain`. One placeholder test fails, as it
   should:

   ```bash
   python -m pytest lab/tests/test_extract_domain.py -q
   ```

2. Open `lab/tests/test_extract_domain.py`. Replace the placeholder with
   four tests of your own, before anything implements the function: the
   file's docstring lists the four cases, and the hint shows the first.
   Run them. They fail, which is right: nothing exists yet.
3. Fresh conversation, **Interactive**:

   > Implement extract_domain in domains.py so that the tests in
   > test_extract_domain.py pass. Run the tests. Do not change the tests.

4. Run the tests yourself.
5. **The hunt.** Put back only the implementation (your tests stay), then
   switch model and ask without mentioning your tests:

   ```bash
   git restore lab/code/domains.py
   ```

   Fresh conversation, **Interactive**:

   > Implement extract_domain in domains.py from its docstring.

   Run your tests on what it wrote. Did code written without your tests
   pass them?

**Expected output**

```text
....                                                                     [100%]
4 passed in 0.02s
```

<details><summary>Hint</summary>

The first test, to show the shape:

```python
from lab.code.domains import extract_domain


def test_strips_the_subdomain():
    assert extract_domain("https://sub.example.com/path") == "example.com"
```

For the two that must raise, `with pytest.raises(ValueError):` wraps the
call, with `import pytest` at the top.

Four tests are a specification that cannot be read two ways: prose can be
misread, a test can only pass or fail. Written first, they turn "looks
right" into "passes". Written after the code, tests tend to check whatever
the code already does, bugs included.

</details>

### DIY 8: The error without the code

1. Run the order tests. One fails:

   ```bash
   python -m pytest lab/tests/test_orders.py -q
   ```

2. Close every editor tab (right-click any tab, then *Close All*). Fresh
   conversation, **Plan**:

   > Without opening, searching for or reading any files: my test fails
   > with KeyError: 'unit_price', fix it.

   Did it ask to see the code, hand you a fix anyway, or both? And did it
   keep to "without opening"? Anything it read is listed above its answer.
3. If it suggested a default value, such as `.get("unit_price", 0)`, try
   it: switch to **Interactive**, same conversation, and say *"Apply that
   fix."* Run the test again. Then put the file back:

   ```bash
   git restore lab/code/orders.py
   ```

4. Start again, carrying only what matters. Fresh conversation, **Plan**:

   > Read order_total in orders.py and the test in test_orders.py. A
   > default value was already tried and is wrong: the test then fails as
   > 0 == 10.0. Propose the minimal fix, and say which key name you treat
   > as the right one.

5. Choosing the key name is your decision, not the model's. Make it,
   switch to **Interactive**, tell it which name to use, and let it apply
   the fix. Run the test.
6. **The hunt.** The step 2 prompt on two other models, fresh
   conversations in **Plan**. Which one asks for the code instead of
   guessing?

**Expected output**

The test, as you received it, after the default-value fix, and after the
real one:

```text
FAILED lab/tests/test_orders.py::test_total - KeyError: 'unit_price'
FAILED lab/tests/test_orders.py::test_total - AssertionError: assert 0 == 10.0
1 passed in 0.02s
```

<details><summary>Hint</summary>

Tested in September 2026 with the error alone, three of four replies
asked to see the code, and all four still offered `.get("unit_price", 0)`
as a fix. That default stops the `KeyError` and hides the bug: every item
now contributes nothing, and the test fails on the arithmetic instead.
A different error is not progress.

With the code and the test in view, the cause is visible at a glance: the
test data says `price` and the function says `unit_price`. No rewording
of "fix it" could have found that, because the model was never shown the
code. That is the question to ask of every bad answer: is this a wording
problem, or a knowledge problem?

</details>

### DIY 9: Context you write once

1. Fresh conversation, **Plan**:

   > Before this conversation started, were you given any instructions
   > about this repository? If so, where did they come from, and what is
   > the first rule?

   Your copy of the repo has an `AGENTS.md` at its root, written for
   exactly this.
2. In the Explorer, right-click the `.github` folder at the top of your
   repo, choose *New File*, name it `copilot-instructions.md`, and put
   these two lines in it:

   ```text
   Dates in this project are day first: 12/08/2026 is 12 August.
   End every answer with one line that starts "TL;DR:" and sums it up in under ten words.
   ```

3. Fresh conversation, **Plan**:

   > Write a Python function that parses dates like 12/08/2026.

   Does the code read the day first? Does the answer end with a TL;DR
   line you never asked for in the chat?
4. Delete the TL;DR line from the file and save it. In the **same**
   conversation, ask a follow-up question. Then ask it again in a
   **fresh** conversation. Where does the TL;DR survive?
5. **The hunt.** Put the TL;DR line back, then ask the step 3 prompt on
   two other models, fresh conversations in **Plan**. Does every model
   obey the file?
   Delete the TL;DR line again when you are done: it applies to every
   conversation you have in this repo.

**What you should have**

Answers that end with a TL;DR line while it is in the file, including an
answer to a question that never mentioned it, and a date parser that
reads the day first because of one line you wrote once.

<details><summary>Hint</summary>

Most coding assistants add a file like this to every request:
`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`. So it steers
every conversation, which is why it must stay short, and why a stale rule
in it steers just as firmly as a correct one. Anything you find yourself
typing into every prompt belongs there.

If the TL;DR survived in the old conversation after you deleted the line,
that is the thread at work: its earlier answers still end with one, and
the model continues a pattern it can see. The thread is context too, and
a fresh conversation is the way to drop it.

</details>

---

## Common mistakes

- **Adjectives instead of decisions.** "Robust", "clean" and "professional"
  decide nothing; "raise ValueError when nothing is left" decides
  something.
- **Judging by eye** when a checker, a test or `git diff` could compare
  for you.
- **Accepting a large diff** because the fix you wanted is somewhere in it.
- **Asking for code before questions**, when the facts that matter are in
  your head rather than in the file.
- **Treating a persona or "step by step" as a way to make it smarter.**
  They change what it attends to and how much it writes.
- **Rewording when it cannot see the problem.** Rewording adds no
  information; putting the file in front of it does.
- **Taking a fix for code it never saw.** A default value that stops a
  `KeyError` usually hides the bug.
- **Leaving a stale rule in an instructions file.** It steers every
  conversation as firmly as a true one.

## Summary

- A prompt is a **specification**. Every decision you leave out, it makes
  for you, and other models agreeing does not make the decision right.
- **Non-goals** keep a change small enough to read, and `git diff` shows
  you whether they worked.
- Ask for **questions before code** when the facts that matter are yours.
- A **persona** changes tone and attention, not knowledge; **step by
  step** is now built in; **examples** pin a format, and a parser checks
  it.
- Before rewording, ask: **wording problem, or knowledge problem?**
  Rewording cannot add information; the right file in the window can.
- The best context is written once: **a test before the code**, and an
  **instructions file** every conversation reads.
