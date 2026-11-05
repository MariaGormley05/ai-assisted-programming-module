#!/usr/bin/env bash
# Refresh the course content in YOUR copy of this repo from the module repo.
#
# Your copy was made from a template, so it shares no history with the
# module repo and `git merge` cannot be used: with unrelated histories git
# reports every differing file as an add/add CONFLICT, even files you never
# opened. This script copies files instead, which cannot conflict.
#
# It refreshes the course files -- the lectures, the lab instructions, the
# README, the Codespace configuration and the lab starter files -- from the
# module repo. It never touches your .env, a file you created, a file you
# edited or a file you deleted: anything that differs from what you were
# given is yours and is left alone, and the script says so when it does.
#
# Run it whenever you like:   bash scripts/update-course-content.sh
# (In a Codespace it also runs by itself each time you open the workspace,
# and the course-sync workflow runs it in your repo on GitHub every night.)
set -uo pipefail
# A path is a path. Left to itself git reads a name such as data[1].txt as a
# pattern that also matches data1.txt, so updating the one would reach the
# other -- which may be yours.
export GIT_LITERAL_PATHSPECS=1

UPSTREAM_URL="https://github.com/danielcregg/ai-assisted-programming.git"
UPSTREAM_SLUG="danielcregg/ai-assisted-programming"
BRANCH="main"
QUIET=""; STRICT=""
for arg in "$@"; do
  case "$arg" in
    --quiet)  QUIET="--quiet" ;;   # say nothing unless something changed
    --strict) STRICT=1 ;;          # exit 1 on any problem: the nightly workflow. By hand and
  esac                             # on Codespace attach the default is to never block.
done

say() { [ "$QUIET" = "--quiet" ] || printf '%s\n' "$*"; }
die() { printf '%s\n' "$*" >&2; [ "$STRICT" = 1 ] && exit 1; exit 0; }   # never block a Codespace

command -v git >/dev/null || die "git not found."
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Not a git repository."
cd "$(git rev-parse --show-toplevel)"

# In the module's own repo there is nothing to pull from -- do nothing at all.
if git remote get-url origin 2>/dev/null | grep -qi "$UPSTREAM_SLUG"; then
  say "This IS the module repo - nothing to update."
  exit 0
fi

# A student copy's origin is always their own GitHub repository (the
# template flow makes it so). A local mirror or a clone of a clone is not a
# student copy, and treating it as one would add a remote and rewrite course
# files there: refuse.
case "$(git remote get-url origin 2>/dev/null)" in
  *github.com*) ;;
  *) die "origin is not a GitHub repository, so this is not a copy of the template. Nothing changed." ;;
esac

git remote get-url upstream >/dev/null 2>&1 || {
  say "Adding the module repo as 'upstream'."
  git remote add upstream "$UPSTREAM_URL"
}

say "Checking the module repo for updates..."
# A full fetch, not --depth=1: a shallow tip cannot be pushed as the
# course-sync baseline ref (git refuses "shallow update"), and the module repo
# is small enough that the first fetch is a few seconds and later ones are
# incremental.
if ! git fetch --quiet upstream "$BRANCH" 2>/dev/null; then
  die "Could not reach the module repo (offline?). Nothing changed."
fi

# The course files, listed one by one (not as directories) so that editing
# one file never blocks the rest from updating: every tracked file under
# lectures-and-labs/ (the lectures, the lab instructions, worksheets AND
# starter code), mcq/, module/ (the schedule and overview), .devcontainer/
# and .vscode/ (the Codespace and editor configuration), plus the README and
# the AGENTS.md / CLAUDE.md briefs an assistant reads.
#
# Starter code is included so that a fix to a lab you have not started yet
# still reaches you. is_yours below keeps every file you have edited,
# staged, created or deleted, which is what makes that safe: a starter file
# you are working in is yours from your first edit onward and stays as you
# left it.
#
# Deliberately NOT included: this script (bash reads a script while it runs,
# so overwriting it mid-run misbehaves; the nightly workflow runs the module
# repo's current copy of it instead), the workflows (a push made with the
# Actions token may not change them, so the nightly run would fail every
# night after the first change), and the theme, practice bank and build
# scripts (the module site serves what those produce).
#
# Plain while-read loops rather than mapfile: the default bash on macOS is
# 3.2, which has no mapfile, and this script is also run by hand on laptops.
COURSE_RE='^(README\.md|AGENTS\.md|CLAUDE\.md|lectures-and-labs/.*|mcq/.*|module/.*|\.devcontainer/.*|\.vscode/.*)$'
# The course-owned PAGES a retirement upstream may remove here (see the pass
# below): the lectures (a Marp deck, or a PowerPoint deck with its exported
# .pdf and .notes.md), the guide and the week explainers under
# lectures-and-labs/, and everything under mcq/ and module/. Never a lab
# folder: those hold your own code.
RETIRE_RE='^(lectures-and-labs/(README\.md|[^/]+/([^/]+-lecture\.(md|notes\.md|pptx|pdf)|README\.md))|mcq/.*|module/.*)$'

