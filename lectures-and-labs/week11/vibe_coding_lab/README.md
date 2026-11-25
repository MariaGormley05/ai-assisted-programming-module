# AIAP From Vibes to Agents Lab

You will build the same small program three times, each time with a
different way of working with AI. First you vibe-code it: one loose
prompt, and you never read the code. Then you build it from a written
spec, checking Copilot's plan before any code exists. Then a coding agent
builds it from the spec, a set of rules and a set of tests, and keeps
going until every test passes. At the end, one script gives all three
versions the same exam.

The program is **Exam Season To-Do**, a small command-line to-do list: add
tasks with a priority and a due date, tick them off, and see what is
overdue. It is small enough to build three times in one lab, and its
sorting, dates and saving give an AI plenty to get wrong.

## What you'll learn

- Vibe-code a small program, then find out how much of it you can explain
  without running it
- Write an acceptance criterion, and correct an AI's plan against a spec
  before any code is written
- Steer a coding agent with an `AGENTS.md` file and tests written by a
  person, and check that the agent's code works for any input, not just
  for the tests' own
- Name the parts of a coding agent while you watch one work: the model, its
  tools, its context, its loop and its guardrails
- Give three versions of one program the same exam, and explain why the
  vibe-coded version usually fails it

## Table of Contents

1. [Vibe-code it](#1-vibe-code-it)
2. [Read what you vibe-coded](#2-read-what-you-vibe-coded)
3. [Build it from a spec](#3-build-it-from-a-spec)
4. [Hand it to an agent](#4-hand-it-to-an-agent)
5. [Give all three the same exam](#5-give-all-three-the-same-exam)
6. [Stretch tasks](#6-stretch-tasks)
7. [Common mistakes](#common-mistakes)
8. [Summary](#summary)

## Getting started

**Words this lab uses.**

- **Vibe coding**: building software by describing what you want to an AI,
  running what it produces and pasting any error back, without reading the
  code. Andrej Karpathy, an AI researcher, named it in February 2025.
- **Spec** (specification): a short document that says what a program must
  do and what it must not do.
- **Acceptance criterion**: a check you can actually run that shows one
  requirement works, for example *add a task with a blank title: you get an
  error, and the list stays empty*.
- **Spec-driven development**: writing the spec first, having the AI plan
  from it, and checking that plan before any code is written.
- **Coding agent**: an AI that does not just answer but acts. A coding
  agent edits files and runs commands, in a loop, until the job is done.
- **`AGENTS.md`**: a file of standing instructions for coding agents, a
  README written for the AI. Most coding agents look for one.
- **Comprehension debt**: the later cost of understanding code that an AI
  wrote and nobody read.

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab's folder and look at what is in it:

   ```bash
   cd lectures-and-labs/week11/vibe_coding_lab
   ls
   ```

3. Open the chat panel with `Ctrl+Alt+I` (`Ctrl+Cmd+I` on a Mac) and
   choose **Copilot** as the session. Every step that uses the assistant
   names the role to pick in the agent picker: **Ask** reads your files
   and answers, but cannot edit a file or run a command that changes
   anything; **Agent** edits files straight away and asks before it runs a
   command. Leave the mode and permissions controls on their defaults,
   **Interactive** and **Manual permissions**. If your picker uses other
   names, look for the read-only one and the one that asks first.

*Fresh conversation* means press the `+` at the top of the chat panel
first.

| File | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The spec: what the program must do, with an acceptance criterion for every requirement |
| [`AGENTS.md`](AGENTS.md) | The rules a coding agent follows in this folder |
| [`tests/test_todo.py`](tests/test_todo.py) | 9 tests, written by a person, that check the spec |
| [`todo.py`](todo.py) | The program the agent will write. For now every part of it is a stub that does nothing |
| [`compare.py`](compare.py) | A script that gives every version of the program the same exam |
| [`PROMPT.md`](PROMPT.md) | The prompt for the loop in the last stretch task |
| [`pytest.ini`](pytest.ini) | Tells pytest, the test runner, to run only the tests in `tests/` |

Each version of the program gets its own place: you create the folders
`vibe/` and `spec/`, and the agent works on `todo.py` in this folder.
pytest is already installed in the Codespace.

**Time:** about 90 minutes: 10 for getting started, then about 15 for
section 1, 10 for section 2, 25 for section 3, 25 for section 4 and 5 for
section 5. Section 6 is for anyone who finishes early. Every step says
exactly what to type, click or look for.

**Your Copilot allowance.** Copilot's student plan has a monthly
allowance, shared by the chat and the command-line agent. Sections 1 to 5
send Copilot about 15 to 25 messages; the loop in section 6 sends at most
3 more.

---

## 1. Vibe-code it

*About 15 minutes.*

The first version is vibe-coded, the way people first built programs with
a chatbot: one loose prompt, accept whatever comes back, run it, and paste
any error straight back. Speed is the only goal. You work in **Ask**, so
Copilot only answers in the chat, and you copy its code into a file
yourself.

**The rules of vibing**

- You may **not** read the code. Copy it, save it and run it.
- You may **not** edit the code yourself.
- When something breaks, paste the error straight back to Copilot with no
  comment.
- Stop at 15 minutes, whether the program works or not.

### DIY 1: Vibe-code the to-do app

1. Close every file that is open in the editor, so that Copilot cannot see
   the spec or the tests. Then, in the terminal, make a folder for this
   version and move into it:

   ```bash
   mkdir vibe
   cd vibe
   ```

2. Fresh conversation, **Ask**. Start a timer, then send this prompt. Its
   last line stops Copilot reading the spec and the tests in this lab's
   folder:

   ```text
   make me a python to-do app for exam season. it should have priorities
   and due dates and save my tasks. command line is fine. just give me the code.
   don't read any files in my project, use only what I have said here.
   ```

3. Without reading the code, save it: open the three-dot menu on the code
   block in Copilot's reply, choose **Insert into New File**, and save the
   new file as `todo.py` in the `vibe` folder (`Ctrl+S`). Then run the
   program the way Copilot's reply says, for example `python todo.py`.
4. Try to break the program: add a task with a blank title, a task with
   the priority "urgent", and a task due "next tuesday". Then run the
   program again: are your tasks still there?
5. When something breaks, paste the error straight back into the same
   conversation with no comment, replace the whole of `vibe/todo.py` with
   the new code, and run the program again. Repeat until it works or the
   15 minutes are up.

**What you should have**

`vibe/todo.py`: a program you have run but never read. On screen, what the
program did with a blank title, with "urgent" and with "next tuesday", and
whether your tasks were still there when you ran the program again. A
program that is still broken after 15 minutes is a result too.

<details><summary>Hint</summary>

Ask can read every file in your Codespace, and the only way to keep
Copilot to what you typed is to say so and then check. If the reply
mentions `SPEC.md`, the tests or a class called `TodoList`, Copilot read
the files in this folder: start a fresh conversation, check that no file
is open in the editor, and send the prompt again.

A blank title, "urgent" and "next tuesday" are not in the prompt, so
whatever the program does with them is a decision Copilot made for you.
You find out which decisions Copilot made only by running the program, or
by reading the code, which is section 2.

If Copilot's reply tells you to `pip install` a package, look the package
up on [pypi.org](https://pypi.org) first and check that it exists and is
the one you expect. AI models sometimes invent package names, and
attackers register invented names with harmful code in them (this is
called slopsquatting). Python's standard library is enough for this
program.

</details>

---

## 2. Read what you vibe-coded

*About 10 minutes.*

You now own a program you have never read. Its comprehension debt is the
time you would need to understand the program before you could safely
change it, and the debt grows with every line nobody reads. This section
measures some of yours.

### DIY 2: Explain it without running it

1. Open `vibe/todo.py` and read it for the first time. Without running
   anything, find the answer to each of these questions in the code:
   - Which file does the program save your tasks in?
   - What does the program do if you mark a task done that does not
     exist, for example number 99?
   - What does the program do if its save file holds rubbish instead of
     tasks?
2. Now check each answer by running the program. For the last question,
   put rubbish in the save file first (this replaces the tasks you saved
   in DIY 1), then list your tasks. If your program's save file has
   another name, use that name instead of `tasks.json`:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab/vibe"
   echo "not a task list" > tasks.json
   ```

3. Find one line in `vibe/todo.py` that you cannot explain, and decide
   what you think the line does.
4. Fresh conversation, **Ask**: type `What does this line of Python do?`,
   paste the line under it, and send. Compare Copilot's answer with what
   you decided.

**What you should have**

Your three answers from reading the code, each beside what the program
really did when you ran it, and one line you could not explain beside
Copilot's explanation of that line.

<details><summary>Hint</summary>

Every gap between what you decided the code does and what it really does
is comprehension debt, measured on code you made twenty minutes ago. A
project made of code like this, which nobody understands and so nobody
dares to change, is what developers call a **haunted codebase**.

The rubbish file is a fair test: files get damaged, and your prompt never
said what should happen when one is. If the program crashed, that was a
choice the AI made for you too.

The save file is usually in the folder you ran the program from, `vibe`,
but some programs keep it in your home folder. To find it, search the code
for `open(` or `json`.

</details>

---

## 3. Build it from a spec

*About 25 minutes.*

The second version is built with spec-driven development: the spec says
what "done" means, Copilot plans from it, and you check that plan before
any code exists. Tools such as GitHub Spec Kit (an open-source toolkit
from GitHub, September 2025) and Kiro (a coding editor from Amazon Web
Services, July 2025) follow the same order: spec, plan, tasks, code. This
lab's spec is `SPEC.md`, and every requirement under **Must have** comes
with an acceptance criterion. You still work in **Ask**, but this time you
read every piece of code before you save it.

### DIY 3: Check the plan before any code

1. Make a folder for this version, with its own copy of the spec:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab"
   mkdir spec
   cp SPEC.md spec/SPEC.md
   ```

2. Open `spec/SPEC.md` and read it properly. Then add one feature of your
   own to the **Must have** list, as point 7, with an acceptance
   criterion: a check someone can run. Ideas: delete a task by its id;
   show how many tasks are done; change a task's priority. Keep clear of
   the spec's **Out of scope** list.
3. Close every other file, so that `spec/SPEC.md` is the only file open in
   the editor: Copilot reads the file you have open. Fresh conversation,
   **Ask**:

   ```text
   Here is my spec, spec/SPEC.md. Do NOT write any code yet.
   1. List any questions or gaps you see in the spec.
   2. Write a short technical plan.
   3. Break the plan into numbered tasks, each small enough to test on its own.
   ```

4. Read Copilot's questions, plan and tasks. Answer the questions in the
   same conversation, and change `spec/SPEC.md` wherever Copilot found a
   real gap.
5. Find at least one thing in the plan you disagree with, and tell Copilot
   to change it.

**What you should have**

In the chat: Copilot's questions, plan and numbered tasks, with your
answers and your change under them. In `spec/SPEC.md`: your point 7, and
any gap you fixed.

<details><summary>Hint</summary>

Checking the plan is the step that makes this spec-driven. Skip it, and
spec-driven development is just vibe coding with extra documents. The plan
is the cheapest place to catch a misunderstanding: cheaper than the code,
and far cheaper than a program people already use.

Nothing to disagree with? Look at how the plan stores the tasks, how it
picks the next id after the list is loaded again (the spec says ids are
never reused), and whether it adds anything the **Out of scope** list
rules out.

Some developers argue that writing a full spec first brings back the
**waterfall** method, in which each stage of a project, from requirements
to design to code, is finished before the next one starts. François
Zaninotto, of the software company Marmelab, made that case in
"Spec-Driven Development: The Waterfall Strikes Back" (November 2025).
This lab keeps the spec to one page and lets you change the plan in the
chat, so each step stays small.

</details>

### DIY 4: Build it one task at a time

1. In the same conversation, still in **Ask**, send:

   ```text
   Write the code for task 1 only, as the whole of spec/todo.py.
   ```

   This time, read the code before you save it. Save it as `todo.py` in
   the `spec` folder: the three-dot menu on the code block, then **Insert
   into New File**, then `Ctrl+S`.
2. For each next task, send this, with the right task number:

   ```text
   Now add task 2. Show the whole of spec/todo.py again.
   ```

   Read the change, then replace the whole file. If time runs short, ask
   for all the remaining tasks together.
3. Check each acceptance criterion by hand, with commands like the ones in
   the spec's **Command line** section:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab/spec"
   python todo.py add "Revise Java" --priority high --due 2026-12-01
   python todo.py add "Lab report" --priority low
   python todo.py add "   "
   python todo.py add "Gym" --priority urgent
   python todo.py done 99
   python todo.py list
   ```

4. When the program breaks a requirement, tell Copilot which point of the
   spec it breaks ("point 2 says a blank title gives a clear error"),
   rather than pasting the error.

**What you should have**

`spec/todo.py`, built one task at a time from the plan, and the commands'
output on screen: an error for the blank title, for "urgent" and for task
99, and a list that shows "Revise Java" above "Lab report". The list comes
from a new run of the program, so it also shows that the tasks were saved
and loaded again.

<details><summary>Hint</summary>

Quoting the spec tells Copilot what the program should do. Pasting an
error only tells Copilot what went wrong, so the fix may change something
else.

Reading each task's code as it arrives is what stops the debt from
section 2 building up again: every piece is small when you read it.

</details>

---

## 4. Hand it to an agent

*About 25 minutes.*

The third version is written by a coding agent: Copilot's **Agent**, which
edits files and runs commands itself, in a loop, until the job is done.
You write no code and paste none. Your job is to set up what the agent
works from: the spec, the rules in `AGENTS.md`, and tests written by a
person. The tests are the referee: they decide when the job is done, not
the agent.

### DIY 5: Red first

1. Go back to the lab folder and run the tests:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab"
   python -m pytest -q
   ```

2. Open `todo.py`. Every method is a stub that does nothing, so every test
   fails. Running the tests before any code exists, and watching them
   fail, is called **red first**: a test you have seen fail is a test that
   can fail, so when it passes later, the pass means something.
3. Open `AGENTS.md` and read the rules the agent will follow.
4. Open `tests/test_todo.py`. For each of the 9 tests, find the point of
   the **Must have** list in `SPEC.md` that the test checks.

**Expected output**

```text
FFFFFFFFF                                                                [100%]
...
FAILED tests/test_todo.py::test_ids_start_at_1_and_go_up - AssertionError: assert None == 1
FAILED tests/test_todo.py::test_default_priority_is_medium - IndexError: list index out of range
FAILED tests/test_todo.py::test_blank_title_is_rejected - Failed: DID NOT RAISE <class 'ValueError'>
...
9 failed in 0.21s
```

<details><summary>Hint</summary>

Each failure says what its test expected. `assert None == 1` means `add()`
should have returned the new task's id, 1, but returned nothing.
`DID NOT RAISE <class 'ValueError'>` means a blank title should have been
refused with a `ValueError`.

`1 error` and no failures is not red. It means the tests could not even
start, usually because `todo.py` is missing or has a syntax error, so
nothing was tested at all.

Copilot reads the `AGENTS.md` at the top of your repository by itself.
Whether Copilot also reads one inside a folder depends on a setting, so
DIY 6's prompt names this folder's `AGENTS.md` to be sure.

</details>

### DIY 6: Let the agent build it

1. Commit everything first, so that you can see exactly what the agent
   changes, and undo it if you need to:

   ```bash
   git add -A . && git commit --allow-empty -m "before the agent"
   ```

2. Close every file in the editor. Fresh conversation, **Agent**. Send
   this prompt, then keep your hands off the keyboard except to answer the
   agent's questions:

   ```text
   Work only in the folder lectures-and-labs/week11/vibe_coding_lab.
   Read the AGENTS.md and SPEC.md in that folder. Then build todo.py in that
   folder so that every test in its tests folder passes, following the rules
   in that AGENTS.md. Run the tests as you go, from that folder, with
   python -m pytest -q
   ```

3. The agent edits files without asking, but asks before it runs a
   command. Read each command before you allow it. Allow
   `python -m pytest -q` and the commands from the spec's **Command line**
   section; skip anything that installs a package or deletes files.
4. While the agent works, watch for the five parts of a coding agent:
   - the **model**: the AI that writes the plan and the code;
   - its **tools**: editing files, and running commands in the terminal;
   - its **context**: `AGENTS.md`, `SPEC.md` and the test results the
     agent reads;
   - its **loop**: edit, run the tests, read the failures, fix, run the
     tests again;
   - its **guardrails**: the questions the agent asks you, and the tests.

   Count how many times the agent runs the tests.
5. When the agent stops, read its last message: `AGENTS.md` told the
   agent to finish with what it built and anything in `SPEC.md` it was
   unsure about. Choose **Keep** if VS Code asks whether to keep the
   agent's changes.

**What you should have**

`todo.py` written by the agent, the agent's last message listing what it
built and what it was unsure about, and how many test runs the agent
needed to get there.

<details><summary>Hint</summary>

Answering each command question puts you **in the loop**: a person
approves each step the agent takes. The loop in the last stretch task runs
without asking, so there you are only **on the loop**: watching, ready to
stop it.

If the agent tries to run the tests from the top of the repository, skip
that command and tell the agent to run it from the lab folder. From the
top, pytest finds every lab's tests, and the agent may start "fixing"
other labs.

Commit first because stopping the agent does not undo what the agent has
already changed. `git` can undo it.

</details>

### DIY 7: Check the agent's work

1. Run the tests yourself:

   ```bash
   python -m pytest -q
   ```

2. Check that the agent left the tests alone. This prints nothing if no
   file in `tests/` was changed or added:

   ```bash
   git status --short -- tests
   ```

3. Check that the agent did not **special-case** the tests, that is, write
   code that recognises the tests' own inputs instead of code that works
   for any input. This prints nothing if `todo.py` never mentions the
   tasks that only the tests use:

   ```bash
   grep -n -e "Lab report" -e "Late but done" -e "High sooner" -e "Buy milk" todo.py
   ```

4. Try the program by hand, starting from an empty list, as the spec's
   **Command line** section says:

   ```bash
   rm -f tasks.json
   python todo.py add "Revise Java" --priority high --due 2026-12-01
   python todo.py add "Panic" --priority urgent
   python todo.py list
   python todo.py done 1
   python todo.py overdue
   ```

**What you should have**

`9 passed` from the tests, nothing printed by `git status` or `grep`, and
the program working by hand: "Revise Java" added and listed, "urgent"
refused with an error, and task 1 marked done.

<details><summary>Hint</summary>

The agent's last message is the agent's own account of its work. The
tests, `git status` and your own commands are the evidence.

An agent that cannot make a test pass honestly can make it pass another
way: by changing the test, or by writing code that only works for the
test's own inputs. Both are called gaming the tests. `AGENTS.md` forbids
both, but `AGENTS.md` is text the model weighs, not a lock: steps 2 and 3
are the check.

The program keeps your tasks in `tasks.json` in this folder. The agent may
have added some tasks while trying the commands, which is why step 4
deletes the file first.

</details>

---

## 5. Give all three the same exam

*About 5 minutes.*

### DIY 8: Run the same exam on all three

1. From the lab folder, run the comparison script:

   ```bash
   python compare.py
   ```

   `compare.py` copies each version into a temporary folder and gives
   every version the same exam: the 9 tests, then the spec's command line,
   run as three separate commands (add a task, add a task with the
   priority "urgent", list the tasks).
2. If your vibe version passed none of the tests, find out why: open
   `vibe/todo.py` and search it (`Ctrl+F`) for `class TodoList`, then for
   `def pending`.
3. Open `SPEC.md` and find the part that settled what your vibe prompt
   left open: the **Technical notes**.

**Expected output**

```text
Giving each version the same exam...

The same exam for every version of the to-do app

                                        vibe     spec     agent
Tests passed (out of 9)                 0        8        9
Lists a task added by an earlier run    yes      yes      yes
Refuses the priority "urgent"           yes      yes      yes

Why a version passed none of the tests:
  vibe: ImportError: cannot import name 'TodoList' from 'todo'
```

This is one student's run, and your numbers will be your own. A vibe
version usually passes none of the tests.

<details><summary>Hint</summary>

The tests call `TodoList()`, `add()`, `pending()` and the other names that
`SPEC.md` lists under **Technical notes**. Your vibe prompt named none of
them, so Copilot chose its own names, and the tests could not even start.
Every decision a prompt leaves out still gets made, by the AI.

The spec version shows how much of the work the spec did: the same
Copilot, given the names and the rules, gets most of the tests right
without being given the tests. If your vibe version passed some tests,
Copilot probably read `SPEC.md` or `todo.py` despite the prompt.

None of this makes vibe coding wrong. For a program you will throw away,
failing someone else's exam does not matter. It matters for code you are
going to keep.

</details>

---

## 6. Stretch tasks

For anyone who finishes early. DIY 9 needs no AI at all. DIY 10 uses up
to three premium requests, which DIY 10 explains.

### DIY 9: Find what the tests do not check

On 8 September 2026, OpenAI claimed that about 10,000 of its AI agents,
working for about 88 hours, had solved a version of the Navier-Stokes
problem, one of the seven Millennium Prize problems in mathematics (each
carries a $1 million prize). The problem asks whether the equations that
describe how water and air move can break down, and OpenAI's claim is that
they can, when a suitable outside force pushes the fluid. The claim came
with a proof written in **Lean**, a programming language in which a
computer checks every step of a proof, and the Lean proof compiles: the
computer found no faulty step. That has not settled the matter. Who
deserves the credit is disputed, and a **preprint** (a paper posted before
other experts have reviewed it) from 6 October 2026 argues that the Lean
proof does not match the written paper. A checker checks exactly what it
is given, and nothing else. Tests are the same: 9 passing tests check 9
things.

1. Read `SPEC.md` again, and find a requirement that none of the 9 tests
   checks. The hint names one if you are stuck.
2. Create the file `tests/test_command_line.py` with this test in it. The
   test runs `todo.py` the way you would type it, in a temporary folder:

   ```python
   """Tests for the part of SPEC.md the first 9 tests never check: the command line."""
   import subprocess
   import sys
   from pathlib import Path

   TODO = Path(__file__).resolve().parent.parent / "todo.py"


   def run(folder, *words):
       """Run todo.py in folder, as if typed in a terminal, and return what it printed."""
       finished = subprocess.run([sys.executable, str(TODO), *words], cwd=folder,
                                 capture_output=True, text=True, timeout=10)
       return finished.stdout + finished.stderr


   def test_a_task_added_by_one_run_is_listed_by_the_next(tmp_path):
       run(tmp_path, "add", "Revise Java", "--priority", "high", "--due", "2026-12-01")
       assert "Revise Java" in run(tmp_path, "list")
   ```

3. Run the tests: `python -m pytest -q`.
4. Write a second test in the same file, in the same way: a task with the
   priority "urgent", added on the command line, must not appear in the
   list. Run the tests again.

**What you should have**

`tests/test_command_line.py` holding two tests, and a test run with 11
tests in it: all passing, or a red one that shows a requirement the agent
never met even though the first 9 tests were green.

<details><summary>Hint</summary>

The requirement the 9 tests never check is the whole **Command line**
section of `SPEC.md`: not one of them runs `python todo.py`. An agent
could pass all 9 with no command line at all. `AGENTS.md` asks the agent to
try the commands by hand, but that is a request, not a check.

One way to write step 4's test:

```python
def test_the_priority_urgent_is_refused_on_the_command_line(tmp_path):
    run(tmp_path, "add", "Revise Java")
    run(tmp_path, "add", "Panic", "--priority", "urgent")
    listing = run(tmp_path, "list")
    assert "Revise Java" in listing
    assert "Panic" not in listing
```

Why add "Revise Java" first? A test that only checks that something is
missing also passes when the program does nothing at all: against the stub
`todo.py`, which lists nothing, `"Panic" not in ...` is true. The first
assert makes the test fail until the list works, the same red first idea
as DIY 5.

`compare.py` uses only `tests/test_todo.py`, so its exam stays the same 9
tests for every version.

</details>

### DIY 10: The Ralph Wiggum loop

The **Ralph Wiggum loop** runs a coding agent on the same prompt file
again and again, with a fresh start every round. Geoffrey Huntley, an
Australian software developer, described it in July 2025 and named it
after Ralph Wiggum, a cheerful and not very clever boy in the cartoon
series *The Simpsons*: the agent remembers nothing between rounds, but the
agent keeps trying. Huntley's own loop never stops by itself. This one stops
when the tests pass, or after three rounds, because every round costs
something: each round is one `copilot -p` call, and each call uses at
least one **premium request**, GitHub's name for a request counted against
your plan's monthly allowance.

`copilot -p` runs GitHub Copilot CLI, the command-line version of Copilot,
**headless**: the command gives the agent one prompt and exits, with
nobody there to answer the agent's questions, so anything not allowed in
advance is refused.

1. Make a folder for the loop with the spec, the rules, the prompt and the
   tests, but no `todo.py`, so that the loop starts from nothing:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab"
   mkdir -p ralph/tests
   cp SPEC.md AGENTS.md PROMPT.md pytest.ini ralph/
   cp tests/test_todo.py ralph/tests/
   cd ralph
   ```

2. Check that Copilot CLI is installed:

   ```bash
   copilot --version
   ```

   If the command is not found, install Copilot CLI with
   `npm install -g @github/copilot`. Then, still in the `ralph` folder,
   start Copilot CLI once by typing `copilot`. When Copilot CLI asks
   whether you trust the files in this folder, choose **Yes, and remember
   this folder for future sessions**: the loop starts Copilot CLI in this
   folder again with nobody there to answer the question, and the folder
   is a throwaway one. If Copilot CLI asks you to sign in, type `/login`,
   choose **GitHub.com**, then **Sign in with a device code**, and follow
   the code that Copilot CLI shows you. Type `/exit` to quit.
3. Open `ralph/PROMPT.md`. The loop sends this same short prompt every
   round, with the latest test results added to the end.
4. Run the loop:

   ```bash
   for round in 1 2 3; do
     python -m pytest -q > results.txt && break
     echo "Round $round: not every test passes yet, so the agent gets another go"
     copilot -p "$(cat PROMPT.md results.txt)" --allow-tool='write'
   done
   python -m pytest -q
   ```

   `--allow-tool='write'` lets the agent edit files without asking, so use
   it only in a throwaway folder like this one. Press `Ctrl+C` to stop the
   loop early.
5. Check the loop's work. The first command prints nothing if the loop
   left the tests alone, and the second gives the loop's version a column
   of its own:

   ```bash
   diff tests/test_todo.py ../tests/test_todo.py
   python ../compare.py
   ```

**What you should have**

A "Round" line for each round the loop needed (three at most), then the
final test run: all 9 passing, or the loop stopped at the cap with some
tests still failing. `diff` printing nothing, and `compare.py`'s table
with a fourth column, `ralph`.

<details><summary>Hint</summary>

Every `copilot -p` call starts a new conversation, so in each round the
agent knows only `PROMPT.md`, the files in the folder and `results.txt`.
That fresh start is the idea behind the loop: in one long conversation the
agent's context window (the most text the model can take in at once) fills
up, and the agent loses track of the goal. The test results carry what was
learned from one round to the next.

The first round's results say `No module named 'todo'`, because the folder
has no `todo.py` yet. The agent's first job is to create it.

The cap is the guardrail that matters here. Huntley's original loop,
`while :; do cat PROMPT.md | claude-code ; done`, never stops: it runs
until a person stops it, and every round costs money. With a cap of three,
the loop may stop before all 9 tests pass. That is the cap working, not
the loop failing.

In DIY 6 you answered each of the agent's questions, so you were in the
loop. Here the agent asks nothing and you only watch, ready to press
`Ctrl+C`, so you are on the loop. A software factory in which no person
watches at all would take the human out of the loop.

</details>

---

## Common mistakes

- **Judging a vibe-coded program by whether it runs.** Running is the
  minimum, not the evidence: `compare.py`'s exam is the evidence.
- **Skipping the plan review.** Without it, spec-driven development is
  vibe coding with extra documents.
- **Pasting the error instead of quoting the spec**, so the AI fixes the
  symptom and may change something else.
- **Taking the agent's word for it.** The agent's summary is a claim. The
  tests, `git status` and your own commands are the evidence.
- **Letting the agent change the tests**, or accepting code that only
  works for the tests' own inputs.
- **Running pytest from the top of the repository**, which runs every
  lab's tests.
- **Running an agent loop with no cap.** Every round uses a premium
  request, and Huntley's original loop never stops by itself.
- Concluding that vibe coding is always wrong. For a program you will
  throw away, vibe coding is the fastest way; the mistake is keeping
  vibe-coded code that nobody has read.

## Summary

- Vibe coding is fast, and the AI makes every decision your prompt leaves
  out. You find out which ones only when you read the code, and the time
  that takes is the comprehension debt.
- A spec says what "done" means. Checking the AI's plan against the spec,
  before any code exists, is the step that makes the difference.
- A coding agent works in a loop: edit, run the tests, read the failures,
  fix. The agent's context (the spec, `AGENTS.md` and the tests) steers the
  agent, and the tests decide when the job is done.
- Tests check only what someone wrote a test for: the 9 green tests never
  ran the command line.
- Check an agent's work yourself: run the tests, look at what changed, and
  look for code that only fits the tests.
- Choose the way of working for each job: vibe coding for a program you
  will throw away, a spec and tests for code you will keep.
