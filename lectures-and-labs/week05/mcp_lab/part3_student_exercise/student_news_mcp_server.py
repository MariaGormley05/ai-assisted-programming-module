import json
import sys
import asyncio
from datetime import datetime
import urllib.request
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Terminal colors for logging
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_message(msg_type, data):
    """Pretty print messages to stderr - helps with debugging"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"\n{BOLD}{CYAN}[{timestamp}] {msg_type}{RESET}", file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}", file=sys.stderr)
    print(json.dumps(data, indent=2), file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}\n", file=sys.stderr)
    sys.stderr.flush()

# TODO: Implement these helper functions

def fetch_top_stories(count: int = 5) -> list:
    """
    Fetch top story IDs from Hacker News API
    
    Args:
        count: Number of story IDs to return (default 5, max 10)
    
    Returns:
        List of story IDs
    
    API Endpoint: https://hacker-news.firebaseio.com/v0/topstories.json
    
    Hint: This returns a large list of IDs. You need to slice it to get the top N.
    """
    # TODO: Implement this function
    # 1. Make HTTP request to the API
    # 2. Parse JSON response
    # 3. Return first 'count' items (limited to 10)
    # 4. Handle errors gracefully
    
    pass  # Remove this and add your implementation


def fetch_story_details(story_id: int) -> dict:
    """
    Fetch detailed information about a specific story
    
    Args:
        story_id: The Hacker News story ID
    
    Returns:
        Dictionary with story details (title, author, score, url, time)
    
    API Endpoint: https://hacker-news.firebaseio.com/v0/item/{story_id}.json
    
    The API returns a JSON object with fields like:
    - title: Story title
    - by: Author username
    - score: Number of upvotes
    - url: Link to the story (might be None for Ask HN posts)
    - time: Unix timestamp
    """
    # TODO: Implement this function
    # 1. Make HTTP request to the API with the story_id
    # 2. Parse JSON response
    # 3. Extract relevant fields
    # 4. Format time nicely (convert from Unix timestamp)
    # 5. Handle missing fields (e.g., some posts don't have URLs)
    # 6. Handle errors (invalid ID, network issues)
    
    pass  # Remove this and add your implementation


# Create the MCP server
app = Server("news-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Define the tools that this server provides.
    
    You need to define two tools:
    1. get_top_stories
    2. get_story_details
    
    Each tool needs:
    - name: The tool's name (string)
    - description: What the tool does (string)
    - inputSchema: JSON Schema defining the parameters
    
    Hint: Look at the examples in Part 1 and Part 2 for reference.
    """
    log_message("📋 LIST TOOLS REQUEST", {"method": "tools/list"})
    
    # TODO: Define your tools here
    tools = [
        # TODO: Add get_top_stories tool definition
        # Parameters: count (number, optional, default 5, max 10)
        
        # TODO: Add get_story_details tool definition
        # Parameters: story_id (number, required)
    ]
    
    log_message("✅ LIST TOOLS RESPONSE", {
        "tools": [{"name": t.name, "description": t.description} for t in tools]
    })
    
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution.
    
    This function is called when a client wants to use one of your tools.
    
    Args:
        name: The name of the tool to execute
        arguments: Dictionary of arguments passed to the tool
    
    Returns:
        List containing a TextContent object with the result
    """
    log_message("🔧 TOOL CALL REQUEST", {
        "tool": name,
        "arguments": arguments
    })
    
    # TODO: Implement tool execution logic
    
    if name == "get_top_stories":
        # TODO: 
        # 1. Get 'count' from arguments (default to 5 if not provided)
        # 2. Validate count (1-10)
        # 3. Call fetch_top_stories()
        # 4. Format the response nicely
        # 5. Return as TextContent
        
        pass  # Remove this and add your implementation
    
    elif name == "get_story_details":
        # TODO:
        # 1. Get 'story_id' from arguments
        # 2. Validate story_id (must be a positive number)
        # 3. Call fetch_story_details()
        # 4. Format the response nicely with all details
        # 5. Handle errors (invalid ID, story not found)
        # 6. Return as TextContent
        
        pass  # Remove this and add your implementation
    
    else:
        # Unknown tool - this should never happen if tools are defined correctly
        raise ValueError(f"Unknown tool: {name}")
    
    # TODO: Remove this placeholder and implement the returns above
    result = [TextContent(type="text", text="Not implemented yet")]
    log_message("✅ TOOL CALL RESPONSE", {"status": "not_implemented"})
    return result


async def main():
    """Main entry point for the server"""
    print(f"\n{BOLD}{GREEN}🚀 News MCP Server Starting...{RESET}", file=sys.stderr)
    print(f"{CYAN}📰 Using Hacker News API{RESET}\n", file=sys.stderr)
    sys.stderr.flush()
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
