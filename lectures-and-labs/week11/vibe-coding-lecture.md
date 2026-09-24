---
title: Vibe Coding and Spec-Driven Development
topic: vibe-coding
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<!-- Speaker notes: ~0:01. Title while they settle.

These two hours are an argument with two sides, not a demonstration of a
tool. Resist letting it become a tools tour: the tools will have changed
by next year and the argument will not. Part 1 makes the argument and the
decision; part 2 explains the mechanism behind each claim and has the
room measure one of them on its own laptops. -->

<!-- _class: lead -->

<span class="kicker">// two answers to the same question</span>

# Vibe Coding and Spec-Driven Development

---

<!-- Speaker notes: ~0:02. The hook is the original quote, with its date,
and the phrase "forget that the code even exists" is doing real work: it
is more radical than students expect. Note the date, February 2025, and
then note what the phrase became — a methodology he never proposed.

The misconception to head off: students arrive assuming the term was
coined as an insult. It was coined with affection, by someone describing
a mode he was enjoying, and the lecture's answer to him is "fine, right
up until you have to change it". -->

## Where the phrase came from

> "There's a new kind of coding I call **vibe coding**, where you fully
> give in to the vibes, embrace exponentials, and **forget that the code
> even exists**."

<span class="kicker">// Andrej Karpathy, February 2025</span>

* He was describing a mode he was enjoying

* Not proposing a methodology

---

<!-- Speaker notes: ~0:04. The idea of the two hours: both modes are
correct for different tasks, and the skill is telling which task you are
on before you start. State the tension rather than picking a side yet.

The misconception to head off early: students expect a lecture telling
them vibe coding is bad. It is not; it is excellent for the thing it is
good at. The skill is knowing which mode a task deserves, and that is a
judgement, not a rule. -->

## The one idea

<div class="callout">

Both modes are correct. For **different tasks**. The skill is telling
which task you are on — before you start, not afterwards.

</div>

* These two hours are an argument, not a verdict

---

<!-- Speaker notes: ~0:05. Agenda, naming both halves. Part 1 is the
argument: what each mode is for, what adoption did, the two terms, and a
decision table. Part 2 is the mechanism: what a spec changes about what
the model produces, why a plan-first loop is not prompt-run-repeat with
paperwork, and how comprehension debt accrues and gets measured. Brisk. -->

<!-- _class: dense -->

## The two hours

**Part 1 — the argument**

- What vibe coding is genuinely good at, and what happened when the industry adopted it
- Comprehension debt and haunted codebases
- The counter-trend: spec-driven development
- Choosing a mode, deliberately

**Part 2 — the mechanism**

- What a spec changes about what the model is optimising for
- Plan-then-implement against prompt-run-repeat
- One feature, built both ways
- Measuring comprehension debt on code you wrote an hour ago

---

<!-- Speaker notes: ~0:07. The case FOR, made properly, because the room
knows these tools work and stops listening to anyone who pretends
otherwise. The unifying property of all four: being wrong is cheap
because you will throw the artefact away. That property, not the tool,
is what the whole decision turns on later. -->

## What it is genuinely good at

- **Prototypes** — the point is to learn something, then delete it
- **Exploring an unfamiliar stack** — you do not know what to specify yet
- **Throwaway tooling** — a script you will run twice
- **Demos** — where "it works on stage" is the entire requirement

<div class="callout">

The pattern: being wrong is **cheap**, because the artefact is disposable.

</div>

---

<!-- Speaker notes: ~0:09. Case 1, and the setup for everything that
follows: one sentence produces a working application. The concept is
that the demo is real — these tools are genuinely good at this — and
that "it works" is nonetheless the ONLY thing you know about what you
now own.

The misconception to head off: students hear this as "the app is
secretly broken". It may be fine. The point is that you cannot tell, and
cannot yet say how you would tell. Hold onto the brief; the same app
comes back in part 2 with a feature added both ways. -->

## Case 1: a to-do app in one prompt

<p class="prompt">Build me a to-do app. I can add a task, mark it done, delete it, and the list survives a page refresh.</p>

* A working app, in minutes, from one sentence — and the tools **are** this good

* You now own a file layout you did not choose, dependencies you did not pick, and lines you have not read

<span class="kicker">// the brief is deliberately small — it comes back in part 2</span>

---

