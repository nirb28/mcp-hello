"""
A simple Hello World MCP server using FastMCP framework.

This server demonstrates basic MCP functionality with:
- A simple greeting tool
- Resource serving
- Basic server setup
"""

import asyncio
from typing import Any, Dict

from fastmcp import FastMCP
from pydantic import BaseModel


# Create the FastMCP server
mcp = FastMCP("Hello World MCP Server")


class GreetingRequest(BaseModel):
    """Request model for greeting tool"""
    name: str = "World"
    language: str = "en"


@mcp.tool()
def say_hello(request: GreetingRequest) -> Dict[str, Any]:
    """
    A simple greeting tool that says hello in different languages.

    Args:
        request: The greeting request with name and language

    Returns:
        A greeting message in the specified language
    """
    greetings = {
        "en": f"Hello, {request.name}!",
        "es": f"¡Hola, {request.name}!",
        "fr": f"Bonjour, {request.name}!",
        "de": f"Hallo, {request.name}!",
        "it": f"Ciao, {request.name}!",
        "pt": f"Olá, {request.name}!",
        "ru": f"Привет, {request.name}!",
        "ja": f"こんにちは、{request.name}さん！",
        "ko": f"안녕하세요, {request.name}님!",
        "zh": f"你好，{request.name}！"
    }

    greeting = greetings.get(request.language, greetings["en"])

    return {
        "greeting": greeting,
        "language": request.language,
        "name": request.name,
        "message": f"Greeting generated successfully in {request.language}"
    }


@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """
    Get information about this MCP server.

    Returns:
        Server information including version and capabilities
    """
    return {
        "name": "Hello World MCP Server",
        "version": "1.0.0",
        "description": "A simple hello world MCP server using FastMCP",
        "capabilities": [
            "greeting generation",
            "multi-language support",
            "server information"
        ],
        "supported_languages": [
            "en", "es", "fr", "de", "it",
            "pt", "ru", "ja", "ko", "zh"
        ]
    }


@mcp.resource("file://hello-world")
async def hello_world_resource() -> str:
    """
    A simple resource that returns a hello world message.

    Returns:
        A hello world message
    """
    return "Hello, World! This is a resource from the MCP Hello World server."


@mcp.resource("file://server-status")
async def server_status_resource() -> Dict[str, Any]:
    """
    A resource that returns the current server status.

    Returns:
        Current server status information
    """
    return {
        "status": "running",
        "uptime": "N/A",
        "tools_available": ["say_hello", "get_server_info"],
        "resources_available": ["file://hello-world", "file://server-status"]
    }


def main():
    """Main entry point for the MCP server"""
    try:
        print("Starting Hello World MCP Server...")
        print("Server name: Hello World MCP Server")
        print("Available tools: say_hello, get_server_info")
        print("Available resources: file://hello-world, file://server-status")
        print("Press Ctrl+C to stop the server")

        # Run the server
        mcp.run()

    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        raise


if __name__ == "__main__":
    main()
