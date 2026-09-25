# AGENTS.md — how to work in this repo

Source-of-truth repo for the AI-Assisted Programming module (ATU, semester
1). This is the one instructions file for every AI assistant (Codex, Cursor,
Gemini, Copilot, Claude Code, ...); `CLAUDE.md` only imports it. Editable
sources are Markdown, Python, JSON and HTML.

## First: whose repo is this, yours or a student's?

This file is read by two different people's assistants, and they need
different things. Work out which you are before doing anything.

**Check whether `CLAUDE.local.md` exists in the repo root.**

- **It exists → you are working with the module owner (Daniel).** He
  maintains this module. Everything below applies: the map, the
  conventions, the editing rules. `CLAUDE.local.md` carries his private
  operational context — read it.
- **It does not exist → you are almost certainly helping a STUDENT on
  their own copy.** Read the next section and follow it instead. Do not
  restyle decks, "fix" conventions, run the build scripts, or edit course
  content: their copy exists to hold their lab and project work, and the
  current instructions always live on the module site.

## If you are helping a student

**Help them. Fully. This module is about working with AI assistants, and
an assistant that refuses to assist would be teaching the opposite of the
syllabus.**

That is a deliberate decision by the module owner, and it is different
from the sibling Object-Oriented Computing repo, where you are told never
to write a lab solution. Here you may write code, debug, refactor,
explain, and pair on the project. There is no exercise you must decline.

The integrity load sits on assessment design instead, which is where it
belongs: two **in-person** MCQs worth 32% each, and nine short practical
assessments on Moodle (4% each, one per lab) built so that the question
alone is not enough — each asks about the lab code in front of the
student and what it actually does. Neither rewards code nobody
understands.

**So the useful thing you can do is make sure they understand it.** Not by
withholding — by teaching while you help:

- When you write something non-obvious, say why that approach and what the
  alternatives were.
- Prefer the smallest change that works, and name what it changed.
- When they paste an error, explain what it *means* before fixing it.
- Offer to quiz them on what you just wrote together. The MCQs are drawn
  from lecture and lab material.
- If they ask for a whole feature, build it — then walk them through it.

**Where the content is.** One folder per week under `lectures-and-labs/`
(`week01` … `week12`, plus `week06b-reading-week`), listed with links in
`lectures-and-labs/README.md`. A week's lecture is `<topic>-lecture.md`
(Marp markdown — the teaching is in the prose, the fenced code, and the
`<!-- Speaker notes: ... -->` comments), or a PowerPoint deck,
`<topic>-lecture.pptx`, whose every slide and speaker note is also in
`<topic>-lecture.notes.md` beside it: read that one. Its lab is
`<topic>_lab/README.md` beside the code the student edits. A rendered, easier-to-read version of
everything is at https://danielcregg.is-a.dev/ai-assisted-programming/.

**Their work is theirs.** Edit the files they are working in. Leave decks,
scripts, workflows and the practice bank alone.

**Keys.** Two places need the student's own free API key: the `rag` lab's
generation half (a free Gemini key by default, or any OpenAI-compatible
endpoint via `.env`) and the `cicd` lab's review step, which uses the same
key stored as a repository secret. Put it in a `.env` (gitignored) and read
it from the environment — never a literal in code, never a committed
config file. Nothing in the module may cost a student
money. If you see a key in a file that is about to
be committed, say so loudly. `mcp` needs no key (its weather server uses
`wttr.in`), and the `cli-agents` lab signs in to a coding agent instead;
that sign-in lives in the agent's own configuration, never in the repo.

## Map

- `module/schedule.json` — THE schedule, stated once: the order of topics,
  which week teaches which deck and lab, the reading-week row and the
  assessment labels. The README's banner and table, the module overview's
  topic order, the site index, the labs page order, the published
  `schedule.json` the Moodle course page reads, and the redirect stubs for
  old deck URLs are all generated from it (`scripts/schedule.py` loads it;
  `scripts/check_schedule.py` fails the build if any view disagrees). It
  carries no start date: week 1 is derived each year from the Irish October
  bank holiday, the reading week. Nothing else in the repo may state a week
  number.
