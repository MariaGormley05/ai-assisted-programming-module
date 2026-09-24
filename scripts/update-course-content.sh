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
# below): the lectures, the guide and the week explainers under
# lectures-and-labs/, and everything under mcq/ and module/. Never a lab
# folder: those hold your own code.
RETIRE_RE='^(lectures-and-labs/(README\.md|[^/]+/([^/]+-lecture\.md|README\.md))|mcq/.*|module/.*)$'
PATHS=()
while IFS= read -r p; do
  [ -n "$p" ] && PATHS+=("$p")
done < <(git ls-tree -r --name-only "upstream/$BRANCH" | grep -E "$COURSE_RE" || true)

# Baseline = the content as you last received it: the commit recorded by the
# previous run, or the initial template commit on the first run. Comparing
# against HEAD would be wrong -- you are told to COMMIT your work, so an
# edit you committed looks "clean" against HEAD and would be overwritten.
#
# The baseline is remembered twice: in the gitignored file .course-sync (a
# Codespace or your laptop) and in the ref refs/course-sync/baseline, which
# the nightly course-sync workflow pushes to your repo on GitHub. The ref is
# fetched here so a Codespace opened after a nightly run knows what that run
# already delivered; otherwise last night's updates would look like your
# own edits and never refresh again. Of the two, the NEWER wins (the one the
# other is an ancestor of); if they are unrelated, the ref -- it was set by
# the run that actually delivered files to your repo.
MARKER=".course-sync"
git fetch --quiet origin '+refs/course-sync/baseline:refs/course-sync/baseline' 2>/dev/null || true
FILE_BASE="$(cat "$MARKER" 2>/dev/null || true)"
REF_BASE="$(git rev-parse -q --verify refs/course-sync/baseline 2>/dev/null || true)"
LAST="$FILE_BASE"
if [ -n "$REF_BASE" ]; then
  if [ -z "$FILE_BASE" ] || ! git merge-base --is-ancestor "$REF_BASE" "$FILE_BASE" 2>/dev/null; then
    LAST="$REF_BASE"    # the ref, unless the file is strictly newer than it
  fi
fi
# A remembered baseline that is no longer a commit the module repo has (a
# rewritten history, a hand-edited marker) would make every diff below fail
# quietly and nothing would update: start over from the template instead.
if [ -n "$LAST" ] && ! git cat-file -e "$LAST^{commit}" 2>/dev/null; then
  say "The remembered baseline is no longer in the module repo's history; comparing against the template's first commit instead."
  LAST=""
fi
ROOT="$(git rev-list --max-parents=0 HEAD | tail -1)"
UPSTREAM="$(git rev-parse "upstream/$BRANCH")"

# Only the files the module repo has changed since the baseline need a look;
# every other course file is either exactly what you received, or yours.
CANDIDATES=()
while IFS= read -r p; do
  [ -n "$p" ] && CANDIDATES+=("$p")
done < <(git diff --name-only --no-renames "${LAST:-$ROOT}" "$UPSTREAM" -- 2>/dev/null | grep -E "$COURSE_RE" || true)

# Is this path yours? It is NOT yours only if you received it from the module
# repo and have not touched it since -- in the working tree or in the index.
# Edited, staged, deleted, or created by you: yours, and left alone.
is_yours() {
  local p="$1" base="$ROOT"
  if [ -n "$LAST" ] && git cat-file -e "$LAST:$p" 2>/dev/null; then base="$LAST"; fi
  if git cat-file -e "$base:$p" 2>/dev/null; then
    if git diff --quiet "$base" -- "$p" 2>/dev/null \
       && git diff --quiet --cached "$base" -- "$p" 2>/dev/null; then
      return 1
    fi
    return 0    # edited, staged or deleted since you received it
  fi
  [ -e "$p" ]   # never received; if something is there, you created it
}

skipped=0
failed=0
touched=()
for p in "${CANDIDATES[@]}"; do
  if is_yours "$p"; then
    say "  kept your version: $p"
    skipped=$((skipped + 1))
    continue
  fi
  # A path the module repo has removed is handled by the pass below.
  git cat-file -e "$UPSTREAM:$p" 2>/dev/null || continue
  if git checkout --quiet "$UPSTREAM" -- "$p" 2>/dev/null; then
    touched+=("$p")
  else
    printf 'could not update %s\n' "$p" >&2
    failed=$((failed + 1))
  fi
done

# Course-owned pages that upstream has since removed or renamed (a deck folder
# under its new name, a retired MCQ page) — drop our copy too, or the old and
# the new sit side by side. Same rule as above: a file you edited is yours and
# stays, and so is a file you created there, which was never ours to remove.
# Only the lectures, the week pages, mcq/ and module/ are scanned (RETIRE_RE);
# lab folders hold your own code and worksheets, so a retired lab file is
# left in place rather than risk deleting your work.
while IFS= read -r p; do
  [ -n "$p" ] || continue
  case " ${PATHS[*]} " in *" $p "*) continue;; esac
  if is_yours "$p"; then
    say "  kept your file (not in the module repo any more, or never from it): $p"
    continue
  fi
  git rm -q -- "$p" 2>/dev/null && touched+=("$p") && say "  removed (retired upstream): $p"
done < <(git ls-files -- lectures-and-labs mcq module | grep -E "$RETIRE_RE")

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
  done < <(git diff --cached --name-only --no-renames -- "${touched[@]}")
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

# Bookkeeping only after everything was applied and committed: advancing
# the baseline past an update that did not land would make that update look
# like your own edit next time, and it would never be retried.
if [ "$failed" -eq 0 ]; then
  git rev-parse "$UPSTREAM" > "$MARKER"     # local, gitignored, never pushed
  git update-ref refs/course-sync/baseline "$UPSTREAM"   # pushed by the nightly workflow
else
  printf '%s problem(s) above; the baseline was not advanced, so the next run will try again.\n' "$failed" >&2
fi
[ "$skipped" -gt 0 ] && printf '(%s file(s) left alone because you had edited them.)\n' "$skipped"
if [ "$failed" -gt 0 ] && [ "$STRICT" = 1 ]; then exit 1; fi
exit 0
