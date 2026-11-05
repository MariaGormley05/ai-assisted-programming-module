# Part 3: Agent (DIY 3 and DIY 4, step by step)

The walkthrough for **DIY 3** and **DIY 4** on the [lab page](../README.md),
with the same steps in the same order.

**Agent** decides the steps itself: which files to create or change, and
which commands to run. In the **Copilot** session, check that the agent
picker under the chat input says **Agent**, and leave the mode and
permissions controls on **Interactive** and **Manual permissions**: it
then asks before it runs a command (read-only ones such as `ls`
excepted). **Autopilot** and **Allow all** stop it asking; this lab never
needs them.

You are no longer reviewing a change. You are reviewing a **result**.

From the lab folder:

```bash
cd part3_agent_mode
```

## DIY 3: Give it a goal, not a plan

1. Commit what you have, so you can see exactly what the agent adds:

   ```bash
   git add -A && git commit -m "before the agent"
   ```

2. Decide what "done" means before you start: a command, and what it
   should print. For example:

   > Done when: python -m pytest -q passes, and python cli.py add "Buy
   > milk" followed by python cli.py list shows Buy milk, in a new
   > terminal too.

3. Fresh conversation, **Agent**. Give it the goal, with your own
   `Done when:` line at the end:

   > Goal: a small command-line to-do list in the part3_agent_mode
   > folder. I can add a task, list my tasks, mark one done and delete
   > one, and my tasks are still there the next time I run it. Include
   > tests. Put every file in part3_agent_mode.
   >
   > Done when: (your line from step 2)

   It says what you want, and how you will judge it, and leaves the how
   (classes, file names, where the tasks are saved) to the agent.
4. Let it work without interrupting. Allow what it asks to run, and watch
   the list of files it touches grow in the chat.
5. Check your `Done when:` line yourself, by hand. Then:

   ```bash
   python -m pytest -q
   git status --short
   ```

**Expected output**

Your `Done when:` line holds when you check it, and `pytest` ends with a
line such as `12 passed in 0.31s`, with no `failed`. `git status --short`
lists the files it created, each marked `??`, all inside
`part3_agent_mode/`. A line for any other file is a file it touched that
you never mentioned: open it. Then ask yourself: *did it do what you
meant, or what you said?*

## DIY 4: Raise the stakes, then review like a detective

1. Commit again:

   ```bash
   git add -A && git commit -m "before the big change"
   ```

2. Fresh conversation, **Agent**. A change that has to touch several
   files, and a line saying what must not change:

   > Add due dates to the to-do list: a task can have a due date, I can
   > list the tasks that are overdue and the tasks due today, and the
   > command line has an option for each. Do not edit or delete any
   > existing test; add new ones.
   >
   > Done when: python -m pytest -q passes.

3. Review in this order: which files, then the tests, then whether it
   works.

   ```bash
   git status --short
   git diff -- '*test*'
   python -m pytest -q
   ```

   If the diff is longer than the terminal, git shows it in a scrolling
   viewer and your prompt disappears. Scroll with the arrow keys, then
   press `q` to get back to the prompt. If `q` does nothing, you are in
   the Vim editor: press `Esc`, type `:q` and press Enter.

4. Decide. Keep it, or undo all of it. `git clean -nd .` only lists what
   the next line will delete:

   ```bash
   git restore .
   git clean -nd .
   git clean -fd .
   git status --short .
   ```

**Expected output**

`git status --short` shows `M` beside the files it changed (most of the
files from DIY 3, usually) and `??` beside any it created. The test diff
shows only `+` lines if it kept to your rule. A `-` line means it changed
an existing test although you told it not to: read which assertion moved,
and why moving it made the tests pass. After an undo, the last command
prints nothing.

## If you finish early

- **The hunt.** Give the DIY 3 goal again in a fresh conversation, but
  ask for every file in a new folder, `part3_agent_mode/second_try`.
  Compare the two folders side by side: same file names? Same way of
  saving the tasks? Same number of tests?
- **Ask for the plan first.** Fresh conversation, **Agent**, and start
  the goal with *"Before you change anything, tell me which files you
  would create, how you would store the tasks, and how you would know it
  worked. Then stop."* Did the plan match what it built the first time?
