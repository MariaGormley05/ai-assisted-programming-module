#!/usr/bin/env bash
# Tests for scripts/update-course-content.sh, the sync that runs in every
# student's copy: each time a Codespace opens, and nightly in the course-sync
# workflow.
#
#   bash scripts/test-course-sync.sh               every test
#   bash scripts/test-course-sync.sh kept stale    only tests whose name has one of these words
#   KEEP=1 bash scripts/test-course-sync.sh ...    leave the scratch repos behind to look at
#
# Nothing here touches GitHub or this repository. Each test builds, in a
# temporary folder, a small module repo, a student's "GitHub" repo made from
# it the way "Use this template" makes one (a single new root commit) and a
# clone of that; it then does what a Codespace or the nightly workflow does,
# and checks whose files changed.
#
# GitHub's rule for the nightly push is modelled, not called: a push made
# with the Actions token is refused if it adds or changes a file under
# .github/workflows/, unless the same file with the same content is already
# on a branch of that repository. (It is the rule that stopped every copy's
# nightly run the day after a workflow in the module repo was edited.)
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="${SCRIPT:-$HERE/update-course-content.sh}"

# The script as it is frozen in copies that already exist. A copy never
# receives a newer scripts/ folder, so its Codespace runs one of these for
# good, against whatever the nightly run (always the current script) left in
# the student's repo. Read from this repo's history; the tests that need them
# are skipped in a clone without it.
FROZEN_REVS="f25852f35f08388730999884ffef16a4d58f9a4a
78513c78a5d59912a6e9637292532a017c864780
841359d7f3a0a980865eb0acbcee316f367bb15c"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/sync-test.XXXXXX")" || exit 1
[ -n "${KEEP:-}" ] || trap 'rm -rf "$WORK"' EXIT
NL='
'
CASES=0

# The same git everywhere: nobody's own configuration decides a result.
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL="$WORK/gitconfig"
git config --global user.name "A Student"
git config --global user.email "student@example.invalid"
git config --global init.defaultBranch main
git config --global core.autocrlf false
git config --global core.longpaths true        # Windows: a temporary folder can be deep
git config --global commit.gpgsign false
git config --global advice.detachedHead false
git config --global --add safe.directory '*'   # a container or WSL may run this as another user

# ---------------------------------------------------------------- the world

put() { mkdir -p "$(dirname "$1/$2")" && printf '%s\n' "$3" > "$1/$2"; }   # put <dir> <path> <text>

# A module repo with one of everything the sync cares about, and nothing yet
# copied from it.
new_case() {
  # Short folder names: Windows cannot make a deep folder the current one.
  CASES=$((CASES + 1)); C="$WORK/$CASES"
  UP="$C/m.git"                    # the module repo on GitHub
  MOD="$C/m"                       # where the lecturer edits it
  ORIGIN="$C/github.com/s.git"     # the student's repo on GitHub
  COPY="$C/cs"                     # the student's Codespace
  OUT=""; RC=""; PUSH=""
  mkdir -p "$C/github.com" && echo "$1" > "$C/test-name"
  git init -q --bare "$UP"
  git init -q "$MOD"
  git -C "$MOD" remote add origin "$UP"
  put "$MOD" .gitignore ".course-sync"
  put "$MOD" README.md "module readme, version 1"
  put "$MOD" AGENTS.md "brief, version 1"
  put "$MOD" lectures-and-labs/README.md "guide, version 1"
  put "$MOD" lectures-and-labs/week01/intro-lecture.md "lecture, version 1"
  put "$MOD" lectures-and-labs/week02/demo_lab/README.md "lab instructions, version 1"
  put "$MOD" lectures-and-labs/week02/demo_lab/starter.py "print('starter, version 1')"
  : > "$MOD/lectures-and-labs/week02/demo_lab/__init__.py"
  put "$MOD" module/schedule.json '{"weeks": 1}'
  put "$MOD" .github/workflows/site.yml "name: site   # version 1"
  put "$MOD" .github/workflows/course-sync.yml "name: course-sync"
  put "$MOD" scripts/build.py "print('not a course file, version 1')"
  module_commit "the module repo on the day of the copy"
}

