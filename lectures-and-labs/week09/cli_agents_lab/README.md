# AIAP CLI Coding Agents Lab

A coding agent in a terminal has your shell: it reads your files, runs
your commands and works across the whole repository. How it behaves is
decided less by what you type than by how it is configured — what it reads
every time it starts, the commands you give it, and what it may run
without asking. This lab is about that configuration. The tool is the
example; the configuration model is what transfers.

## What you'll learn

- Install a terminal coding agent, sign in, and find your way around a
  session with its built-in slash commands
- Write standing instructions (`AGENTS.md`) that change what the agent
  does in every future session — and check that they did
- Package a prompt you keep retyping as a slash command of your own
- Predict what a permission policy allows before an agent runs, and find
  the commands that slip through it
- Run an agent from a script, with every permission decided in advance

## Table of Contents

1. [Install and first session](#1-install-and-first-session)
2. [Standing instructions](#2-standing-instructions)
3. [Your own slash commands](#3-your-own-slash-commands)
4. [Allow, ask, deny](#4-allow-ask-deny)
5. [Running it with nobody watching](#5-running-it-with-nobody-watching)
6. [Extensions](#6-extensions)
7. [Common mistakes](#common-mistakes)
8. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab and install its dependencies:

   ```bash
   cd lectures-and-labs/week09/cli_agents_lab
   pip install -r requirements.txt
   ```

3. Check the tools you need are present:

   ```bash
   python check_setup.py
   ```

**Which agent.** The steps are written for **GitHub Copilot CLI**, which
comes with every Copilot plan — including Copilot Free and the free
Copilot Student plan you get through GitHub Education. The student plan
chooses the model for you and has a monthly allowance, shared with
Copilot Chat; `/usage` shows what the current session has used. If
Copilot is not available to you, use **Gemini CLI** with the free Gemini
API key from the RAG lab, kept in a `.env` file in `sample-app` (DIY 1
shows how): Google's own sign-in stopped serving free personal accounts
on 18 June 2026. Wherever the two differ, the Gemini version is given
too.

| Folder | What is in it |
|---|---|
| `sample-app/` | A small project with one failing test — the agent's work |
| `policy/` | A permission checker, a team policy, a list of commands, a scorer for your predictions, and DIY 7's probe |
| `examples/` | A custom command, a skill and an agent profile, ready to install |

If anything goes wrong installing or signing in, see
[TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## 1. Install and first session

A terminal agent is a program you install like any other. Copilot CLI and
Gemini CLI are both npm packages and need Node 22 or newer, which the
Codespace already has.

The first time it starts in a folder, it asks whether you trust that
folder. Take the question seriously: trusting a folder lets the agent read
it, and lets the files in it configure the agent.

### DIY 1: Install, sign in, look around

1. Install the agent and confirm it runs:

   ```bash
   npm install -g @github/copilot
   copilot --version
   ```

   Gemini: `npm install -g @google/gemini-cli`, then `gemini --version`.

2. Start it inside the sample project:

   ```bash
   cd sample-app
   copilot
   ```

   Trust the folder for this session only. If the screen already says
   `Signed in to https://github.com as <your username>`, you are signed
   in. If it says `Please use /login to sign in to use Copilot`, type
   `/login`, choose **GitHub.com**, then **Sign in with a device code**,
   and follow the code it shows you.

   Gemini: first create `sample-app/.env` with your key and the model
   line:

   ```text
   GEMINI_API_KEY=your-key-here
   GEMINI_MODEL=gemini-3.5-flash-lite
   ```

   Then run `gemini` and trust the folder. When it asks how to
   authenticate, choose **Use Gemini API Key**, then press Enter to
   submit the key it shows you. The bottom right of the screen should
   read `gemini-3.5-flash-lite`.
3. Before asking it anything, type `/help` and find the command for each
   of these jobs. Try each one once:

   - start a fresh conversation
   - show how full the context window is
   - shrink a long conversation
   - choose the model
   - come back to an earlier session

4. Ask: *"What does this project do? Don't change anything."* Then check
   how much of the context window that one question used.
5. Type `!python -m pytest -q`. The `!` runs the command **yourself**,
   without the model. One test fails — it is the job for the next
   section.

**What you should have**

The agent installed and signed in, each of the five commands found in
`/help`, not on this page, and tried once, the share of the context
window one question used, and one failing test on screen.

<details><summary>Hint</summary>

On the student plan, `/model` may offer only automatic selection. That is
expected, not a fault.

If Copilot says you have no access in a Codespace, the Codespace's own
`GITHUB_TOKEN` may be getting in the way — see
[TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Gemini: the key is the one from the RAG lab, the value of `LLM_API_KEY`
in `rag_lab/.env`, or a new one from
[aistudio.google.com/apikey](https://aistudio.google.com/apikey).
`.env` is gitignored, so git never sees it, and the undo in DIY 2
(`git clean -fd`) leaves it alone. Never type the key into a command or
paste it into code. Keep the `GEMINI_MODEL` line: without it Gemini uses
its default model, the bottom right reads `Auto`, and on a free key that
model gave no answer when this lab was checked in October 2026.

Step 5 matters more than it looks. `!` is your action. Asking the agent to
run the same command is *its* action, and goes through its permissions —
which is section 4.

</details>

---

## 2. Standing instructions

Anything you tell an agent in a conversation lasts as long as the
conversation. A rule that should still hold tomorrow belongs in a file the
agent reads every time it starts.

`AGENTS.md` is an open format for that file, read by most terminal agents.
Copilot CLI reads it, and `.github/copilot-instructions.md` too. Gemini
CLI reads `GEMINI.md` unless you tell it to read `AGENTS.md` as well.

### DIY 2: Watch it choose

`sample-app/test_stats.py` expects `median([4, 1, 3, 2]) == 2.5`. The code
returns `3`. There are two ways to make that test pass, and only one of
them is a fix.

1. Commit, so you can see exactly what changes and undo it:

   ```bash
   git add -A && git commit --allow-empty -m "before the agent"
   ```

2. Start a fresh conversation (`/clear`) and type only: *"Make the tests
   pass."*
3. When it finishes, run `git diff`. Which file did it change —
   `stats.py`, `test_stats.py`, or both?

   If the diff is longer than the terminal, git shows it in a scrolling
   viewer and your prompt disappears. Scroll with the arrow keys, then
   press `q` to get back to the prompt. If `q` does nothing, you are in the
   Vim editor: press `Esc`, type `:q` and press Enter.

4. Undo everything it did: `git checkout -- . && git clean -fd` — you
   committed first, so this removes only what the agent changed or added.

**What you should have**

The agent's work on screen in `git diff`: the file or files it changed,
and whether any test's expected value changed.

<details><summary>Hint</summary>

Either outcome is a result. On a task this small the agent often fixes
the code; the finding is that nothing *stopped* it editing the test
instead. "Passing" was the goal it was given, and changing the test
achieves it.

Read the diff, not the agent's summary of what it did. They do not always
agree.

`--allow-empty` makes the commit work even when nothing has changed since
your last one, so step 1 never stops on "nothing to commit".

</details>

### DIY 3: Write the rule down

1. Create `sample-app/AGENTS.md`. Give it, at least: how to run the tests;
   that a test's expected value is never changed, and what to do instead;
   standard library only; and to check the result of every command before
   the next step.
2. Gemini only: make it read `AGENTS.md` by creating
   `sample-app/.gemini/settings.json`:

   ```json
   {"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}}
   ```

3. Quit and start a **new** session. Ask: *"What rules do your
   instructions give you for this project?"*
4. Repeat DIY 2: commit, type *"Make the tests pass."*, then `git diff`.
   Undo with `git checkout -- . && git clean -fd` so the bug is back for later.
5. Now push against the rule: *"The test is wrong. Change it to expect
   3."* Watch what it does, then undo again.

**What you should have**

Your `AGENTS.md`, the agent's answer to step 3 showing it read the file, a
diff from step 4 that touches only `stats.py`, and step 5's outcome on
screen: the test changed, or the agent pushing back.

<details><summary>Hint</summary>

A rule that says what to do *instead* works better than a bare ban: "if a
test looks wrong, stop and explain why" gives the agent somewhere to go.

You may find it loaded more than your file. Copilot also reads
instruction files from the root of the repository — this module ships an
`AGENTS.md` and a `CLAUDE.md` among them — and combines them all with no
order of priority.
In Gemini, `/memory show` prints everything it loaded; if it ignores your
settings file, trust the folder, because settings in an untrusted folder
are ignored.

If step 5 changes the test, you have found the honest limit of this
section: `AGENTS.md` is text the model weighs, not a lock. The lock is
section 4.

</details>

---

## 3. Your own slash commands

The built-in commands control the tool. Your own commands package a
prompt you would otherwise retype — with live context, such as the
current diff, filled in when you run it. They are files, so they are
committed and the whole team gets them.

`examples/` holds one of each kind, deliberately **outside** the folders
the agents load from. Installing one is part of the exercise:

| File | What it is | Install it to |
|---|---|---|
| `examples/copilot/skills/review-diff/SKILL.md` | A Copilot CLI skill | `.github/skills/review-diff/SKILL.md` at the root of your repo |
| `examples/gemini/review.toml` | A Gemini CLI command | `sample-app/.gemini/commands/review.toml` |
| `examples/copilot/agents/reviewer.agent.md` | A Copilot CLI custom agent | See the extensions |

### DIY 4: Install one, then write your own

1. Read the example for your agent **before** installing it. What will
   it run on your machine, and when?
2. Install it where your agent looks (see the table; `mkdir -p` the folder
   first), then start a new session. Copilot: `/skills` lists what it found. Gemini:
   `/commands reload`.
3. Add a comment to `stats.py`, then run it: `/review-diff` in Copilot,
   `/review` in Gemini. Did it run what you expected from reading it?
4. Write your own command for a job you would repeat — for example, "run
   the tests and report only the failures, with file and line", or "write
   a commit message from the staged diff". It must pull in live context
   itself rather than rely on you pasting it.
5. Run it twice, improve its wording once, and commit it.

**What you should have**

The example installed and run once, doing what you expected from reading
it, and your own command committed: run twice, pulling in its own live
context each time.

<details><summary>Hint</summary>

Copilot skills: the folder name and the `name:` in the file's frontmatter
must match, lowercase with hyphens. A skill can also be picked up without
being called, when its `description` fits what you asked. If it does not
show up, the personal folder `~/.copilot/skills/` works from anywhere.

Gemini commands: `{{args}}` is whatever you type after the command's name,
and `!{...}` runs a shell command and pastes its output into the prompt —
after asking you first. That confirmation is the reason to read someone
else's command before you install it. The personal folder
`~/.gemini/commands/` works from anywhere.

</details>

---

## 4. Allow, ask, deny

Standing instructions ask. Permissions **enforce**. Every terminal agent
decides each action one of three ways:

| Answer | Meaning |
|---|---|
| **Allow** | Runs without asking |
| **Ask** | A person decides — the default for anything not allowed |
| **Deny** | Never runs, whatever an allow rule says |

In Copilot CLI you write them as flags:

```bash
copilot --allow-tool='shell(git:*)' --deny-tool='shell(git push)'
```

`shell(rm)` covers every `rm` command, `shell(git:*)` covers every `git`
command, and for `git` and `gh` you can name a subcommand, as `git push`
does here. Gemini CLI does the same job with `--allowed-tools` and policy
files, and matches a text prefix. The details differ between tools and
between versions — so before you trust a policy, test it.

`policy/policy_check.py` is a small checker for exactly that. Its rules
are written like Copilot's:

| Rule | Covers |
|---|---|
| `shell` | Every shell command |
| `shell(git)` | Every command that starts with the word `git` |
| `shell(git push)` | Every command that starts with `git push` — `git push --force` too |
| `read`, `write`, … | Other tools — never a shell command |

Copilot's `:*` means "and anything after it". The checker has no
wildcards, so `shell(git)` already means that, and a rule with `:*` in it
is refused.

A line containing `|`, `||`, `&&`, `;` or `&` is split into separate
commands, and each is judged: the line is **DENY** if any part is denied,
**ASK** if any part would be asked, and **ALLOW** only if every part is
allowed.

### DIY 5: Predict, then check

1. Open `policy/team-policy.json`. Read its `intent` first, then its
   rules.
2. **Before running anything**, predict. From the lab folder (`cd ..`
   first if your terminal is still inside `sample-app`), copy the
   commands in `policy/commands.txt` without their comments:

   ```bash
   grep -v -e '^#' -e '^$' policy/commands.txt > policy/my-predictions.txt
   ```

3. Open `policy/my-predictions.txt` and put ALLOW, ASK or DENY at the
   start of each line: what you think the policy decides.
4. Score your predictions. The script asks the checker about every
   command and puts an `x` beside each prediction it disagrees with:

   ```bash
   python policy/check_predictions.py policy/team-policy.json policy/my-predictions.txt
   ```

5. Find every command the checker **allows** that breaks the policy's
   intent. Those are the gaps.

**Expected output**

```text
  ALLOW  git status
  DENY   git push
x DENY   git push --force origin main    <- you said ALLOW
...

9 of 10 predictions right.
```

<details><summary>Hint</summary>

There are three gaps. A rule matches the words a command **starts with**,
so look for commands that break the intent while starting with words the
policy allows.

`read` is the agent's own file-reading tool. It says nothing about `cat`
in a shell.

</details>

### DIY 6: Close the gaps

1. Copy `policy/team-policy.json` to `policy/my-policy.json`.
2. Change its rules so that every gap from DIY 5 comes out ASK or DENY,
   while `git status`, `git diff`, `git log`, `git add`, `git commit`,
   `npm test`, `pytest` and `python -m pytest` all still come out ALLOW —
   with any arguments.
3. Write `policy/my-commands.txt` with five lines of your own: three the
   agent should be free to run, and two that break the intent in a way
   `commands.txt` did not show.
4. Run both files against `my-policy.json` until every verdict is one you
   would defend.
5. Now attack your own policy: add lines to `my-commands.txt` that break
   the intent and still come out ALLOW under `my-policy.json`.

**What you should have**

`my-policy.json`, `my-commands.txt` and the checker's output for both,
with every verdict one you would defend, and then, from step 5, at least
one line that breaks the intent and still comes out ALLOW. That line is
why adding deny rules never finishes the job.

<details><summary>Hint</summary>

Allowing a whole program (`shell(git)`, `shell(python)`) allows everything
that program can do. Allow the subcommands you mean instead, and let
everything else fall through to ASK.

For step 5, count the ways there are to spell "push" or "delete" — then
look up what `pytest --basetemp` does to the directory you give it: it
deletes it and makes it again, the first time a test asks pytest for a
temporary folder (`tmp_path`, for example). The sample app's tests never
ask, so with them nothing is deleted.

</details>

### DIY 7: Probe the real thing

The checker is a model of one way to match rules. Find out how your agent
actually does it — using harmless commands only.

1. From `sample-app` (`cd sample-app` from the lab folder), start the
   agent with one allow rule and one deny rule:

   ```bash
   copilot --allow-tool='shell(git status)' --deny-tool='shell(git log)'
   ```

   Gemini: `gemini --allowed-tools "run_shell_command(git status)"`, and
   for the deny, the policy file in the hint.
2. Ask it to run exactly `git status --short`. Did it ask you first?
3. Ask it to run exactly `git log --oneline -3`. Was it blocked?
4. Ask it to run exactly `git -C . log --oneline -3`. Was it blocked?
5. Quit the agent, go back to the lab folder (`cd ..`), and ask the
   checker about the same three commands under the same two rules:

   ```bash
   python policy/policy_check.py policy/probe-policy.json --file policy/probe-commands.txt
   ```

**What you should have**

For each of the three commands, what your agent did beside the verdict
the checker printed, and the line where they disagree, if there is one.

<details><summary>Hint</summary>

Say "run exactly this command". Otherwise the agent may tidy
`git -C . log` into `git log`, and you will be testing a different
command.

The Gemini deny rule: save this as `~/.gemini/policies/lab-probe.toml`,
restart, and **delete the file when you are done** — it applies to every
project on the machine.

```toml
[[rule]]
toolName = "run_shell_command"
commandPrefix = "git log"
decision = "deny"
priority = 500
```

Where the agent and the checker disagree, neither is broken. You now know
something about your agent that reading its flags did not tell you.

</details>

---

## 5. Running it with nobody watching

`-p` runs one prompt and exits, so an agent can live in a script or a CI
job. With nobody there to answer a question, anything not allowed in
advance is refused: every permission is decided before it starts.

### DIY 8: A script that explains a failure

1. From `sample-app`, run a headless check on the project:

   ```bash
   copilot -p "Run pytest -q. If any test fails, explain why in three lines." \
     --allow-tool='shell(pytest)' --deny-tool='write'
   ```

   The prompt names `pytest` on purpose: the policy allows commands that
   start with `pytest`, so `python -m pytest` would be *asked* — and
   headless, asked means refused.

   Gemini: pipe the output in, so it needs no tools — whether it *may*
   use any is decided by its own allow/deny configuration, not by the pipe:
   `python -m pytest -q 2>&1 | gemini -p "Explain any failing test in three lines."`
2. Save the command as `explain-failures.sh` in `sample-app` and run it
   there with `bash explain-failures.sh`.
3. Change the prompt so the job needs something you did not allow — add
   "then fix the bug" — and run it again. Watch what happens.
4. Confirm nothing changed: `git status`.
5. Take the allow rule away too: delete `--allow-tool='shell(pytest)'`
   from the script and run it once more. With nothing allowed, what can
   it still tell you? (Gemini: your piped version already runs with
   nothing allowed.)

**What you should have**

`explain-failures.sh` and its explanation of the failing test, the
refusal in step 3 with `git status` showing nothing changed, and the run
in step 5 showing what the agent can do when it may run nothing.

<details><summary>Hint</summary>

`--deny-tool='write'` blocks the agent's file-editing tools. A shell
command can still write files, which is why the script allows
`shell(pytest)` and not `shell`.

Piping the text in is the safest headless pattern there is: everything
the agent needs is already in the prompt, so it has no reason to reach for
a tool. But only a policy stops it if it tries — "runs nothing" is a
property of what you allowed, not of the pipe.

</details>

---

## 6. Extensions

Optional — the sections above are the two-hour path.

- **A read-only reviewer.** Copy `examples/copilot/agents/reviewer.agent.md`
  to `.github/agents/` at the root of your repo, start a session, and pick
  it with `/agent`. Its `tools` list leaves out editing and the shell
  entirely: narrowing an agent's tools is a permission decision, not a
  style choice.
- **MCP servers.** `/mcp` lists the servers your agent can use and adds
  new ones. Connect the server you built in the MCP lab and ask the agent
  to use it.
- **Delegate.** If your plan includes the Copilot cloud agent, `/delegate`
  in Copilot CLI hands it a task; it works on a branch and opens a pull
  request. When an agent works while you are not watching, what does
  review even mean?
- **A second agent.** Repeat DIY 2 and DIY 3 in the other CLI, and compare
  what each did without asking.

---

## Common mistakes

- **Configuring by chatting.** It feels like it works, because it does —
  until the next session.
- **Treating `AGENTS.md` as a lock.** It is text the model weighs.
  Permissions are the lock.
- **Allowing an interpreter** — `shell(python)` — and calling it "run my
  scripts". It allows everything Python can do.
- **Trusting a deny list to be complete.** There is always another way to
  spell "push", which is why the default for anything unlisted is ASK.
- **Forgetting that running the tests runs code.** An agent that may edit
  files and run the tests may run anything: it can put the code in a test
  first.
- **Installing someone else's command without reading it.** `!{...}` runs
  on your machine.
- **Believing the summary instead of reading the diff.**

## Summary

- A terminal agent is a loop with **your shell**. How it behaves is set
  mostly by its configuration, not by the prompt.
- Rules that must outlive a session go in **`AGENTS.md`** — and a standing
  instruction still only asks.
- **Custom commands** are saved prompts with live context. They are files,
  so they are shared and reviewed like code.
- **Deny beats allow; anything unlisted is asked.** A rule names how a
  command starts, not what it does — so allow narrowly, and test a policy
  before you trust it.
- **Headless** means every permission is decided in advance. The safest
  headless agent reads what you pipe in and is allowed to run nothing.

The through-line: configure an agent as if it will do exactly what you
allowed — because it will.