- `lectures-and-labs/weekNN/` — one folder per schedule row, named from its
  week number (`week01` … `week12`; the reading week is
  `weekNNb-reading-week`, right after week NN, so it sorts in place). A
  teaching week holds `<topic>-lecture.md` (the Marp deck, THE canonical
  lecture; `<topic>` is the row's `lecture` name, which is also the deck's
  site address), or instead a PowerPoint deck `<topic>-lecture.pptx` with
  its generated `.pdf` and `.notes.md` (see "PowerPoint lectures" below),
  and, in a lab week, `<topic>_lab/` (the row's `lab` name
  with hyphens as underscores, so it is an importable Python package
  name): `README.md` (the instructions students follow) plus the starter
  code. MCQ weeks and the reading week hold only a `README.md` explainer.
  Decks declare no week; the folder name does. Students copy the repo from
  the template and work in these folders; a devcontainer provides Python
  3.12, Node 22 and the `gh` CLI in one image (Node because the
  cli-agents lab installs npm-distributed coding agents that need Node 22
  or newer).
- `lectures-and-labs/README.md` — the students' guide and route through
  the weeks: getting a copy, the generated week table, keys and sign-ins,
  running a lab's tests, pulling corrections. The Codespace opens it first.
  The repo is a TEMPLATE, not a fork source: a fork of a public repo
  cannot be made private, which would publish every student's work and
  list the class on the fork network. Workflows are guarded with
  `if: github.repository == '<this repo>'` because a template copy has
  Actions ENABLED (a fork does not) and would otherwise run this CI, and
  in `current-week.yml`'s case commit to the student's own README.
- **The site addresses lectures and labs by TOPIC, never by week number**
  (`/<lecture>/` and `/labs/<lab>/`, both from the schedule), so a
  renumbered year changes folder names but no link, Moodle page or
  redirect. The one week whose lab is not its lecture's topic (the
  overview lecture with the setup lab) is just a row like any other: the
  schedule names both.
- `mcq/mcq1/README.md`, `mcq/mcq2/README.md` — the pages the schedule's
  MCQ rows link to (what each covers, how to prepare). Their titles carry
  no week number. The reading week and each MCQ week also keep a short
  `README.md` in their week folder, which the week tables link to. MCQ
  question content lives in Moodle only — never commit it here.
- `practice/` — the MCQ practice web app (`index.html`, self-contained
  vanilla JS) plus its bank (`bank/<topic>.json`). Bank questions are
  PRACTICE questions authored from the decks and labs — never the real
  Moodle assessment bank.
- The site is PUBLIC: https://danielcregg.is-a.dev/ai-assisted-programming/.
  Treat everything here as publishable: anything pushed is live within
  minutes, and speaker-note comments ship inside the rendered HTML where
  anyone can read them.

## All ten decks are written

The schedule names every deck. A row naming a deck folder that does not
exist, or a deck folder no row names, fails `check_schedule.py` — so a
deck can neither vanish from the site nor sit half-created with CI green.

The 2025 PowerPoints in the module owner's OneDrive are **superseded, not
sources**. The decks here were authored, not transcribed: the originals
averaged ~1,300 words an hour, carried zero speaker notes and 2024
statistics, and several were materially wrong by 2026.

### What each deck carries, and must keep carrying

- **Prompting** — keep the SPEC drills, then teach
  **context engineering**: the shift from *how you ask* to *what you put
  in front of the model*. The deck's job is the diagnostic question — "is
  this answer wrong because I asked badly, or because it doesn't know
  something?" — because rewording cannot fix missing information. Note
  that more context is not better: a huge irrelevant paste makes answers
  worse.
