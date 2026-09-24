---
title: Module Introduction
topic: introduction
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<!-- Speaker notes: ~0:01. Title slide while the room settles. This is a
two-act hour: the argument first, then the logistics they need today. Say
the argument out loud early — most of them assume
this module is "how to use Copilot", and it is not. -->

<!-- _class: lead -->

<span class="kicker">// AI-Assisted Programming</span>

# Module Introduction

---

<!-- Speaker notes: ~0:02. The hook. Ask for hands: "who used an AI tool
to write code in the last week?" Nearly every hand goes up. Then the
second question, and far fewer hands stay up.

Do NOT resolve it here — it is answered deliberately three slides later
("So — must you understand every line?"), after the industry data has
made the honest answer defensible. Resolving it now costs the payoff.

The misconception to expect: the room reads the second question as an
accusation and assumes the expected answer is "you should be able to".
The real answer is no, almost nobody can, and the interesting question is
what replaced it. Let them sit in the discomfort for three slides. -->

## Two questions

* Who used an AI tool to write code in the last week?

* Who could **explain every line** it gave you?

* <span class="kicker">// the gap between those two answers is this module</span>

---

<!-- Speaker notes: ~0:04. The thesis. The misconception to name out loud:
students expect a tools module ("learn Copilot, learn Cursor"). Tools
change every few months; the judgement does not. Say that the tool list in
week 12 will not match the tool list in week 1 — and that this is the
point, not a flaw. -->

## What this module is

* Not "how to use Copilot" — tools change every few months

* How to **direct** an AI assistant, and how to **judge** what comes back

* Prompting, retrieval, protocols, agents, deployment, review

* <span class="callout" style="display: block;"><strong>The uncomfortable part.</strong> You are accountable for code you did not write. The assistant is fast; your name is on the commit.</span>

---

<!-- Speaker notes: ~0:05. The load-bearing pair is rows two and three: 29%
trust the output and 48% always review it. Keep them separate: most
developers do not trust what it produces, and fewer than half always
review it before committing. The surveys do not say the same people do
both, so do not claim that a majority ships code it neither trusts nor
checked. The honest reading is that trust is low and review is partial —
not through carelessness, but because reviewing everything is no longer
possible at the rate it arrives. The rest of the table is association,
not proven consequence: in the studies quoted, AI-assisted code carried
1.7x the major issues and ~45% of samples a known vulnerability class;
nothing here shows what caused what.

The misconception is that professionals have solved this and there is a
correct process about to be taught. There is not. The faulty model is that
industry practice is settled and students are being inducted into it; in
fact this is an uncontrolled experiment in progress and these are early
results. A student who believes a solved process exists will look for the
rule instead of building the judgement.

Provenance matters as much as the figures: these are 2026 industry surveys
of varying rigour that recycle each other, so the direction is sound and
the precision is not. Deck weight: heavy, and it pays off the opening two
questions. Delivery: pause. -->

## Where this actually is, in 2026

| | |
|---|---|
| US developers using AI coding tools daily | **92%** |
| …who trust the code it produces | **29%** |
| …who always review it before committing | **48%** |
| Major issues vs human-written code | **1.7×** |
| AI samples with an OWASP Top-10 vulnerability | **~45%** |

<span class="kicker">// they don't trust it — and they ship it anyway</span>

---

<!-- Speaker notes: ~0:08. This resolves the opening question honestly,
and it is the intellectual spine of the hour. Do NOT let them leave with
"so reading code doesn't matter".

The misconception: students hear "nobody reads every line" as permission
to read none of it. The actual shift is that the UNIT of review moved —
from the line to the behaviour — and the guarantee moved from your eyes
to your tests. If you have no tests, you have not moved up a level; you
have just stopped checking.

Callback to the two questions at the start. -->

## So — must you understand every line?

* **No.** Almost nobody does, and pretending otherwise is dishonest

* But the review didn't disappear — it **moved**

* From *reading every line* → to *tests, types, and CI that must pass*

* From *"looks right"* → to *"prove it behaves right"*