module_commit() { git -C "$MOD" add -A && git -C "$MOD" commit -q -m "$1" && git -C "$MOD" push -q origin HEAD:main; }
module_edit()   { put "$MOD" "$1" "$2"; module_commit "module: $1"; }                   # one file, one commit
module_remove() { git -C "$MOD" rm -q -- "$1" && module_commit "module: remove $1"; }

# "Use this template": the student's repo is one new root commit holding the
# template's files, and shares no history with the module repo.
make_copy() {
  local root
  root="$(git -C "$MOD" commit-tree "HEAD^{tree}" -m "Initial commit")"
  git init -q --bare "$ORIGIN"
  git -C "$MOD" push -q "$ORIGIN" "$root:refs/heads/main"
  git clone -q "$ORIGIN" "$COPY"
  git -C "$COPY" remote add upstream "$UP"
}

student_edit()   { put "$COPY" "$1" "$2"; }                # in the Codespace, not committed
student_commit() { git -C "$COPY" add -A && git -C "$COPY" commit -q -m "my lab work" && git -C "$COPY" push -q origin HEAD:main; }

# Opening the Codespace (its postAttachCommand): fast-forward to whatever the
# nightly run pushed, then the script. Arguments are passed to the script.
codespace() {
  local script="${CODESPACE_SCRIPT:-$SCRIPT}"
  (
    cd "$COPY" || exit 99
    git pull -q --ff-only origin main 2>/dev/null
    bash "$script" "$@"
  ) > "$C/out" 2>&1
  RC=$?; OUT="$(cat "$C/out")"
}

# GitHub's rule for a push made with the Actions token (see the top of this file).
github_accepts() {   # $1 = clone, $2 = the ref being pushed
  local theirs mine line
  theirs="$(git -C "$1" ls-tree -r "$(git -C "$1" rev-parse refs/remotes/origin/main)" -- .github/workflows)"
  mine="$(git -C "$1" ls-tree -r "$(git -C "$1" rev-parse "$2")" -- .github/workflows)"
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    case "$NL$theirs$NL" in *"$NL$line$NL"*) ;; *) return 1 ;; esac
  done <<EOF
$mine
EOF
  return 0
}

# The course-sync workflow, step for step: a fresh checkout with full
# history, the baseline ref from the last run, the script with --strict, then
# the two pushes. PUSH says what became of the baseline push.
nightly() {
  local job="$C/job" ref=refs/course-sync/baseline
  rm -rf "$job"; git clone -q "$ORIGIN" "$job" || return 1
  PUSH="not attempted"
  (
    cd "$job" || exit 99
    git fetch -q origin "+$ref:$ref" 2>/dev/null
    git remote add upstream "$UP" && git fetch -q upstream main || exit 98
    bash "$SCRIPT" --strict
  ) > "$C/out" 2>&1
  RC=$?; OUT="$(cat "$C/out")"
  [ "$RC" = 0 ] || return 0                 # a failed step stops the job
  if [ "$(git -C "$job" rev-parse HEAD)" != "$(git -C "$job" rev-parse refs/remotes/origin/main)" ]; then
    git -C "$job" push -q origin HEAD:main
  fi
  if ! git -C "$job" rev-parse -q --verify "$ref" >/dev/null; then
    PUSH="no ref to push"
  elif [ "$(git -C "$job" rev-parse "$ref")" = "$(git -C "$ORIGIN" rev-parse -q --verify "$ref")" ] \
       || github_accepts "$job" "$ref"; then
    git -C "$job" push -q --force origin "$ref:$ref" && PUSH=accepted
  else
    PUSH=rejected
  fi
}

