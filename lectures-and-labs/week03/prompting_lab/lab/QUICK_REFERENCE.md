# Prompting Quick Reference

## When to use what

| I need to... | Do this | Tried in |
|--------------|---------|----------|
| Get code that does what I mean | SPEC: make the decisions yourself | [DIY 1](../README.md#diy-1-slugify-on-a-trap) |
| Keep a change small enough to review | Constraints and non-goals | [DIY 2](../README.md#diy-2-count-the-lines-it-changed) |
| Find the decisions I have not made yet | Ask for its questions before its code | [DIY 3](../README.md#diy-3-make-it-ask-first) |
| Change what a review looks at | A persona (tone and attention, not knowledge) | [DIY 4](../README.md#diy-4-test-the-persona) |
| See the reasoning, to check it | Ask for the steps (it reasons anyway) | [DIY 5](../README.md#diy-5-does-step-by-step-still-help) |
| Pin an exact output format | Show examples, then parse the output | [DIY 6](../README.md#diy-6-show-the-format) |
| Say what "done" means | Tests first | [DIY 7](../README.md#diy-7-tests-first) |
| Fix an error | Show it the error AND the code | [DIY 8](../README.md#diy-8-the-error-without-the-code) |
| Stop repeating myself | An instructions file | [DIY 9](../README.md#diy-9-context-you-write-once) |

## SPEC template (copy and fill in)

**S**pecific goal: [one sentence: what exactly do you want?]

**P**rogramming language and place: [Python 3.12, which file, the signature]

**E**xamples:
- [a normal input] → [the output you want]
- [the awkward input] → [what should happen: an output, or an error]

**C**onstraints:
- [e.g. no external libraries]
- [e.g. raise ValueError on bad input]

**Non-goals** (what it must not touch):
- [e.g. change nothing else in the file]
- [e.g. no formatting, no type hints, no new comments]

## Before you reword a prompt, ask

- **Is this a wording problem or a knowledge problem?** If it cannot see
  the file, the error or the test, no rewording will help: put it in the
  window.
- **Is the window too full?** A long thread of failed attempts is context
  too. Start a fresh conversation and carry only what matters.

## Red flags

- It "fixed" an error it never saw the code for, with a default value
- It changed lines you did not ask about (read `git diff` before you keep anything)
- It added a dependency you did not ask for
- Several models agree, so it must be right (they can all make the same unmade decision)

## Chat shortcuts in a Codespace

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Chat panel | `Ctrl+Alt+I` | `Ctrl+Cmd+I` |
| Inline chat | `Ctrl+I` | `Cmd+I` |
| Accept a completion | `Tab` | `Tab` |
| Reject a completion | `Esc` | `Esc` |