* <span class="callout" style="display: block;"><strong>The trade only works if the verification is real.</strong> Skip the tests and you have not moved up a level — you have just stopped checking.</span>

---

<!-- Speaker notes: ~0:11. PREDICT beat, and the first legal question of
the year. The concept under test: a licence attaches to the code, not to
whoever typed it, so an assistant that reproduces licensed code verbatim
hands the obligations over with it.

The wrong answer to expect is the first: "it is yours — the tool wrote
it". The faulty model is that the assistant is an author who owns what it
produces and can give it away; it is a predictor that sometimes reproduces
its training data, and "a tool typed it" has not been established as a
defence anywhere. The second wrong answer, "nobody can tell", mistakes
"unlikely to be caught" for "allowed". Keep the legal claim modest: the
law around training data is unsettled; what is settled is that the licence
follows the code. Verbatim reproduction of long, well-known code is rare;
the scenario is chosen for the principle, not the frequency. -->

## Predict: whose code is it?

The assistant gives you a 40-line function. It is character-for-character
identical to one in a well-known open-source project, released under a
licence that requires anything built on it to be open-sourced too.

You paste it into your employer's closed-source product.

* It is yours — the tool wrote it, so no licence applies
* The licence may apply — it follows the code, not the typist
* Nobody can tell, so it does not matter

---

<!-- Speaker notes: ~0:13. The reveal, kept honest. Copyright and licence
obligations attach to code; a tool reproducing it does not strip them,
and the disputes over the training data itself are still being argued in
court, so nothing here should be taught as settled beyond that one
principle. Two practical consequences are the point of the slide. Most
assistants offer a setting that blocks suggestions matching public code,
and students should know whether theirs is on. And the habit that outlasts
any ruling: generated code is code of unknown origin, which you can stand
over once you have read and tested it, or cannot ship. That is the
accountability callout from "What this module is", arriving from the
legal side: the name on the commit is yours either way. -->

## The licence follows the code

* A licence attaches to the **code**, not to whoever typed it. "The tool
  wrote it" is not a defence anyone has established

* Word-for-word copies of well-known code are rare, but real. Most
  assistants can **block suggestions that match public code** — find out
  whether yours does

* The law on training data is still being argued in court. Do not build
  your habits on how it comes out

* <span class="callout" style="display: block;">Treat generated code as code of <strong>unknown origin</strong>: you can stand over it once you have read and tested it — or you cannot ship it.</span>

---

<!-- Speaker notes: ~0:15. Confidentiality, taught before the first tool
is installed, because the habit has to exist before the first paste. The
concept: a hosted assistant is a service, so everything typed into it
leaves the machine; where it goes next depends on the plan and a setting,
not on the tool's name. Consumer plans commonly keep conversations and may
use them for training unless told not to; business plans commonly promise
not to. Read the setting. The three things that must never go into a
prompt — credentials, other people's personal data, code you have no
right to share — are absolute whatever the plan says.

The misconception: "it is just a chat window", meaning a paste is private
the way a local text editor is. It is closer to emailing the text to a
company. Connection to the labs: nothing in this module ever needs a real
secret or anyone's personal data in a prompt, and the one lab that uses an
API key keeps it in an ignored file, never in the conversation. A local
model keeps everything on the machine at a cost in capability — name it as
the trade, not the recommendation. -->

## Where what you paste goes

<div class="flow">
  <div class="step"><span class="n">01</span>Your prompt, with any code or file you attach</div>
  <div class="step"><span class="n">02</span>The provider's servers — <strong>always</strong>, for a hosted model</div>
  <div class="step"><span class="n">03</span>Kept, and maybe trained on — <strong>depends on plan and settings</strong></div>
</div>

* It is not a text editor. It is closer to **emailing the text to a
  company** — read the data setting on the plan you use

* Never in a prompt: **credentials**, other people's **personal data**,
  code you have **no right to share**. Whatever the plan says

* Employer code goes only into the tool the employer licensed. A local
  model keeps everything on your machine — at a cost in capability