UPSTREAM="$(git rev-parse "upstream/$BRANCH")"
NL='
'
TAB="$(printf '\t')"

# Whose file is it? The test is its CONTENT. A file is the module repo's when
# what you have committed at that path is, byte for byte, a version the
# module repo has published there: today's, or an older one that a fix has
# since replaced. Anything else you typed, and so is anything you have not
# committed yet: yours, and left alone. (Comparing against HEAD alone would be
# wrong -- you are told to COMMIT your work, so an edit you committed looks
# "clean" against HEAD and would be overwritten.)
#
# It used to be decided by comparing each file with a remembered baseline,
# "what you were last given". That held only while the baseline kept up, and
# in autumn 2026 it did not: GitHub refused the nightly run's push of it (see
# the end of this script), so each file was updated once, no longer matched
# the stale baseline, looked like your edit and was never updated again. A
# version the module repo published stays recognisable however old it is.
#
# PUBLISHED holds one "<mode> <blob id> <path>" line for every version of
# every file in the module repo's history. The mode is part of a version: a
# file you made executable is yours, though its bytes are the module repo's.
PUBLISHED="$NL$(git -c core.quotepath=false -c log.showRoot=true log --format= --raw --no-abbrev --no-renames -m "$UPSTREAM" 2>/dev/null \
  | awk -F'\t' 'NF == 2 { split($1, f, " "); print f[2] " " f[4] " " $2 }')$NL"
[ "$PUBLISHED" != "$NL$NL" ] || die "Could not read the module repo's history. Nothing changed."
published() {   # $1 = "<mode> <blob id>", $2 = path
  case "$PUBLISHED" in *"$NL$1 $2$NL"*) return 0 ;; esac
  return 1
}

is_yours() {
  local p="$1" mine last
  mine="$(git ls-tree HEAD -- "$p" 2>/dev/null)"     # "<mode> <type> <id><TAB><path>"
  if [ -n "$mine" ]; then
    # In your last commit. Yours if you have changed it since (edited, staged
    # or deleted, not committed), or if what you committed is your own.
    git diff --quiet HEAD -- "$p" 2>/dev/null || return 0
    git diff --quiet --cached HEAD -- "$p" 2>/dev/null || return 0
    mine="${mine%%$TAB*}"
    if published "${mine%% *} ${mine##* }" "$p"; then return 1; fi
    return 0
  fi
  # Not in your last commit. If something is there, you created it.
  if [ -e "$p" ] || [ -L "$p" ] || git ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then
    return 0
  fi
  # Nothing is there. If nothing ever was, the module repo has added a file.
  # Otherwise somebody deleted it: you, and it stays deleted; or an earlier
  # run of this script, retiring a page the module repo has since brought
  # back, and it comes back.
  last="$(git log -1 --format=%an HEAD -- "$p" 2>/dev/null || true)"
  if [ -z "$last" ] || [ "$last" = "course-update" ]; then return 1; fi
  return 0
}