# A delivery from the days the baseline push was being refused: the module's
# current version of a file lands in the student's repo as a sync commit,
# and the baseline stays where it was.
delivery_with_the_baseline_stuck() {
  git -C "$COPY" pull -q --ff-only origin main
  mkdir -p "$(dirname "$COPY/$1")" && cp "$MOD/$1" "$COPY/$1"
  git -C "$COPY" add -- "$1"
  git -C "$COPY" -c user.name=course-update -c user.email=course-update@local \
    commit -q -m "chore: update course content from the module repo" -- "$1"
  git -C "$COPY" push -q origin HEAD:main
}

frozen_script() {   # $1 = commit -> the path of that commit's script; fails without the history
  local f="$WORK/frozen-$1.sh"
  [ -s "$f" ] && { printf '%s\n' "$f"; return 0; }
  git -C "$HERE/.." show "$1:scripts/update-course-content.sh" > "$f" 2>/dev/null || { rm -f "$f"; return 1; }
  printf '%s\n' "$f"
}

# ------------------------------------------------------------------ checking

# A commit is resolved to its id before a path is appended: Git Bash rewrites
# an argument shaped like a/b:.c/d as a Windows path list.
blob()       { local c; c="$(git -C "$1" rev-parse -q --verify "$2^{commit}")" || return 0; git -C "$1" rev-parse -q --verify "$c:$3" 2>/dev/null || true; }
on_github()  { blob "$ORIGIN" main "$1"; }      # what the student's repo holds at a path; empty if nothing
in_module()  { blob "$MOD" HEAD "$1"; }         # what the module repo holds there now
is_current() { [ -n "$(in_module "$1")" ] && [ "$(on_github "$1")" = "$(in_module "$1")" ]; }
is_absent()  { [ -z "$(on_github "$1")" ]; }
reads()      { [ "$(cat "$1" 2>/dev/null)" = "$2" ]; }          # reads <file> <text>
says()       { case "$OUT" in *"$1"*) return 0 ;; esac; return 1; }
not()        { ! "$@"; }

expect() {   # expect "<what should be true>" <command...>
  local what="$1"; shift
  "$@" && return 0
  FAILED=1; printf '       expected %s\n' "$what"
  return 0
}
skip() { SKIPPED=1; printf '       skipped: %s\n' "$1"; }

LAB=lectures-and-labs/week02/demo_lab
LECTURE=lectures-and-labs/week01/intro-lecture.md
WORKFLOW=.github/workflows/site.yml

# -------------------------------------------------- what the module repo owns

test_an_untouched_file_is_updated() {
  make_copy
  module_edit "$LAB/README.md" "lab instructions, version 2"
  nightly
  expect "the script to succeed" [ "$RC" = 0 ]
  expect "the lab instructions to be the module's current ones" is_current "$LAB/README.md"
  expect "the sync commit to be authored course-update" \
    [ "$(git -C "$ORIGIN" log -1 --format=%an main)" = course-update ]
}

test_a_new_module_file_arrives() {
  make_copy
  module_edit lectures-and-labs/week03/next-lecture.md "a lecture added after the copy was made"
  nightly
  expect "the new lecture to be in the copy" is_current lectures-and-labs/week03/next-lecture.md
}

test_only_course_files_are_touched() {
  make_copy
  local script_before workflow_before
  script_before="$(on_github scripts/build.py)"; workflow_before="$(on_github "$WORKFLOW")"
  module_edit scripts/build.py "print('not a course file, version 2')"
  module_edit "$WORKFLOW" "name: site   # version 2"
  nightly
  expect "the copy's build script to be as it was" [ "$(on_github scripts/build.py)" = "$script_before" ]
  expect "the copy's workflow to be as it was" [ "$(on_github "$WORKFLOW")" = "$workflow_before" ]
}

test_a_file_with_a_non_ascii_name_is_updated() {
  local page="lectures-and-labs/week01/café-lecture.md"
  put "$MOD" "$page" "lecture, version 1"; module_commit "module: a page with an accent in its name"
  make_copy
  module_edit "$page" "lecture, version 2"
  nightly
  expect "the script to succeed" [ "$RC" = 0 ]
  expect "the page to be the module's current one" is_current "$page"
}

