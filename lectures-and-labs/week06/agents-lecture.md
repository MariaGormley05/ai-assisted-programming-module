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

<!-- Speaker notes: ~0:01. Title. The spine of these two hours is a LADDER
of autonomy — ask, edit, act — and the skill being taught is choosing a rung
deliberately. Students arrive with one of two unexamined defaults: always
the most autonomous mode, or never anything above chat. Both are treated
here as the same mistake. Part 1 climbs the ladder and asks what review
means on each rung; part 2 opens the agent loop to show why "done" and the
diff are the only two things that matter once the assistant can act. -->

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

<!-- Speaker notes: ~0:02. The hook: three requests to the same model on
the same day, and the question of what changed between them. The answer
students give is "it got smarter". The answer that matters is "it got
PERMISSION": the first may only answer, the second may rewrite a selection
you chose, the third may open files and run commands until it decides the
suite is green. Do not reveal that yet. The third request comes back in
part 2 as the worked case, because "make the tests pass" is the request
whose shortest route need not go through the bug. -->

## Three requests

<p class="prompt">What does this function do?</p>

<p class="prompt">Rewrite this function to handle empty input.</p>

<p class="prompt">Make the test suite pass.</p>

* Same model, same day. What changed?

---

<!-- Speaker notes: ~0:05. The idea the two hours turn on. The misconception
to kill: agent mode is a smarter model. It is the same model with permission
to act and to keep going until it decides it is done. The distinction tells
you where to look when it goes wrong — not "the model was dumb" but "I gave
it the wrong amount of rope, or the wrong definition of done". Part 2 makes
"keep going until it decides it is done" literal: a loop, with a stopping
condition the model evaluates from whatever it can observe. -->

## The one idea

<div class="callout">

It is not a smarter model. It is the **same model with permission to act**
— and to keep going until it decides it is done.

</div>

* What changes across the ladder is **authority**, not intelligence

* So the question is never "can it?" — it is "how much rope?"

---

<!-- Speaker notes: ~0:07. Agenda, naming both halves. Part 1 is the ladder
itself and what review means at each rung, with the honest case for a lower
rung. Part 2 is the mechanism: what an agent loop actually does between the
request and the result, a second worked case, a short activity on their own
laptops, and the decision procedure for picking a rung. -->

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

<!-- Speaker notes: ~0:09. The ladder, the reference slide for both hours.
The right-hand column is the payload: the unit of review changes at every
rung — a suggestion, a diff, a result — and most people never notice that
it changed, so they review a result the way they reviewed a diff (skim it
for plausibility) and miss everything a diff would have shown them. The
terminal-agent row is here for scope only: same instruction, whole
repository, your shell. Configuring one is a subject of its own and is not
covered here. -->

## The ladder

| Rung | It may | You review |
|---|---|---|
| **Ask** | Answer only. Touch nothing | A suggestion |
| **Edit** | Change a selection you chose | A diff |
| **Agent** | Choose files, make changes, run things | A result |
| **Terminal agent** | All of that, across a whole repo | A result, and a trail |

<span class="kicker">// the unit of review changes at every rung</span>

---

<!-- Speaker notes: ~0:12. Ask mode, and why it is the rung students skip:
it feels slow because nothing lands in the files. The argument for it: it is
the only rung whose output lands in your HEAD, and every rung above assumes
you already understand the code well enough to judge a change to it.
Understanding is the step that gets skipped, and it is the one that does not
survive skipping. Students assume ask mode is for beginners; it is the
default for code you did not write, at any level. -->

## Ask: the rung people skip

* It answers. It cannot touch a single file

* Every change is still one **you** make

<div class="callout">

The only rung where the output lands in your **head** rather than in your
files. Every rung above assumes you already understand the code.

</div>

- Best tool in the room for code you did not write

---