* <span class="kicker">// nothing in this module ever needs a secret in a prompt</span>

---

<!-- Speaker notes: ~0:17. Vocabulary slide. These are current terms
students will meet online and in interviews this year, and knowing them
is genuinely useful social capital — say that.

"Comprehension debt" is the one worth dwelling on: it is the technical-debt
argument applied to understanding rather than to code, and it reframes
speed as borrowing. Ask the room who has already inherited a haunted
codebase from their own past self. Most hands go up, AI or no AI. -->

## The words you'll hear this year

* **Vibe coding** <span class="kicker" data-marpit-fragment="2">— prompt it, run it, ship it, barely read it</span>
* **Comprehension debt** <span class="kicker" data-marpit-fragment="4">— the future cost of understanding code a machine wrote and nobody read</span>
* **Haunted codebase** <span class="kicker" data-marpit-fragment="6">— a working system the team no longer understands</span>
* **Context engineering** <span class="kicker" data-marpit-fragment="8">— the shift from *how you ask* to *what you put in front of the model*</span>
* **Spec-driven development** <span class="kicker" data-marpit-fragment="10">— the backlash: write the spec, let the agent implement it</span>

* <span class="kicker">// half of these did not exist two years ago</span>

---

<!-- Speaker notes: ~0:20. Agenda. Reference slide, immediate bullets, take
it at pace. The argument is done; this is the logistics that remain. -->

## Module Delivery

- Act 1 — how the module runs: schedule, assessment, effort
- Act 2 — the tools you need set up before next week

---

<!-- Speaker notes: ~0:21. Schedule. The number that matters is 12 weeks,
not 13 — this changed from previous years. Reading week is the October
bank-holiday week and sits between weeks 6 and 7, right before MCQ 1. Say
explicitly that reading week is for revision, not a holiday: MCQ 1 is
the week straight after it. -->

## Duration and contact time

- **12 teaching weeks**, plus a reading week
- Reading week is the October bank-holiday week — it sits between week 6
  and MCQ 1
- Each week: **2 hour lecture + 2 hour lab**
- **No lab in week 1** — labs start next week
- The class is split into groups for labs; check your timetable

<span class="kicker">// your lab group and room are on your timetable</span>

---

<!-- Speaker notes: ~0:24. Enrolment. Do this live — walk the room while
they enrol, it is faster than answering it by email for two weeks. The
group passwords are given out HERE, verbally, and are deliberately not in
this deck or the repo: the deck is published on a public website. -->

## Enrol on the VLE

1. Go to your college's **VLE** — the link is on your timetable
2. Search for **AI-Assisted Programming**
3. Find out which lab group you are in (A, B, C or D)
4. Click **Enrol** and use your group's enrolment password

<div class="callout">

**Passwords are given out in this lecture**, not published. If you miss
them, email me — this deck is on a public site.

</div>

---

<!-- Speaker notes: ~0:27. Learning outcomes. Reference slide, read fast,
it is a validation requirement more than a teaching moment. Outcome 3 is
the one that actually drives the assessment design — flag it. -->

## Module learning outcomes

- **Identify and evaluate** AI-powered coding tools — generation,
  completion, debugging
- **Integrate** them into a real development workflow
- **Critically analyse** their limits: code quality, over-reliance, bias
- **Explore** emerging trends in the field

---

<!-- Speaker notes: ~0:30. Assessment. THE slide of the hour — expect
photographs, pause here. The shape changed this year: there is no project.
Two in-person MCQs at 32% each, and nine small practical assessments at 4%
each, one per lab. The misconception to head off: "4% is nothing, I'll skip
the odd one". Nine of them are 36% of the module, and a skipped one counts
as zero — it is not dropped from the total. -->

## Assessment

| Component | Weight | When |
|---|---|---|
| MCQ 1 | **32%** | Week 7, in the lab |
| MCQ 2 | **32%** | Week 12, in the lab |
| Practical Assessments | **9 × 4%** | One per week, open all that week |

<div class="callout">

**Nine small continuous assessments are 36% of the module.** A missed one counts as
zero, and each closes at the end of its week.