test_a_name_with_brackets_touches_that_file_only() {
  # To git, data[1].txt is also a pattern that matches data1.txt.
  put "$MOD" "$LAB/data[1].txt" "data, version 1"
  put "$MOD" "$LAB/data1.txt" "other data, version 1"
  module_commit "module: two data files"
  make_copy
  student_edit "$LAB/data1.txt" "my own data"
  student_commit
  local mine; mine="$(on_github "$LAB/data1.txt")"
  module_edit "$LAB/data[1].txt" "data, version 2"
  nightly
  expect "the file the module changed to be current" is_current "$LAB/data[1].txt"
  expect "the student's file beside it to be untouched" [ "$(on_github "$LAB/data1.txt")" = "$mine" ]
}

test_a_page_the_module_retired_is_removed() {
  make_copy
  module_remove "$LECTURE"
  nightly
  expect "the retired lecture to be gone from the copy" is_absent "$LECTURE"
}

test_a_page_retired_and_later_restored_comes_back() {
  make_copy
  module_remove "$LECTURE"
  nightly
  module_edit "$LECTURE" "lecture, restored"
  nightly
  expect "the restored lecture to be in the copy" is_current "$LECTURE"
}

test_a_retired_lab_file_is_left_where_it_is() {
  make_copy
  local before; before="$(on_github "$LAB/starter.py")"
  module_remove "$LAB/starter.py"
  nightly
  expect "the lab file to still be in the copy (a lab folder is never pruned)" \
    [ "$(on_github "$LAB/starter.py")" = "$before" ]
}

# ----------------------------------------------------- what the student owns

test_a_file_you_changed_and_committed_is_kept() {
  make_copy
  student_edit "$LAB/starter.py" "print('my lab work')"
  student_commit
  local mine; mine="$(on_github "$LAB/starter.py")"
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  nightly
  expect "the starter file to still be the student's" [ "$(on_github "$LAB/starter.py")" = "$mine" ]
  expect "the script to say it kept it" says "kept your version: $LAB/starter.py"
  expect "the closing count of files left alone" says "(1 file(s) left alone because you had edited them.)"
}

test_an_edit_you_have_not_committed_is_kept() {
  make_copy
  student_edit "$LAB/starter.py" "print('work in progress')"
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  codespace
  expect "the unsaved-to-git edit to survive" reads "$COPY/$LAB/starter.py" "print('work in progress')"
}

test_an_edit_you_have_only_staged_is_kept() {
  make_copy
  student_edit "$LAB/starter.py" "print('staged work')"
  git -C "$COPY" add -- "$LAB/starter.py"
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  codespace
  expect "the staged edit to survive" reads "$COPY/$LAB/starter.py" "print('staged work')"
  expect "it to still be staged" [ -n "$(git -C "$COPY" diff --cached --name-only)" ]
}

test_your_staged_work_is_not_swept_into_the_sync_commit() {
  make_copy
  student_edit "$LAB/mine.py" "print('a file of my own')"
  git -C "$COPY" add -- "$LAB/mine.py"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  codespace
  expect "the sync commit to hold the lab instructions only" \
    [ "$(git -C "$COPY" show --format= --name-only HEAD)" = "$LAB/README.md" ]
  expect "the student's file to still be staged, not committed" \
    [ "$(git -C "$COPY" diff --cached --name-only)" = "$LAB/mine.py" ]
}

test_a_file_you_created_where_the_module_later_adds_one_is_kept() {
  make_copy
  student_edit "$LAB/notes.md" "my own notes"
  module_edit "$LAB/notes.md" "notes the module added later"
  codespace
  expect "the student's file to survive" reads "$COPY/$LAB/notes.md" "my own notes"
}

test_a_page_you_created_is_never_removed() {
  make_copy
  student_edit lectures-and-labs/week05/README.md "a page of my own"
  student_commit
  local mine; mine="$(on_github lectures-and-labs/week05/README.md)"
  module_edit README.md "module readme, version 2"
  nightly
  expect "the student's page to still be there" [ "$(on_github lectures-and-labs/week05/README.md)" = "$mine" ]
}

