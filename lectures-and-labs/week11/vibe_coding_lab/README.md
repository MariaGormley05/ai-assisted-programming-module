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

**Words this lab uses.**

- **Vibe coding**: building software by telling an AI what you want in
  plain language, running what it produces and asking for changes,
  without reading the code. Andrej Karpathy, an AI researcher, named it in
  February 2025.
- **Prompt-first builder**: a website that turns a prompt into a working
  app, writing, running and hosting the code for you.
- **Comprehension debt**: the later cost of understanding code that a
  machine wrote and nobody read.
- **Spec** (specification): a short document saying what a feature must
  do and must not do. **Spec-driven development** means writing the spec
  and checking the assistant's plan against it before any code is written.
- **Acceptance criterion**: a check you can actually run that says the
  feature works, for example *add "milk", refresh the page: "milk" is
  still there*.
- **Mode**, in this lab: a way of working (vibe coding, spec-first, or no
  assistant at all), not the **Ask** and **Agent** choices in Copilot's
  picker.

**Before the lab, if you can,** create a free account on each of three
prompt-first builders. Nothing needs installing: they all run in a browser.

- **Bolt.new** — [bolt.new](https://bolt.new)
- **Lovable** — [lovable.dev](https://lovable.dev)
- **v0** — [v0.app](https://v0.app), which signs you in with a Vercel
  account

Each free plan allows only a few builds or messages a day, and the limits
change often, so keep follow-up prompts few: after the first build, DIY 3
needs one more message in one builder. If a limit stops you, use Build
mode in [Google AI Studio](https://aistudio.google.com/apps) instead, which
needs a Google account. Free plans may use what you type to train their
models, so keep anything private out of your prompts.

**In the lab:**

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab's folder. Every file the lab asks you to create
   (`prompt.md`, `spec.md` and the `todo-spec` folder) goes here:

   ```bash
   cd lectures-and-labs/week11/vibe_coding_lab
   ```

DIY 2, DIY 4 and DIY 6 use the Copilot chat in your Codespace. Open the chat panel
with `Ctrl+Alt+I` (`Ctrl+Cmd+I` on a Mac) and choose **Copilot** as the
session under the chat input (it may say **Local** currently), as in the
setup lab. Every step that talks to the assistant then says what to pick
in the agent picker, the control that first says **Agent** (in some VS
Code versions the picker sits under **Add Context**): **Ask** reads
your files and answers, but cannot edit a file or run a command that
changes anything; **Agent** edits files straight away and runs commands.
Leave the mode and permissions controls on their defaults, **Interactive**
and **Manual permissions**, and **Agent** asks before it runs a command
(read-only ones such as `ls` excepted). **Autopilot** and **Allow all**
stop it asking; this lab never needs them. If your picker uses other
names, look for the read-only one and the one that asks first. *Fresh
conversation* means press the `+` at the top of the chat panel first.

> **Tool names change.** The three used here are examples of a *category*,
> not a prescription. If one has changed name, pricing or shut down, pick
> another prompt-first builder. The exercise is about the category.

---

## 1. Build it three times

One brief, three tools. The repetition is the point: it separates what is
true of the *approach* from what is true of one product.

**The brief.** A to-do application. Add a task, mark it done, delete it,
and the list survives a page refresh.

### DIY 1: The same app, three ways

1. Write your prompt **once**, before opening any tool, in `prompt.md` in
   this folder. Paste that same prompt into all three.
2. Build the app in tool one. How many follow-up prompts did it need
   before it met the brief?
3. Repeat in tool two.
4. Repeat in tool three.
5. Check each app against the brief: add two tasks, tick one, delete the
   other, refresh the page. Then try what the brief never said: an empty
   task, and the same task twice.

**What you should have**

Three working to-do apps built from one prompt, each checked against the
brief, and for each tool the first thing it got *wrong* — or, if it got
nothing wrong, the first thing it decided that your prompt did not say.

<details><summary>Hint</summary>

Using the same prompt for all three is what makes this a comparison rather
than three anecdotes. Resist improving the prompt between tools: once the
prompt changes, the comparison has gone.

"Survives a page refresh" is the requirement that separates a demo from an
app. Check it explicitly in all three. If one fails, that is your first
mistake. If all three pass, look at what each one chose without being
asked: what an empty task does, whether the same task can go in twice. The
brief says nothing about either, so every tool answered for you.

</details>

---

## 2. Read what you shipped

You now own three applications you did not write. This section is the
whole reason the lab exists.

### DIY 2: Find something you would not ship

Pick **one** of the three and spend about twenty minutes in its source.

1. Open its code view — the **Code** tab in Lovable, v0 and Google AI
   Studio, the `<>` icon in Bolt.new — and find the file that handles
   **user input** or **data storage**.
2. If you have time: find where it lists its dependencies (`package.json`,
   in most builders) and count them. Pick one you have never heard of and
   find out what it does.
3. Attack it from the app itself: add an empty task, a very long one
   (paste a paragraph ten times), and a task that reads
   `<img src=x onerror=alert(1)>`. Which does it accept? Does the last one
   show as text, or as a broken image?
4. Find **one line you genuinely cannot explain**, and decide what you
   think it does.
5. Fresh conversation, **Ask**, in the Copilot chat: paste the line and
   ask what it does. Did the explanation match what you had assumed?
6. Fresh conversation, **Ask**: paste the whole file and ask directly:

   > Review this code for security vulnerabilities as a security engineer
   > would.

   Does it name what your attacks in step 3 found?

**What you should have**

On screen: what the app accepted when you attacked it, the line you could
not explain beside Ask's explanation of it, and the security review, with
which of your step 3 results it named and which it missed.

<details><summary>Hint</summary>

In Veracode's 2025 test, the code AI models wrote had a common security
flaw in about 45% of tasks when the prompt never mentioned security
(Veracode sells security testing; a peer-reviewed 2022 New York University
study found a similar rate, 40%, in GitHub Copilot's programs). So you
have a good chance of finding one. Unvalidated input is the usual
suspect — look for anything that goes from a form straight into storage:
is there a limit on how long a task can be, or a check for an empty one?

Most builders generate React, which shows the `<img>` task as plain text:
that is the safe result. A broken image, perhaps with an alert box, means
the app put your text into the page as code (cross-site scripting). In
plain JavaScript, look for text that goes back onto the page through
`innerHTML`: that is where it happens.

Step 5 is the real exercise. The gap between what you *assumed* a line did
and what it *does* is comprehension debt, measured directly, on code you
created an hour ago.

Lovable shows its code read-only on the free plan. Reading is all this
step needs.

</details>

### DIY 3: Estimate the debt

1. Pick the app you understand least.
2. Give yourself five minutes and no assistant. Find every file you would
   have to change to **let a user edit an existing task's text**, and
   open them. Change nothing.
3. When the five minutes are up: did you find them all, and how sure are
   you?
4. Now let the tool do it: ask for the feature in one follow-up prompt.
   Look at what it changed. Were those the files you found? (If that
   tool's daily limit stops you, pick another of the three apps and do
   step 2 on that app first, so you compare like with like.)

**What you should have**

The files you found in five minutes, beside the tool's own change: the
files it touched that you missed, and any you found that it never needed.

<details><summary>Hint</summary>

To find the files, search the code for `localStorage` and for the text on
the delete button: editing a task touches the same places as deleting
one.

There is no correct answer, and the honest result is often that the tool
was faster — these tools genuinely save time. The exercise is to make the
trade *visible* rather than to conclude it is bad.

Asking the tool to add it is a legitimate strategy. Step 4 shows what it
depends on: that the tool still understands a codebase it wrote and you
did not read. The files you missed are the debt.

</details>

---

## 3. Build it once more, spec-first

Now the other side of the argument, so your opinion is based on having
done both.

### DIY 4: Write the spec before the prompt

1. Create `spec.md` in this lab's folder, **before touching any tool**,
   and write one page under these four headings:

   ```markdown
   # To-do app spec

   ## What the app does

   ## What the app does not do

   ## The data it stores, and its shape

   ## Acceptance criteria (three checks you can actually run)
   ```

2. Open `spec.md`. Fresh conversation, **Ask**, in the Copilot chat:

   > Here is spec.md. Give me a plan: which files you will create and what
   > each one does. Do not write code yet.

3. Read the plan against your spec. Wherever the plan differs from the
   spec, correct it in the same conversation.
4. Only now switch the agent picker to **Agent**, stay in the same
   conversation, and ask:

   > Build this plan in a new folder
   > lectures-and-labs/week11/vibe_coding_lab/todo-spec.

   Agent asks before it creates files and before each command. Read each
   request before you allow it.
5. Open the app: use the link Agent gives you, or the **Ports** tab. If
   the app is a plain `index.html`, first run
   `python3 -m http.server 8000` inside `todo-spec` and open port 8000.
   Then check the app against your three acceptance criteria.

**What you should have**

`spec.md`, the plan in the chat with your corrections under it, a working
app in `todo-spec`, and your three acceptance criteria checked against
it, one by one.

<details><summary>Hint</summary>

Step 3 is the step everyone skips, and skipping it turns spec-driven
development into vibe coding with extra documents. The plan is the
cheapest place to catch a misunderstanding — cheaper than the code and far
cheaper than the deployed app.

If your spec has no "does not do" section, it is not finished. Saying
what the app will not do stops the assistant adding features nobody asked
for, and that is most of the value.

</details>

### DIY 5: Compare, honestly

Put the spec-first app through exactly what the vibe-coded apps went
through.

1. DIY 1's check: add two tasks, tick one, delete the other, refresh the
   page. Then an empty task, and the same task twice.
2. DIY 2's attacks: a very long task, and `<img src=x onerror=alert(1)>`.
3. Put it beside the vibe-coded app you read in DIY 2. Find one
   difference in behaviour you can point at on screen, and the line in
   `spec.md` that caused it, if one did.

**What you should have**

Both apps through the same checks, and at least one difference you can
point at with the spec line behind it — or no difference at all, which on
a to-do app is a real finding.

<details><summary>Hint</summary>

Spec-driven being slower is not a criticism — it is the cost, and the
question is what the cost buys. If it bought nothing on a to-do app, that
is a real finding, and it is the argument *for* vibe coding on small
disposable work.

Look first at what your spec says the app does **not** do, and at the
shape of the data it stores: that is where writing it down usually
changes what gets built.

</details>

---

## 4. Choosing a mode

### DIY 6: Pick the mode, then do it

Three small jobs. For each, choose the mode first: **vibe it** (prompt,
check it runs, move on), **spec it first** (a line in `spec.md`, the plan
in **Ask**, then **Agent**), or **no assistant** at all. Decide all three
before you start; the answers are under the hint.

- **Job 1:** a page that shows today's date in big letters, for a
  screenshot you need in five minutes and will then delete.
- **Job 2:** a button in `todo-spec` that clears every done task.
  `todo-spec` is the app you are keeping.
- **Job 3:** the longest text a task in `todo-spec` may have.

1. Do job 1 the way you chose, take the screenshot, and delete the page.
2. Do job 2 the way you chose, and check that the button works.
3. Before job 3, see what the wrong mode does. Save everything you have
   in one commit, and check that the commit holds `spec.md` and
   `todo-spec`:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab"
   git add -A . && git commit -m "before the wrong mode"
   git log -1 --stat
   ```

   The last command must list `spec.md` and files in `todo-spec`. If it
   does not, stop and ask for help before going on.
4. Fresh conversation, **Agent**: *"Add a sensible length limit to tasks
   in todo-spec."* Find the number it chose, or notice that it asked you
   instead. Then put everything back:

   ```bash
   cd "$(git rev-parse --show-toplevel)/lectures-and-labs/week11/vibe_coding_lab"
   git status --short .
   git diff .
   git clean -nd .
   git restore . && git clean -fd .
   git status --short .
   ```

   `git status --short .` lists what changed in this folder only: `M` is
   a changed file and `??` a new one, which `git diff` does not show.
   `git clean -nd .` only lists the new files the next line will delete.
   The last command should print nothing.
5. Now job 3 your way: write the number into `spec.md` as a line and an
   acceptance criterion.

**What you should have**

Job 1's page gone, a working "clear done" button in `todo-spec` with its
line in `spec.md`, the number Agent chose (or its question) seen in the
diff and then undone, `git status --short .` printing nothing, and your
own number in `spec.md`.

<details><summary>Hint</summary>

Four questions decide the mode: how much is at stake, whether a mistake
can be undone, how long the code will live, and who will maintain it. A
job that is cheap on all four is a vibe job; one that will live and be
relied on is a spec job; and a decision only you can make belongs to no
assistant.

If the diff is longer than the terminal, press `q` to get back to the
prompt (`Esc`, `:q`, Enter if `q` does nothing).

</details>

<details><summary>Which mode each job deserved</summary>

1. **Vibe it**: nobody will maintain it, and one look tells you whether
   it is right.
2. **Spec it first**: you are keeping this app, so the change starts as a
   line and an acceptance criterion in `spec.md`, and a plan you check
   before any code.
3. **No assistant.** How long a task may be is a decision about your
   product, not code. Write the number into `spec.md` yourself; the build
   follows from it. Step 4 showed the alternative: the assistant picked a
   number for you, and nothing records why.

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
- Reading what you shipped usually finds something you would not ship.
- **Spec-driven** moves review from the implementation to the intent, and
  charges you real time for it.
- Choose **per task**: how much is at stake, whether a mistake can be
  undone, how long the code will live, and who will maintain it.