<!-- Speaker notes: ~0:11. What the one prompt actually left you with,
ranked by how much you know about it. The concept: running is the
minimum, not the evidence. The only layer you have checked is the top
one, and everything under it was decided by the model and read by
nobody.

This is the first sighting of the pattern part 2 explains: every decision
the prompt did not make still got made. Students characteristically
equate "I watched it work" with "I know what it does"; the stack is there
to separate those two. -->

## What you actually have

<div class="stack">
  <div class="layer top"><span>It runs — you added a task and refreshed</span><span class="rank">checked</span></div>
  <div class="layer"><span>The list is stored somewhere, in a shape the model chose</span><span class="rank">unread</span></div>
  <div class="layer"><span>Whatever the user types goes from the form into that storage — validated?</span><span class="rank">unread</span></div>
  <div class="layer untrusted"><span>What the code does with input it was never demoed on</span><span class="rank">unknown</span></div>
</div>

* Running is the **minimum**, not the evidence

* Every layer below the top was decided by the model and read by nobody

---

<!-- Speaker notes: ~0:13. From the one app to the population: what
happened when the industry adopted the mode. The finding is the
contradiction in the middle two rows — they do not trust it, and they
ship it anyway — and the bottom rows are what that contradiction costs.

Read as direction, never precision; the next slide says why out loud.
Students characteristically fixate on one number; the useful reading is
that every row points the same way. -->

## Then the industry adopted it

| | |
|---|---|
| US developers using AI coding tools daily | **92%** |
| …who say they trust the output | **29%** |
| …who always review before committing | **48%** |
| Major issues vs human-written code | **1.7×** |
| Samples with an OWASP Top-10 vulnerability | **~45%** |
| Sprint capacity on AI-traceable bugs, a quarter in | **a fifth to a third** |

<span class="kicker">// treat these as direction, not decimal points</span>

---

<!-- Speaker notes: ~0:16. The provenance caveat, said out loud: these
figures come from industry surveys of varying rigour that cite each
other. The direction is not in dispute; the second decimal place is
meaningless. Modelling that scepticism is part of the job, and it buys
credibility for everything else in the two hours. The same caveat applies
when a figure reappears in part 2. -->

## A word on those numbers

* Industry surveys, varying rigour, heavily recycled

* The **direction** is not in dispute. The precision is fiction

<div class="callout">

Being able to say "I believe the trend, not the decimal" is itself an
engineering skill.

</div>

---

<!-- Speaker notes: ~0:18. The two terms. Comprehension debt is the one
to dwell on: it is the technical-debt metaphor applied to understanding.
You borrowed against knowing how the thing works, and a haunted codebase
is what the bill looks like when it arrives — a working system the team
can no longer change with confidence.

Most people have inherited a haunted codebase from their own past self,
AI or no AI; the point is that AI accelerates the process rather than
inventing it. Part 2 explains how the debt accrues line by line and how
to measure it. -->

## Two words worth knowing

<div class="stack">
  <div class="layer top"><span><strong>Comprehension debt</strong> — the future cost of understanding code a machine wrote and nobody read</span><span class="rank">borrowed</span></div>
  <div class="layer untrusted"><span><strong>Haunted codebase</strong> — a working system the team no longer understands</span><span class="rank">the bill</span></div>
</div>

* Technical debt, but what you borrowed against is **understanding**

* AI did not invent this. It accelerated it

---

<!-- Speaker notes: ~0:21. PREDICT beat 1: when the cost of a vibe-coded
project actually lands. The room commits before the reveal.

The wrong answer to expect is "immediately — it does not work". The
faulty model is that AI-built projects fail visibly and early. They do
not: day one is euphoric, because the demo works. The cost lands when
you must CHANGE something you did not write, typically well into a
project, by which point the decisions are baked in. "If the tests pass"
is the other wrong answer, from the model that running is evidence. -->

## Predict: when does a vibe-coded project hurt?

* Immediately — it does not work
* Day one is fine; the pain starts when you must **change** it
* Only if you picked the wrong tool
* It does not, if the tests pass

---

<!-- Speaker notes: ~0:24. The reveal. Day one is euphoric, and that is
precisely what makes it dangerous: the feedback signal arrives long after
the decision that caused it, so nothing at decision time feels wrong.

The capacity figure lands here: within a quarter, teams report a fifth to a third
of sprint capacity going on bugs traceable to generated code. Direction,
not decimals. Part 2 gives the mechanism — every unstated decision is
made silently, and every later change inherits it. -->