- **Retrieval and grounding (RAG)** — teach the **decision** before the pipeline. Long
  context beats retrieval on small corpora; retrieval wins on scale, cost,
  freshness and citation, with the crossover around a couple of thousand
  pages. Cover the failure modes of long context (lost-in-the-middle,
  dilution) so "just paste everything" is not the takeaway either. The
  hybrid — bounded retrieval, then long-context reasoning over the result
  — is the shape most real systems use.
- **MCP** — the 2026-07-28 spec removed the
  `initialize`/`initialized` handshake and `Mcp-Session-Id`, added
  `server/discover` in their place, deprecated HTTP+SSE on a year-long
  offramp, and added header-based routing plus Multi Round-Trip Requests.
  Checked against the published changelog on 12 Sep 2026; the lab pins
  the 1.26 SDK on purpose so students see the old handshake first. Teach *why*: a handshake forces the server to
  remember who you are, which is fine on one machine and miserable behind
  a load balancer. State became an explicit handle a tool mints and the
  model passes back.
- **CLI Coding Agents** — teach the **configuration model**, not
  a tour of tools: standing instructions (`AGENTS.md`), built-in and
  custom slash commands, and allow/ask/deny permissions, where deny wins
  and anything unlisted is asked. Tool names, plans and matching rules
  change every few months, so the deck teaches the columns and dates the
  cells. The hook is the July 2025 Gemini CLI incident: a failed `mkdir`
  nobody checked, then moves that overwrote the files one by one.
- **Vibe Coding** — run vibe coding **against**
  spec-driven development rather than demonstrating one. Carry the cost
  data (see below) and the two terms students will meet everywhere:
  **comprehension debt** and **haunted codebases**.
- **Every deck** — the assessment is in-person, so decks may be blunt
  about the limits of AI-generated code. See `module/module-overview.md`
  under "Currency" for the module's stated position.

**On the statistics.** The introduction and the vibe-coding lab quote 2026 industry
figures (92% daily use / 29% trust / 48% always review / 1.7× defects /
~45% OWASP). These come from surveys of varying rigour that recycle each
other. They are taught as **direction, not decimal points**, and the
speaker notes say so out loud. Do not add a statistic to a deck without
that caveat attached, and do not sharpen these into false precision.

## Conventions (guaranteed repo-wide)

- Folder/file names: kebab-case, no spaces. Week folders are `weekNN` (two
  digits, so they sort) and `weekNNb-reading-week`; lab folders are
  `<topic>_lab` (underscores: a Python package name).
