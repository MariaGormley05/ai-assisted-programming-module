# AI-Assisted Programming

Everything for the **AI-Assisted Programming** module (semester 1) at
Atlantic Technological University: the lectures, the labs, and an MCQ
practice app.

### Start here → **[danielcregg.is-a.dev/ai-assisted-programming](https://danielcregg.is-a.dev/ai-assisted-programming/)**

The whole module in one page — every lecture, every lab and the MCQ
practice, readable in the browser with nothing to install.

## Before the first lab

1. **A GitHub account under your real name.** You will be sending links
   to it all semester, and it is the account an employer will look at.
2. **The [GitHub Student Developer Pack](https://education.github.com/pack)**
   — free for verified students. It gives you the Copilot Student plan
   (the editor assistant and the terminal coding agent this module uses)
   and Pro-level Codespaces. Verification can take a few days, so apply
   early.
3. **Moodle enrolment.** The group password is given out in the first
   lecture, not published.

## Doing the labs

You work in **your own copy** of this repo:

1. Click **Use this template → Create a new repository** (green button,
   top-right). Name it anything; **make it Private** — it's your work.
   Don't *Fork*: a fork of a public repo can never be made private.
2. On *your* repo: **Code → Codespaces → Create codespace**. Python 3.12,
   Node 22 and the `gh` CLI are already there.
3. Open this week's folder under `lectures-and-labs/` (the lecture is there
   too) and follow the lab's README.