## Day one is euphoric

* Which is exactly the problem: the **feedback arrives long after the
  decision**

* You cannot feel comprehension debt accruing. You can only feel it
  arriving

<div class="callout">

Within a **quarter**, teams report a fifth to a third of sprint capacity going on bugs
traceable to AI-generated code.

</div>

---

<!-- Speaker notes: ~0:26. The counter-trend, introduced as a response
rather than a competing fashion. The core move: the artefact you review
changes from the implementation to the intent. One page of spec is
genuinely easier to judge than 800 lines of generated code, and the plan
in step 02 is the model's reading of that page, which you check before
any code exists. Part 2 explains what that reading changes. -->

## The counter-trend: spec-driven development

<div class="flow">
  <div class="step"><span class="n">01</span>Write the spec</div>
  <div class="step"><span class="n">02</span>Agent produces a plan</div>
  <div class="step"><span class="n">03</span>You review the plan</div>
  <div class="step"><span class="n">04</span>Then it implements</div>
</div>

* The artefact you review becomes the **intent**, not the implementation

* One page of spec is easier to judge than 800 lines of generated code

---

<!-- Speaker notes: ~0:29. The two shapes side by side, mostly for the
contrast, with one honest thing about the spec-driven row: reviewing the
plan is the step people skip, and skipping it turns spec-driven into vibe
coding with extra paperwork. Students characteristically treat the plan
as the model restating their spec; it is the model's interpretation, and
interpretations drift — case 2 in part 2 shows one drifting. -->

## The two shapes

```text
Vibe coding:   intent -> code -> hope

Spec-driven:   intent -> spec -> plan -> tasks -> code -> check against spec
```

* Skip the plan review and spec-driven becomes vibe coding **with
  paperwork**

---

<!-- Speaker notes: ~0:31. The honest objection, and this slide is why
the lecture is an argument rather than a sermon. Practitioners genuinely
complain that spec-driven work produces piles of markdown to review
instead of code to review — ceremony that feels like rigour. That
criticism is fair and should be stated, not strawmanned. The cost is
real; the question the decision table answers is when the cost is worth
paying. -->

## The honest objection

> "I'd rather review code than all these markdown files."

* Ceremony that **feels** like rigour is not rigour

* A spec nobody reads is worse than no spec: it manufactures confidence

<div class="callout">

Spec-driven has a real cost. If the task does not justify it, the cost is
all you get.

</div>

---

<!-- Speaker notes: ~0:34. PREDICT beat 2: which mode a disposable
weekend prototype deserves. The room commits before the reveal.

The wrong answer to expect is "spec-driven, always — it's the responsible
one". The faulty model is that rigour is always the safe choice, so
students who have absorbed the warnings over-correct. For a prototype you
intend to delete, writing a specification first is pure waste: you do not
yet know what you want, and finding out is the point of building it. -->

## Predict: a weekend prototype you intend to delete

Which mode?

* Spec-driven — always the responsible choice
* Vibe coding — you do not know what you want yet
* Spec-driven, but a short spec
* Neither; write it by hand

---

<!-- Speaker notes: ~0:36. The reveal and the reframe: specification
requires knowledge you may not have yet. You cannot specify what you have
not understood, and sometimes building the thing IS the requirements
gathering. That is a legitimate engineering position, not laziness. The
failure is not vibe coding; it is vibe coding something you then keep. -->

## Vibe coding — and this is not the lazy answer

* You cannot specify what you have not yet understood

* Sometimes building the thing **is** the requirements gathering

<div class="callout">

The failure is not vibe coding. The failure is vibe coding something you
then **keep**.

</div>

---

<!-- Speaker notes: ~0:39. The decision table, the slide of the two
hours: four questions, and the mode falls out of the answers. The bottom
row is the sharpest — who maintains this? If the answer is "somebody, for
years", the spec is cheap by comparison.

The concept students miss: the rows are questions about the TASK, not
categories of task. The same piece of code changes mode when its answers
change, which the closing round of part 1 tests. -->

## Choosing, deliberately

| | Vibe coding | Spec-driven |
|---|---|---|
| Stakes | Prototype, demo, throwaway | Production, shared, long-lived |
| Requirements | Discovering them | Known well enough to write |
| Being wrong costs | Delete and retry | Somebody maintains it for years |
| You review | The running app | The spec, then the tests |

