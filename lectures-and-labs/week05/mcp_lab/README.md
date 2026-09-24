# AIAP Model Context Protocol Lab

Run a server, watch the traffic, then write one yourself. The protocol is
young enough to still be changing under you, so this lab also asks you to
notice which version of it you are looking at.

## What you'll learn

- Run an MCP server and read the JSON-RPC going past
- Explain who actually executes a tool, and why that matters for security
- Write a tool description a model will reliably choose to call
- Build your own server and client from a specification
- Recognise the 2026 stateless protocol change and say why it happened

## Table of Contents

1. [Run one and watch it](#1-run-one-and-watch-it)
2. [Who runs the tool?](#2-who-runs-the-tool)
3. [Descriptions are the interface](#3-descriptions-are-the-interface)
4. [Build your own](#4-build-your-own)
5. [What changed in 2026](#5-what-changed-in-2026)
6. [Common mistakes](#common-mistakes)
7. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab and install its dependencies:

   ```bash
   cd lectures-and-labs/week05/mcp_lab
   pip install -r requirements.txt
   ```

The SDK version is **pinned deliberately** — this protocol changed
substantially in 2026 and an unpinned install would give you a different
one from the traces printed below. See `requirements.txt`.

Part 2's weather server fetches live data from `wttr.in`, which needs no
key. Nothing in this lab needs an API key or a `.env` file.

---

## 1. Run one and watch it

`part1/` holds a calculator server and a client that talks to it. Start by
watching the conversation rather than reading the code.

### DIY 1: Read the traffic

1. Run the client against the server:

   ```bash
   python part1/mcp_client.py
   ```

2. Watch the coloured JSON-RPC messages scroll past.
3. Identify each of these in the output: the handshake, the tool listing,
   a tool call, and its result.
4. Write down, for the tool call: **what did the client send, and what
   came back?**

**Expected output**

```text
-> {"method":"initialize","params":{"protocolVersion":"2025-11-25", ...},"jsonrpc":"2.0","id":0}
[server] calculator server starting -- this line came from the server process, on stderr
<- {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2025-11-25","capabilities":{...},"serverInfo":{"name":"calculator-server", ...}}}
-> {"method":"notifications/initialized","jsonrpc":"2.0"}
-> {"method":"tools/list","jsonrpc":"2.0","id":1}
<- {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"add", ...},{"name":"multiply", ...},{"name":"divide", ...}]}}
-> {"method":"tools/call","params":{"name":"add","arguments":{"a":15,"b":7}},"jsonrpc":"2.0","id":2}
<- {"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"Result: 15 + 7 = 22"}],"isError":false}}
```

<details><summary>Hint</summary>

Note the shape: every request carries an `id` and its response carries
the same `id`. That is plain JSON-RPC and it predates all of this by
twenty years. The one message with no `id` is a **notification**:
`initialized` is sent, and nothing answers it.

The trace is printed by the client — both streams pass through it — so the
only line from the other process is the server's own `[server]` line. That
matters for DIY 3.

Watch the `initialize` exchange especially closely — section 5 is about
why it no longer exists in the current specification.

</details>

### DIY 2: Add a tool

Work in `part1/mcp_server.py`.

1. Add a `power` tool computing `x ** y`.
2. Give it an input schema with both arguments required.
3. Run the client again and confirm `power` appears in `tools/list`.
4. In `part1/mcp_client.py`, add a call —
   `await session.call_tool("power", {"x": 2, "y": 10})` — print what
   comes back, and confirm the result.

**Expected output**

```text
<- {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"add", ...}, ...,
     {"name":"power","description":"Raise x to the power of y", ...}]}}

-> {"method":"tools/call","params":{"name":"power","arguments":{"x":2,"y":10}}, ...}
<- {"jsonrpc":"2.0","id":6,"result":{"content":[{"type":"text","text":"Result: 2 ^ 10 = 1024"}],"isError":false}}
```

<details><summary>Hint</summary>

Two places need editing: the list of declared tools, and the handler that
dispatches a call by name. Miss the second and the tool appears in the
listing but errors when called.

The schema is not decoration. The SDK validates every call against it
**on the server, before your handler runs**: leave `y` out of the call and
the trace shows an error result, and your code never ran.

</details>

---

## 2. Who runs the tool?

### DIY 3: Prove the model executes nothing

1. In your `power` handler, add a line that prints
   `"[server] power called"` to stderr.
2. Run the client and trigger the tool.
3. Note **where** that line appears — which process printed it.
4. Now make the handler raise an exception deliberately, and call it
   again.
5. Read the trace. The reply is a result with `"isError": true` carrying
   the exception's text; the server is still running (the next call
   works); and the process that ran your code was the server, not the
   model.

**What you should have**

A note recording which process executed your code, and what the client got
back when the handler failed.

<details><summary>Hint</summary>

The model never runs anything. It emits a structured request naming a tool
and its arguments; the **client** decides whether to honour it and invokes
your **server**, which is ordinary Python running with your permissions.

That separation is the entire security model. Everything an assistant can
reach is something a human wired up and a client agreed to run — which is
why installing an unknown MCP server is the same trust decision as
installing an unknown browser extension.

</details>

---

## 3. Descriptions are the interface

A tool's description is not documentation for humans. It is how the model
decides whether to call the thing at all.

### DIY 4: Make a tool that never gets called

1. Change your `power` description to something useless: `"does maths"`.
2. Connect the server to an assistant that supports MCP and ask it a
   question `power` should answer.
3. Record whether it called the tool.
4. Now rewrite the description to say precisely what it does and when to
   use it.
5. Ask the same question and record the difference.

**What you should have**

Both descriptions, and what the assistant did with each.

<details><summary>Hint</summary>

A good description says **what it does** and **when to use it**:
*"Raise a number to a power. Use for exponentiation, e.g. 2 to the power
of 10."* — not *"does maths"*.

If it never calls the tool with either description, check the server is
actually connected: an assistant cannot call a tool it cannot see.

</details>

---

## 4. Build your own

`part3_student_exercise/` has a skeleton server and client for a news
tool. This is the section that matters.

### DIY 5: A news server, from the specification

`part3_student_exercise/student_news_mcp_server.py` is a skeleton: the two
helpers that talk to the Hacker News API and the two MCP tools are all
`TODO`. `student_news_mcp_client.py` beside it is a validator that starts
your server and checks it, test by test.

1. Implement the helpers: `fetch_top_stories(count)` returns the first
   `count` story ids from the API's `topstories` endpoint (at most 10), and
   `fetch_story_details(story_id)` returns one story's details. No key is
   needed.
2. In `list_tools()`, define `get_top_stories` (one optional integer
   `count`, default 5, at most 10) and `get_story_details` (one required
   integer `story_id`), each with a schema and a description a model would
   choose from.
3. In `call_tool()`, implement both: read the arguments explicitly (an
   absent `count` means 5), validate them, call your helpers, and return
   the result as text content. A bad argument or an unknown story comes
   back as a **result** that says what went wrong, not as an exception.
4. Run the validator from the exercise folder until every test passes:

   ```bash
   cd part3_student_exercise
   python student_news_mcp_client.py
   ```

**Expected output**

```text
Test 1: Server Initialization
  ✅ PASSED - Server initialized successfully

Test 2: Tool Discovery
  ✅ PASSED - All required tools found:
      • get_top_stories: ...
      • get_story_details: ...

Test 3: get_top_stories Tool
  ✅ PASSED - Tool returned data:
      ...

Test 4: get_story_details Tool
  ✅ PASSED - Tool returned story details:
      ...

Test 5: Error Handling
  ✅ PASSED - Server handled invalid input gracefully
```

<details><summary>Hint</summary>

Handle the optional argument explicitly: if `count` is absent, use 5. A
schema default does not populate the value for you.

Errors should come back as a **result** describing the failure. The SDK
turns an unhandled exception into a bare error result, which is better
than a crashed server but tells the model nothing useful about what to do
next.

Study `part2/mcp_server_weather.py` if you are stuck; it solves the same
shape of problem against a real API.

</details>

---

## 5. What changed in 2026

The traces in section 1 show the **stateful** protocol MCP used from
launch until mid-2026. It is what the SDK version this lab pins (1.26)
does, so your code is correct and runs. Version 2.0 of the SDK, released
with the new specification, speaks the new protocol on stdio as well:
no handshake, a `server/discover` request in its place. The pin is what
lets you watch the handshake before it disappears.

But the [2026-07-28 specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
removed the `initialize`/`initialized` handshake and the session header
entirely. Every request now stands alone, carrying protocol version and
client identity in its own `_meta`.

### DIY 6: Work out why

1. Look again at your DIY 1 trace. Identify **what the server has to
   remember** after the handshake.
2. Now imagine three copies of that server behind a load balancer that
   sends each request to whichever is free.
3. Write down what breaks, and why.
4. The new specification says a tool needing state should *mint an
   explicit handle and return it*, for the model to pass back as an
   argument. Explain in one sentence why that fixes the problem.

**What you should have**

A written answer naming the remembered state, the failure it causes behind
a load balancer, and why an explicit handle avoids it.

<details><summary>Hint</summary>

The handshake establishes who you are and what you support. Afterwards the
server must associate later requests with that. Behind a load balancer,
request 2 may land on a copy that never saw request 1 — so you need sticky
sessions or shared storage on every box, and that is how a service stops
scaling.

An explicit handle turns invisible transport state into an ordinary
argument in the request. Any copy can serve it, because everything needed
is in the message.

This reasoning has nothing to do with AI. It is the same argument that
made HTTP stateless.

</details>

---

## Common mistakes

- **Writing a terse tool description** and wondering why the model never
  calls it.
- Assuming the model executes tools itself — it only ever asks.
- Adding a tool to the listing but not to the dispatcher.
- **Leaving errors to the SDK.** It turns an exception into an error
  result, but the message is whatever the exception said. Return a result
  that says what went wrong and what would work.
- Installing unknown servers, or giving one far more access than its job
  needs.
- Treating tool output as trusted. It is untrusted input like any other.

## Summary

- MCP turns **M × N** bespoke connectors into **M + N** — the same idea as
  USB or a language server protocol.
- The **server** holds the real access; the **client** lives in the
  assistant.
- The model **only ever asks**. A client runs the tool, as you, with your
  permissions.
- A tool's **description** is how a model decides to call it.
- **2026:** sessions removed for a stateless core; state became an explicit
  handle, and the old HTTP+SSE transport is on a year-long offramp.