test_a_file_you_deleted_stays_deleted() {
  make_copy
  git -C "$COPY" rm -q -- "$LECTURE"
  student_commit
  nightly
  expect "it to stay deleted while the module leaves it alone" is_absent "$LECTURE"
  module_edit "$LECTURE" "lecture, version 2"
  nightly
  expect "it to stay deleted when the module changes it" is_absent "$LECTURE"
}

test_a_retired_page_you_edited_is_kept() {
  make_copy
  student_edit "$LECTURE" "my annotated copy of the lecture"
  student_commit
  local mine; mine="$(on_github "$LECTURE")"
  module_remove "$LECTURE"
  nightly
  expect "the student's annotated lecture to survive" [ "$(on_github "$LECTURE")" = "$mine" ]
}

test_a_file_you_emptied_is_kept() {
  # The module repo has an empty file too (__init__.py). Emptying the starter
  # is still the student's edit: what counts is what the module published at
  # THAT path.
  make_copy
  : > "$COPY/$LAB/starter.py"
  student_commit
  local mine; mine="$(on_github "$LAB/starter.py")"
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  nightly
  expect "the emptied starter file to still be the student's" [ "$(on_github "$LAB/starter.py")" = "$mine" ]
}

mode_on_github() { git -C "$ORIGIN" ls-tree main -- "$1" | cut -c1-6; }

test_a_file_you_only_made_executable_is_kept() {
  # chmod +x is an edit too. The module repo published that content, but
  # never as an executable file, and taking the file back would undo the
  # student's chmod every night.
  make_copy
  local mine; mine="$(on_github "$LAB/starter.py")"
  git -C "$COPY" update-index --chmod=+x -- "$LAB/starter.py"
  git -C "$COPY" commit -q -m "make the starter runnable" && git -C "$COPY" push -q origin HEAD:main
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  nightly
  expect "the starter file to still be executable" [ "$(mode_on_github "$LAB/starter.py")" = 100755 ]
  expect "its content to be as the student left it" [ "$(on_github "$LAB/starter.py")" = "$mine" ]
}

test_a_file_the_module_made_executable_follows() {
  make_copy
  # Windows has no executable bit, so there git cannot commit a change of
  # mode from the working tree. The nightly run and a Codespace are Linux.
  if [ "$(git -C "$COPY" config --get core.filemode)" = false ]; then
    skip "this filesystem does not record the executable bit"; return
  fi
  git -C "$MOD" update-index --chmod=+x -- "$LAB/starter.py"
  git -C "$MOD" commit -q -m "module: the starter is executable" && git -C "$MOD" push -q origin HEAD:main
  nightly
  expect "the untouched starter file to be executable in the copy too" \
    [ "$(mode_on_github "$LAB/starter.py")" = 100755 ]
}

# ------------------------------------- the failure of September-October 2026

test_the_baseline_push_survives_a_workflow_edit() {
  make_copy
  nightly
  expect "the first night's baseline push to be accepted" [ "$PUSH" = accepted ]
  module_edit "$WORKFLOW" "name: site   # version 2"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  nightly
  expect "the script to succeed" [ "$RC" = 0 ]
  expect "the baseline push to be accepted after the module edits a workflow" [ "$PUSH" = accepted ]
}

test_a_file_updated_while_the_baseline_was_stuck_is_refreshed() {
  # The state every older copy was left in: the baseline is the module commit
  # from before a workflow edit, and a file has been delivered once since.
  make_copy
  git -C "$MOD" push -q "$ORIGIN" HEAD:refs/course-sync/baseline
  module_edit "$WORKFLOW" "name: site   # version 2"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  delivery_with_the_baseline_stuck "$LAB/README.md"
  module_edit "$LAB/README.md" "lab instructions, version 3"
  nightly
  expect "the lab instructions to be the module's current ones" is_current "$LAB/README.md"
  expect "nothing to be reported as the student's" not says "kept your"
  expect "the baseline push to be accepted" [ "$PUSH" = accepted ]
}