<!-- Speaker notes: ~0:14. The worked example for the ask rung: the
difference between an explanation you can check and one you can only find
plausible. "What does this do?" returns a summary, and a fluent summary of
the wrong behaviour reads exactly like a fluent summary of the right one,
so you cannot tell them apart. A line-by-line trace on a concrete input
forces specifics and, crucially, produces a PREDICTION you can run the code
to test. The check is what moves it from "I followed that" to "I understand
it". The lab's first exercise is exactly this move — predict, then run — on
code the student has never seen. -->

## Ask, done well

<p class="prompt bad">What does this do?</p>

* A summary invites hand-waving — and a fluent summary of the wrong
  behaviour reads just like a fluent summary of the right one

<p class="prompt good">Walk me through this line by line with the input [3, 1, 4, 1, 5],
and tell me what it returns. I will run it and check.</p>

* A trace forces specifics, and hands you a **prediction to test**

<span class="kicker">// the check is the part that puts it in your head</span>

---

<!-- Speaker notes: ~0:17. Edit mode. You select, you describe the change,
it rewrites in place, and you accept or reject a diff — the diff is the
entire safety mechanism at this rung, not a formality. The two-line diff on
the slide is what a student pictures when they ask for a rename; the next
two slides are about the gap between that picture and what arrives. The
lab's second exercise has them read a refactor diff line by line and find
the change they did not ask for. -->

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

<!-- Speaker notes: ~0:19. Predict beat 1: what comes back from a narrow
edit instruction. The wrong answer to expect is "just the rename". The
faulty model is that a narrow instruction produces a narrow change — that
the assistant edits only what the sentence names. In practice assistants
tidy while they are in there: imports reordered, type hints added, a
docstring written, a stray reformat. None of it was asked for, and all of
it is inside the diff about to be approved. -->

## Predict: you ask for one rename

<p class="prompt bad">rename calculate to compute_total in this file</p>

What comes back?

* Exactly that rename, nothing else
* The rename, plus reordered imports and a few added type hints
* A full rewrite of the file
* It asks a clarifying question first

---

<!-- Speaker notes: ~0:22. The reveal — usually the tidying — shown as the
diff that "rename one function" tends to return. One line of the nine is
the rename; the rest is an import split, a typing import, type hints and a
docstring, none of it asked for and all of it inside the diff about to be
approved. Students assume the extra lines are harmless improvements; the
problem is not that they are bad but that they were never reviewed as
changes, because the reviewer was looking for a rename. -->

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

<!-- Speaker notes: ~0:24. The rule that is the practical takeaway of the
edit section: say what must NOT change, not only what must. The sentence to
carry away is about diff size — a three-line diff gets read, a forty-line
diff gets skimmed — and the reviewer chose which one they would be
reviewing at the moment they wrote the prompt. The lab's second exercise
has them state "no behaviour change" explicitly and then find the change
they did not ask for anyway. -->

## Say what must not change

* Say what must **not** change, not just what must

<p class="prompt good">Rename calculate to compute_total in this file.
Change nothing else: no import reordering, no type hints, no reformatting.</p>

<div class="callout">

A 3-line diff gets **read**. A 40-line diff gets **skimmed**. You choose
which you are reviewing when you write the prompt.

</div>

---

<!-- Speaker notes: ~0:26. Agent mode: the genuine step change. You give a
goal; it works out the files, the changes and the commands; and you stop
reviewing a change and start reviewing a RESULT. The practical consequence
is the callout: you must be able to say what "done" means BEFORE it starts,
or you cannot tell whether it got there and will accept whatever looks
finished. Part 2 shows why this is mechanical rather than a habit — the
loop's stopping condition is its own reading of "done". -->

## Agent: describing outcomes, not steps

* You give a **goal**. It works out the files, the changes, the commands

* You review a **result**, not a change

<div class="callout">

If you cannot say what "done" means **before** it starts, you cannot tell
whether it got there — and you will accept whatever looks finished.

</div>

---

