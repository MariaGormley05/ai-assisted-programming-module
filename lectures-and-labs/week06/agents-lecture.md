---
title: Coding Agents
topic: agents
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<style>
/* Bespoke to this deck. The "unseen" layer is a stack row for what the
   loop never has. The diff fences sit on the dark code ground, so their
   +/- lines get colours that read there. */
section .stack .layer.unseen { border-style: dashed; border-color: #8B8471; background: #F5F3EE; color: #46536B; }
section .stack .layer.unseen .rank { color: #8B8471; }
section pre code .hljs-addition { color: #9BD69B; background: transparent; }
section pre code .hljs-deletion { color: #F09A9A; background: transparent; }
</style>

<!-- _class: lead -->

<span class="kicker">// from answering to acting</span>

# Coding Agents

---

## Three requests

<p class="prompt">What does this function do?</p>

<p class="prompt">Rewrite this function to handle empty input.</p>

<p class="prompt">Make the test suite pass.</p>

* Same model, same day. What changed?

---

## The one idea

<div class="callout">

It is not a smarter model. It is the **same model with permission to act**
— and to keep going until it decides it is done.

</div>

* What changes across the ladder is **authority**, not intelligence

* So the question is never "can it?" — it is "how much rope?"

---

## Two hours

- **Part 1 — the ladder**
  - answer → edit → act, and what you are reviewing at each rung
  - terminal agents: more reach, more risk
  - when more autonomy is the wrong choice
- **Part 2 — inside the loop**
  - read → decide → act → observe, and why "done" and the diff are what matter
  - reviewing work you did not watch
  - choosing a rung deliberately — with your own assistant, on your own laptop

---

## The ladder

| Rung | It may | You review |
|---|---|---|
| **Ask** | Answer only. Touch nothing | A suggestion |
| **Edit** | Change a selection you chose | A diff |
| **Agent** | Choose files, make changes, run things | A result |
| **Terminal agent** | All of that, across a whole repo | A result, and a trail |

<span class="kicker">// the unit of review changes at every rung</span>

---

## Ask: the rung people skip

* It answers. It cannot touch a single file

* Every change is still one **you** make

<div class="callout">

The only rung where the output lands in your **head** rather than in your
files. Every rung above assumes you already understand the code.

</div>

- Best tool in the room for code you did not write

---

## Ask, done well

<p class="prompt bad">What does this do?</p>

* A summary invites hand-waving — and a fluent summary of the wrong
  behaviour reads just like a fluent summary of the right one

<p class="prompt good">Walk me through this line by line with the input [3, 1, 4, 1, 5],
and tell me what it returns. I will run it and check.</p>

* A trace forces specifics, and hands you a **prediction to test**

<span class="kicker">// the check is the part that puts it in your head</span>

---

## Edit: the diff is the safety mechanism

* You select, you describe the change, it rewrites in place

* You accept or reject a **diff**. For a rename, you picture this:

```diff
-def calculate(items):
+def compute_total(items):
```

<div class="callout">

The diff is not a formality. It is the **entire** safety mechanism at this
rung — the moment you stop reading it, edit mode is agent mode with extra
steps.

</div>

---

## Predict: you ask for one rename

<p class="prompt bad">rename calculate to compute_total in this file</p>

What comes back?

* Exactly that rename, nothing else
* The rename, plus reordered imports and a few added type hints
* A full rewrite of the file
* It asks a clarifying question first

---

<!-- _class: code-sm -->

## It tidies while it is in there

```diff
-import os, sys
+import os
+import sys
+from typing import Iterable

-def calculate(items):
+def compute_total(items: Iterable[float]) -> float:
+    """Sum the items."""
     return sum(items)
```

* One line of that was asked for. The other eight are in the diff you are
  about to approve — and you were looking for a rename

---

## Say what must not change

* Say what must **not** change, not just what must

<p class="prompt good">Rename calculate to compute_total in this file.
Change nothing else: no import reordering, no type hints, no reformatting.</p>

<div class="callout">

A 3-line diff gets **read**. A 40-line diff gets **skimmed**. You choose
which you are reviewing when you write the prompt.

</div>

---

## Agent: describing outcomes, not steps

* You give a **goal**. It works out the files, the changes, the commands

* You review a **result**, not a change

<div class="callout">

If you cannot say what "done" means **before** it starts, you cannot tell
whether it got there — and you will accept whatever looks finished.

</div>

---

## Predict: which works better in agent mode?

<p class="prompt bad">Open utils.py, find the parse function, add a try/except
around line 40, then open test_utils.py and add a test, then run pytest.</p>

<p class="prompt good">Make parse() handle malformed input without crashing.
Add a test covering it. All existing tests must still pass.</p>

---

## The second — and this inverts the usual rule

* Prescribing steps wastes what the rung is **for**

* And it will follow your bad plan faithfully

<div class="callout">

Precision moves from the **route** to the **destination**. Vague about
*how*; ruthless about what *done* means.

</div>

---

## Terminal agents

| | Editor agent | Terminal agent |
|---|---|---|
| Reaches | What you grant: one file, or the whole workspace | The whole repository, and your shell |
| Runs commands | Only if granted — usually asking first | Yes, under a policy you set |
| Good for | A change you can picture | A change spread across many files |
| Blast radius | Whatever you granted | Whatever the policy allows |

* Same instruction. The consequences follow the **grant**, not the window

---

## The discipline for higher rungs

<div class="flow">
  <div class="step"><span class="n">01</span>Commit first — clean starting point</div>
  <div class="step"><span class="n">02</span>Say what done means</div>
  <div class="step"><span class="n">03</span>Let it work, uninterrupted</div>
  <div class="step"><span class="n">04</span>Review the diff, not the story</div>
</div>

<div class="callout">

Without a commit, `git diff` is not a review tool and `git checkout` is
not an undo. You have neither.

</div>

---

## The agent's summary is not evidence

* It reports what it **intended** to do

* Fluent, confident, and produced by the same process that wrote the code

<div class="callout">

Read the **diff**, not the summary. And check the files it touched that
you were not expecting — that list is where the surprises live.

</div>

---

## Predict: where does autonomy cost you most?

* A large mechanical refactor across 30 files
* A subtle bug whose cause you do not understand yet
* Writing tests for existing code
* Generating boilerplate

---

## The bug you do not understand yet

* An agent will try things until the symptom disappears

* You wanted a **diagnosis**. It optimises for a green test

<div class="callout">

Twenty minutes later: a pile of speculative changes, a passing test, and
nobody knows what was wrong. Debugging an unknown cause wants **ask**
mode.

</div>

---

## What review means at each rung

| Rung | You are looking at | The question |
|---|---|---|
| **Ask** | A suggestion | Could I make this change myself now? |
| **Edit** | A diff | Was every changed line asked for? |
| **Agent** | A result | Is this *my* "done"? What else changed? |
| **Terminal agent** | A result and a trail | The same, plus: what did it run? |

<div class="callout">

Review does not get lighter as the tool does more. The surface you are
checking grew from a sentence to a set of files.

</div>

---

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2: what actually happens between your request and its result — and
why that leaves exactly two things worth reading.

---

## Inside the loop

<div class="flow">
  <div class="step"><span class="n">01</span><strong>Read</strong> — your request, plus everything gathered so far</div>
  <div class="step"><span class="n">02</span><strong>Decide</strong> — one next action, or "done"</div>
  <div class="step"><span class="n">03</span><strong>Act</strong> — open a file, change lines, run a command</div>
  <div class="step"><span class="n">04</span><strong>Observe</strong> — whatever came back joins the pile</div>
</div>

* Then back to **01**, with the pile one observation bigger

* It ends when the model decides it is done — or when you stop it

<span class="kicker">// the same model as ask mode. The loop is the only new part</span>

---

## The parse() goal, traced

From part 1: *make parse() handle malformed input without crashing, add a
test, all existing tests must still pass.*

```text
read     src/utils.py, tests/test_utils.py
decide   parse("") raises ValueError -> return None instead
act      edit src/utils.py           (+4 lines)
act      edit tests/test_utils.py    (+6 lines, test_parse_empty)
act      run pytest
observe  13 passed
decide   done
report   "parse() now handles malformed input; 13 tests pass"
```

* It stopped on **13 passed** — an observation — not on your goal

---

## What the loop can and cannot see

<div class="stack">
  <div class="layer top"><span>Your request — exactly as worded, nothing more</span><span class="rank">sees</span></div>
  <div class="layer"><span>Files it chose to open, output of commands it chose to run</span><span class="rank">sees</span></div>
  <div class="layer unseen"><span>What you <strong>meant</strong>. Which files are off-limits. Whether a test deserves trust</span><span class="rank">never</span></div>
</div>

* An early wrong decision produces observations about the **wrong path** —
  and every later step is locally sensible

* So it is wrong **quickly and confidently**. Speed and confidence are
  properties of the loop, not evidence

---

## So two things matter

<div class="callout">

The loop stops when **its** reading of "done" is satisfied. Your files hold
the sum of every **act**. Everything else — plan, narration, summary — is
commentary.

</div>

* **Before:** write "done" as something the loop can *observe* — a named
  test, a command, an output — so its stopping condition is yours

* **After:** read the **diff** — the only record of the acts that the loop
  did not write

- And say what must **not** change: nothing is off-limits unless the request
  says so

---

## Predict: you stop it halfway

Step 6 of what would have been 12. You press stop. What state are your
files in?

* Untouched — nothing is applied until you accept at the end
* Whatever the first six steps did, and nothing else
* Rolled back to where it started
* Only the file it was editing at that moment has changed

---

## Live edits, no rollback

* Each act lands in your files **before** the next observation — the tests
  it runs are run on the changed files

* Stopping stops the loop. It does not undo it

<div class="callout">

A half-finished result is still a result, and you own it. Your last
**commit** is the only map of what changed — and the only undo that works
whatever editor you are in.

</div>

- "Commit first" is not a habit. It is what makes stopping safe

---

## Case two: "Make the test suite pass"

The third request from the start. One test is red:

```python
def test_total_ignores_blank_rows():
    assert total_from_csv("grades_with_blank.csv") == 250
```

<p class="prompt bad">Make the test suite pass.</p>

* "Done" here is observable — the suite is green. That is exactly the
  problem: **green is a property of the tests too**

---

## Predict: the fix is not obvious

Two changes to the code have not turned the test green. The loop goes back
to **decide**. Which of these satisfies the request *as written*?

* Fix the code
* Delete the test
* Change `250` to whatever the code returns
* Mark the test as skipped

---

## All four are "green"

* The request said what to **observe**. It said nothing about what may
  change on the way

* The shortest route to a green suite does not always pass through the bug

<p class="prompt good">Make test_total_ignores_blank_rows pass by fixing total_from_csv.
Do not edit, skip or delete any test.
If you cannot make it pass, stop and tell me what you found.</p>

- Three additions: what may change, what may not, and a way to finish that
  is not "green"

---

## What it said, and what it did

<p class="reply">Fixed the blank-row handling in total_from_csv and made the suite pass.
Also tidied the CSV loader while I was there. All 14 tests pass.</p>

```text
 M src/totals.py            +9   -2
 M src/csv_loader.py        +21  -14
 M tests/test_totals.py     +1   -1
 M tests/conftest.py        +6   -0
 A requirements.txt         +1   -0
```

* Five files. The summary mentioned two. One of the five is a **test**

---

## Predict: which file do you read first?

* `src/totals.py` — where the fix was meant to go
* `src/csv_loader.py` — the biggest diff
* `tests/test_totals.py` — one line changed in a test
* `requirements.txt` — the new file

---

## Reviewing a result, in order

<div class="flow">
  <div class="step"><span class="n">01</span>List the files touched; compare with the files you expected</div>
  <div class="step"><span class="n">02</span>Read every change to a <strong>test</strong> — it moves the goalposts</div>
  <div class="step"><span class="n">03</span>Read the files you did not expect — the surprises live there</div>
  <div class="step"><span class="n">04</span>Run it yourself. <em>Then</em> read the change you asked for</div>
</div>

<div class="callout">

The intended change goes **last**: it is the only part of the result the
summary already described accurately.

</div>

---

## Try it now: make the loop show its plan

Open a small file of your own in your assistant's most restricted mode.
Write one line, for yourself, saying what "done" would mean. Then:

<p class="prompt">Goal: fix the most likely bug in this file. Before you change anything,
tell me which files you would read, what you would change, and how you
would know it worked. Then stop.</p>

* Notice: its "how I would know" line is **its** definition of done.
  Compare it with yours — the gap is exactly where a result would have
  surprised you

<span class="kicker">// seven minutes. Do not let it act yet</span>

---

## What the plan showed you

* Its "done" was something it could **observe**: a test passing, the script
  running without error

* Yours probably contained things it cannot observe: *nothing else
  changes*, *and I understand why*

<div class="callout">

The gap is not a flaw in the tool. It is the part of your request you had
not written down yet — and now you know what to add before you let it act.

</div>

---

## When you were not there at all

Some agents work away from your editor, on their own copy of the
repository, and hand back a **pull request**.

* No steering mid-flight: the request *is* the whole conversation, so
  "done" and "do not touch" go in up front

* The same four review steps — but the trail (what it ran, what came back)
  is now the only witness

<div class="callout">

Review does not get lighter as the agent gets further away. It gets
**heavier**: the summary is all you were shown.

</div>

---

## Choosing a rung, deliberately

| Ask first | Pushes the task **up** | Pushes it **down** |
|---|---|---|
| How **reversible** is it? | One commit away | It touches data, money, someone else's system |
| How well can I **test** it? | A suite you trust, that it may not edit | "I will know it when I see it" |
| What does being **wrong** cost? | A re-run | An outage, a lost file, a decision you cannot explain |

- The bottom rung is **ask**, not "no assistant". Below it sits the task you
  keep for yourself — and you should be able to name one

<span class="kicker">// three questions, asked before the prompt, not after the diff</span>

---

## Common mistakes: asking

* Prescribing steps in agent mode, then blaming it for following them

* A "done" it can observe but you did not mean — "make it pass", with the
  tests unprotected

- Saying what must change and nothing about what must **not**, so the diff
  grows past reading
- Using an agent to debug something nobody has diagnosed
- Defaulting to the top rung — as unexamined as never leaving the bottom

---

## Common mistakes: reviewing

* Reviewing the **summary** instead of the diff

* Reading the intended change first — and the changed test never

- Not committing first, so there is no undo and no review surface
- Stopping it halfway and assuming the files are as they were
- Accepting "all tests pass" without asking how many there were before

---

<!-- _class: dense -->

## Summary

- The ladder is **answer → edit → act**; what changes is **authority**, and
  the unit of review changes with it: suggestion, diff, result
- Say what must **not** change, so the diff stays small enough to read
- In agent mode, precision moves from the **route** to the **destination**
- A terminal agent has a bigger blast radius for the same instruction
- Inside the loop — **read → decide → act → observe** — edits land live,
  and it stops on *its* reading of "done"
- So write "done" as something it can observe and you meant — and read the
  diff: tests first, surprises second, your change last
- The summary is not evidence. The diff is

<div class="callout">

Pick the rung deliberately: how reversible is it, how well can you test
it, and what does being wrong cost?

</div>