test_a_file_a_codespace_updated_during_the_day_is_refreshed_that_night() {
  make_copy
  nightly
  module_edit "$LAB/README.md" "lab instructions, version 2"       # a fix during the lab
  codespace                                                        # the student gets it
  git -C "$COPY" push -q origin HEAD:main
  module_edit "$LAB/README.md" "lab instructions, version 3"       # a second fix, later that day
  nightly
  expect "the lab instructions to be the module's current ones" is_current "$LAB/README.md"
}

test_a_page_left_behind_while_the_baseline_was_stuck_is_removed() {
  # A page delivered once while the baseline was stuck, then retired by the
  # module repo (the exported lecture PDFs of October 2026).
  make_copy
  git -C "$MOD" push -q "$ORIGIN" HEAD:refs/course-sync/baseline
  module_edit lectures-and-labs/week01/intro-lecture.pdf "an exported copy of the lecture"
  delivery_with_the_baseline_stuck lectures-and-labs/week01/intro-lecture.pdf
  module_remove lectures-and-labs/week01/intro-lecture.pdf
  nightly
  expect "the retired export to be gone from the copy" is_absent lectures-and-labs/week01/intro-lecture.pdf
}

# ------------------------------------------------------------ the bookkeeping

test_a_second_run_changes_nothing() {
  make_copy
  module_edit "$WORKFLOW" "name: site   # version 2"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  nightly
  local head baseline
  head="$(git -C "$ORIGIN" rev-parse main)"
  baseline="$(git -C "$ORIGIN" rev-parse -q --verify refs/course-sync/baseline)"
  nightly
  expect "no new commit in the copy" [ "$(git -C "$ORIGIN" rev-parse main)" = "$head" ]
  expect "the script to say so" says "Already up to date."
  expect "the baseline to be the same commit as the night before" \
    [ "$(git -C "$ORIGIN" rev-parse -q --verify refs/course-sync/baseline)" = "$baseline" ]
  expect "the baseline push to be accepted" [ "$PUSH" = accepted ]
}

test_the_baseline_holds_the_module_files_and_your_workflows() {
  # What an older script in a Codespace needs from the baseline (it compares
  # course files against it), and what GitHub needs (no workflow of the
  # module repo's in it).
  make_copy
  module_edit "$WORKFLOW" "name: site   # version 2"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  nightly
  local ref=refs/course-sync/baseline
  expect "a baseline in the student's repo" [ -n "$(git -C "$ORIGIN" rev-parse -q --verify "$ref")" ]
  expect "its lab instructions to be the module's current ones" \
    [ "$(blob "$ORIGIN" "$ref" "$LAB/README.md")" = "$(in_module "$LAB/README.md")" ]
  expect "its starter file to be the module's current one" \
    [ "$(blob "$ORIGIN" "$ref" "$LAB/starter.py")" = "$(in_module "$LAB/starter.py")" ]
  expect "its workflow to be the copy's own" \
    [ "$(blob "$ORIGIN" "$ref" "$WORKFLOW")" = "$(on_github "$WORKFLOW")" ]
}

test_a_kept_file_is_mentioned_when_the_module_changes_it_and_not_again() {
  make_copy
  student_edit "$LAB/starter.py" "print('my lab work')"
  student_commit
  nightly
  expect "silence about the student's file while the module leaves it alone" not says "$LAB/starter.py"
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  nightly
  expect "the file to be mentioned the night the module changes it" says "kept your version: $LAB/starter.py"
  nightly
  expect "silence about it the night after" not says "$LAB/starter.py"
  expect "no count of files left alone the night after" not says "left alone"
}

test_a_quiet_run_with_nothing_to_do_says_nothing() {
  make_copy
  student_edit "$LAB/starter.py" "print('my lab work')"
  student_commit
  codespace --quiet
  expect "no output at all" [ -z "$OUT" ]
  expect "success" [ "$RC" = 0 ]
}

