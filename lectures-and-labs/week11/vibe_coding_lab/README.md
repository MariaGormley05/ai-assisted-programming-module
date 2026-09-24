# AIAP Vibe Coding Lab

Build the same application three times without writing much code, then
find out what you actually shipped — and build it once more the other way,
so you have felt both sides of the argument rather than just heard it.

## What you'll learn

- Get a working application out of three prompt-first tools
- Read code you did not write, and find something you would not ship
- Recognise comprehension debt in something you made an hour ago
- Write a specification first and observe what changes
- Decide, with reasons, which mode a task deserves

## Table of Contents

1. [Build it three times](#1-build-it-three-times)
2. [Read what you shipped](#2-read-what-you-shipped)
3. [Build it once more, spec-first](#3-build-it-once-more-spec-first)
4. [Choosing a mode](#4-choosing-a-mode)
5. [Common mistakes](#common-mistakes)
6. [Summary](#summary)

## Getting started

Nothing to install — every tool in this lab runs in a browser. You will
need accounts for three prompt-first builders. All have a free tier that
is enough for this lab.

Create a `REFLECTION.md` in this folder now; you will write into it
throughout.

> **Tool names change.** The three used here are examples of a *category*,
> not a prescription. If one has changed name, pricing or shut down, pick
> another prompt-first builder and note which you used. The exercise is
> about the category.

---

## 1. Build it three times

One brief, three tools. The repetition is the point: it separates what is
true of the *approach* from what is true of one product.

**The brief.** A to-do application. Add a task, mark it done, delete it,
and the list survives a page refresh.

### DIY 1: The same app, three ways

1. Write your prompt **once**, before opening any tool, and save it in
   `REFLECTION.md`. Use the same prompt for all three.
2. Build the app in tool one. Record how long it took and how many
   follow-up prompts you needed.
3. Repeat in tool two.
4. Repeat in tool three.
5. Note the first thing each tool got *wrong*.

**What you should have**

Three working to-do apps, one shared prompt, and a table in
`REFLECTION.md` recording time, number of follow-ups, and the first
mistake for each tool.

<details><summary>Hint</summary>

Using the same prompt for all three is what makes this a comparison rather
than three anecdotes. Resist improving the prompt between tools — if you
must, record that you did and why.

"Survives a page refresh" is the requirement that separates a demo from an
app. Check it explicitly in all three; at least one will usually fail it
until asked again.

</details>

---

## 2. Read what you shipped

You now own three applications you did not write. This section is the
whole reason the lab exists.

### DIY 2: Find something you would not ship

Pick **one** of the three and spend fifteen minutes in its source.

1. Find the file that handles **user input** or **data storage**.
2. Answer in `REFLECTION.md`:
   - How many dependencies did it add? Do you know what any of them do?
   - Is user input validated anywhere before being stored or displayed?
   - If this held real people's data, what would worry you?
3. Find **one line you genuinely cannot explain.** Paste it.
4. Ask the assistant to explain that line. Did the explanation match what
   you had assumed?
5. Ask it directly: *"Review this code for security vulnerabilities as a
   security engineer would."* Record what it finds.

**What you should have**

At least one concrete thing you would not ship, the line you could not
explain, and the security review's findings.

<details><summary>Hint</summary>

Around 45% of AI-generated samples carry a common vulnerability class, so
the base rate is on your side. Unvalidated input is the usual suspect —
look for anything that goes from a form straight into storage or straight
back onto the page.

Step 4 is the real exercise. The gap between what you *assumed* a line did
and what it *does* is comprehension debt, measured directly, on code you
created an hour ago.

</details>

### DIY 3: Estimate the debt

1. Pick the app you understand least.
2. Write down what it would take to add one feature: **let a user edit an
   existing task's text.**
3. Do not build it. Estimate: which files would you need to understand
   first, and how long would that take?
4. Now answer honestly: is that estimate longer or shorter than writing
   the whole app yourself would have been?

**What you should have**

An estimate with reasoning, and an honest comparison against building it
by hand.

<details><summary>Hint</summary>

There is no correct answer and the honest one is often "shorter" — these
tools genuinely save time. The exercise is to make the trade *visible*
rather than to conclude it is bad.

If your answer is "I would just ask the tool to add it", that is a
legitimate strategy. Note what it depends on: that the tool still
understands a codebase it wrote and you did not read.

</details>

---

## 3. Build it once more, spec-first

Now the other side of the argument, so your opinion is based on having
done both.

### DIY 4: Write the spec before the prompt

1. In `spec.md`, **before touching any tool**, write one page:
   - What the app does
   - What it explicitly does **not** do
   - The data it stores, and its shape
   - Three acceptance criteria you could actually test
2. Give the spec to an AI coding assistant and ask for a **plan** — not
   code.
3. Read the plan against your spec. Correct it where it drifted.
4. Only now let it implement.
5. Check the result against your three acceptance criteria.

**What you should have**

`spec.md`, the plan you reviewed and corrected, a working app, and a note
of where the plan drifted from your spec.

<details><summary>Hint</summary>

Step 3 is the step everyone skips, and skipping it turns spec-driven
development into vibe coding with extra paperwork. The plan is the
cheapest place to catch a misunderstanding — cheaper than the code and far
cheaper than the deployed app.

If your spec has no "does not do" section, it is not finished. Bounding
the work is most of the value.

</details>

### DIY 5: Compare, honestly

Record in `REFLECTION.md`:

```text
## Vibe vs spec-driven

Time, vibe coding: ......... [minutes]
Time, spec-driven: ......... [minutes]
Which produced code you would defend? ....... [which, and why]
Which for a throwaway prototype? ............ [which]
Which for something assessed and demonstrated? [which]
Where did writing the spec change what you built? [be specific]
```

1. Fill every line.
2. Add two sentences on which mode you will actually use for your own
   work, and why.

**What you should have**

A completed comparison with a stated preference and a reason that is not
"it is the responsible choice".

<details><summary>Hint</summary>

Spec-driven being slower is not a criticism — it is the cost, and the
question is what the cost buys. If it bought nothing on a to-do app, say
so. That is a real finding, and it is the argument *for* vibe coding on
small disposable work.

The last line is the one worth thinking about: what did writing it down
change about what you built? Usually something.

</details>

---

## 4. Choosing a mode

### DIY 6: Write your own rule

1. Complete this table in `REFLECTION.md` with **your own** examples:

   | Task | Mode I'd choose | Why |
   |---|---|---|
   | A weekend prototype | | |
   | A feature in assessed work | | |
   | Something a stranger maintains | | |
   | Code handling other people's data | | |

2. Add one row for a task you would give **no** assistant.
3. Write two sentences on what would have to change for you to move a task
   from one mode to the other.

**What you should have**

A completed table with concrete tasks, including one you would not
delegate, and a stated condition for switching modes.

<details><summary>Hint</summary>

Useful axes for the last question: how reversible is it, how well can you
test it, how long will it live, and who pays if it is wrong.

If every row says the same mode, you have not found your boundary. Push
until you do — the boundary is the actual output of this lab.

</details>

---

## Common mistakes

- **Judging a generated app by whether it runs.** Running is the minimum,
  not the evidence.
- **Improving the prompt between tools**, which turns a comparison into
  three separate anecdotes.
- **Skipping the plan review** in the spec-first build, which removes the
  only thing that made it different.
- **Writing a spec for something you will delete on Sunday** — that is the
  over-correction, and it is just as wrong.
- Concluding that vibe coding is bad. It is excellent for disposable work;
  the failure is vibe coding something you then **keep**.

## Summary

- Prompt-first tools genuinely produce working applications, fast.
- The cost is **comprehension debt** — and you can measure it on your own
  code within an hour of creating it.
- Reading what you shipped reliably finds something you would not ship.
- **Spec-driven** moves review from the implementation to the intent, and
  charges you real time for it.
- Choose **per task**: stakes, reversibility, lifespan, and who pays if it
  is wrong.
