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

3. Open the chat panel with `Ctrl+Alt+I` (`Ctrl+Cmd+I` on a Mac). Its
   icon should also be in the status bar.
4. Look at the row of controls under the chat input and choose
   **Copilot** as the session (it may say **Local** currently), as in the
   setup lab. Every step that talks to the assistant then says what to
   pick in the agent picker, the control that first says **Agent**:
   **Ask** reads your files and answers, but cannot edit a file or run a
   command that changes anything; **Agent** edits files straight away
   and runs commands. Leave the mode and permissions controls on their
   defaults, **Interactive** and **Manual permissions**, and **Agent**
   asks before it runs a command (read-only ones such as `ls` excepted).
   **Autopilot** and **Allow all** stop it asking; this lab never needs
   them. If your picker uses other names, look for the read-only one and
   the one that asks first.

The three levels in this lab's headings map onto those controls: *Ask* is
**Ask**, *Edit* is inline chat (`Ctrl+I`, or `Cmd+I` on a Mac, with the
code selected) and *Agent* is **Agent**. *Fresh conversation* means press
the `+` at the top of the chat panel first.

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

Work in `part1_ask_mode/` (`cd part1_ask_mode` from the lab folder). Its
[walkthrough](part1_ask_mode/README.md) has every prompt and command.

1. Open `mystery_code.py`. **Do not run it yet.**
2. Fresh conversation, **Ask**: ask the assistant to walk you through it
   and say exactly what it prints. Then tell it your own guess for the
   total and ask whether you are right.
3. Run it (`python mystery_code.py`) and see who was right. Then ask what
   `add_discount(150)` would do, and run that too.
4. Open `buggy_code.py`. It processes `grades.csv` and happens to get the
   right answer on that file; its bugs bite on data it has not seen yet.
   Fresh conversation, **Ask**: ask the assistant *what input could make
   this crash or produce the wrong average*. Do not ask it to fix
   anything.
5. Make two of those inputs, a decimal grade and a negative grade, and run
   the code on them (the walkthrough has the commands). Fix one of the
   bugs **yourself**, using what it told you, and run it again.
6. **The hunt.** Ask the step 4 question again in two more fresh
   conversations. Does it name the same inputs each time?

**Expected output**

Step 3 ends with `Total: $1025.96`, and a cart with a 150% discount has a
negative total: the shop pays you. Step 5, before your fix:

```text
ValueError: invalid literal for int() with base 10: '72.5'
```

and the negative grade is averaged in without a word (`Average Grade:
-14.00`). After your fix, the same command does what you decided it
should.

<details><summary>Hint</summary>

For step 2, ask "walk me through this line by line and tell me what each
print produces" rather than "what does this do". The trace forces
specifics; the summary invites hand-waving.

For step 4, if you are stuck, ask what assumptions the code makes about
the CSV: the bug is about a value that is not the type it looks like.

</details>

---

## 2. Edit mode: it changes your files

A step up. You select code, describe the change, and it rewrites that
code in place. You review a diff before accepting.

The diff is the whole safety mechanism. The moment you stop reading it,
edit mode and agent mode are the same tool.

### DIY 2: Refactor with the diff open

Work in `part2_edit_mode/` (`cd ../part2_edit_mode`). Its
[walkthrough](part2_edit_mode/README.md) has every prompt.

1. Run the checker. It calls `calc()` from `messy_code.py` on four lists
   and compares each answer with the original's:

   ```bash
   python check_refactor.py
   ```

2. Open `messy_code.py`, select the whole file, press `Ctrl+I` (`Cmd+I` on
   a Mac) for inline chat, and ask for a refactor: better variable names,
   smaller functions, no behaviour change, and keep the function names
   `calc`, `proc_data` and `get_stuff` because other code calls them.
3. **Read the diff before you choose Keep.** Find one change you did not
   ask for. There is almost always one. Then choose **Keep** and run the
   checker again.
4. If it says `CHANGED`, put the file back with `git restore
   messy_code.py` and ask again, this time saying that every result must
   stay the same, for negative numbers, a list containing 0 and an empty
   list too. Run the checker a third time.
5. Run `broken_calculator.py`. It has several planted bugs (`5!` prints
   24, and `Is 1 prime?` prints True): pick one. Select only that
   function and ask for that bug to be fixed **without** other changes.
   Run it again, then count what changed:

   ```bash
   python broken_calculator.py
   git diff --stat broken_calculator.py
   ```

**Expected output**

Step 1 prints `same` four times. After step 3, if the refactor swapped
in `max()` and `min()`, you will see lines like:

```text
  [-5, -3]               CHANGED  before: {'avg': -4.0, 'max': 0, 'min': -5, 'sum': -8}
                                  now:    {'avg': -4.0, 'max': -3, 'min': -5, 'sum': -8}
```

The old `calc` was wrong on negative numbers and on a list containing 0;
the refactor quietly fixed that, a behaviour change you asked it not to
make. If every line says `same`, its unrequested changes are in the
diff: docstrings, type hints, a guard for the empty list. Step 5: your
line reads `5! = 120` or `Is 1 prime? False`, and `git diff --stat`
counts a few lines, not dozens.

<details><summary>Hint</summary>

"No behaviour change" is worth stating explicitly in step 2. Without it,
assistants tend to add error handling, logging or type hints you did not
ask for, and those are exactly the changes that hide inside a large diff.
Saying it is still not a test: the checker is.