---

<!-- Speaker notes: ~0:42. PREDICT beat 3, and the one that lands closest
to home: a large piece of their own work, built over weeks. The room
commits before the reveal.

The wrong answer to expect is a single mode for the whole project, in
either direction. The faulty model is that mode is a property of the
project. It is a property of the task: explore by vibe coding to find out
what you are building, then specify the parts you are keeping. -->

## Predict: a large project, built over ten weeks

* Vibe coding — speed matters, deadlines are real
* Spec-driven throughout — the stakes are high
* Vibe the exploration, specify what you keep
* It does not matter as long as it works

---

<!-- Speaker notes: ~0:45. The reveal. Mode is chosen per task, not per
project, and switching deliberately is the mark of someone who
understands both. The practical instruction for any real project:
prototype freely, then before you commit to an architecture, write the
page. The callout is the test: anything you would have to explain in
person and cannot is something you should have specified. -->

## Both — and switching on purpose

* Explore by building. Then **write the page** before you commit to it

* Mode is chosen **per task**, not per project

<div class="callout">

If you have to defend it in person, anything you cannot explain is
something you should have specified.

</div>

---

<!-- Speaker notes: ~0:48. Closing round of part 1: the decision table
applied to tasks it never listed, the room calling a mode for each. The
concept is that the table is a set of questions, not a list of task
types, so the same task changes mode when its answers change.

Expect the chart and the addresses to be instant and unanimous. The
rename script is where the room splits, which is the point: run once on
your own files it is vibe coding; run monthly on a shared drive, being
wrong now costs somebody else, and the mode moves with that answer. The
last line makes the move explicit. About five minutes. -->

## Try the table on tasks it never listed

Call a mode for each:

- A script to rename two hundred files, once
- A chart for tomorrow's meeting
- The page that stores other people's addresses
- The function that works out what a customer is charged
- A prototype to find out whether an idea is even possible

* Now the rename script again — but it runs **every month, on a shared drive**

<div class="callout">

The table is a set of questions, not a list of task types. Change the
answers and the mode moves.

</div>

---

<!-- Speaker notes: ~0:55. Break. Part 1 established the two modes and
the decision between them; part 2 explains the mechanism behind the three
claims it leaned on — that a spec changes what the model produces, that a
plan-first loop is different in kind from prompt-run-repeat, and that
comprehension debt accrues line by line — and has the room measure the
first of those on its own laptops. Resume at about ~1:05. -->

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2: what a spec actually changes, why patching is not planning, and
how to measure what you did not read.

---

<!-- Speaker notes: ~1:05. Part 2 opens with the mechanism behind
everything in part 1. A model generating code is choosing the most
plausible continuation of whatever is in front of it. A one-line prompt
constrains almost nothing, so every decision it does not mention — the
storage shape, what "done" means, whether input is checked, what happens
to data that already exists — is resolved toward whatever is most typical
in the code the model learned from. That is why generated apps look so
alike, and why they look right: typical code looks right.

The misconception: students treat an unstated requirement as "left open
for later". It is not left open. It is decided at generation time,
silently, by the training data rather than by them, and every later
prompt inherits the decision. This is case 1's "a shape the model
chose", now with the reason. -->

## Every gap gets filled

<div class="flow">
  <div class="step"><span class="n">01</span>Your one-line prompt</div>
  <div class="step"><span class="n">02</span>Every decision it never mentions</div>
  <div class="step"><span class="n">03</span>Each filled with the most typical choice</div>
  <div class="step danger"><span class="n">04</span>Code that looks right — because typical looks right</div>
</div>

* The model produces the most plausible code **given what is in front of it**

* Every requirement you leave out is not left open. It is answered — by the training data, not by you

<div class="callout">

Underspecified is not unspecified. The decisions still get made — silently,
and not by you.

</div>

---

<!-- Speaker notes: ~1:07. PREDICT beat 4: what a one-page spec changes
about the code, compared with a one-line prompt. The room commits before
the reveal.

The wrong answer to expect is "the model tries harder, so the code is
better". The faulty model is that a spec is a quality instruction — a way
of telling the model to be careful — when it is a set of constraints: it
changes which continuation is most plausible, not how much effort goes
in. The tell for this model is a spec full of adjectives ("robust",
"clean", "secure") and no decisions. The second wrong answer, "nothing
changes", comes from the opposite faulty model: that the output is fixed
by the task, when it is fixed by the context. -->