<!-- Speaker notes: ~0:29. Predict beat 2, and the most useful thirty
seconds of the two hours for their own agent work. The wrong answer to
expect is "the detailed one, obviously". The faulty model is that more
specification is always better — the specific-prompt lesson transferred
wholesale to a rung where it inverts. Prescribing steps wastes exactly what
agent mode is for, and worse, the agent follows a bad plan faithfully: if
line 40 was the wrong place, the try/except goes there anyway. Specify the
OUTCOME and the constraints precisely; leave the route open. -->

## Predict: which works better in agent mode?

<p class="prompt bad">Open utils.py, find the parse function, add a try/except
around line 40, then open test_utils.py and add a test, then run pytest.</p>

<p class="prompt good">Make parse() handle malformed input without crashing.
Add a test covering it. All existing tests must still pass.</p>

---

<!-- Speaker notes: ~0:32. The reveal and the distinction, which is subtle
and worth the time: precision moves from the ROUTE to the DESTINATION.
Vague about how; ruthless about what done means. Students find this
counter-intuitive after learning to write specific prompts, so name the
tension: "vague about how" means which files and which lines, never the
behaviour — "handles malformed input" is still under-specified until you
say what it should do with that input. -->

## The second — and this inverts the usual rule

* Prescribing steps wastes what the rung is **for**

* And it will follow your bad plan faithfully

<div class="callout">

Precision moves from the **route** to the **destination**. Vague about
*how*; ruthless about what *done* means.

</div>

---

<!-- Speaker notes: ~0:35. Terminal agents, for scope only: the distinction
that matters is what each is GRANTED, not which window it lives in. An
editor agent in chat mode reads the file you opened; in its agent mode it
can navigate the workspace, edit many files and run commands, if you let
it. A terminal agent has your shell and the whole repository by default.
So the same instruction has a very different blast radius only because the
grants differ: which tools, what filesystem scope, whether commands run
and who approves them. The misconception is that the editor is a sandbox.
It is not; the grant is, and the grant is a setting. How a grant is
configured — standing instructions, permissions — is a subject of its own
and deliberately not covered here; what carries over unchanged is the
discipline on the next slide. -->

## Terminal agents

| | Editor agent | Terminal agent |
|---|---|---|
| Reaches | What you grant: one file, or the whole workspace | The whole repository, and your shell |
| Runs commands | Only if granted — usually asking first | Yes, under a policy you set |
| Good for | A change you can picture | A change spread across many files |
| Blast radius | Whatever you granted | Whatever the policy allows |

* Same instruction. The consequences follow the **grant**, not the window

---

<!-- Speaker notes: ~0:38. The four habits that make the higher rungs
survivable. Commit first is the one to insist on: without a clean starting
point, git diff is not a review tool and git checkout is not an undo, and
the student has neither. Students assume these four are etiquette; part 2
shows each one is forced by the mechanism — edits land live, the loop stops
on its own reading of done, and the summary is written from inside the
loop. -->

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

<!-- Speaker notes: ~0:41. Review the diff, not the story — the subtlest
failure at high autonomy. An agent reports what it INTENDED. The summary is
fluent, confident, and generated by the same process that produced the
code, so it cannot be independent evidence about that code. The diff is
evidence; so is the list of files it touched that you were not expecting,
which is where the surprises live. Part 2 turns this into an ordered
review procedure. -->

## The agent's summary is not evidence

* It reports what it **intended** to do

* Fluent, confident, and produced by the same process that wrote the code

<div class="callout">

Read the **diff**, not the summary. And check the files it touched that
you were not expecting — that list is where the surprises live.

</div>

---

<!-- Speaker notes: ~0:44. Predict beat 3: the honest one about where
autonomy costs you. The wrong answer to expect is "the big refactor" — it
sounds hardest. The faulty model is that autonomy should go where the
difficulty is. Agents do sweeping mechanical changes well; where they burn
time is the subtle bug with an unclear cause. The agent tries something, it
does not work, it tries something else, and twenty minutes later there is
a pile of speculative changes and no diagnosis. Debugging an unknown cause
wants ask mode. -->

## Predict: where does autonomy cost you most?