- Every `<topic>-lecture.md` starts with YAML frontmatter: `title`, `topic`
  (the row's `lecture` name — `check_schedule.py` fails if they differ),
  `type` (`lecture`), `source` (`authored`), `marp: true`, `theme: aiap`,
  `paginate` — and no `week:`, which the folder name states and
  `check_schedule.py` rejects. Lab READMEs carry no
  frontmatter — they are read as plain markdown on GitHub and on the site.
- Slides are separated by `---` on its own line; slide 1 uses `#`, the rest `##`.
- All decks use `themes/aiap.css` — edit the theme to restyle every deck at
  once. Per-slide classes via `<!-- _class: ... -->`: `lead` (title),
  `cols` (2-column bullets), `grid2`, `logos`, `dense`, `centered-table`,
  `side`, `code-sm`/`code-xs`. Kicker lines use
  `<span class="kicker">// ...</span>` (requires the workflow's `--html`).
- **NO IMAGE FILES in the teaching path.** Every diagram is drawn in CSS.
  A PNG of an attack chain cannot be diffed in git, cannot be restyled
  from one place, and — the reason that matters most here — cannot be read
  by an assistant helping a student. Shared components in the theme:

  | Component | For |
  |---|---|
  | `.callout` | An aside or a warning. Warm violet |
  | `.prompt` | **Something you type at a model.** Cool blue, monospace, labelled |
  | `.prompt.bad` / `.prompt.good` | A vague-vs-better pair. Red / green |
  | `.reply` | The model's response, when the contrast matters |
  | `.flow` | Left-to-right chain of steps; `.step.danger` for the bad end |
  | `.stack` | Ranked layers; `.layer.top`, `.layer.untrusted` |

  A prompt is neither prose nor code and must not be set as either — this
  module quotes prompts constantly, and undifferentiated grey text is how
  a slide stops teaching. Anything bespoke to one deck goes in that deck's
  own `<style>` block, which wins over the theme because it comes later.
- **Code goes in a fenced block, always** — never inline in a bullet, never
  as an image. Tag the fence with its real language: `verify_snippets.py`
  parses `python`/`json`/`yaml`/`bash`, so a SQL example tagged ```python
  fails the build (correctly).
- Bullet markers carry meaning: `* ` = fragmented (revealed one per
  keypress in the HTML presentation), `- ` = shown immediately. Fragment
  build-up slides; leave reference slides (agendas, summaries, tables)
  immediate.
### Speaker notes are primarily FOR AN AI, not for a presenter

This is the single highest-value convention in the repo and the easiest to
get wrong. Notes live in `<!-- Speaker notes: ... -->` comments at the TOP
of the slide, straight after the `---`.

**Who reads them, in priority order:**

1. **An assistant helping a student** who is stuck on this slide. It can
   already infer what the code does. What it cannot infer is what a
   learner *characteristically gets wrong here* — and without that it
   explains the right answer to someone who needed the wrong one
   diagnosed.
2. **An assistant reading the deck** to answer questions about the
   material, needing the slide's intent rather than its bullets.
3. **A presenter**, who gets pacing and weight as a by-product.

Reader 3 is a by-product. Do not write for reader 3 first.

**So a note carries:**

- `~H:MM` cumulative elapsed time, matching the sibling OOC module's
  format — `~0:20` means twenty minutes in, **not** twenty seconds.
- **The concept the slide is actually testing**, stated so an assistant
  could teach from it without the slide.
- **The misconception** — the specific wrong answer to expect and the
  faulty mental model that produces it. **Mandatory on every `Predict:`
  slide**, and enforced by `scripts/check_speaker_notes.py`.
- What it connects to: which earlier idea it pays off, which later one it
  sets up, whether it maps onto an assessment.

**What a note is NOT:**

- Not stage direction. "Ask for hands", "take a vote", "expect
  photographs", "put it on the board" are worth at most a clause, and
  most notes should have none. An assistant cannot use any of it, and it
  crowds out what it can use.
- Not a restatement of the slide's own bullets.

**The asymmetry that justifies all of this:** the slide states the *right*
answer. It never states the wrong one — and the wrong one is the entire
reason a predict slide exists. A student who got it wrong does not need
the correct answer repeated; they need to know *which* mistaken model
produced theirs. Write that down and an assistant stops explaining and
starts diagnosing.

Notes **ship inside the rendered HTML** and are readable by anyone viewing
source, so write them publishable: nothing about individual students or
cohorts.
- Decks are SELF-CONTAINED and reusable: never reference other weeks or
  the module schedule, and never name an institution, a lecturer, a VLE
  or a course code — any lecturer in any college must be able to present
  a deck as it stands. Exempt from the schedule rule only: the
  introduction's module-logistics act, which
  may state its own schedule and link its own site and repo (the links are
  what another lecturer swaps) but is held to the identity rule like every
  other deck. `check_deck_portability.py` enforces both.

### PowerPoint lectures (a pilot since September 2026: the overview lecture)

A week may be taught from a PowerPoint deck instead of a Marp one,
`<topic>-lecture.pptx` (the module owner builds them with the
powerpoint-maker skill: the stock Office look, code in dark
syntax-coloured boxes, every bullet revealed on click). Everything above
about content still holds (the deck flow below, portability, notes written
for an AI first, the misconception on every Predict slide), with the
notes in PowerPoint's notes pane.

CI runs on Linux and cannot open a deck, so two files are generated beside
it on Windows and committed with it. Neither is ever edited by hand:

- `<topic>-lecture.pdf`: the slides exactly as PowerPoint prints them. The
  site shows it.
- `<topic>-lecture.notes.md`: every slide's text and speaker notes as
  markdown in the shape of a Marp deck. The snippet, notes and portability
  gates read it, the site prints it under the PDF, and it is what an
  assistant should read to learn what the lecture says.

`python scripts/export_decks.py` writes both (with the deck closed:
PowerPoint locks a deck it has open). The text copy records the SHA-256 of
the deck, of the PDF and of its own text, and `check_schedule.py` fails
when any of them stops matching: a deck saved since its export, or a text
copy edited by hand. A code box's alt text names its language
(`Code, python`); add `, no-parse` to exempt a deliberately incomplete
snippet, as `<!-- no-parse -->` does above a fence. The lecture's page on
the site shows the PDF, a download of the deck, a link to Microsoft's web
viewer (experimental: Microsoft does not support it for production use),
and every slide's text with its notes.

### Deck flow — every topic deck, same shape

Lectures are **two-hour** slots. The shape mirrors the sibling OOC module
so a student moving between them never has to relearn where things are:

    title (lead + kicker)
      -> hook: a problem, a number, or a question (1-2 slides)
      -> "the idea": the one sentence the two hours are about
      -> agenda, naming both halves
      -> PART 1 (~0:05 to ~0:55): the core concepts, each with a worked
         example, and 2-3 PREDICT beats
      -> break: one `lead` slide at about ~0:55 — "ten minutes", and the
         question part 2 answers
      -> PART 2 (~1:05 to ~1:45): the deeper mechanism, a second worked
         case, and ONE "try it now" activity (5-10 minutes, students on
         their own laptops, with a .prompt box to type), plus 2-3 more
         PREDICT beats
      -> common mistakes / honest limits
      -> Summary            <- ALWAYS last, no resources slide after it

Timing notes run from ~0:01 to about ~1:45, which leaves the break and
questions inside the slot; `check_speaker_notes.py` accepts hours 0 and 1.
Part 2 is not padding: it is where the mechanism gets explained rather
than named, and where the room does something with its hands. Do not add
a statistic or a dated claim to fill time — reuse a figure the deck or its
lab already carries, or make the point without one.

**Predict beats** are the load-bearing part. A slide poses something and
the room commits to an answer out loud *before* the reveal; answers are
`* ` bullets so they appear after the class has committed. Every predict
slide's speaker note must name **the wrong answer to expect and the
faulty reasoning behind it** — the slide already states the right answer,
and the misconception is the thing an AI reading the deck cannot infer.

The introduction is the one exception: a two-act deck (the argument, then
logistics), about an hour long by design, still hook-first and Summary-last.

### Lab formula — every lab, same shape

    # AIAP <Topic> Lab
    ## What you'll learn          <- 4-6 bullets, outcomes not topics
    ## Table of Contents
    ## Getting started            <- the standard block; identical everywhere
    ## 1. <Section>
    ### DIY 1: <name>
    ## 2. <Section>
    ### DIY 2: <name>
    ...
    ## Common mistakes
    ## Summary                    <- ALWAYS last

**Every `### DIY k` carries all three of:**

1. numbered steps,
2. a `**What you should have**` block (or `**Expected output**` with a
   ```text fence where the step produces console output), and
3. a hint in `<details><summary>Hint</summary>`.

A DIY without a hint is not finished. `scripts/check_lab_structure.py`
enforces all of this.

**Size a lab to a two-hour slot, and judge it by COMPOSITION.** The number
that matters is the fraction of DIY steps asking the student to *do or
write something themselves* rather than copy a supplied fence. When a lab
runs long, cut transcription before you cut exercises.

**Why the self-check block differs from OOC.** OOC labs produce console
output, so `**Expected output**` can be exact text. Many AIAP steps end in
something on screen that is not console output — a chat answer, a diff, a
table a shipped script printed — which is why `**What you should have**`
exists. It describes what the student should be looking at by the end of
the DIY, so they can tell they are on track. It is never a file to hand
in: nothing in a lab is submitted (see below). Use whichever the exercise
actually produces; never omit both, or the student has no way to
self-check.

### How a lab is delivered — tasks, not write-ups

The setup lab (`lectures-and-labs/week02/setup_lab/`) is the worked
example.

- **Where it runs.** In the student's own private template copy, in a
  Codespace built from the root `.devcontainer/` (Debian, Python 3.12,
  Node 22, `gh` signed in, Copilot Chat installed), usually in the
  browser. So a lab may assume Linux commands, network access and a
  signed-in Copilot, and must not assume anything else about the machine.
  In a browser the browser owns some shortcuts — `Ctrl+W`, `Ctrl+N`,
  `Ctrl+T` and any chord ending in them — so instructions use the menus,
  the right-click menu or the Command Palette instead. `Ctrl+Alt+I` (the
  chat panel) and `Ctrl+I` (inline chat) are safe.
- **Nothing is submitted and nothing is corrected.** The 4% Practical
  Assessment on Moodle is the only assessed piece of a lab week. A lab
  therefore never asks for a file, table or note "to hand in", and never
  says "record", "write down" or "for submission".
- **Tasks, not reflection.** A lab is built from tasks with visible
  results, not from reflection tables or write-ups. Every DIY step is a
  prompt to type, a command to run, or something to look at. No
  reflection tables, no `REFLECTION.md`. When the point needs a
  comparison, ship a script that makes it (the setup lab's
  `email_check.py` runs every validator the student got against the same
  awkward addresses and counts where they disagree) rather than asking
  the student to compare by eye and write it down. When a lab runs
  short, extend a task rather than adding a write-up: the same prompt
  put to two or three other models from the model picker, framed as a
  hunt ("which one can you catch out?"), is the cheapest extension.
- **Surprises that teach either way.** Model behaviour moves every few
  months, so a DIY must land whichever way the model behaves — anchor it
  on something the student checks themselves (`hasattr`, `wc -l`,
  running the file, a shipped harness) rather than on the model failing.
  A lab that depends on the model failing has a shelf life.
- **Say which chat mode, every time — and know there is no no-tools
  mode.** In a Codespace the Copilot chat offers **Interactive** (reads
  freely, asks before it runs a command or changes a file), **Plan**
  (read-only) and **Autopilot** (never asks); the "Ask" role that the VS
  Code docs describe is not offered by the Copilot harness. Every mode
  can read the workspace, so an answer "from memory" is asked for in the
  prompt ("without using any tools"), never selected in a picker, and the
  step watches whether the instruction was obeyed. A step that talks to
  the assistant names the mode and says when to start a fresh
  conversation.
- **The why lives in the hint, short.** Steps stay bare and imperative;
  the mechanism behind the surprise goes in the `<details>` hint, a
  paragraph or two, so a student who wants it has it and one who does not
  is not made to sit through it.
- **Sized to two hours.** Let the exercises run to about 110 minutes
  including Codespace start-up.

Labs written before this rule (prompting, agents, vibe-coding) still carry
`REFLECTION.md` exercises; bring each into line when it is next edited,
keeping the formula above and `check_lab_structure.py` green.

## Editing rules

- To change a lecture: edit its week's `<topic>-lecture.md` and push —
  CI re-renders the deck and republishes the site.
- To change a PowerPoint lecture: edit the `.pptx` in PowerPoint, close
  it, run `python scripts/export_decks.py`, and commit the deck with the
  `.pdf` and `.notes.md` it rewrites. Never edit the `.notes.md`: it is
  regenerated from the deck, and `check_schedule.py` fails if it was
  touched.
- To add a lab: create `<topic>_lab/` in its week's folder with a
  `README.md` to the formula above plus starter code, name it in the row's
  `lab`, and add `"<topic>"` to `CONFORMING` in
  `scripts/check_lab_structure.py`. If its tests need a live key, add it to
  `NEEDS_KEY` in `scripts/verify_labs.py`; if it ships a test meant to stay
  red until the student writes it, add it to `PLACEHOLDER_TESTS`.
- To add, move or drop a teaching week: edit `module/schedule.json` (the
  order, the week numbers, each row's `lecture` and `lab` names and
  `assessment` label), create, rename or remove the `weekNN/` folders to
  match (a renumber is a `git mv` of the folders; the files inside keep
  their names), then run `python scripts/update_current_week.py` to
  regenerate both week tables. `check_schedule.py` fails on any
  disagreement; nothing else may state a week number. When a deck's site
  name changes, add the old name to `OLD_FOLDERS` in `build_index.py` so
  its old URL still resolves.
- Never edit the published HTML — it is generated. Edit the Markdown source
  and let CI rebuild.

## The gates

Ten run on every push. Before any push, all must pass:

    python scripts/safety_audit.py           # credentials, student data, bad paths
    python scripts/check_links.py            # every relative link and anchor resolves
    python scripts/verify_snippets.py        # every fenced snippet parses
    python scripts/verify_labs.py            # lab code compiles; tests where possible
    python scripts/check_practice_bank.py    # practice bank is well-formed
    python scripts/check_lab_structure.py    # every lab follows the formula
    python scripts/check_deck_portability.py # every deck is liftable to another course
    python scripts/check_speaker_notes.py    # notes are AI-usable; predicts name the misconception
    python scripts/check_schedule.py         # the schedule is stated once, every view agrees, pptx exports are current
    python scripts/build_index.py build      # week <-> deck <-> lab structure holds

- `verify_snippets.py` is this repo's replacement for OOC's `javac` gate.
  There is no single language to compile here, so it PARSES: `ast.parse`
  for python, `json.loads`, `yaml.safe_load`, and `bash -n` (syntax only,
  never executed). A deliberately-broken snippet is skipped with
  `<!-- no-parse -->` on the line directly above its fence. **The marker
  is the point** — a fence is either verified or explicitly declared
  unverifiable, and nothing is silently unchecked.
- `verify_labs.py` compiles every lab `.py` and runs pytest where it can.
  `NEEDS_KEY` names the one lab (rag) that cannot be verified beyond
  syntax without live credentials, and it prints that limit on every run
  rather than letting a green tick imply otherwise.
  `PLACEHOLDER_TESTS` names test files that are *expected to fail* —
  student scaffolding (`prompting`), or a real test over a planted bug
  (`cli-agents`, where an agent is pointed at it). If one starts passing,
  a worked solution has reached the public repo and the gate says so.
- `check_links.py` matters more here than in OOC: the lab READMEs run
  10k–30k characters with their own tables of contents, and they arrived
  by migration from nine separate Classroom repos.

## Never commit

- Student personal data of any kind (names, IDs, grades, submissions).
- **Worked solutions or instructor guides.** They live in the private
  `ai-assisted-programming-labs-solutions` repo. This boundary carries
  more weight here than in OOC, because the tutor brief above places no
  restriction on the assistant — the repo split is the only thing between
  a student and an answer key.
- **Credentials of any kind.** Only `.env.example` may be tracked; every
  other `.env*` is gitignored and the audit rejects it.
- **Moodle enrolment passwords.** The week-01 deck deliberately says the
  group passwords are given out verbally: the deck is published on a
  public website.
- Real assessment material — the live MCQ bank stays in Moodle.
- Bulk third-party materials.

## Local preview (before committing)

    npm install          # once per machine — the marp-cli version pinned in
                         # package.json, the same one CI installs. There is no
                         # committed lockfile: CI uses `npm install -g <pinned>`
                         # and never reads one.
    npm run preview      # live server over the repo -> http://localhost:8080
    npm run export:intro # one deck straight to build/…/slides.pdf

After editing a deck's layout, re-render and check nothing overflows the
720px slide — content that spills is silently cropped in the PDF.