## Predict: a one-page spec instead of a one-line prompt

What changes about the code?

* The model tries harder, so the code is better
* Nothing — the model mostly ignores long instructions
* The decisions you wrote down become yours; the rest are still the model's
* The style changes; the decisions do not

---

<!-- Speaker notes: ~1:09. The reveal: the model did not get smarter, the
gaps got smaller. A spec buys three things. Decisions you wrote down are
now made by you rather than by the training data. The output can now be
WRONG against something — without a spec, code cannot drift, because
there is nothing to drift from; it can only be disliked. And acceptance
criteria give a check that is not "does it run". The "does not do"
section is the part people skip and the part that bounds the work:
without it, the most typical continuation includes features nobody asked
for.

Honest limit: the rest of the decisions are still the model's. A spec
moves the ones that matter; it never covers everything, and trying to
cover everything makes it the paperwork the objection complained
about. -->

## The model did not get smarter. The gaps got smaller

<div class="stack">
  <div class="layer top"><span><strong>Spec</strong> — does, does not do, the data's shape, acceptance criteria</span><span class="rank">decided by you</span></div>
  <div class="layer"><span><strong>Plan</strong> — the model's reading of your spec, in prose</span><span class="rank">reviewable</span></div>
  <div class="layer untrusted"><span><strong>Code</strong> — the plausible continuation of both</span><span class="rank">check against the spec</span></div>
</div>

* A spec buys three things: decisions **you** made, something the output can be **wrong against**, and a check that is not "does it run"

* The **does not do** section bounds the work — leave it out and the typical continuation includes features nobody asked for

---

<!-- Speaker notes: ~1:11. TRY IT NOW, about seven minutes, on their own
laptops with whichever assistant they have; pair up if someone has none.
The activity makes the mechanism countable: a one-line feature request
hides a list of decisions, and asking for the list instead of the code
shows how long it is. Expect entries like the date's format, optional or
required, what happens to tasks saved before the feature, sorting,
display, what "overdue" means, and whether a date can be cleared — the
rows case 2 turns on.

The misconception this surfaces: students who think the request was
complete because it named the feature. Naming a feature is not
specifying it. The second bullet turns the list into the start of a
spec, which is what the lab asks them to write in full. Resume at about
~1:18. -->

## Try it now: count the gaps

Seven minutes, your own laptop, whichever assistant you have.

<p class="prompt">I want to add a due date to each task in a to-do app that stores its tasks in the browser. Before writing any code, list every decision you would have to make that I have not specified. Number them. Do not write code.</p>

- **Notice the length of the list.** Every entry would have been decided silently by "just add due dates"
- Pick the three you would have wanted to make yourself. Written as one line each, those are the start of a spec
- If it wrote code anyway, notice that too

---

<!-- Speaker notes: ~1:18. The loop most vibe coding actually runs, and
what accumulates in it. The concept: feedback in this loop is about
behaviour, after the code exists, and each correction is generated as a
patch on the previous output rather than a revisit of the decisions that
produced it. The structure is whatever attempt one happened to choose,
because nobody asked for it to change and every later prompt takes it as
given. In a single conversation the earlier attempts are still in front
of the model, so later output is shaped by the wrong turns as well as by
the intent. And you only test what you clicked.

Students characteristically picture this loop as convergence; the next
predict tests that. -->

## Prompt, run, repeat

<div class="flow">
  <div class="step"><span class="n">01</span>Prompt</div>
  <div class="step"><span class="n">02</span>Code appears</div>
  <div class="step"><span class="n">03</span>Run it, click around</div>
  <div class="step danger"><span class="n">04</span>"No — fix that." Back to 02</div>
</div>

* Every correction is a **patch on the previous guess** — the structure is whatever attempt one chose

* You correct **behaviour**, after the code exists — and only the behaviour you happened to click

* The conversation fills with wrong turns, and each new patch is generated on top of all of them

---

<!-- Speaker notes: ~1:20. PREDICT beat 5: what five rounds of "no, fix
that" do to the structure of the code. The room commits before the
reveal.

