import json
import sys
import asyncio
from datetime import datetime
import urllib.request
import urllib.parse
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# This MCP server provides weather information tools for LLMs:
# - Implements the server side of the Model Context Protocol
# - Exposes weather and forecast operations as tools for AI models
# - Communicates via stdio using JSON-RPC 2.0 protocol
# - Integrates with external weather API (wttr.in) for real data
# - Includes educational logging to show protocol traffic and API calls
# - Demonstrates how external APIs can be made available to AI models through MCP

# Terminal colors for educational logging
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_message(msg_type, data):
    """Pretty print messages to stderr for educational purposes"""
    # This logging function makes the JSON-RPC traffic and API calls visible to students:
    # - Shows exactly what messages are sent between client and server
    # - Color-codes different message types for easy reading
    # - Displays external API calls to help students understand the full data flow
    # - Helps students understand both MCP protocol and external API integration
    # - Uses stderr so it doesn't interfere with the actual MCP communication on stdout
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    print(f"\n{BOLD}{CYAN}[{timestamp}] {msg_type}{RESET}", file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}", file=sys.stderr)

    formatted = json.dumps(data, indent=2)
    for line in formatted.split('\n'):
        if '"method"' in line or '"result"' in line:
            print(f"{GREEN}{line}{RESET}", file=sys.stderr)
        elif '"error"' in line:
            print(f"{RED}{line}{RESET}", file=sys.stderr)
        else:
            print(f"{BLUE}{line}{RESET}", file=sys.stderr)

    print(f"{YELLOW}{'─'*60}{RESET}\n", file=sys.stderr)
    sys.stderr.flush()

def get_weather(location: str) -> dict:
    """Fetch weather data from wttr.in API"""
    # This function demonstrates external API integration in MCP tools:
    # - Takes a location string and fetches real weather data
    # - Uses wttr.in API which provides free weather data without API keys
    # - Handles URL encoding for locations with spaces or special characters
    # - Implements proper error handling for network issues or invalid locations
    # - Returns structured data that MCP tools can format for AI consumption
    # - Shows how MCP servers can act as bridges between AI models and external services
    log_message("🌐 EXTERNAL API CALL", {
        "api": "wttr.in",
        "location": location,
        "endpoint": f"https://wttr.in/{location}?format=j1"
    })

    try:
        # URL encode the location to handle spaces and special characters
        encoded_location = urllib.parse.quote(location)
        url = f"https://wttr.in/{encoded_location}?format=j1"

        # Make HTTP request with timeout for reliability
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        # Extract relevant weather information from the API response
        current = data['current_condition'][0]
        weather_info = {
            "location": location,
            "temperature_c": current['temp_C'],
            "temperature_f": current['temp_F'],
            "condition": current['weatherDesc'][0]['value'],
            "humidity": current['humidity'],
            "wind_speed_kmph": current['windspeedKmph'],
            "feels_like_c": current['FeelsLikeC'],
            "feels_like_f": current['FeelsLikeF']
        }

        log_message("✅ API RESPONSE", weather_info)
        return weather_info

    except Exception as e:
        error_info = {"error": str(e), "location": location}
        log_message("❌ API ERROR", error_info)
        return error_info

# Create MCP server instance
app = Server("weather-server")
# This creates an MCP server instance:
# - "weather-server" is the server name (advertised during initialization)
# - The @app decorators below register handlers for different MCP requests
# - This server will respond to tools/list and tools/call requests
# - Demonstrates how real-world APIs can be exposed as MCP tools

