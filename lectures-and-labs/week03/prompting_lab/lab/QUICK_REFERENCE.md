# Prompting Patterns Quick Reference

## When to Use What

| I need to... | Use this pattern | Jump to |
|--------------|------------------|---------|
| Get specific working code | SPEC framework | [DIY 1](../README.md#diy-1-make-the-same-request-twice), [DIY 2](../README.md#diy-2-spec-on-something-with-a-real-trap) |
| Prevent AI from adding extra features | Constraints + Non-Goals | [DIY 3](../README.md#diy-3-stop-it-helping) |
| Understand requirements before coding | Clarifying Questions | [DIY 4](../README.md#diy-4-ask-for-questions-first) |
| Get expert-level feedback | Persona prompting | [DIY 5](../README.md#diy-5-persona) |
| Debug complex logic | Chain-of-Thought | [DIY 6](../README.md#diy-6-chain-of-thought-on-a-real-bug) |
| Control exact output format | Few-Shot examples | [DIY 7](../README.md#diy-7-few-shot-for-exact-format) |
| Avoid over-engineering | Tests-First | [DIY 8](../README.md#diy-8-tests-first) |
| Make surgical code changes | Patch/Diff request | [DIY 9](../README.md#diy-9-ask-for-a-patch-not-a-file) |

---

## SPEC Template (Copy & Modify)

**Task**: [One sentence: what exactly do you want?]

**Programming**:
- Language: [Python 3.11, JavaScript, etc.]
- Location: [file path or new file name]
- Signature: [function/class name and types]

**Examples**:
- Input: [concrete example] → Output: [expected result]
- Input: [edge case] → Output: [expected behavior]

**Constraints**:
- [Limit 1: e.g., "No external libraries"]
- [Limit 2: e.g., "Must handle empty input gracefully"]
- [Limit 3: e.g., "Max 20 lines of code"]

**Non-Goals (Don't do these)**:
- [Thing 1: e.g., "Don't add database caching"]
- [Thing 2: e.g., "Don't refactor existing code"]

**Return**: [Only the code | Only a diff | Code + 3 tests | etc.]

---

## My Top Prompts This Week

**Keep your winners here for reuse:**

### 1. [Prompt name]
[Paste your best prompt here]

**Why it worked**: [Note to self]

### 2. [Prompt name]
[Paste your best prompt here]

**Why it worked**: [Note to self]

### 3. [Prompt name]
[Paste your best prompt here]

**Why it worked**: [Note to self]

---

## Common Copilot Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Accept suggestion | `Tab` | `Tab` |
| Reject suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Option+]` |
| Previous suggestion | `Alt+[` | `Option+[` |
| Open Chat | `Ctrl+Alt+I` | `Ctrl+Cmd+I` |
| Inline Chat | `Ctrl+I` | `Cmd+I` |

---

## Red Flags (AI Mistakes to Watch For)

- ❌ AI invents functions that don't exist (`urlparse.get_domain()`)
- ❌ AI adds dependencies you didn't ask for (`import beautifulsoup4`)
- ❌ AI writes 100 lines when 10 would work
- ❌ AI ignores your constraints (you said "no loops", it uses loops)
- ❌ AI formats output with extra commentary when you said "code only"

**Defense**: Always test the code. Re-prompt with stronger constraints if needed.

---

## Commit Message Templates

- `Complete Task 1: Rewrite vague prompt using SPEC`
- `Complete Task 8: Implement extract_domain with tests`
- `Fix Task 8: Handle localhost ValueError`
- `Complete Task 9: Apply docstring patch via diff`
- `Complete Task 10: Add reflection on prompting patterns`