The wrong answer to expect is "it converged — each round improved the
whole". The faulty model is that iteration improves a codebase the way a
human refactoring does, revisiting earlier decisions as it goes. The
model revisits nothing it is not asked to revisit: each round produces
the smallest plausible change to the previous output that answers the
complaint, and everything else is inherited. "It refactored as it went"
is the same faulty model with more optimism. This is why part 1's pain
starts when you must change it: by round five the decisions are baked in
under five layers of patches. -->

## Predict: five rounds of "no, fix that" later

What has happened to the structure of the code?

* It converged — each round improved the whole
* It is still whatever attempt one chose, with five patches on top
* The model refactored it as it went
* There is no structure to speak of

---

<!-- Speaker notes: ~1:22. The reveal, and the loop that differs in kind.
The plan is an intermediate artefact in prose: the model's interpretation
of your spec, readable in a minute, and the first point at which a
misunderstanding is visible. A correction there costs a sentence; the
same misunderstanding in code costs a rewrite, and in a deployed app
costs whatever the app was holding. Once approved, the plan sits in front
of the model and constrains the implementation, so the structure was
chosen on purpose rather than by attempt one, and the tasks are small
enough to check one at a time against the spec.

The honest limit, from part 1: the plan review is the step people skip.
Skipped, this loop degenerates into prompt-run-repeat with a spec
attached. -->

## Plan first — what actually differs

| | Prompt, run, repeat | Plan, then implement |
|---|---|---|
| You correct | Behaviour, after the code exists | The model's **reading of your intent**, before any code |
| A correction costs | A patch on a patch | A sentence |
| What carries forward | Every wrong turn | The plan you approved |
| The structure is chosen by | Attempt one, by accident | The plan, on purpose |
| You know it is done when | It seems to work | It meets the criteria you wrote |

<span class="kicker">// the plan is the model's interpretation, made visible while a fix is still cheap</span>

---

<!-- Speaker notes: ~1:24. Case 2: the app from case 1 exists and works,
and one small feature — a due date on each task — is added by both
routes. The concept is that the feature, the starting app and the
assistant are held constant, so whatever differs is the route; and what
to watch is the decisions, not the code. The decisions are the ones the
room listed in the activity ten minutes ago. -->

## Case 2: one feature, two routes

The to-do app from case 1 exists and works. Add a **due date** to each task.

<div class="stack">
  <div class="layer"><span><strong>Route A</strong> — one prompt, then run it and see</span><span class="rank">vibe</span></div>
  <div class="layer top"><span><strong>Route B</strong> — half a page of spec, a plan, a review, then the code</span><span class="rank">spec-driven</span></div>
</div>

* Same feature, same starting app, same assistant — only the route differs

* Watch the **decisions**, not the code. You listed them ten minutes ago

---

<!-- Speaker notes: ~1:26. Route A is the mechanism from the start of
part 2 applied to a change: every unstated decision resolved toward the
typical, invisibly, and the demo passes because the demo starts with a
fresh task. The row that bites is the third. The tasks already in storage
have no due-date field, and whether they still load depends on a decision
nobody made; it will not show on the demo, and it will show on the first
refresh with real data. That is the cheapest concrete instance of part
1's "the feedback arrives long after the decision".

Honest caveat: the exact behaviour differs by tool and by run. What does
not differ is that every row was decided without the person who owns the
app. The misconception is that "it works" means the feature is done — the
faulty model being that a passing demo exercises the cases that matter,
when it exercises the case you tried. -->

## Route A: one prompt

<p class="prompt">Add a due date to each task.</p>

- It works: a fresh task takes a date and shows it. **Day one is euphoric**

| Decided somewhere in the code | By |
|---|---|
| Stored as what — text, a number, a date object? | the model |
| Optional, or required? | the model |
| What happens to tasks saved **before** the feature? | the model — or nobody |
| Does the list now sort by it? | the model |

---

<!-- Speaker notes: ~1:28. Route B starts with half a page, and the
concept is that a spec is made of decisions, not adjectives. Read the
four parts against what a spec buys: does and does not do bound the work;
the data line fixes the shape; the acceptance lines are a check that is
not the demo. The line about existing tasks is route A's trap closed in
one sentence — the decision nobody made, made.

The misconception: students write "the due-date feature should be robust
and user-friendly". That is a wish, and the model fills it with the
typical again. The test of a spec line is whether the model could have
got it wrong; if it could not, it is not a decision. -->

## Route B: half a page first