* A large mechanical refactor across 30 files
* A subtle bug whose cause you do not understand yet
* Writing tests for existing code
* Generating boilerplate

---

<!-- Speaker notes: ~0:47. The reveal: unknown-cause debugging is the trap,
because an agent optimises for making the symptom go away and you wanted a
diagnosis. This is the strongest practical argument in the two hours for
choosing a LOWER rung deliberately, and it returns in part 2 with the
mechanism behind it: a loop whose stopping condition is "the symptom is
gone" takes the shortest route to that, and the shortest route does not
always pass through the cause. -->

## The bug you do not understand yet

* An agent will try things until the symptom disappears

* You wanted a **diagnosis**. It optimises for a green test

<div class="callout">

Twenty minutes later: a pile of speculative changes, a passing test, and
nobody knows what was wrong. Debugging an unknown cause wants **ask**
mode.

</div>

---

<!-- Speaker notes: ~0:50. Consolidation of part 1: the review question
changes at every rung, and the characteristic failure is asking the wrong
rung's question. At ask, whether you could now make the change yourself;
at edit, whether every changed line was asked for; at agent, whether the
result meets YOUR definition of done and what else was touched on the way.
Students assume review gets lighter as the tool does more; it gets heavier,
because the surface being checked grew from a sentence to a set of files. -->

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

<!-- Speaker notes: ~0:55. Break. Part 2 answers the question part 1 kept
deferring: what actually happens between the request and the result. The
answer is a loop — read, decide, act, observe — and once it is visible, the
two rules from part 1 (say what done means; read the diff, not the story)
stop being advice and become the only two places a reviewer can stand. -->

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2: what actually happens between your request and its result — and
why that leaves exactly two things worth reading.

---

<!-- Speaker notes: ~1:05. The mechanism part 1 only named. "Agent mode" is
the same model called repeatedly: each call sees your request plus
everything gathered so far, and answers with one action — open this file,
change these lines, run this command — or with "done". The surrounding tool
performs the action and appends whatever came back, and the next call
starts from that bigger pile. Students imagine a planner that understands
the whole task and then executes it; in fact every step is a fresh
judgement from the transcript so far, which is why an early wrong step is
built on rather than noticed. The loop ends when the model decides it is
done, or when you stop it. -->

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

<!-- Speaker notes: ~1:07. An illustrative trace — not a transcript from any
particular product — of the agent-mode goal from part 1 going well, to make
the loop concrete. Three things to notice. Every "act" line changed the
files before the student saw anything. The "decide" line chose a behaviour,
return None, that the request never specified: that is the destination
being under-specified, not the route. And the loop stopped on the
observation "13 passed", not on the goal — had the new test been weak, the
loop would have stopped just the same. -->

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

<!-- Speaker notes: ~1:10. What the loop has to work with: your request as
worded, and whatever its own actions returned. It never has what you meant,
which files you consider off-limits, or whether a test deserves trust —
none of that is in the pile unless you put it there. This is also the
mechanism behind "confidently wrong, quickly": an early wrong decision
produces observations about the wrong path, every later step is locally
sensible given those observations, and the summary is written from inside
the path. Students read speed and confidence as signs of competence; both
are properties of the loop and evidence of nothing. -->

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

<!-- Speaker notes: ~1:12. The payoff of the mechanism: exactly two things
matter, and they are the two rules part 1 gave as advice. The loop stops
when ITS reading of "done" is satisfied, so "done" must be written as
something the loop can observe — a named test, a command, an output — or its
stopping condition and yours are different conditions. And your files hold
the sum of every act, so the diff is the only record of what happened that
the loop did not write. Plan, narration and summary are commentary.
Students assume the fix for a bad result is a better description of the
task; usually it is a better description of done, and of what may not
change. -->

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

