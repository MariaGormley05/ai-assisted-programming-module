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
- In a Codespace, Copilot starts signed in with the Codespace's own
  `GITHUB_TOKEN`. If that is not the account with the plan, type
  `/login` to sign in as the right one. If it still uses the wrong
  account, clear the token for that terminal only, start the agent, and
  type `/login`:

  ```bash
  unset GITHUB_TOKEN GH_TOKEN
  copilot
  ```

### `/login` shows a code and a web address

That is the sign-in. Open the address, type the code, approve. There is
nothing to paste into a file.

### Gemini's key box says "Paste your API key here"

Gemini did not find your key, so it is asking for it. Quit it, then check
that the file is `sample-app/.env` and its name starts with a dot, that
it has a line `GEMINI_API_KEY=` followed by your key, and that you
started `gemini` from `sample-app`. Start it again. **Sign in with
Google** is not the way in: Google's own sign-in stopped serving free
personal accounts on 18 June 2026. In a script (`gemini -p`) the same
problem shows as `Please set an Auth method` and exit code 41.

### Where does a token or key go?

Never in a file git tracks — the module's safety audit rejects one, and
your repository may be public. Copilot's `/login` stores what it needs in
its own configuration, outside the repo. Gemini's key goes in
`sample-app/.env`, which `.gitignore` covers, and Gemini also keeps the
key you confirm in a file under `~/.gemini/`, outside the repo. Never type
a key into a command or paste it into code.

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

### Gemini never answers

Look at the bottom right of its screen. It should read
`gemini-3.5-flash-lite`. If it reads `Auto`, Gemini did not read the
`GEMINI_MODEL=gemini-3.5-flash-lite` line from `sample-app/.env`, and on a
free key its default model gave no answer when this lab was checked in
October 2026. Fix the file, quit, and start it again.

### Gemini says it is not running in a trusted directory

That is a script run (`gemini -p`) in a folder you have not trusted yet.
Start `gemini` once in `sample-app` and trust the folder, or add
`--skip-trust` to the command.

### It says I have run out of requests

The free plans have limits: a monthly allowance on the Copilot student
plan, shared with Copilot Chat (`/usage` shows what the current session
has used), and per-minute and daily limits on Gemini's free API key. Wait,
or switch to the other agent.

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
