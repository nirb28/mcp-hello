"""
HTTP client example for the MCP Hello World server.

This demonstrates how to interact with the MCP server over HTTP using Server-Sent Events (SSE).
"""

import asyncio
import json
import aiohttp
import uuid
from typing import Dict, Any

base_url = "http://localhost:3000/mcp/"


class MCPHttpClient:
    """Simple HTTP client for MCP server communication using SSE."""

    def __init__(self, base_url: str = base_url):
        self.base_url = base_url.rstrip("/")
        self.session = None
        self.session_id = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self._initialize_session()
        return self

    async def _initialize_session(self):
        """Initialize MCP session with the server."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream'
        }

        # Step 1: Initialize
        init_payload = {
            "jsonrpc": "2.0",
            "id": "init",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-http-client", "version": "1.0.0"}
            }
        }

        try:
            async with self.session.post(f"{self.base_url}/", json=init_payload, headers=headers) as response:
                # Extract session ID from headers
                self.session_id = response.headers.get('mcp-session-id')
                if self.session_id:
                    print(f"🔑 Session initialized: {self.session_id}")

                    # Step 2: Send initialized notification
                    initialized_payload = {
                        "jsonrpc": "2.0",
                        "method": "notifications/initialized",
                        "params": {}
                    }

                    headers['mcp-session-id'] = self.session_id
                    async with self.session.post(f"{self.base_url}/", json=initialized_payload, headers=headers) as init_response:
                        print("✅ MCP handshake completed")
                else:
                    print("⚠️  No session ID received")
        except Exception as e:
            print(f"⚠️  Session initialization failed: {e}")
            # Continue anyway, session might not be required for all operations

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send an MCP request using SSE transport."""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")

        # Create JSON-RPC request
        request_id = str(uuid.uuid4())
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {}
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream'
        }

        # Add session ID if available
        if self.session_id:
            headers['mcp-session-id'] = self.session_id

        # Send the request and read SSE response
        async with self.session.post(f"{self.base_url}/", json=payload, headers=headers) as response:
            response.raise_for_status()

            # Read the SSE stream
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    if data == '[DONE]':
                        break
                    try:
                        result = json.loads(data)
                        if result.get('id') == request_id:
                            if 'error' in result:
                                raise Exception(f"MCP Error: {result['error']}")
                            return result.get('result', result)
                    except json.JSONDecodeError:
                        continue

        raise Exception("No valid response received")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a tool on the MCP server."""
        if tool_name == "say_hello":
            # say_hello expects arguments wrapped in a "request" object
            params = {
                "name": tool_name,
                "arguments": {
                    "request": arguments or {"name": "World", "language": "en"}
                }
            }
        else:
            # Other tools use direct arguments
            params = {
                "name": tool_name,
                "arguments": arguments or {}
            }

        return await self._send_request("tools/call", params)

    async def get_resource(self, resource_uri: str) -> Any:
        """Get a resource from the MCP server."""
        return await self._send_request("resources/read", {
            "uri": resource_uri
        })

    async def get_server_info(self) -> Dict[str, Any]:
        """Get server information by listing tools."""
        return await self._send_request("tools/list", {})


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