</div>

---

<!-- Speaker notes: ~0:34. How the MCQs work. Point out they are drawn
from lectures AND labs — students consistently revise only the slides and
are surprised by lab questions. The NotebookLM tip is genuinely good; also
point at the practice app on the module site, which is built from this
module's own material. -->

## The two MCQs

* Multiple choice, sat **in person** in the lab slot

* Drawn from the lectures **and the labs** of previous weeks

* MCQ 1 covers weeks 1–6 · MCQ 2 covers weeks 8–11

* **To practise:** use the practice app on the module site, or upload the
week's material to a tool like NotebookLM and ask it to generate questions.

---

<!-- Speaker notes: ~0:37. The practical assessments. One short online
question per lab on the VLE, open Monday to Sunday of that lab's week, one attempt,
submitted automatically when the week closes. AI tools are allowed, as in
the labs. The misconception to head off: "if AI is allowed, I can paste the
question in". Each question is built so the question alone is not enough —
it asks about the lab code in front of them, what it actually does when
run, or what is true right now. Doing the lab is the preparation. -->

## The Practical Assessments (PAs)

* **One per week**, on the VLE, worth **4%** each
* Open **all week** — do it when it suits you
* You **may** use AI tools

* <span class="kicker">// the first one opens week 2</span>

---

<!-- Speaker notes: ~0:43. Act 2 begins — tools. This is the slide they
need to act on before next week's lab, so be concrete. The Student
Developer Pack is free and takes ten minutes; without it they hit paywalls
in week 4 onward. -->

## Tools you need

| Tool | What for |
|---|---|
| **GitHub** | Where your work lives |
| **Codespaces** | A full dev environment in the browser |
| **GitHub Copilot** | AI assistance inside the editor |
| **CLI coding agents** | Covered in week 9 |

<span class="kicker">// nothing to install — Codespaces runs in a browser</span>

---

<!-- Speaker notes: ~0:46. The to-do. Make them write these two down. The
username one sounds trivial and is not: they will be sending me repo links
all semester, and "xX_dark_slayer_Xx" makes marking genuinely harder. Also
it is the account they will show an employer. -->

## Before next week

* Sign up for the **GitHub Student Developer Pack** — it is free and
  unlocks Copilot

* Change your GitHub username to **your actual name**

* <span class="callout" style="display: block;">Your GitHub account is the one an employer will look at. Start it as you mean to continue.</span>

---

<!-- Speaker notes: ~0:49. Where everything lives. Show the site live —
open it, click into a lab, show it works on a phone. Emphasise that the
site is canonical: if a lab is corrected mid-semester, the site has the
correction and their copy may not. -->

## Where everything lives

- **The module site** — every lecture, every lab and the MCQ practice, in a browser
<div style="text-align: center; font-size: 1.5em;">
  <a href="https://danielcregg.is-a.dev/ai-assisted-programming">https://danielcregg.is-a.dev/ai-assisted-programming</a>
</div>
<br>

- **Your own copy** — click below to create a private copy of the module repository for your lab work


<div style="text-align: center; font-size: 1.5em;">
  <a href="https://github.com/danielcregg/ai-assisted-programming">https://github.com/new?template_owner=danielcregg&amp;template_name=ai-assisted-programming&amp;visibility=private&amp;name=ai-assisted-programming-module</a>
</div>
<br>

---

<!-- Speaker notes: ~0:52. Summary and close. Return to the two questions
from the start — that symmetry is the point of the hour. Then: next week
is the overview lecture and the first lab, which is environment setup.
Leave time for questions. -->

## Summary

- **12 weeks**, 2 hour lecture + 2 hour lab, no lab this week
- **32% + 32% + 9 × 4%** — two MCQs and nine practical assessments
- The first practical assessment opens **next week**, with the first lab
- Set up GitHub and the Student Developer Pack **before** next week

**The one idea to keep:** you don't have to read every line — but
something has to check it, and if that something isn't a test, it's you.

**Next week:** what AI-assisted programming actually is — and the first lab.