```markdown
Feature: due dates
Does: each task may carry a due date, shown beside the task.
Does not: reminders, notifications, time zones, recurring tasks.
Data: `due` is an optional text field on each task, as YYYY-MM-DD.
Tasks saved before this change have no `due` and must still load and
display unchanged.

Acceptance:
1. A task saved with a due date still shows it after a page refresh.
2. A task saved before this change still appears, with no date.
3. A task saved with no due date can be given one later.
```

* Every line is a decision the model would otherwise have made. The **does not** line is the one that stops the feature growing

---

<!-- Speaker notes: ~1:30. The plan, and where it drifted. The concept:
the plan is where the model's interpretation becomes visible and a
correction is cheapest. Two drifts, of the two common kinds. Step 2 is
destructive and contradicts acceptance criterion 2 — the exact failure
route A left to chance, now written down where it can be refused. Step 3
is scope growth: sorting nobody asked for. Both are caught by reading
four lines against half a page, and both cost one sentence to fix here.
Skipped, the same two lines become code, and the destructive one shows
up only after a refresh with real data.

The misconception: "the plan is just the model restating my spec, so why
read it". The plan is the model's reading, and readings drift — this is
part 1's "skip the plan review and it becomes vibe coding with
paperwork", shown happening. -->

## Route B: the plan — and the drift

<p class="prompt">Here is spec.md. Give me a plan: which files you will change and what each change does. Do not write code yet.</p>

<p class="reply">1. Add an optional due field when a task is created or edited.
2. Rewrite the storage format to the new shape; discard any saved entry that does not match it.
3. Show the date beside each task and sort overdue tasks to the top.
4. Check the three acceptance criteria.</p>

* Step 2 **deletes every existing task** — criterion 2 says they must survive

* Step 3 adds sorting nobody asked for. Both are one sentence to fix — **here**

---

<!-- Speaker notes: ~1:32. The honest comparison, taught as direction.
Route B costs real time, and the spec is most of it. On a disposable
to-do app that time may buy nothing — which is part 1's argument for
vibe coding on disposable work, and a real finding, not a failure. On
the app that holds other people's data it buys criterion 2, the one that
would otherwise have been discovered by the people whose tasks vanished.

Note "the rest still the model's": a spec is never complete; it moves the
decisions that matter. The misconception is the over-correction from
part 1 — that route B is always the right answer — and the last row is
the honest version of why it often is: what you can tell a reviewer. -->

<!-- _class: dense -->

## What each route produced

| | Route A | Route B |
|---|---|---|
| Time | Minutes | Longer — the spec is most of it |
| Decisions made by you | None | The ones in the spec; the rest still the model's |
| Tasks saved before the change | Whatever happened | Criterion 2 — checked |
| What you reviewed | The running app | Spec, then plan, then three criteria |
| What you can tell a reviewer | "It works" | Why each decision went the way it did |

<div class="callout">

Route B is slower. The question is what the slowness bought — on a to-do
app, maybe nothing; on the app that holds other people's data, criterion 2.

</div>

---

<!-- Speaker notes: ~1:34. Comprehension debt, line by line. The concept:
every line accepted without being read is a small loan, and the loans
compound, because a line's meaning depends on what it calls. The line you
did read saves the list; what it calls turns the list into text somehow,
with a library you did not choose, into a shape the model picked — and
your due-date change has to preserve that shape. So understanding half
the lines is not half the understanding: the read half rests on the
unread half.

It is invisible at acceptance time and visible only at change time,
which is the mechanism under part 1's "day one is euphoric" and "the pain
starts when you must change it". Students characteristically picture the
debt as additive; the next predict tests that. -->

## How the debt accrues

<div class="stack">
  <div class="layer top"><span>The line you read: it saves the list</span><span class="rank">read</span></div>
  <div class="layer"><span>…which calls a helper that turns the list into text — how?</span><span class="rank">unread</span></div>
  <div class="layer"><span>…with a library you did not choose, on defaults you do not know</span><span class="rank">unread</span></div>
  <div class="layer untrusted"><span>…into a shape the model picked, which your due-date change must now preserve</span><span class="rank">unknown</span></div>
</div>

* Each accepted-unread line is a small loan. They **compound**: the line you read means whatever the lines you did not read make it mean

* You cannot feel it accruing. You feel it when you must **change** something

---