# What is worth a line of output: a file of yours that was kept, but only if
# the module repo has changed that file since this script last ran here. An
# edit you made weeks ago to a file it has not touched since is not news.
# This decides what is MENTIONED, never what is kept or replaced.
#
# "Last ran" is remembered twice: in the gitignored file .course-sync (a
# Codespace or your laptop) and in the ref refs/course-sync/baseline, which
# the nightly course-sync workflow pushes to your repo on GitHub and which is
# fetched here. The ref is a stand-in commit (see the end of this script)
# whose subject names the module commit it stands for. Of the two, the NEWER
# wins (the one the other is an ancestor of); if they are unrelated, the ref.
# On the first run it is the template's first commit.
MARKER=".course-sync"
git fetch --quiet origin '+refs/course-sync/baseline:refs/course-sync/baseline' 2>/dev/null || true
FILE_BASE="$(cat "$MARKER" 2>/dev/null || true)"
REF_BASE="$(git rev-parse -q --verify refs/course-sync/baseline 2>/dev/null || true)"
if [ -n "$REF_BASE" ]; then
  named="$(git log -1 --format=%s "$REF_BASE" 2>/dev/null \
    | sed -n 's/^course-sync baseline: module repo at \([0-9a-f]\{40\}\)$/\1/p')"
  if [ -n "$named" ] && git cat-file -e "$named^{commit}" 2>/dev/null; then REF_BASE="$named"; fi
fi
LAST="$FILE_BASE"
if [ -n "$REF_BASE" ]; then
  if [ -z "$FILE_BASE" ] || ! git merge-base --is-ancestor "$REF_BASE" "$FILE_BASE" 2>/dev/null; then
    LAST="$REF_BASE"    # the ref, unless the file is strictly newer than it
  fi
fi
if [ -n "$LAST" ] && ! git cat-file -e "$LAST^{commit}" 2>/dev/null; then LAST=""; fi
ROOT="$(git rev-list --max-parents=0 HEAD | tail -1)"
NEWS="$NL$(git -c core.quotepath=false diff --name-only --no-renames "${LAST:-$ROOT}" "$UPSTREAM" -- 2>/dev/null || true)$NL"
is_news() { case "$NEWS" in *"$NL$1$NL"*) return 0 ;; esac; return 1; }

# Every course file the module repo has that is not, here, the version it has
# now: yours differs (M) or is missing (D). Not just the files it changed
# lately -- a copy that fell behind for any reason catches up by itself.
CANDIDATES=()
while IFS= read -r p; do
  [ -n "$p" ] && CANDIDATES+=("$p")
done < <(git -c core.quotepath=false diff --name-only --no-renames --diff-filter=MDT "$UPSTREAM" -- 2>/dev/null | grep -E "$COURSE_RE" || true)