Details — including how to pull corrections into your copy mid-semester —
in **[lectures-and-labs/README.md](lectures-and-labs/README.md)**. Read-only lab pages are also on
the [site](https://danielcregg.is-a.dev/ai-assisted-programming/labs/),
always the current version.

The RAG lab and one step of the CI/CD lab need a free API key of your own
(the same key, once in a `.env` and once as a repository secret), and the
CLI agents lab needs you to sign in to a coding agent with your GitHub or
Google account. Each README says what, and how. Nothing in the module
costs money. **Never commit a key** — put it
in a `.env`, which is gitignored and rejected by the repo's safety audit.

## Assessment

| Component | Weight | When |
|---|---|---|
| MCQ 1 | 32% | In person, during the lab slot, straight after reading week |
| MCQ 2 | 32% | In person, during the lab slot, in the last week |
| Practical Assessments 1–9 | 4% each | One per lab, on Moodle, open for that lab's week |

The **Practical Assessments** are short Moodle questions, one for each
lab, open from the Monday to the Sunday of the lab's week — do each
whenever suits you that week. You may use AI tools for them, as you do in
the labs. They are built so that pasting the question into an assistant is
not enough on its own: each asks about the lab code in front of you, what
it actually does when you run it, or what is true right now. A missed one
counts as zero.

The **MCQs** are drawn from the lectures *and* the labs. Practise with the
[MCQ practice app](https://danielcregg.is-a.dev/ai-assisted-programming/practice/):
self-test quizzes on every topic, with your progress kept in your browser
only.

## Module schedule

<!-- current-week:start -->
> 🗓️ **Current teaching week: 2 — AIAP Overview** (week beginning 21 Sep 2026).
<!-- current-week:end -->

<!-- schedule-table:start -->
| Week | Topic | Lecture | Lab |
|---|---|---|---|
| 1 | Module Introduction | [slides](lectures-and-labs/week01/introduction-lecture.md) | _No labs week 1. Labs start week 2._ |
| **➡️ 2** | AIAP Overview | [slides](lectures-and-labs/week02/overview-lecture.pdf) | [lab](lectures-and-labs/week02/setup_lab/README.md) |
| 3 | Prompting & Context Engineering | [slides](lectures-and-labs/week03/prompting-lecture.md) | [lab](lectures-and-labs/week03/prompting_lab/README.md) |
| 4 | Retrieval & Grounding | [slides](lectures-and-labs/week04/rag-lecture.md) | [lab](lectures-and-labs/week04/rag_lab/README.md) |
| 5 | MCP | [slides](lectures-and-labs/week05/mcp-lecture.md) | [lab](lectures-and-labs/week05/mcp_lab/README.md) |
| 6 | Coding Agents | [slides](lectures-and-labs/week06/agents-lecture.md) | [lab](lectures-and-labs/week06/agents_lab/README.md) |
| — | Reading week | [details](lectures-and-labs/week06b-reading-week/README.md) | — |
| 7 | **MCQ 1** (32%) · held during the lab slot | [details](lectures-and-labs/week07/README.md) · [what it covers](mcq/mcq1/README.md) | — |
| 8 | Security of AI-Generated Code | [slides](lectures-and-labs/week08/security-lecture.md) | [lab](lectures-and-labs/week08/security_lab/README.md) |
| 9 | CLI Coding Agents | [slides](lectures-and-labs/week09/cli-agents-lecture.md) | [lab](lectures-and-labs/week09/cli_agents_lab/README.md) |
| 10 | CI/CD & Evals | [slides](lectures-and-labs/week10/cicd-lecture.md) | [lab](lectures-and-labs/week10/cicd_lab/README.md) |
| 11 | Vibe Coding & Spec-Driven | [slides](lectures-and-labs/week11/vibe-coding-lecture.md) | [lab](lectures-and-labs/week11/vibe_coding_lab/README.md) |
| 12 | **MCQ 2** (32%) · held during the lab slot | [details](lectures-and-labs/week12/README.md) · [what it covers](mcq/mcq2/README.md) | — |
<!-- schedule-table:end -->

The schedule is defined once, in [`module/schedule.json`](module/schedule.json);
this table, the banner above it, the module site and the Moodle course page
are all generated from it. Reading week is always the week of the Irish
October bank holiday, and week 1 is worked out from that each year.

### The everyday uses, and where you practise them

Four things you will do with an assistant most days are not weeks of their
own. They recur through the labs, so you meet each one more than once:

| You want to… | Practised in |
|---|---|
| **Explain** code you did not write | [setup DIY 4](lectures-and-labs/week02/setup_lab/README.md#diy-4-the-file-it-has-never-read), [setup DIY 8](lectures-and-labs/week02/setup_lab/README.md#diy-8-break-a-regex-with-its-help), [agents DIY 1](lectures-and-labs/week06/agents_lab/README.md#diy-1-understand-code-you-did-not-write) |
| **Debug** from an error or a failing test | [prompting DIY 6](lectures-and-labs/week03/prompting_lab/README.md#diy-6-chain-of-thought-on-a-real-bug), [cli-agents DIY 8](lectures-and-labs/week09/cli_agents_lab/README.md#diy-8-a-script-that-explains-a-failure) |
| **Write tests**, before or after the code | [prompting DIY 8](lectures-and-labs/week03/prompting_lab/README.md#diy-8-tests-first), [cicd DIY 1](lectures-and-labs/week10/cicd_lab/README.md#diy-1-make-it-run-your-tests), [cicd DIY 5](lectures-and-labs/week10/cicd_lab/README.md#diy-5-climb-the-assertion-ladder) |
| **Review** a change you did not watch being made | [agents DIY 2](lectures-and-labs/week06/agents_lab/README.md#diy-2-refactor-with-the-diff-open), [cicd DIY 3](lectures-and-labs/week10/cicd_lab/README.md#diy-3-a-review-step-that-cannot-lie), [vibe-coding DIY 2](lectures-and-labs/week11/vibe_coding_lab/README.md#diy-2-find-something-you-would-not-ship) |

## Module info

- [Module overview — weekly topics and what each week covers](module/module-overview.md)

<details>
<summary>How the repo is put together (for maintainers)</summary>

- **The schedule is one file**, `module/schedule.json`: the order of
  topics, which week teaches which deck and lab, and the assessment labels.
  The table above, the site, the labs page and the Moodle course page are
  generated from it, and `scripts/check_schedule.py` fails the build if
  anything disagrees with it. There is no start date in it: week 1 is
  derived from the October bank holiday every year.
- **Lectures and labs** live together, one folder per week, under
  `lectures-and-labs/weekNN/`: the deck is `<topic>-lecture.md` (Marp
  markdown) or, in the PowerPoint pilot, `<topic>-lecture.pptx` with its
  PDF and text copy exported beside it by `scripts/export_decks.py`; the
  lab is `<topic>_lab/`. The week number names the
  folder and nothing else; the site keeps topic addresses, taken from the
  schedule. All ten decks are written. Every deck is
  self-contained and names no lecturer or institution, so any week can be
  lifted into another course unchanged; the introduction may state its
  own schedule and link its own site. `scripts/check_deck_portability.py`
  enforces that.
- **Labs** are plain Python in each week's `<topic>_lab/` folder. On the
  site they are addressed by topic (`/labs/<topic>/`), so a reshuffled
  schedule renames folders but never a link.
- **Three GitHub Actions workflows.** `marp` runs on every push to `main`:
  it runs the ten gates (safety audit, links, snippets, lab code, practice
  bank, lab and deck structure, speaker notes, schedule, site index), renders every
  deck to HTML and PDF, builds the lab pages and the practice app, and
  publishes the site straight to GitHub Pages — nothing is committed back.
  `current-week` runs every Monday and rewrites the banner above this
  schedule. Both are guarded to run only in this repository, never in a
  student's copy. `course-sync` is the inverse: it runs only in a
  student's copy, nightly, and commits any changed lectures, lab
  instructions, READMEs, devcontainer and untouched lab starter files from
  this repo into theirs. A file the student edited, created or deleted is
  always kept. It needs this repository to be public.
- **Conventions and editing rules** live in [`AGENTS.md`](AGENTS.md)
  (`CLAUDE.md` imports it). Local preview: `npm install`, then
  `npm run preview`.

</details>

## For AI tools

Read [`AGENTS.md`](AGENTS.md) first — it defines the conventions this repo
guarantees, and how to behave depending on whose copy you are in. (`CLAUDE.md`
imports it, so Claude Code reads the same file.)
