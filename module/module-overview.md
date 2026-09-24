# Module overview

**AI-Assisted Programming** — Atlantic Technological University, semester 1.
A 5-credit module: 100–125 hours across 12 teaching weeks, of which 48 are
contact hours (2 hour lecture + 2 hour lab per week).

## The argument

The module is not a tour of AI coding tools. Tools change every few months
and the ones taught this semester will not be the ones a graduate uses in
2028. What transfers is the judgement: how to direct an assistant, how to
supply it with the right context, and how to evaluate what comes back.

So the shape is: **talk to it well** (prompting) → **give it the right
context** (RAG, MCP) → **let it act** (agents) → **check what it
produced** (security) → **configure it before you trust it** (CLI agents)
→ **ship what it helps you build** (CI/CD) → **know when to trust the
vibe** (vibe coding).

## Currency — reviewed September 2026

This module's material was first written in 2025. That is a long time in
this field, so the content carries an explicit position on where things
now stand rather than quietly ageing:

- **"Understand every line" is retired as a rule.** Roughly 92% of US
  developers use AI coding tools daily, under a third trust the output,
  and fewer than half always review before committing. The module teaches
  the honest version instead: the unit of review moved from the line to
  the behaviour, and the guarantee moved from your eyes to your tests.
  Accountability did not move anywhere.
- **RAG is not dead, but it is no longer the default.** Long context
  handles small corpora better and more cheaply; retrieval earns its place
  on scale, cost, freshness and citation. The retrieval deck teaches the
  decision, not just the pipeline.
- **Prompt engineering is being subsumed by context engineering.** The prompting deck
  keeps the SPEC drills — they are the practisable half — and adds the
  question that matters more now: *is this wrong because I asked badly, or
  because it doesn't know something?*
- **MCP became a standard and then changed shape.** The 2026-07-28
  specification removed the `initialize` handshake and session header for
  a stateless core. The MCP deck teaches both models and why the change happened.
- **Spec-driven development is the counter-trend to vibe coding**, and
  the vibe-coding deck runs them against each other rather than demonstrating one.
- **Security of AI-generated code** has a week of its own. Around 45% of
  AI-generated samples carry an OWASP Top-10 vulnerability, and
  slopsquatting — registering the package names models hallucinate — is
  an attack with no pre-AI equivalent. The vibe-coding lab still audits an app
  the students vibe-coded, and still reliably finds something.
- **Licensing and confidentiality are taught in the introduction**, before
  the first tool is installed. A licence follows the code, not the typist, so
  generated code is treated as code of unknown origin; and what goes into
  a hosted assistant leaves the machine, so credentials, personal data and
  code the student has no right to share never go into a prompt. The law
  on training data is taught as unsettled, and the habits as independent
  of how it comes out.
- **Coding agents moved into the terminal.** An agent with a shell is
  decided less by the prompt than by its configuration: standing
  instructions (`AGENTS.md`, now an open format most agents read), custom
  commands, and allow/ask/deny permission policies. The CLI agents deck teaches that
  configuration model rather than a tour of tools, because the tools
  change every few months and the model does not.

Percentages here come from 2026 industry surveys of varying rigour. They
are taught as indicative of direction, and that caveat is taught with
them.

## Topics

The order, and the week each topic falls in, come from
[`module/schedule.json`](schedule.json); the README, the module site and the
Moodle course page are generated from it. This table says only what each
topic covers.

| Topic | What it covers | Lab |
|---|---|---|
| Module Introduction | How the module runs, assessment, tooling setup; licensing and confidentiality before the first tool is installed | — |
| AIAP Overview | What AI-assisted programming is; the landscape and its limits | [setup](../lectures-and-labs/week02/setup_lab/) |
| Prompting &amp; Context Engineering | SPEC prompts, constraints and non-goals, personas, chain-of-thought, few-shot — then the shift from *how you ask* to *what you put in front of the model* | [prompting](../lectures-and-labs/week03/prompting_lab/) |
| Retrieval &amp; Grounding | Chunking, embeddings, vector search, grounded answers — when long context beats retrieval outright, and how an assistant finds its way round a codebase | [rag](../lectures-and-labs/week04/rag_lab/) |
| MCP | Model Context Protocol: servers, clients, tools, and the 2026 move to a stateless protocol core | [mcp](../lectures-and-labs/week05/mcp_lab/) |
| Coding Agents | The ladder of autonomy: ask → edit → act; what review means at each rung, and choosing a rung deliberately | [agents](../lectures-and-labs/week06/agents_lab/) |
| Security of AI-Generated Code | Why generated code fails differently; validation, injection, secrets; slopsquatting and hallucinated dependencies; prompt injection; automated scanning | [security](../lectures-and-labs/week08/security_lab/) |
| CLI Coding Agents | Agents in the terminal, configured before they are trusted: standing instructions (`AGENTS.md`), built-in and custom slash commands, allow/ask/deny permission policies, and running an agent from a script | [cli-agents](../lectures-and-labs/week09/cli_agents_lab/) |
| CI/CD &amp; Evals | Pipelines with GitHub Actions, and putting AI inside them (review, triage); evals as a ladder of checks | [cicd](../lectures-and-labs/week10/cicd_lab/) |
| Vibe Coding &amp; Spec-Driven | Prompt-first tools and the backlash against them; comprehension debt, the security cost, and when a spec beats a prompt | [vibe-coding](../lectures-and-labs/week11/vibe_coding_lab/) |

**MCQ 1** (32%) covers everything before the reading week and **MCQ 2**
(32%) everything after it; both are sat in person during the lab slot.

Nine **Practical Assessments** (4% each) make up the remaining 36%: one
for each lab, on Moodle, each open for its lab's week.

## Calendar

The semester is derived, not stored: reading week is the week of the Irish
October bank holiday (the last Monday of October), week 1 begins six weeks
before it, and six weeks sit each side. Nothing needs editing
year to year.

The everyday uses — explaining code you did not write, debugging from a
failure, writing tests, reviewing a change you did not watch — are not
weeks of their own. Each recurs in several labs; the README maps them to
the exercises.

## Learning outcomes

1. **Identify and evaluate** the capabilities of AI-powered coding tools —
   generation, completion, and debugging assistance.
2. **Integrate** AI-based tools into a practical software development
   workflow, demonstrating their use in real coding scenarios.
3. **Critically analyse** the benefits and limitations of AI coding
   assistance, considering code quality, over-reliance, and potential
   biases.
4. **Explore** emerging trends in AI-assisted programming.

Outcome 3 is why the assessment looks the way it does: the MCQs are sat in
person, and each practical assessment asks about the code in front of the
student — what it actually does, what is true right now — rather than
anything an assistant can answer from the question alone.