<!-- Speaker notes: ~1:14. Predict beat 4: the state of the files when the
loop is interrupted. The wrong answer to expect is "untouched — nothing is
applied until I accept at the end". The faulty model is edit mode's
transaction carried up a rung: at the edit rung you approve a diff before
it lands, so students assume agent mode batches its changes for a final
approval too. It cannot: each act has to land in the files before the next
observation can see it — the tests it runs are run on the changed files —
so the edits are live from step one, and stopping the loop does not undo
them. The right answer is the second option. -->

## Predict: you stop it halfway

Step 6 of what would have been 12. You press stop. What state are your
files in?

* Untouched — nothing is applied until you accept at the end
* Whatever the first six steps did, and nothing else
* Rolled back to where it started
* Only the file it was editing at that moment has changed

---

<!-- Speaker notes: ~1:16. The reveal: the edits are live and stopping does
not undo them, and this is why "commit first" was never etiquette. Each act
lands before the next observation because the next observation depends on
it. A half-finished result is still a result the student now owns; the
last commit is the only map of what changed and the only undo that works
in every editor — an editor may offer its own session undo, but the commit
is the one that does not depend on which tool was used. -->

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

<!-- Speaker notes: ~1:18. The second worked case, different in kind from
part 1's: those were about what you type; this one traces what the loop
does with a "done" that is perfectly observable and wrongly shaped. It is
the third request from the opening slide, with one red test. "The suite is
green" is exactly the kind of done the loop can observe — and green is a
property of the tests as much as of the code, which is the problem the
next slide poses. -->

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

<!-- Speaker notes: ~1:20. Predict beat 5: what the loop may do when the
code fix does not come easily. The wrong answer to expect is "only the
first — it obviously knows I mean fix the code". The faulty model is that
the loop shares your intent. It has your words and its observations, and
"the suite is green" is satisfied by all four options. Which one a given
run takes varies; the point is that the request as written permits every
one of them, so the request is the thing to fix. This is the mechanism
behind part 1's "it optimises for a green test". -->

## Predict: the fix is not obvious

Two changes to the code have not turned the test green. The loop goes back
to **decide**. Which of these satisfies the request *as written*?

* Fix the code
* Delete the test
* Change `250` to whatever the code returns
* Mark the test as skipped

---

<!-- Speaker notes: ~1:22. The reveal: all four. The request said what to
observe and nothing about what may change on the way, and the shortest
route to a green suite does not always pass through the bug. The better
prompt adds three things: the file that may change, the files that may
not, and a legitimate way to finish that is not "green" — stop and report.
That last clause matters: without an exit, the only way the loop can end
is by making the observation come true. Ruthless about done includes what
must not change and what to do instead of forcing it. -->

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

<!-- Speaker notes: ~1:24. The result of the original, unconstrained
request, seen two ways: the summary the loop wrote, and the file list
version control gives you — which exists only because of the commit made
first. The summary names two files and reports a green suite; the listing
shows five files, a one-line change to a test, a fixture file, and a new
dependency nobody asked for. Students assume "all 14 tests pass" is the
end of review; it is where review starts, because the number and the tests
themselves may have changed. -->

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

<!-- Speaker notes: ~1:26. Predict beat 6: the order of review. The wrong
answer to expect is "totals.py — check the fix is right". The faulty model
is that reviewing a result means checking that the feature works; but a
changed test changes what "works" means, so until the one-line change in
tests/test_totals.py has been read, "14 pass" is evidence of nothing in
particular. The answer is the test. Then the files nobody expected —
requirements.txt is a dependency you now own, csv_loader.py is a tidy
nobody asked for — and the intended change last, because it is the only
part the summary already described accurately. -->

## Predict: which file do you read first?

* `src/totals.py` — where the fix was meant to go
* `src/csv_loader.py` — the biggest diff
* `tests/test_totals.py` — one line changed in a test
* `requirements.txt` — the new file

---

<!-- Speaker notes: ~1:28. The reveal as a procedure, ordered by what each
step can invalidate. Tests first, because a changed test moves the
goalposts and makes every later "pass" meaningless. Unexpected files
second, because the surprises live there and the summary did not mention
them. Run it yourself third, because the observation that stopped the loop
was the loop's, not yours. The intended change last: it is the one part
you already know about. Students review in the opposite order — feature
first, and the test never. -->

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

