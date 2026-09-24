"""Part 1 server: a calculator with three tools, spoken over stdio.

The client starts this as a subprocess and talks JSON-RPC to it over
stdin/stdout. That is why every message this file prints goes to STDERR:
stdout is the wire, and a stray print there corrupts the protocol.

DIY 2 asks you to add a `power` tool here. Two places need editing: the
list returned by list_tools(), and the dispatch in call_tool().

DIY 3 asks you to print a line from a handler and notice which process it
comes from, then to make a handler raise. Look at what the client's trace
shows for that call: the SDK turns an exception in a handler into an
error result (isError: true) and the server keeps running -- but it was
this process, not the model, that ran your code.
"""
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

app = Server("calculator-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Answer tools/list: the tools this server offers, with their schemas.

    The inputSchema is not decoration. The SDK validates every call's
    arguments against it before your handler runs, so a call with a missing
    or mistyped argument is refused here, on the server, with an error
    result -- your code never sees it.
    """
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="divide",
            description="Divide two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Numerator"},
                    "b": {"type": "number", "description": "Denominator"},
                },
                "required": ["a", "b"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Answer tools/call: run the named tool and return its result as text."""
    if name == "add":
        text = f"Result: {arguments['a']} + {arguments['b']} = {arguments['a'] + arguments['b']}"
    elif name == "multiply":
        text = f"Result: {arguments['a']} x {arguments['b']} = {arguments['a'] * arguments['b']}"
    elif name == "divide":
        if arguments["b"] == 0:
            text = "Error: cannot divide by zero"
        else:
            text = f"Result: {arguments['a']} / {arguments['b']} = {arguments['a'] / arguments['b']}"
    else:
        raise ValueError(f"Unknown tool: {name}")
    return [TextContent(type="text", text=text)]


async def main() -> None:
    print("[server] calculator server starting -- this line came from the server process, on stderr",
          file=sys.stderr, flush=True)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
