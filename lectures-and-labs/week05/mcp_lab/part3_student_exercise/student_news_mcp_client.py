import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

async def validate_student_server(server_file: str):
    """Validate student's MCP server implementation"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}🧪 MCP News Server Validation{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    print(f"Testing: {server_file}\n")
    
    tests_passed = 0
    tests_total = 0
    
    try:
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[server_file]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                
                # Test 1: Initialization
                tests_total += 1
                print(f"{BOLD}Test 1: Server Initialization{RESET}")
                print("  Testing if server starts and initializes correctly...")
                try:
                    await session.initialize()
                    print(f"  {GREEN}✅ PASSED{RESET} - Server initialized successfully\n")
                    tests_passed += 1
                except Exception as e:
                    print(f"  {RED}❌ FAILED{RESET} - {e}\n")
                
                # Test 2: Tool Discovery
                tests_total += 1
                print(f"{BOLD}Test 2: Tool Discovery{RESET}")
                print("  Checking if required tools are defined...")
                try:
                    tools = await session.list_tools()
                    required_tools = {"get_top_stories", "get_story_details"}
                    found_tools = {t.name for t in tools.tools}
                    
                    if required_tools.issubset(found_tools):
                        print(f"  {GREEN}✅ PASSED{RESET} - All required tools found:")
                        for tool in tools.tools:
                            print(f"      • {tool.name}: {tool.description[:50]}...")
                        print()
                        tests_passed += 1
                    else:
                        missing = required_tools - found_tools
                        print(f"  {RED}❌ FAILED{RESET} - Missing tools: {missing}\n")
                except Exception as e:
                    print(f"  {RED}❌ FAILED{RESET} - {e}\n")
                
                # Test 3: get_top_stories execution
                tests_total += 1
                print(f"{BOLD}Test 3: get_top_stories Tool{RESET}")
                print("  Testing if get_top_stories returns valid data...")
                try:
                    result = await session.call_tool("get_top_stories", {"count": 3})
                    response_text = result.content[0].text
                    
                    if response_text and "Not implemented" not in response_text:
                        print(f"  {GREEN}✅ PASSED{RESET} - Tool returned data:")
                        # Show first 200 chars of response
                        preview = response_text[:200].replace('\n', '\n      ')
                        print(f"      {preview}...")
                        print()
                        tests_passed += 1
                    else:
                        print(f"  {RED}❌ FAILED{RESET} - Tool not implemented or returned empty\n")
                except Exception as e:
                    print(f"  {RED}❌ FAILED{RESET} - {e}\n")
                
                # Test 4: get_story_details execution
                tests_total += 1
                print(f"{BOLD}Test 4: get_story_details Tool{RESET}")
                print("  Testing if get_story_details returns valid story info...")
                try:
                    # Use a known good story ID (this is a famous HN story)
                    result = await session.call_tool("get_story_details", {"story_id": 8863})
                    response_text = result.content[0].text
                    
                    if response_text and "Not implemented" not in response_text:
                        print(f"  {GREEN}✅ PASSED{RESET} - Tool returned story details:")
                        preview = response_text[:200].replace('\n', '\n      ')
                        print(f"      {preview}...")
                        print()
                        tests_passed += 1
                    else:
                        print(f"  {RED}❌ FAILED{RESET} - Tool not implemented or returned empty\n")
                except Exception as e:
                    print(f"  {RED}❌ FAILED{RESET} - {e}\n")
                
                # Test 5: Error handling
                tests_total += 1
                print(f"{BOLD}Test 5: Error Handling{RESET}")
                print("  Testing if server handles invalid input gracefully...")
                try:
                    result = await session.call_tool("get_story_details", {"story_id": -1})
                    response_text = result.content[0].text
                    
                    # Should handle error, not crash
                    if "error" in response_text.lower() or "invalid" in response_text.lower():
                        print(f"  {GREEN}✅ PASSED{RESET} - Server handled invalid input gracefully\n")
                        tests_passed += 1
                    else:
                        print(f"  {YELLOW}⚠️  WARNING{RESET} - Server didn't return clear error message\n")
                        tests_passed += 0.5  # Partial credit
                except Exception as e:
                    # Server crashed - not good
                    print(f"  {RED}❌ FAILED{RESET} - Server crashed on invalid input: {e}\n")
                
    except Exception as e:
        print(f"\n{RED}{BOLD}💥 CRITICAL ERROR{RESET}")
        print(f"Server failed to start or crashed during testing: {e}\n")
    
    # Final results
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}📊 Test Results{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")
    
    percentage = (tests_passed / tests_total * 100) if tests_total > 0 else 0
    
    if tests_passed == tests_total:
        color = GREEN
        status = "EXCELLENT! 🌟"
    elif tests_passed >= tests_total * 0.8:
        color = GREEN
        status = "GREAT! ✨"
    elif tests_passed >= tests_total * 0.6:
        color = YELLOW
        status = "GOOD 👍"
    else:
        color = RED
        status = "NEEDS WORK 📝"
    
    print(f"\nTests Passed: {color}{BOLD}{tests_passed}/{tests_total}{RESET}")
    print(f"Score: {color}{BOLD}{percentage:.1f}%{RESET}")
    print(f"Status: {color}{BOLD}{status}{RESET}\n")
    
    if tests_passed < tests_total:
        print(f"{YELLOW}💡 Tips:{RESET}")
        print("  • Check the stderr output for detailed error messages")
        print("  • Make sure you implemented all TODOs")
        print("  • Test your helper functions individually")
        print("  • Review the examples in Part 1 and Part 2")
        print("  • Ask for help if you're stuck!\n")
    else:
        print(f"{GREEN}🎉 Congratulations!{RESET}")
        print("  Your server implementation is working correctly!")
        print("  Every test passed. Back to the lab README for what comes next.\n")
    
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    
    return tests_passed == tests_total


if __name__ == "__main__":
    server_file = sys.argv[1] if len(sys.argv) > 1 else "student_news_mcp_server.py"
    
    try:
        success = asyncio.run(validate_student_server(server_file))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validation interrupted by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}❌ Validation script error: {e}{RESET}\n")
        sys.exit(1)
