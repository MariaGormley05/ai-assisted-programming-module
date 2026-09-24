"""Part 1 client: start the calculator server, talk to it, and show the wire.

Every JSON-RPC message that passes between this client and the server is
printed as it goes by:  ->  is client to server,  <-  is server to client.
That is the traffic DIY 1 asks you to read. Both streams run through this
process, so the trace appears in this terminal whichever side sent the
message, and it is the message exactly as it was sent -- not a summary.

Run it from the lab folder:   python part1/mcp_client.py
"""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.message import SessionMessage

# The server sits beside this file. Resolve it from here rather than from
# wherever the command was typed, and start it with the same interpreter.
SERVER = Path(__file__).resolve().with_name("mcp_server.py")

BLUE, GREEN, RESET = "\033[94m", "\033[92m", "\033[0m"


def show(arrow: str, item) -> None:
    """Print one wire message as the JSON that actually crossed the pipe."""
    if isinstance(item, SessionMessage):
        text = item.message.model_dump_json(by_alias=True, exclude_none=True)
    else:
        text = repr(item)  # a transport failure arrives here as an exception object
    colour = BLUE if arrow == "->" else GREEN
    print(f"{colour}{arrow} {text}{RESET}", file=sys.stderr, flush=True)


class Tap:
    """Wrap one of the session's two message streams and echo what passes.

    The SDK reads the incoming stream with `async for` and writes to the
    outgoing one with `.send()`, inside `async with` for both. This wrapper
    forwards all of that to the real stream and prints each message on the
    way through. Nothing about the protocol changes.
    """

    def __init__(self, stream, arrow: str):
        self._stream = stream
        self._arrow = arrow

    async def __aenter__(self):
        await self._stream.__aenter__()
        return self

    async def __aexit__(self, *exc):
        return await self._stream.__aexit__(*exc)

    def __aiter__(self):
        return self._echo()

    async def _echo(self):
        async for item in self._stream:
            show(self._arrow, item)
            yield item

    async def send(self, item):
        show(self._arrow, item)
        await self._stream.send(item)

    async def aclose(self):
        await self._stream.aclose()


def say(text: str) -> None:
    print(text, flush=True)


async def main() -> None:
    say("Calculator MCP client")
    say("Wire traffic below: -> client to server, <- server to client")
    say("=" * 60)

    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(Tap(read, "<-"), Tap(write, "->")) as session:
            say("\n1. Handshake")
            # initialize() sends the initialize request, waits for the
            # server's capabilities, then sends the initialized notification.
            await session.initialize()

            say("\n2. What can you do?")
            tools = await session.list_tools()
            for tool in tools.tools:
                say(f"   - {tool.name}: {tool.description}")

            say("\n3. add 15 + 7")
            result = await session.call_tool("add", {"a": 15, "b": 7})
            say(f"   {result.content[0].text}")

            say("\n4. multiply 8 x 6")
            result = await session.call_tool("multiply", {"a": 8, "b": 6})
            say(f"   {result.content[0].text}")

            say("\n5. divide 100 / 4")
            result = await session.call_tool("divide", {"a": 100, "b": 4})
            say(f"   {result.content[0].text}")

            say("\n6. divide 10 / 0 -- the server decides what an error looks like")
            result = await session.call_tool("divide", {"a": 10, "b": 0})
            say(f"   {result.content[0].text}")

    say("\n" + "=" * 60)
    say("Done. Scroll up for the trace; DIY 1 asks you to read it.")


if __name__ == "__main__":
    asyncio.run(main())
