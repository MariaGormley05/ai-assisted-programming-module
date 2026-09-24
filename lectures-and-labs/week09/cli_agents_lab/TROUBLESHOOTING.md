# CLI agents lab — troubleshooting

Start with the setup check in this folder. It names what is missing:

```bash
python check_setup.py
```

## Installing

### `copilot: command not found` after installing

npm put it somewhere your shell is not looking. `npm prefix -g` prints
npm's global folder, and its `bin` folder must be on your `PATH`. In a
Codespace, opening a new terminal is usually enough.

### npm complains about the Node version

Both agents need Node 22 or newer; `node --version` shows yours. The
Codespace already has it. On your own machine, install a current LTS
release of Node.

### On your own Windows machine

The lab works in PowerShell too. `npm install -g @github/copilot` is the
same, and `winget install GitHub.Copilot` is an alternative. PowerShell
does not understand `\` at the end of a line, so type multi-line commands
on one line.

## Signing in

### Copilot says you have no access

- Check that a plan is active at https://github.com/settings/copilot —
  Copilot Free, or Copilot Student through GitHub Education.
- In a Codespace, the Codespace's own `GITHUB_TOKEN` can be picked up in
  place of your sign-in, and it has no Copilot access. Clear it for that
  terminal only, start the agent, and type `/login`:

  ```bash
  unset GITHUB_TOKEN GH_TOKEN
  copilot
  ```

### `/login` shows a code and a web address

That is the sign-in. Open the address, type the code, approve. There is
nothing to paste into a file.

### Gemini's sign-in never comes back to the terminal

In a Codespace the browser cannot always reach the terminal. Start it as
`NO_BROWSER=true gemini`: it prints a link to open, then asks you to paste
back a code.

### Where does a token or key go?

Never in a file in this repository — the module's safety audit rejects
one, and your repository may be public. Signing in with `/login` or with
Google stores what the agent needs in its own configuration, outside the
repo.

## In a session

### The agent ignores my `AGENTS.md`

- Instruction files are read when a session **starts**. Quit and start a
  new one.
- Check where you created it: `sample-app/AGENTS.md`, beside the code,
  in the folder you start the agent from.
- Gemini reads `GEMINI.md` unless `context.fileName` says otherwise
  (DIY 3, step 2), and ignores a folder's settings until you trust the
  folder. `/memory show` prints what it loaded.

### My command or skill does not appear

- Check the folder: `.github/skills/<name>/SKILL.md` at the root of your
  repository for Copilot, `.gemini/commands/<name>.toml` in the folder
  you start Gemini in.
- A skill's folder name and its `name:` must match.
- Copilot: `/skills` lists what it found. Gemini: `/commands reload`.

### It keeps asking permission — or has stopped asking

An approval you give during a session can last for the rest of that
session. In Copilot, `/reset-allowed-tools` clears them; starting a new
session clears them in both agents.

### It says I have run out of requests

The free plans have limits: a monthly allowance on the Copilot student
plan, and per-minute and daily limits on Gemini's free tier. Wait, or
switch to the other agent — every exercise works in both.

## The policy checker

### `policy error: ... has no wildcards`

A rule in this checker names the words a command starts with, so
`shell(git)` already covers every git command. Write `shell(git)`, not
`shell(git:*)`.

### `No module named 'pytest'`

Run `pip install -r requirements.txt` from this folder.

### The checker and my agent disagree

That is DIY 7's finding, not a bug. The checker is one model of matching;
each agent has its own, and it can change between versions.
