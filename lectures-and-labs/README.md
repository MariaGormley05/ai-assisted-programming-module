# Lectures and labs

Everything for each week of the module is here, one folder per week, in
order. A teaching week's folder holds:

- **`<topic>-lecture.md`**: that week's lecture slides (for example
  `prompting-lecture.md`). In a Codespace it opens as slides; in VS Code on
  your own computer, install *Marp for VS Code* and open the preview.
- **`<topic>_lab/`**: the lab, with its **`README.md`** (the instructions)
  and the starter code you work in. Your own code goes in that folder too.

The MCQ weeks and the reading week hold just a `README.md` saying what
happens that week.

<!-- schedule-table:start -->
| Week | Topic | Lecture | Lab |
|---|---|---|---|
| 1 | Module Introduction | [slides](week01/introduction-lecture.md) | _No labs week 1. Labs start week 2._ |
| **➡️ 2** | AIAP Overview | [slides](week02/overview-lecture.md) | [lab](week02/setup_lab/README.md) |
| 3 | Prompting & Context Engineering | [slides](week03/prompting-lecture.md) | [lab](week03/prompting_lab/README.md) |
| 4 | Retrieval & Grounding | [slides](week04/rag-lecture.md) | [lab](week04/rag_lab/README.md) |
| 5 | MCP | [slides](week05/mcp-lecture.md) | [lab](week05/mcp_lab/README.md) |
| 6 | Coding Agents | [slides](week06/agents-lecture.md) | [lab](week06/agents_lab/README.md) |
| — | Reading week | [details](week06b-reading-week/README.md) | — |
| 7 | **MCQ 1** (32%) · held during the lab slot | [details](week07/README.md) · [what it covers](../mcq/mcq1/README.md) | — |
| 8 | Security of AI-Generated Code | [slides](week08/security-lecture.md) | [lab](week08/security_lab/README.md) |
| 9 | CLI Coding Agents | [slides](week09/cli-agents-lecture.md) | [lab](week09/cli_agents_lab/README.md) |
| 10 | CI/CD & Evals | [slides](week10/cicd-lecture.md) | [lab](week10/cicd_lab/README.md) |
| 11 | Vibe Coding & Spec-Driven | [slides](week11/vibe-coding-lecture.md) | [lab](week11/vibe_coding_lab/README.md) |
| 12 | **MCQ 2** (32%) · held during the lab slot | [details](week12/README.md) · [what it covers](../mcq/mcq2/README.md) | — |
<!-- schedule-table:end -->

## Before you start

Sign up for the **[GitHub Student Developer Pack](https://education.github.com/pack)**
if you have not already. It is free for verified students, and it gives
you the **Copilot Student plan** — the editor assistant and the terminal
agent these labs use — and Pro-level Codespaces. Verification can take a
few days, so do it before the first lab rather than during it.

Use your real name on your GitHub account. You will be sending links to it
all semester, and it is the account an employer will look at.

## Getting your own copy (once)

1. On the module repo, click **Use this template → Create a new
   repository**. Name it anything; **make it Private** — it's your work.
2. On *your* repo: **Code → Codespaces → Create codespace**.
3. The devcontainer gives you Python 3.12, Node 22 and the `gh` CLI. There
   is nothing to install, and the Codespace opens on this page.
4. If VS Code asks whether you trust the authors of the files in this
   folder, choose **Yes**: it is your own copy of the module's files, and
   nothing in the labs can run in Restricted Mode.
5. Open this week's folder and follow the lab's README.

Don't *Fork*. A fork of a public repo can never be made private, so your
work would be world-readable, and the fork network would publish a list of
everyone taking the module.

Stop your Codespace when you finish for the day (it also stops itself
after half an hour idle). The free allowance is generous, not infinite.

## Doing a lab

Open the week's lab folder (for example
`lectures-and-labs/week03/prompting_lab/`) and follow its `README.md`. Its
first step is to `cd` into the folder in the terminal and install the lab's
requirements, if it has any. Every exercise ends with
**What you should have** or an **Expected output** block, so you can check
yourself before asking, and every exercise has a **Hint** you can expand.

Each lab has a short Practical Assessment on Moodle, worth 4% and open for
that lab's week. There is no lab in the introduction week or in the two
MCQ weeks; the table above says which weeks those are.

## Saving your work

Git keeps your work, not the Codespace. After each exercise (or at least
before you close the browser):

1. Open the **Source Control** panel (the branch icon in the left bar, or
   `Ctrl+Shift+G`).
2. Type a one-line message such as `prompting DIY 3 done` in the box.
3. Click **Commit**, then **Sync Changes** (that is the push).

Your repo on GitHub now has the code, and stays there whatever happens to
the Codespace. GitHub deletes a Codespace that sits unused for 30 days;
only what you have committed and pushed survives.

## Labs that need a key or a sign-in

The RAG lab's generation half calls a hosted model and needs an API key;
the default is the Gemini API's free tier, and its README says where to
get one. The CI/CD lab's review step (its section 3) reuses that same free
key, stored as a repository secret so GitHub Actions can read it; the rest
of that lab runs offline. Nothing else needs a key: the MCP lab's weather
server uses a free service without one, and the security lab runs
offline by design. The CLI agents lab needs you to sign in to a coding
agent with your GitHub or Google account — a sign-in, never a key in a
file.

**Never commit a key.** Put it in a `.env` file in the lab folder; `.env`
is gitignored, and the repo's safety audit will reject one if it ever gets
staged. Read it from the environment in code — never a literal, never a
default value.

```bash
cp .env.example .env   # then edit .env with your own key
```

## Running a lab's tests

Labs are self-contained projects. Install from inside the lab folder:

```bash
cd lectures-and-labs/week10/cicd_lab
pip install -r requirements.txt
python -m pytest
```

## If a lab is corrected mid-semester

The [live site](https://danielcregg.is-a.dev/ai-assisted-programming/labs/)
always shows the current instructions — read there if something looks
wrong. To pull corrections into your own copy:

- **Automatically** — it runs each time you open your Codespace.
- **A button** — *Terminal → Run Task → Update course content*.
- **One line** — `bash scripts/update-course-content.sh`.

It refreshes the lectures, the lab instructions, the week pages, this
guide, the Codespace configuration, and any lab starter file you have
**not** changed — so a fix to a lab you have not started yet reaches you
too. A file you have edited, created or deleted is always yours: it is
kept, and the script tells you so.

The same update also runs **in your repo on GitHub every night**, so you
may see a commit called *update course content* appear that you did not
make. That is expected. If `git push` is ever rejected because of it, run
`git pull --rebase` first, then push again: a rebase drops a sync commit
that both sides made, where a plain pull would keep a merge of two
identical copies. When the module is over you can switch Actions off in
your copy (Settings → Actions) so the nightly run stops.