<!-- Speaker notes: ~1:30. The activity, seven minutes, on their own
laptops with whatever assistant they have — a chat window with the file
pasted in works as well as an editor. The point is to make the loop show
its plan before it acts, and to compare the assistant's definition of done
with the student's own, written down first. The "how you would know it
worked" line is the loop's stopping condition in plain words; the gap
between it and the student's line is precisely where a result would have
surprised them. If their assistant has no read-only mode, "then stop" does
the same job; if it acts anyway, that is a finding about the tool. -->

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

<!-- Speaker notes: ~1:37. Debrief. What the plans typically contained: a
"done" the loop could observe — a test passing, the script running without
error — and rarely the things the student wrote down: nothing else changes,
and I understand why. The gap is not a defect in the tool; it is the part of
the request that had not been written down yet, and now it can be. Students
assume the gap means the assistant misunderstood; it means the request was
incomplete, which is fixable in a way misunderstanding is not. -->

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

<!-- Speaker notes: ~1:39. The far end of the ladder within the editor's
world: agents that work away from you — on their own copy of the repository
— and hand back a pull request. Two consequences of the loop model. There
is no mid-flight steering, so the request is the whole conversation and
"done" and "do not touch" must go in up front. And the trail — what it ran,
what came back — is the only witness, so the four review steps apply
unchanged and weigh more. Students assume distance makes review lighter,
because the work arrives packaged; it makes review heavier, because the
package is all they were shown. The lab's optional extension is exactly
this kind of agent. -->

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

<!-- Speaker notes: ~1:41. The decision procedure the two hours were
building towards, and what the lab's last exercise asks each student to
write for themselves. Three questions, asked before the prompt rather than
after the diff: how reversible is it, how well can I test it, and what does
being wrong cost. Each answer pushes a task up or down the ladder, and the
bottom of the ladder is ask mode, not "no assistant" — below ask sits the
task you keep for yourself, and being able to name one is the honest output
of the exercise. Students assume the axis is difficulty; it is
verifiability. -->

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

<!-- Speaker notes: ~1:43. Common mistakes on the asking side, ordered by
how often they hit. Every one is a "done" problem or a "rope" problem: steps
instead of an outcome; a done the loop can observe but you did not mean;
nothing said about what may not change; an agent sent to debug what nobody
has diagnosed; and the top rung by default, which is the same unexamined
choice as never leaving the bottom one. -->

## Common mistakes: asking

* Prescribing steps in agent mode, then blaming it for following them

* A "done" it can observe but you did not mean — "make it pass", with the
  tests unprotected

- Saying what must change and nothing about what must **not**, so the diff
  grows past reading
- Using an agent to debug something nobody has diagnosed
- Defaulting to the top rung — as unexamined as never leaving the bottom

---

<!-- Speaker notes: ~1:44. Common mistakes on the reviewing side. The
summary read as evidence; the intended change read first and the changed
test never; no commit, so no review surface and no undo; a stopped loop
assumed to have left the files alone; and "all tests pass" accepted without
asking how many tests there were before it started. Each one is the
mechanism from part 2 ignored: the summary is written by the loop, edits
are live, and green is a property of the tests. -->

## Common mistakes: reviewing

* Reviewing the **summary** instead of the diff

* Reading the intended change first — and the changed test never

- Not committing first, so there is no undo and no review surface
- Stopping it halfway and assuming the files are as they were
- Accepting "all tests pass" without asking how many there were before

---

<!-- Speaker notes: ~1:45. Summary and close. Back to the three requests
from the start: what changed between them was permission, not intelligence,
and the third one — make the tests pass — is the one whose shortest route
need not pass through the bug. The two rules to leave with are the two the
loop forces: write "done" as something it can observe and you actually
mean, and read the diff — tests first, surprises second, the intended
change last. The callout is the decision the lab asks each student to make
for themselves. -->

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