If step 5's diff touches more than a couple of lines, choose **Undo** and
ask again with "change as little as possible".

</details>

---

## 3. Agent mode: it decides the steps

Now you describe an outcome and it works out the steps: which files to
open, what to change, what to run. It may edit several files and execute
commands before handing back.

You are no longer reviewing a change. You are reviewing a **result**.

### DIY 3: Give it a goal, not a plan

Work in `part3_agent_mode/` (`cd ../part3_agent_mode`). Its
[walkthrough](part3_agent_mode/README.md) has the goal to give it.

1. Commit what you have, so you can see exactly what the agent adds:

   ```bash
   git add -A && git commit -m "before the agent"
   ```

2. Decide what "done" means before you start, as something you can check
   on screen in a minute: a command, and what it should print.
3. Fresh conversation, **Agent**: give it the goal from the walkthrough,
   the outcome and not the steps, with your definition as the last line,
   starting `Done when:`.
4. Let it work without interrupting. Allow what it asks to do.
5. Check your `Done when:` line yourself, then run the tests and list
   every file it touched:

   ```bash
   python -m pytest -q
   git status --short
   ```

**Expected output**

Your `Done when:` line holds when you check it by hand, `pytest` ends
with `passed` and no `failed`, and `git status --short` lists new files
(`??`) inside `part3_agent_mode/`. A line for a file anywhere else is a
file it touched that you never mentioned: open it. *Did it do what you
meant, or what you said?*

<details><summary>Hint</summary>

Step 2 matters more than it looks. If you cannot say what done means
before you start, you cannot tell whether the agent got there, and you
will accept whatever it produces because it looks finished.

If it touched files you did not expect, that is a finding, not a failure.
Open them before you go on.

</details>

### DIY 4: Raise the stakes, then review like a detective

Still in `part3_agent_mode/`.

1. Commit again: `git add -A && git commit -m "before the big change"`.
2. Fresh conversation, **Agent**: a change that touches several files.
   Use the walkthrough's due-dates task or one of your own, and say what
   must not change: *Do not edit or delete any existing test.*
3. Review it in this order: which files, then the tests, then whether it
   works.

   ```bash
   git status --short
   git diff -- '*test*'
   python -m pytest -q
   ```

4. Decide. Keep it, or undo all of it (still inside `part3_agent_mode/`;
   `git clean -nd .` only lists what the next line will delete):

   ```bash
   git restore .
   git clean -nd .
   git clean -fd .
   git status --short .
   ```

**Expected output**

`git status --short` lists every file it touched: `M` for a file it
changed, `??` for one it created. If the test diff shows `-` lines, it
changed an existing test although you told it not to: read which
assertion moved, and why that made the tests pass. After an undo, the
last command prints nothing: the folder is back where your commit left
it.

<details><summary>Hint</summary>

There is no correct place to stop and no minimum autonomy you are
supposed to reach. Somebody who undoes the lot because it touched three
files they had not read has done this exercise properly.

*Do not edit any existing test* is the line that blocks the cheapest way
to green: change the test, or the data, until it agrees with the code.
Stop does not undo an edit; your commit does.

If the diff is longer than the terminal, git shows it in a scrolling
viewer and your prompt disappears. Scroll with the arrow keys, then
press `q` to get back to the prompt. If `q` does nothing, you are in the
Vim editor: press `Esc`, type `:q` and press Enter.

</details>

---

## 4. Choosing a mode

By now you have used three levels of autonomy on real tasks. The skill this
lab is actually building is picking one deliberately.

### DIY 5: Pick the rung, then do it

Four small jobs. For each, choose the rung first: **Ask**, Edit (inline
chat), **Agent**, or no assistant at all. Then do the job that way. Work
from the lab folder (`cd ..` from `part3_agent_mode/`).

1. Does `calculate_average` in `part1_ask_mode/buggy_code.py` round its
   answer?
2. Give `get_stuff` in `part2_edit_mode/messy_code.py` a docstring that
   says what it returns.
3. Give your to-do program from DIY 3 a `--version` option that prints
   `1.0`, with a test for it.
4. Make the class average in `part1_ask_mode/grades.csv` come out at
   exactly 75.
5. Now try job 4 on the wrong rung, to see why it is wrong: fresh
   conversation, **Agent**, ask for exactly that. See what it changed,
   then put the folder back as your last commit left it:

   ```bash
   git status --short
   git diff part1_ask_mode/grades.csv
   git restore part1_ask_mode/
   ```

**Expected output**

1. **Ask**: you only need to understand. It does not round; the report
   rounds when it prints the average (`{avg:.2f}`).
2. **Edit**: one function, one small diff you can read in seconds.
3. **Agent**: at least two files and a test run, so you review a result.
   Your program prints `1.0` and `pytest` still passes.
4. **No assistant.** The grades are the record. If the average is not
   75, either the marks or the code is wrong, and deciding which is your
   job. If step 5's diff shows a mark went up or a student appeared, it
   changed the record to hit the number: exactly what you asked for,
   which is the point. If it asked you which marks to change instead, it
   handed the decision back to you, where it belongs.

<details><summary>Hint</summary>

Three questions decide the rung: can you undo it, can you test it, and
what does being wrong cost? Job 4 is easy to undo and easy to test, but
being wrong costs a student a real grade, and no test can tell you which
number is true.

If the diff is longer than the terminal, press `q` to get back to the
prompt (`Esc`, `:q`, Enter if `q` does nothing).

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