test_the_module_repo_itself_is_left_alone() {
  # The same script sits in the module repo; there it must do nothing.
  make_copy
  local own="$C/github.com/danielcregg/ai-assisted-programming.git"
  mkdir -p "$(dirname "$own")" && git clone -q --bare "$ORIGIN" "$own"
  git -C "$COPY" remote set-url origin "$own"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  local before; before="$(git -C "$COPY" rev-parse HEAD)"
  codespace
  expect "no commit" [ "$(git -C "$COPY" rev-parse HEAD)" = "$before" ]
  expect "the script to say why" says "This IS the module repo"
}

# ---------------------------- copies that already exist, and their old script

# One nightly run by the current script, then a Codespace opened with an
# older one. $1 = the older script, $2 = "opened before" to give the
# Codespace a marker from an earlier day.
an_older_codespace_after_a_nightly_run() {
  make_copy
  [ "${2:-}" = "opened before" ] && { CODESPACE_SCRIPT="$1" codespace --quiet; }
  student_edit "$LAB/starter.py" "print('my lab work')"
  student_commit
  module_edit "$WORKFLOW" "name: site   # version 2"
  module_edit "$LAB/README.md" "lab instructions, version 2"
  nightly                                                    # the current script
  module_edit "$LAB/README.md" "lab instructions, version 3"   # the next day's fixes
  module_edit "$LAB/starter.py" "print('starter, version 2')"
  module_edit "$LECTURE" "lecture, version 2"
  student_edit "$LECTURE" "my own notes on the lecture"      # not committed
  CODESPACE_SCRIPT="$1" codespace --quiet
}

test_an_older_script_in_a_new_codespace_keeps_your_work_and_takes_fixes() {
  local rev old
  for rev in $FROZEN_REVS; do
    old="$(frozen_script "$rev")" || { skip "needs this repository's history"; return; }
    new_case "older-new-${rev:0:7}"
    an_older_codespace_after_a_nightly_run "$old"
    expect "${rev:0:7}: the committed lab work to survive" reads "$COPY/$LAB/starter.py" "print('my lab work')"
    expect "${rev:0:7}: the uncommitted notes to survive" reads "$COPY/$LECTURE" "my own notes on the lecture"
    expect "${rev:0:7}: the day's fix to the lab instructions to arrive" \
      reads "$COPY/$LAB/README.md" "lab instructions, version 3"
  done
}

test_an_older_script_in_a_codespace_opened_before_keeps_your_work() {
  local rev old
  for rev in $FROZEN_REVS; do
    old="$(frozen_script "$rev")" || { skip "needs this repository's history"; return; }
    new_case "older-used-${rev:0:7}"
    an_older_codespace_after_a_nightly_run "$old" "opened before"
    expect "${rev:0:7}: the committed lab work to survive" reads "$COPY/$LAB/starter.py" "print('my lab work')"
    expect "${rev:0:7}: the uncommitted notes to survive" reads "$COPY/$LECTURE" "my own notes on the lecture"
  done
}

# ------------------------------------------------------------------- running

PASS=0; FAIL=0; SKIP=0
for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  if [ $# -gt 0 ]; then
    wanted=""; for word in "$@"; do case "$t" in *"$word"*) wanted=1 ;; esac; done
    [ -n "$wanted" ] || continue
  fi
  FAILED=0; SKIPPED=0
  new_case "$t"
  "$t"
  if [ "$FAILED" != 0 ]; then FAIL=$((FAIL + 1)); printf 'FAIL   %s\n' "$t"
  elif [ "$SKIPPED" != 0 ]; then SKIP=$((SKIP + 1)); printf 'skip   %s\n' "$t"
  else PASS=$((PASS + 1)); printf 'ok     %s\n' "$t"; fi
done
printf '\n%s passed, %s failed, %s skipped   (%s)\n' "$PASS" "$FAIL" "$SKIP" "$SCRIPT"
[ -n "${KEEP:-}" ] && printf 'scratch repos kept in %s\n' "$WORK"
[ "$FAIL" -eq 0 ]