skipped=0
failed=0
touched=()
if [ ${#CANDIDATES[@]} -gt 0 ]; then
  for p in "${CANDIDATES[@]}"; do
    if is_yours "$p"; then
      if is_news "$p"; then
        say "  kept your version: $p"
        skipped=$((skipped + 1))
      fi
      continue
    fi
    if git checkout --quiet "$UPSTREAM" -- "$p" 2>/dev/null; then
      touched+=("$p")
    else
      printf 'could not update %s\n' "$p" >&2
      failed=$((failed + 1))
    fi
  done
fi

# Course-owned pages that upstream has since removed or renamed (a deck folder
# under its new name, a retired MCQ page) — drop our copy too, or the old and
# the new sit side by side. Same rule as above: a file you edited is yours and
# stays, and so is a file you created there, which was never ours to remove.
# Only the lectures, the week pages, mcq/ and module/ are scanned (RETIRE_RE);
# lab folders hold your own code and worksheets, so a retired lab file is
# left in place rather than risk deleting your work.
RETIRED=()
while IFS= read -r p; do
  [ -n "$p" ] && RETIRED+=("$p")
done < <(git -c core.quotepath=false diff --name-only --no-renames --diff-filter=A "$UPSTREAM" -- 2>/dev/null | grep -E "$RETIRE_RE" || true)
if [ ${#RETIRED[@]} -gt 0 ]; then
  for p in "${RETIRED[@]}"; do
    if is_yours "$p"; then
      is_news "$p" && say "  kept your file (not in the module repo any more): $p"
      continue
    fi
    git rm -q -- "$p" 2>/dev/null && touched+=("$p") && say "  removed (retired upstream): $p"
  done
fi

# Commit ONLY the content paths this script rewrote. A bare `git commit`
# would sweep in anything you happened to have staged -- and this runs
# automatically when a Codespace attaches, so work you had run `git add` on
# would land in a commit authored "course-update" and captioned as a
# content sync.
changed=()
if [ ${#touched[@]} -gt 0 ]; then
  # --no-renames: a folder that moved upstream is a delete plus an add here,
  # and rename detection would print only the new name, leaving the old
  # file staged but never committed.
  while IFS= read -r p; do
    [ -n "$p" ] && changed+=("$p")
  done < <(git -c core.quotepath=false diff --cached --name-only --no-renames -- "${touched[@]}")
fi

if [ ${#changed[@]} -eq 0 ]; then
  say "Already up to date."
else
  printf 'Updated:\n'
  printf '  %s\n' "${changed[@]}"
  if git -c user.name="course-update" -c user.email="course-update@local" \
       commit --quiet -m "chore: update course content from the module repo" \
       -- "${changed[@]}"; then
    printf 'Done - your own work was not touched.\n'
  else
    printf 'The update could not be committed; it is staged, not committed.\n' >&2
    failed=$((failed + 1))
  fi
fi

# The baseline the nightly workflow pushes to your repo on GitHub: "the
# module repo as of this run". It is a stand-in commit, not the module repo's
# own: the module repo's files, with YOUR copy's .github/workflows in place
# of the module repo's. The module repo's own commit cannot be pushed. It
# carries the module repo's workflow files, and GitHub refuses a push made
# with the Actions token that adds or changes a workflow file unless the same
# file is already on a branch of your repo -- so from the night after a
# workflow in the module repo was edited, that push failed in every copy made
# before the edit.
#
# The stand-in still holds every course file as the module repo has it,
# because an older copy of this script (scripts/ is never synced, so a copy
# keeps the one it was made with) compares your files against the baseline
# when a Codespace opens. It has no parent, and the same module commit gives
# the same stand-in, so a night with nothing new pushes nothing.
stand_in() {
  local index tree when head
  index="$(git rev-parse --absolute-git-dir)/course-sync.index" || return 1   # a scratch index: yours is not touched
  head="$(git rev-parse HEAD)" || return 1
  rm -f "$index"
  GIT_INDEX_FILE="$index" git read-tree "$UPSTREAM" || return 1
  GIT_INDEX_FILE="$index" git ls-files -z -- .github/workflows \
    | GIT_INDEX_FILE="$index" git update-index -z --force-remove --stdin || return 1
  if git cat-file -e "$head:.github/workflows" 2>/dev/null; then
    GIT_INDEX_FILE="$index" git read-tree --prefix=.github/workflows/ "$head:.github/workflows" || return 1
  fi
  tree="$(GIT_INDEX_FILE="$index" git write-tree)" || return 1
  rm -f "$index"
  when="$(git log -1 --format=%cI "$UPSTREAM")" || return 1
  GIT_AUTHOR_NAME="course-update" GIT_AUTHOR_EMAIL="course-update@local" GIT_AUTHOR_DATE="$when" \
  GIT_COMMITTER_NAME="course-update" GIT_COMMITTER_EMAIL="course-update@local" GIT_COMMITTER_DATE="$when" \
    git commit-tree "$tree" -m "course-sync baseline: module repo at $UPSTREAM"
}

# Bookkeeping only after everything was applied and committed, so a run that
# did not finish is not recorded as one that did.
if [ "$failed" -eq 0 ]; then
  git rev-parse "$UPSTREAM" > "$MARKER"     # local, gitignored, never pushed
  if baseline="$(stand_in)" && [ -n "$baseline" ]; then
    git update-ref refs/course-sync/baseline "$baseline"   # pushed by the nightly workflow
  else
    printf 'could not record the baseline for the nightly run.\n' >&2
    failed=$((failed + 1))
  fi
fi
if [ "$failed" -gt 0 ]; then
  printf '%s problem(s) above; the baseline was not advanced, so the next run will try again.\n' "$failed" >&2
fi
[ "$skipped" -gt 0 ] && printf '(%s file(s) left alone because you had edited them.)\n' "$skipped"
if [ "$failed" -gt 0 ] && [ "$STRICT" = 1 ]; then exit 1; fi
exit 0
