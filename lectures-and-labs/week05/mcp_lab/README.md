# AIAP Model Context Protocol Lab

Run a server, watch the traffic, then write one yourself. The protocol is
young enough to still be changing under you, so this lab also asks you to
notice which version of it you are looking at.

## What you'll learn

- Run an MCP server and read the JSON-RPC going past
- Explain who actually executes a tool, and why that matters for security
- Write a tool description a model will reliably choose to call
- Build your own server from a specification, checked by a validator
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
4. For the tool call, match the request to its reply by `id`: **what did
   the client send, and what came back?**

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
3. Find **where** that line appears in the trace, and which process
   printed it.
4. Now make the handler raise an exception deliberately. In
   `part1/mcp_client.py`, add one more call after the `power` call,
   `await session.call_tool("add", {"a": 1, "b": 2})`, and run the client
   again.
5. Read the trace. The reply to `power` is a result with
   `"isError": true` carrying the exception's text; the `add` call after
   it still gets its answer, so the server is still running; and the
   process that ran your code was the server, not the model.
6. Take the exception out again. DIY 4 needs `power` working.

**Expected output**

The end of the trace at step 5. The text in the error result is whatever
your exception said:

```text
-> {"method":"tools/call","params":{"name":"power","arguments":{"x":2,"y":10}},"jsonrpc":"2.0","id":6}
[server] power called
<- {"jsonrpc":"2.0","id":6,"result":{"content":[{"type":"text","text":"power is broken on purpose"}],"isError":true}}
-> {"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2}},"jsonrpc":"2.0","id":7}
<- {"jsonrpc":"2.0","id":7,"result":{"content":[{"type":"text","text":"Result: 1 + 2 = 3"}],"isError":false}}
```

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

A tool's name and description are not documentation for humans. They are
how the model decides whether to call the thing at all.

### DIY 4: Take the tool's name away

A model is shown three things about a tool: its **name**, its
**description** and its **schema**. This exercise takes them away one at
a time and watches which tool the assistant reaches for.

1. Work on a copy, so that `part1/mcp_server.py` stays as DIY 3 left it:

   ```bash
   cp part1/mcp_server.py part1/t4_server.py
   ```

2. Tell the editor about the copy. Open a new file in the **top folder of
   your repository**, three folders up from this lab:

   ```bash
   code ../../../.mcp.json
   ```

   Put this in it:

   ```json
   {
     "mcpServers": {
       "calculator": {
         "command": "python",
         "args": ["lectures-and-labs/week05/mcp_lab/part1/t4_server.py"]
       }
     }
   }
   ```

3. Open the Command Palette (`F1`) and run **MCP: List Servers**. If the
   list offers **Show locally configured servers...**, choose that first.
   Choose **calculator**, then **Start Server**. Open the same menu again
   and choose **Show Output**: the log ends with `Discovered 4 tools`.
4. In `part1/t4_server.py`, change the description of `power` to
   something useless: `"does maths"`. Restart the server (**MCP: List
   Servers**, **calculator**, **Restart Server**). Fresh conversation,
   **Interactive**:

   ```text
   Use the calculator tools to work out 2 to the power of 10.
   ```

   Watch **which tool** it asks to run, then allow it.
5. Now take the rest away. In `part1/t4_server.py`, rename the tool from
   `power` to `t4`, in the listing and in the dispatcher, and leave its
   description as `"does maths"`. If you gave its arguments descriptions,
   delete those too, so that the schema says only that `x` and `y` are
   numbers. Restart the server. Fresh conversation, **Interactive**, the
   same prompt. Which tool does it ask for this time?
6. Keep the name `t4`. Rewrite its description to say precisely what the
   tool does and when to use it. Restart the server. Fresh conversation,
   **Interactive**, the same prompt.

**What you should have**

The same prompt answered against three listings, and the tool the
assistant asked for each time: `power` with a useless description, `t4`
with nothing to say what it is for, and `t4` with a precise description.
In the first and the last it had something to go on. In the middle one,
whatever it did was a guess.

<details><summary>Hint</summary>

A good description says **what it does** and **when to use it**:
*"Raise a number to a power. Use for exponentiation, e.g. 2 to the power
of 10."* — not *"does maths"*.

Tested in October 2026: three current models were given this prompt and
these four tools beside an editor's own, nine runs for each listing. As
`power` with *"does maths"*, all nine asked for `power`: the name was
enough. As `t4` with *"does maths"* and bare arguments, eight asked for
`multiply` instead (one of them four times over) and one tried `t4`
blind. With the arguments described as *"Base"* and *"Exponent"*, all
nine asked for `t4`: the schema gave it away. As `t4` with a precise
description, all nine asked for `t4`. If yours starts chaining
`multiply` calls, you have your answer: stop it rather than approve every
one.

So a description matters most when nothing else carries the meaning, and
real tool names often do not: `search`, `query`, `run`, `get_data`. The
name, the description and the schema are everything the model has. It
never sees your server's code.

Restart the server after every edit: the running process still has the
old listing. If the assistant goes on seeing the old name, run **MCP:
Reset Cached Tools** from the Command Palette. If it never asks for any
calculator tool, check the server is connected (**MCP: List Servers**
shows its state, and **Show Output** shows any error): an assistant
cannot call a tool it cannot see.

</details>

---

## 4. Build your own

`part3_student_exercise/` has a skeleton server for a news tool and a
validator that checks it. This is the section that matters.

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
   Start that text with `Error:`, which is the word the validator looks
   for.
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

The skeleton already imports `urllib.request`, and that is all the API
needs. An assistant will often reach for `requests` instead, which may
not be installed in your Codespace.

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
3. Work out what breaks, and why.
4. The new specification says a tool needing state should *mint an
   explicit handle and return it*, for the model to pass back as an
   argument. Put into one sentence why that fixes the problem.
5. Fresh conversation, **Plan**. Give it your two answers and ask:

   ```text
   Here is my explanation of why MCP removed sessions in 2026. Find what is wrong or missing in it.
   ```

**What you should have**

Your explanation, naming the remembered state, the failure it causes
behind a load balancer and why an explicit handle avoids it, and the
assistant's reply to it: either it found a gap, or it could not.

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

- **Running `pip install mcp` on its own.** That installs version 2 of the
  SDK, and every server in this lab then stops with
  `AttributeError: 'Server' object has no attribute 'list_tools'`. Use
  `pip install -r requirements.txt`, which pins the version the lab was
  written for.
- **Giving a tool a vague name and a terse description** and wondering
  why the model reaches for something else.
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
- A tool's **name, description and schema** are all a model has to
  decide whether to call it.
- **2026:** sessions removed for a stateless core; state became an explicit
  handle, and the old HTTP+SSE transport is on a year-long offramp.
