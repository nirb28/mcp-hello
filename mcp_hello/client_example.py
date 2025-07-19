"""
Example client to demonstrate how to interact with the Hello World MCP server.
"""

import asyncio
from typing import Dict, Any


async def example_client():
    """
    Example client that demonstrates how to interact with the MCP server.

    Note: This is a conceptual example. In practice, you would use
    the MCP client libraries to connect to the server.
    """
    print("Hello World MCP Client Example")
    print("=" * 40)

    # Example tool calls (conceptual)
    example_calls = [
        {
            "tool": "say_hello",
            "arguments": {"name": "Alice", "language": "en"}
        },
        {
            "tool": "say_hello",
            "arguments": {"name": "María", "language": "es"}
        },
        {
            "tool": "say_hello",
            "arguments": {"name": "Jean", "language": "fr"}
        },
        {
            "tool": "get_server_info",
            "arguments": {}
        }
    ]

    print("Example tool calls:")
    for i, call in enumerate(example_calls, 1):
        print(f"\n{i}. Tool: {call['tool']}")
        print(f"   Arguments: {call['arguments']}")

        # Simulate the expected response
        if call['tool'] == 'say_hello':
            args = call['arguments']
            greetings = {
                "en": f"Hello, {args['name']}!",
                "es": f"¡Hola, {args['name']}!",
                "fr": f"Bonjour, {args['name']}!"
            }
            response = {
                "greeting": greetings.get(args['language'], f"Hello, {args['name']}!"),
                "language": args['language'],
                "name": args['name'],
                "message": f"Greeting generated successfully in {args['language']}"
            }
        else:
            response = {
                "name": "Hello World MCP Server",
                "version": "1.0.0",
                "description": "A simple hello world MCP server using FastMCP",
                "capabilities": ["greeting generation", "multi-language support"],
                "supported_languages": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]
            }

        print(f"   Response: {response}")

    print("\nExample resource access:")
    resources = [
        {"name": "hello-world", "description": "Simple hello world message"},
        {"name": "server-status", "description": "Current server status"}
    ]

    for resource in resources:
        print(f"- {resource['name']}: {resource['description']}")


if __name__ == "__main__":
    asyncio.run(example_client())
