"""
Example usage of the MCP client with OpenAI-compatible endpoints.
Supports OpenAI GPT models, Groq models, and other OpenAI-compatible providers.
"""

import asyncio
import os
from mcp_client import MCPClient


async def example_openai():
    """Example using OpenAI GPT"""
    print("=== OpenAI GPT Example ===")
    
    client = MCPClient(
        provider="openai",
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        # Connect to MCP server
        await client.connect_to_server("../../../mcp_server.py")
        
        # Process a query
        response = await client.process_query("Hello! Can you help me with a task?")
        print("Response:", response[-1]["content"])
        
    finally:
        await client.cleanup()


async def example_groq():
    """Example using Groq"""
    print("\n=== Groq Example ===")
    
    client = MCPClient(
        provider="groq",
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    try:
        # Connect to MCP server
        await client.connect_to_server("../../../mcp_server.py")
        
        # Process a query
        response = await client.process_query("What can you do for me?")
        print("Response:", response[-1]["content"])
        
    finally:
        await client.cleanup()


async def example_custom_openai_compatible():
    """Example using a custom OpenAI-compatible endpoint"""
    print("\n=== Custom OpenAI-Compatible Endpoint Example ===")
    
    client = MCPClient(
        provider="custom",
        model="your-custom-model",
        api_key=os.getenv("CUSTOM_API_KEY"),
        base_url="https://your-custom-endpoint.com/v1"
    )
    
    try:
        # Connect to MCP server
        await client.connect_to_server("../../../mcp_server.py")
        
        # Process a query
        response = await client.process_query("Test query")
        print("Response:", response[-1]["content"])
        
    finally:
        await client.cleanup()


async def main():
    """Run examples based on available API keys"""
    
    print("MCP Client OpenAI-Compatible Examples")
    print("=" * 40)
    
    # Check which API keys are available
    if os.getenv("OPENAI_API_KEY"):
        await example_openai()
    else:
        print("Skipping OpenAI example - OPENAI_API_KEY not set")
    
    if os.getenv("GROQ_API_KEY"):
        await example_groq()
    else:
        print("Skipping Groq example - GROQ_API_KEY not set")
    
    print("\nTo run these examples:")
    print("1. Set your API keys as environment variables:")
    print("   - OPENAI_API_KEY for OpenAI GPT")
    print("   - GROQ_API_KEY for Groq")
    print("   - CUSTOM_API_KEY for custom endpoints")
    print("2. Make sure your MCP server is available")
    print("3. Run: python example_usage.py")


if __name__ == "__main__":
    asyncio.run(main())