<!-- Speaker notes: ~1:36. PREDICT beat 6: how much comprehension debt
you carry after accepting 300 generated lines and reading 150 of them.
The room commits before the reveal.

The wrong answer to expect is "150 lines". The faulty model is that the
debt is additive per line — that reading half the file gives half the
understanding — when a line's meaning depends on what it calls, so the
unread half contaminates the read half. "Nothing — it works" is the
older faulty model from part 1, that running is evidence of
understanding. "Whatever the tests do not cover" is closer than it looks
but still wrong: if the model wrote the tests as well, they check its
decisions, not your understanding. -->

## Predict: 300 generated lines accepted, 150 read

How much do you owe?

* 150 lines
* Nothing — it works
* More than 150: the lines you read depend on the lines you did not
* Whatever the tests do not cover

---

<!-- Speaker notes: ~1:38. The reveal, and three ways to measure the
debt on code written an hour ago. The explain test is the direct
measure: pick a line, write down what you think it does, ask, compare —
the gap between assumption and fact IS the debt, on one line. The change
estimate is the forward measure: name a feature and list the files you
would have to understand first, which is the bill before you pay it. The
review ratio is the rate: how much of what you accepted did you read.
The "fewer than half" line is the 48% figure from part 1, direction not
decimal.

The lab has them run the first two on an app they generated themselves;
do not pre-empt the result. The misconception: that understanding cannot
be measured. It can, as a gap, one line at a time — and none of the three
is a number to optimise; they make the trade visible. -->

## Measuring it: three instruments

| Instrument | How | What it measures |
|---|---|---|
| **The explain test** | Pick a line. Write what you think it does. Ask. Compare | The gap between assumption and fact |
| **The change estimate** | Name a feature. List the files you must understand first | The bill, before you pay it |
| **The review ratio** | Of what you accepted, how much did you read? | How fast you are borrowing |

<div class="callout">

Fewer than half of daily users say they always review before committing —
direction, not decimal. Whatever your own ratio is, it is the rate at
which the debt grows.

</div>

---

<!-- Speaker notes: ~1:41. Common mistakes, both directions: over-
correction is as real as under-correction, and the room contains both.
The first two are the pair — keeping what you vibed, and specifying what
you will delete. The last three are the ways a spec-driven process fails
while looking like it is working. -->

## Common mistakes: choosing a mode

* Vibe coding something you then **keep**

* Writing a specification for a prototype you will delete on Sunday

- Producing a spec nobody reads, and calling that rigour
- Judging a generated app by whether it runs
- Choosing a mode by habit rather than by task

---

<!-- Speaker notes: ~1:43. Common mistakes inside the mode, each the
failure of a part-2 mechanism. Adjectives instead of decisions leave the
gaps open, so the typical fills them. Skimming the plan removes the only
cheap place to catch drift. Patching a wrong structure is cheap per patch
and expensive in total. Counting read lines as understanding ignores that
they rest on unread ones. -->

## Common mistakes: running the mode

- A spec made of adjectives — "robust", "clean", "user-friendly" — instead of decisions
- Reading the plan as the model restating your spec, and skimming it
- Patching a wrong structure for the fifth time because each patch is cheap
- Counting the lines you read as understanding, when they rest on lines you did not
- Measuring the debt by whether the demo runs

---

<!-- Speaker notes: ~1:45. Summary and close. Return to Karpathy's quote:
he said "forget that the code even exists", and the lecture's answer is
that this is fine right up until you have to change it — and part 2 said
why: the decisions were made without you, the patches sit on attempt one,
and the debt compounds through lines nobody read. Leave the callout up
for questions. -->

<!-- _class: dense -->

## Summary

- Vibe coding is **excellent** where being wrong is cheap and the artefact
  is disposable
- Adoption outran governance: **1.7×** the major issues, **~45%** with an
  OWASP Top-10 issue — direction, not decimals
- **Comprehension debt** is borrowed understanding. It compounds through lines
  nobody read; the explain test, the change estimate and the review ratio measure it
- **Spec-driven** moves review from implementation to intent, at a real cost of
  its own. A spec makes the **gaps smaller**, not the model smarter: the decisions become yours
- **Plan first**: a misunderstanding costs a sentence, not a rewrite
- Choose **per task**: stakes, reversibility, lifespan, and who maintains it

<div class="callout">

"Forget that the code even exists" is fine — right up to the moment you have to change it.

</div>