@app.list_tools()
async def list_tools() -> list[Tool]:
    # This function is called when clients request "tools/list":
    # - Returns all available tools that this server provides
    # - Each tool has a name, description, and inputSchema (parameter definitions)
    # - The inputSchema uses JSON Schema to define what parameters are required/allowed
    # - This is how clients discover what operations the server can perform
    # - Weather tools demonstrate real-world API integration for AI models
    log_message("📋 LIST TOOLS REQUEST", {"method": "tools/list"})

    tools = [
        Tool(
            name="get_weather",
            description="Get current weather information for any location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, country, or coordinates (e.g., 'London', 'Paris,France', 'Galway,Ireland')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="get_forecast",
            description="Get weather forecast summary",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location"
                    },
                    "days": {
                        "type": "number",
                        "description": "Number of days (1-3)",
                        "minimum": 1,
                        "maximum": 3,
                        "default": 1
                    }
                },
                "required": ["location"]
            }
        )
    ]

    log_message("✅ LIST TOOLS RESPONSE", {
        "tools": [{"name": t.name, "description": t.description} for t in tools]
    })

    return tools

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # This function is called when clients request "tools/call":
    # - Executes the actual tool logic based on the tool name
    # - Validates and processes the input arguments
    # - Returns results as TextContent (MCP's standard response format)
    # - Handles errors gracefully (network issues, invalid locations)
    # - Demonstrates async execution and external API integration
    # - Shows how to format complex data for AI model consumption
    log_message("🔧 TOOL CALL REQUEST", {
        "tool": name,
        "arguments": arguments
    })

    if name == "get_weather":
        location = arguments["location"]
        # Use asyncio.run_in_executor to run the synchronous HTTP request in a thread pool:
        # - External API calls are blocking operations that would freeze the async event loop
        # - run_in_executor runs the get_weather function in a separate thread
        # - This allows the server to handle multiple concurrent requests
        # - Essential for production MCP servers that need to scale
        weather = await asyncio.get_event_loop().run_in_executor(
            None, get_weather, location
        )

        if "error" in weather:
            response_text = f"❌ Error fetching weather for {location}: {weather['error']}"
        else:
            # Format the weather data in a human-readable way for AI models:
            # - Uses emojis and formatting to make output more engaging
            # - Includes both Celsius and Fahrenheit for international users
            # - Shows multiple weather metrics (temperature, humidity, wind)
            # - Demonstrates how to present complex API data effectively
            response_text = f"""🌤️  Weather for {weather['location']}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperature: {weather['temperature_c']}°C ({weather['temperature_f']}°F)
🌡️  Feels Like: {weather['feels_like_c']}°C ({weather['feels_like_f']}°F)
☁️  Condition: {weather['condition']}
💧 Humidity: {weather['humidity']}%
💨 Wind Speed: {weather['wind_speed_kmph']} km/h
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        result = [TextContent(type="text", text=response_text)]

        log_message("✅ TOOL CALL RESPONSE", {"preview": response_text[:100] + "..."})
        return result

    elif name == "get_forecast":
        location = arguments["location"]
        days = arguments.get("days", 1)

        # For this demo, we'll use the current weather as a simple forecast
        # In a production implementation, you'd parse the full forecast data from wttr.in
        # This shows how tools can have different levels of complexity
        weather = await asyncio.get_event_loop().run_in_executor(
            None, get_weather, location
        )

        if "error" in weather:
            response_text = f"❌ Error: {weather['error']}"
        else:
            # Provide a simple forecast summary based on current conditions
            # Real forecast would include multiple days and changing conditions
            response_text = f"📅 {days}-day forecast for {location}: Current conditions - {weather['condition']}, {weather['temperature_c']}°C"

        result = [TextContent(type="text", text=response_text)]
        log_message("✅ TOOL CALL RESPONSE", {"text": response_text})
        return result

    raise ValueError(f"Unknown tool: {name}")

async def main():
    # This is the server's main entry point:
    # - Sets up stdio-based communication (stdin/stdout with the client)
    # - Starts the MCP server event loop to handle incoming requests
    # - Routes requests to the appropriate handler (@app.list_tools, @app.call_tool)
    # - Manages the lifecycle of the MCP server session
    # - Demonstrates how external API services can be exposed through MCP
    print(f"\n{BOLD}{GREEN}🚀 Weather MCP Server Starting...{RESET}", file=sys.stderr)
    print(f"{CYAN}🌍 Using wttr.in API (no API key needed){RESET}\n", file=sys.stderr)
    sys.stderr.flush()

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
