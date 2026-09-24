# AIAP Coding Agents Lab

An assistant that answers questions is a different tool from one that
edits your files, which is different again from one that runs commands on
its own. This lab walks up that ladder of autonomy in the editor, and asks
you to decide where you want to stand on it. An agent with your whole
terminal is a step further again, and has [a lab of its own](../../week09/cli_agents_lab/).

## What you'll learn

- Tell the three editor modes apart by what each is allowed to touch:
  answer only, edit files, act on its own
- Write an agent request as an outcome with a definition of done, not a
  list of steps
- Judge how much autonomy a task deserves, rather than defaulting to the
  most or the least
- Review an agent's work when it changed several files at once
- Recognise the failure mode where an agent confidently does the wrong
  thing quickly

## Table of Contents

1. [Ask mode: it answers, you type](#1-ask-mode-it-answers-you-type)
2. [Edit mode: it changes your files](#2-edit-mode-it-changes-your-files)
3. [Agent mode: it decides the steps](#3-agent-mode-it-decides-the-steps)
4. [Choosing a mode](#4-choosing-a-mode)
5. [Extensions](#5-extensions)
6. [Common mistakes](#common-mistakes)
7. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab and install its dependencies:

   ```bash
   cd lectures-and-labs/week06/agents_lab
   pip install -r requirements.txt
   ```

3. Confirm the editor assistant is active — you should see its icon in the
   status bar, and `Ctrl+Alt+I` should open its chat panel.

Each section has a folder beside this README (`part1_ask_mode/`,
`part2_edit_mode/`, …) holding the code you work on and the detailed
walkthrough. This page is the spine; the folders are the detail.

---

## 1. Ask mode: it answers, you type

The most restricted mode. It reads what you show it and replies in the
chat panel. It cannot touch a single file — every change is one you make
yourself.

That restriction is the feature. Ask mode is how you understand code
before deciding what to do to it, and understanding is the thing that
does not survive being skipped.

### DIY 1: Understand code you did not write

Work in `part1_ask_mode/`.

1. Open `mystery_code.py`. **Do not run it yet.**
2. Ask the assistant to explain what it does, then write down what it will
   print **before** running anything.
3. Run it. Compare the real output with your prediction.
4. Open `buggy_code.py`. It processes `grades.csv` and happens to get the
   right answer on that file; its bugs bite on data it has not seen yet.
   Ask the assistant *what input could make this crash or produce the
   wrong average* — do not ask it to fix anything.
5. Fix the bug **yourself**, using what it told you.

**What you should have**

`mystery_code.py` explained in your own words, your prediction recorded
alongside the real output, and a one-line fix to `buggy_code.py` you can
justify.

<details><summary>Hint</summary>

For step 2, ask "walk me through this line by line and tell me what each
print produces" rather than "what does this do". The trace forces
specifics; the summary invites hand-waving.

For step 4, if you are stuck, ask what assumptions the code makes about
the CSV — the bug is about a value that is not the type it looks like.

</details>

---

## 2. Edit mode: it changes your files

A step up. You select code, describe the change, and it rewrites that
code in place. You review a diff before accepting.

The diff is the whole safety mechanism. The moment you stop reading it,
edit mode and agent mode are the same tool.

### DIY 2: Refactor with the diff open

Work in `part2_edit_mode/`.

1. Open `messy_code.py` and read it. Note two things you dislike.
2. Select the whole file and ask for a refactor: better names, smaller
   functions, no behaviour change.
3. **Read the diff before accepting.** Find one change you did not ask
   for. There is almost always one.
4. Accept, reject, or amend — and record which and why.
5. Repeat on `broken_calculator.py`, which has a real bug. Ask for the
   bug to be fixed **without** other changes.

**What you should have**

Two refactored files, and a note naming the unrequested change from step 3
and what you did about it.

<details><summary>Hint</summary>

"No behaviour change" is worth stating explicitly in step 2 — without it,
assistants tend to add error handling, logging or type hints you did not
ask for, and those are exactly the changes that hide inside a large diff.

If step 5's diff touches more than a couple of lines, reject it and ask
again with "change as little as possible".

</details>

---

## 3. Agent mode: it decides the steps

Now you describe an outcome and it works out the steps: which files to
open, what to change, what to run. It may edit several files and execute
commands before handing back.

You are no longer reviewing a change. You are reviewing a **result**.

### DIY 3: Give it a goal, not a plan

Work in `part3_agent_mode/` and follow its README for the full brief.

1. Read the task in `part3_agent_mode/README.md`.
2. Before starting, write down in one sentence what "done" means to you.
3. Give the agent the goal — the outcome, not the steps.
4. Let it work without interrupting. Note every file it touched.
5. Check the result against your definition from step 2. Then run the
   tests.

**What you should have**

A working result, a list of every file the agent modified, and an honest
answer to: *did it do what you meant, or what you said?*

<details><summary>Hint</summary>

Step 2 matters more than it looks. If you cannot say what done means
before you start, you cannot tell whether the agent got there — and you
will accept whatever it produces because it looks finished.

If it touched files you did not expect, that is a finding, not a failure.
Write it down.

</details>

### DIY 4: Find the edge of your comfort

1. Give the agent a task deliberately at the edge of what you would trust
   it with — touching several files, or something you would find tedious
   to review.
2. **Before running it**, write down what you would need to see to accept
   the result.
3. Run it. Review against your own criteria from step 2.
4. Record where your comfort ran out, and why.

**What you should have**

A written answer to: *at what point did you stop being able to verify
this, and what would you need in place to go further?*

<details><summary>Hint</summary>

There is no correct answer and no minimum autonomy you are supposed to
reach. Somebody who writes "I stopped trusting it once it touched three
files I had not read" has done this exercise properly.

Commit before you start, so `git diff` is your review tool and `git
checkout` is your undo.

</details>

---

## 4. Choosing a mode

By now you have used three levels of autonomy on real tasks. The skill this
lab is actually building is picking one deliberately.

### DIY 5: Write your own rule

1. Create `REFLECTION.md` in this folder and fill in the table below for
   yourself.
2. For each row, give a concrete task from this lab or your own work.
3. Add one row of your own for a task you would give **no** assistant.

   | Mode | When I'd use it | Example task |
   |---|---|---|
   | Ask | | |
   | Edit | | |
   | Agent | | |
   | None | | |

4. Write two sentences on what would have to change for you to move a task
   up one level.

**What you should have**

A completed table in `REFLECTION.md` with real examples, including at
least one task you would not delegate at all.

<details><summary>Hint</summary>

The last row is the important one. If you cannot name a task you would
keep, either you have not found your limit yet or you are not looking —
and both are worth writing down honestly.

Useful axes for step 4: how reversible is it, how well can you test it,
and how much does being wrong cost.

</details>

---

## 5. Extensions

Optional, and genuinely optional — the sections above are the two-hour
path. These are worth doing at home if agents interest you.

- **`part4_cloud_agent/`** — an agent that works asynchronously on a
  repository and opens a pull request, rather than working beside you.
- **`part5_google_jules/`** — a second asynchronous agent, useful mainly
  as a comparison against the first.

The interesting question in both: when the agent works while you are not
watching, what does review even mean?

---

## Common mistakes

- **Reaching for the most autonomous mode by default.** Ask mode is the
  right tool more often than it gets used, because understanding is the
  step people skip.
- **Accepting a diff without reading it.** The diff is the only safety
  mechanism edit mode has. Skipping it converts it into agent mode with
  extra steps.
- **Describing steps instead of outcomes in agent mode**, which wastes
  what the mode is for — then blaming the agent for following them.
- **Not committing first.** `git diff` is your review tool and
  `git checkout` is your undo. Without a clean starting point you have
  neither.
- **Judging a tool on capability when the difference is behaviour.** Two
  agents that can both do the task may differ entirely in what they do
  without asking.

## Summary

- The modes form a ladder: **answer → edit → act**, and each rung trades
  review effort for reach.
- The unit of review changes as you climb: a suggestion, then a diff,
  then a result. Know which one you are looking at.
- In agent mode, say what **done** means before it starts — otherwise
  you will accept whatever looks finished.
- Pick the level deliberately per task. Reversibility, testability, and
  the cost of being wrong are the axes that matter.
- The honest output of this lab is knowing where **your** comfort ends,
  and what would have to be true to move it.
