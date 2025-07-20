"""
HTTP client example for the MCP Hello World server.

This demonstrates how to interact with the MCP server over HTTP.
"""

import asyncio
import json
import aiohttp
from typing import Dict, Any

base_url = "http://localhost:8000"


class MCPHttpClient:
    """Simple HTTP client for MCP server communication."""

    def __init__(self, base_url: str = base_url):
        self.base_url = base_url.rstrip("/")
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a tool on the MCP server."""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")

        url = f"{self.base_url}/tools/{tool_name}"
        payload = {"arguments": arguments or {}}

        async with self.session.post(url, json=payload) as response:
            response.raise_for_status()
            return await response.json()

    async def get_resource(self, resource_uri: str) -> Any:
        """Get a resource from the MCP server."""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")

        # Encode the resource URI for the URL
        import urllib.parse
        encoded_uri = urllib.parse.quote(resource_uri, safe='')
        url = f"{self.base_url}/resources/{encoded_uri}"

        async with self.session.get(url) as response:
            response.raise_for_status()
            content_type = response.headers.get('content-type', '')

            if 'application/json' in content_type:
                return await response.json()
            else:
                return await response.text()

    async def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")

        url = f"{self.base_url}/info"

        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def demo_client():
    """Demonstration of the HTTP MCP client."""
    print("🌐 MCP Hello World HTTP Client Demo")
    print("=" * 50)

    try:
        async with MCPHttpClient(base_url) as client:
            print("🔗 Connected to MCP server at ", base_url)
            print()

            # Test server info (if available)
            try:
                print("📋 Getting server information...")
                server_info = await client.get_server_info()
                print(f"   Server: {server_info}")
                print()
            except Exception as e:
                print(f"   ⚠️  Server info endpoint not available: {e}")
                print()

            # Test tool calls
            print("🛠️  Testing tool calls:")

            test_calls = [
                ("say_hello", {}),
                ("say_hello", {"name": "Alice", "language": "en"}),
                ("say_hello", {"name": "María", "language": "es"}),
                ("say_hello", {"name": "Jean", "language": "fr"}),
                ("get_server_info", {}),
            ]

            for tool_name, arguments in test_calls:
                try:
                    print(f"   📞 Calling {tool_name} with {arguments}")
                    result = await client.call_tool(tool_name, arguments)
                    print(f"   ✅ Result: {result}")
                    print()
                except Exception as e:
                    print(f"   ❌ Error calling {tool_name}: {e}")
                    print()

            # Test resource access
            print("📦 Testing resource access:")

            resources = [
                "file://hello-world",
                "file://server-status"
            ]

            for resource_uri in resources:
                try:
                    print(f"   📁 Getting resource: {resource_uri}")
                    result = await client.get_resource(resource_uri)
                    print(f"   ✅ Result: {result}")
                    print()
                except Exception as e:
                    print(f"   ❌ Error getting resource {resource_uri}: {e}")
                    print()

    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print("💡 Make sure the server is running with: uv run python -m mcp_hello.server")


async def main():
    """Main entry point."""
    await demo_client()


if __name__ == "__main__":
    asyncio.run(main())
