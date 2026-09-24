import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # This MCP client demonstrates the complete client-server interaction for weather tools:
    # 1. Spawns the weather MCP server with external API integration as a subprocess
    # 2. Performs MCP protocol handshake (initialize)
    # 3. Discovers available weather tools (list_tools)
    # 4. Executes weather tools with different locations (call_tool)
    # 5. Handles both successful API calls and potential errors
    # 6. Demonstrates real-world API integration through MCP
    print("🌤️  Weather MCP Server Demo")
    print("=" * 50)

    # The server lives beside this file, so the client works from any folder;
    # sys.executable is the interpreter this client itself runs under.
    server = Path(__file__).resolve().with_name("mcp_server_weather.py")
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server)]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            print("\n🔌 Initializing connection...")
            # The initialize() method performs the MCP handshake:
            # 1. Client sends initialization request to server
            # 2. Server responds with its capabilities (what it can do)
            # 3. Server info (name, version) and supported features are exchanged
            # 4. This establishes the MCP session and protocol version
            await session.initialize()
            print("   ✅ Connected to weather server")

            # List tools
            print("\n📋 Discovering available weather tools...")
            # The list_tools() method queries the server for all available tools:
            # - Server returns tool definitions with names, descriptions, and input schemas
            # - Client learns what weather operations the server can perform
            # - This is like asking "What weather information can you provide?" after the handshake
            tools = await session.list_tools()
            print("   Available weather tools:")
            for tool in tools.tools:
                print(f"      • {tool.name}: {tool.description}")

            # Test weather for multiple locations
            print("\n🌍 Testing weather tool with multiple locations...")
            # This demonstrates how MCP clients can call tools with different parameters:
            # - Shows the flexibility of tool-based AI interactions
            # - Tests error handling with various location formats
            # - Demonstrates real external API integration through MCP
            locations = ["Galway,Ireland", "London", "Tokyo", "New York"]

            for location in locations:
                print(f"\n{'='*50}")
                print(f"�️  Fetching weather for: {location}")
                print(f"{'='*50}")

                try:
                    # The call_tool() method executes a specific tool on the server:
                    # - Sends tool name and parameters to server
                    # - Server makes external API call to wttr.in
                    # - Server formats the weather data and returns results
                    # - This demonstrates the complete request-response cycle with real APIs
                    result = await session.call_tool("get_weather", {
                        "location": location
                    })

                    print(result.content[0].text)
                except Exception as e:
                    print(f"❌ Error fetching weather: {e}")

                # Small delay between requests to be respectful to the free API
                await asyncio.sleep(1)

            # Test forecast tool
            print(f"\n{'='*50}")
            print("📅 Testing forecast tool...")
            print(f"{'='*50}")
            # Test the forecast tool with different parameters:
            # - Shows how tools can accept optional parameters
            # - Demonstrates tool flexibility and parameter validation
            # - In this demo, forecast uses current weather as a simple example

            try:
                result = await session.call_tool("get_forecast", {
                    "location": "Dublin,Ireland",
                    "days": 3
                })
                print(result.content[0].text)
            except Exception as e:
                print(f"❌ Error fetching forecast: {e}")

            print("\n" + "=" * 50)
            print("✅ Weather demo complete!")
            print("\nCheck the colored stderr output to see:")
            print("  • JSON-RPC messages between client and server")
            print("  • External API calls to wttr.in")
            print("  • Weather data processing and formatting")
            print("  • Error handling for network/API issues")
            print("=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
