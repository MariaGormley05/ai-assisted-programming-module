# AIAP Prompting Lab

Drill the mechanics of asking well, then meet the thing that matters more:
what the model can actually see. Both halves are in here because the
second one is invisible until you have felt the first one stop working.

## What you'll learn

- Apply SPEC — specific goal, language, example, constraints — every time
- Use constraints and non-goals to keep a diff small enough to review
- Reach for persona, chain-of-thought and few-shot on the right problems
- Diagnose whether a bad answer is a wording problem or a knowledge problem
- Get a patch instead of a rewrite, and tests before an implementation

## Table of Contents

1. [Vague versus specified](#1-vague-versus-specified)
2. [Constraints and non-goals](#2-constraints-and-non-goals)
3. [Three techniques](#3-three-techniques)
4. [Context engineering](#4-context-engineering)
5. [Professional habits](#5-professional-habits)
6. [Common mistakes](#common-mistakes)
7. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab:

   ```bash
   cd lectures-and-labs/week03/prompting_lab
   pip install -r requirements.txt
   ```

3. Check your progress at any point — this runs locally and reports
   nowhere (its tests fail until DIY 8, and that is expected):

   ```bash
   python scripts/check_progress.py
   ```

You record your work in `lab/prompts/taskN.md`, which are blank templates.
`lab/QUICK_REFERENCE.md` is a one-page reminder of the patterns.

---

## 1. Vague versus specified

### DIY 1: Make the same request twice

Record in `lab/prompts/task1.md`.

1. Ask an assistant, vaguely: *"write a function to get the second largest
   number from a list"*. Save the result.
2. Now write a SPEC version: state the goal, the language and signature,
   two or three worked examples including a tricky one, and the
   constraints.
3. Save that result too.
4. List every **behavioural** difference — not stylistic ones.
5. Write one sentence naming a decision the vague prompt made *for* you.

**What you should have**

`task1.md` containing both prompts, both outputs, and your list of
behavioural differences.

<details><summary>Hint</summary>

Test both against `[10, 10, 9]` and `[5]`. Duplicates and too-short lists
are where the two versions usually diverge, because the vague prompt never
said what should happen.

Step 5 is the point of the exercise. "It was more detailed" is not an
answer; "it decided that duplicates count once" is.

</details>

### DIY 2: SPEC on something with a real trap

Record in `lab/prompts/task2.md`.

1. Write a SPEC prompt for a `slugify` function turning a title into a
   URL-safe string.
2. Include an example containing an apostrophe and one containing
   consecutive spaces.
3. Run it. Test the output against your own examples.
4. If it fails an example, refine **the prompt**, not the code, and try
   again.
5. Record how many iterations it took.

**What you should have**

`task2.md` with your final prompt, the accepted output, and the iteration
count.

<details><summary>Hint</summary>

Apostrophes and repeated spaces are where slugify implementations quietly
disagree — `"Ireland's Best"` can become `irelands-best`, `ireland-s-best`
or `ireland's-best`, and all three are defensible until you say which you
want.

That is exactly the point: it is a decision, and if you do not make it,
something else will.

</details>

---

## 2. Constraints and non-goals

### DIY 3: Stop it helping

Record in `lab/prompts/task3.md`.

1. Take your slugify prompt and add explicit constraints: no external
   libraries, ASCII output only, must not modify its input.
2. Add explicit **non-goals**: no error handling yet, no type hints, do
   not reformat anything else.
3. Run it and compare against your DIY 2 result.
4. Note what disappeared from the output.

**What you should have**

`task3.md` with the constraints, the non-goals, and a note of what the
assistant stopped adding once you said not to.

<details><summary>Hint</summary>

Assistants over-deliver. Without non-goals you routinely get logging, a
CLI, defensive branches and a docstring you did not ask for — all
plausible, none requested.

That matters for review, not tidiness: unrequested changes are the ones
nobody is looking at, which is exactly where a defect survives.

</details>

### DIY 4: Ask for questions first

Record in `lab/prompts/task4.md`.

1. Write a deliberately under-specified request: *"add caching to this
   function"*.
2. Instead of asking for code, ask it to list the questions it would need
   answered first.
3. Record its questions.
4. Answer them, then ask for the implementation.
5. Note which of its questions you had not thought of.

**What you should have**

`task4.md` with the questions it asked, your answers, and at least one
question you had not considered.

<details><summary>Hint</summary>

Given an under-specified request an assistant does not stop — it fills the
gaps and carries on. Asking for the questions makes those assumptions
visible while they are still free to change.

Expect questions about cache size, expiry and whether arguments are
hashable. Any of those, answered wrongly and silently, is a bug.

</details>

---

## 3. Three techniques

### DIY 5: Persona

Record in `lab/prompts/task5.md`.

1. Take `scripts/check_progress.py`, the progress checker you ran in
   Getting started.
2. Ask for a plain review: *"review this code"*. Save the response.
3. Ask again with a persona: a senior engineer specialising in security
   and performance, reviewing for production.
4. Compare what each surfaced.
5. Record the top three improvements you would actually make.

**What you should have**

`task5.md` with both reviews and your three chosen improvements.

<details><summary>Hint</summary>

The persona does not make it smarter — it changes what it *attends to*.
The plain review tends toward style and naming; the security-and-
performance persona goes after validation and complexity.

Neither is complete. That is why the exercise asks you to choose, rather
than to accept a list.

</details>

### DIY 6: Chain-of-thought on a real bug

Record in `lab/prompts/task6.md`.

1. Take a function with a subtle bug — `lab/code/batches.py` has one. It
   passes the obvious example in its docstring, which is the point.
   (`lab/code/domains.py` is the DIY 8 stub; leave it.)
2. Ask it to reason step by step: what the code does, what it should do,
   and where those diverge, **before** proposing a fix.
3. Record the reasoning it produced.
4. Ask for the minimal fix — one to three lines.
5. Write the root cause in your own words.

**What you should have**

`task6.md` with the reasoning trace, a minimal fix, and a root-cause
explanation you wrote yourself.

<details><summary>Hint</summary>

Asking for reasoning matters when correctness depends on intermediate
steps, which is exactly what debugging is. For a one-step lookup it adds
length without adding accuracy.

Step 5 is the exercise. If you cannot explain the root cause without
re-reading its answer, you have not finished.

</details>

### DIY 7: Few-shot for exact format

Record in `lab/prompts/task7.md`.

1. Decide an output format: CSV with a fixed header and column order, no
   commentary.
2. Write **two** IN → OUT examples showing exactly that format.
3. Ask for a third case and check the format matches precisely.
4. Now try the same request *described in prose* instead of shown.
5. Record which held the format better.

**What you should have**

`task7.md` with both attempts and a note on which controlled the format.

<details><summary>Hint</summary>

Vary your two examples along the dimension that matters — a value
containing a comma, or an empty field. Two near-identical examples teach
nothing about edge cases.

Few-shot beats prose for format almost every time: showing is exact,
describing is interpretable.

</details>

---

## 4. Context engineering

Everything above was about wording. This section is about what it can see,
which is the larger half.

### DIY 8: Tests first

Work in `lab/tests/test_extract_domain.py`.

1. That file is a **placeholder that fails on purpose**. Read it.
2. Write real tests for `extract_domain` first — the placeholder's docstring
   lists the four cases: a normal address, a multi-part suffix like
   `.co.uk`, and two malformed inputs that must raise.
3. Only then ask an assistant for an implementation that passes them.
4. Run the tests.
5. Record whether it passed first time, and what you changed if not.

**Expected output**

```text
lab/tests/test_extract_domain.py ....                            [100%]
4 passed in 0.03s
```

<details><summary>Hint</summary>

Tests before implementation gives an executable definition of done. Tests
written afterwards tend to encode whatever the code already does —
including its bugs.

Give it the tests themselves, not a description of them. That is the
context-engineering point in miniature: showing beats summarising.

</details>

### DIY 9: Ask for a patch, not a file

Record in `lab/prompts/task9.md`, saving the diff to `lab/diffs/task9.diff`.

1. Pick a small change to a file you have.
2. Ask for it as a **unified diff**, not a rewritten file.
3. Save the diff.
4. Read every line of it. Find anything you did not ask for.
5. Apply it and confirm it still works.

**What you should have**

A diff in `lab/diffs/task9.diff`, and a note of anything unrequested you
found while reading it.

<details><summary>Hint</summary>

A regenerated file can silently drop a comment, reorder imports or change
an unrelated function, and you would have to diff it yourself to notice.

A 3-line diff gets read. A 40-line diff gets skimmed. You choose which one
you are reviewing when you write the prompt.

</details>

### DIY 10: Wording problem or knowledge problem?

Record in `lab/prompts/task10.md`.

1. Ask the assistant something about **your own** repository that it
   cannot possibly know — the behaviour of a specific function in another
   lab, without showing it.
2. Record the answer. It will be plausible.
3. Reword the question twice more. Record each answer.
4. Now **paste the actual file** and ask again.
5. Write one sentence on what changed, and why rewording could not have
   achieved it.

**What you should have**

`task10.md` with three reworded attempts, the answer after supplying the
file, and your explanation.

<details><summary>Hint</summary>

This is the diagnostic the whole second half turns on: *is this wrong
because I asked badly, or because it does not know something?*

Consistent failure across rewordings is evidence of the second. No amount
of rephrasing adds information that was never there.

</details>

---

## 5. Professional habits

### DIY 11: Write your reflection

Complete `lab/REFLECTION.md`.

1. Give one example where a **constraint** changed the output.
2. Name the technique that worked best for you, and on which problem.
3. Describe one time you caught the assistant inventing something.
4. State what you relied on most: examples, constraints, or supplied
   context.
5. Name two things you will do differently.

**What you should have**

A completed `REFLECTION.md` with five specific answers referring to work
you actually did in this lab.

<details><summary>Hint</summary>

Specific beats general everywhere here. "Constraints help" is not an
answer; "saying *no external libraries* stopped it reaching for a
dependency I would have had to justify" is.

Question 3 is the one worth being honest about. If you did not catch it
inventing anything, you probably did not check.

</details>

---

## Common mistakes

- **Padding with adjectives instead of decisions.** "Robust",
  "professional" and "clean" specify nothing.
- Rewording when the real problem is that it cannot see something.
- Omitting non-goals, then accepting a large diff because the change you
  wanted is somewhere inside it.
- Writing few-shot examples that are near-identical, teaching nothing
  about edge cases.
- Writing tests *after* the implementation, so they encode its bugs.
- Collecting frameworks instead of picking one and using it every time.

## Summary

- A prompt is a **specification**. What you leave out, it decides for you.
- **SPEC** every time; **non-goals** keep the diff small enough to review.
- Persona shifts attention, chain-of-thought helps multi-step problems,
  few-shot controls format.
- Ask the diagnostic: **wording problem, or knowledge problem?** Rewording
  cannot add information.
- Tests before implementation; **diffs, not files**.
