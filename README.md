# MCP Hello World Server

A simple Hello World MCP (Model Context Protocol) server built with the FastMCP framework in Python using HTTP transport.

## Prerequisites

- Python 3.10 or higher

## Install

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# For development dependencies
uv sync --dev
```

## Usage

### Running the Server

#### Using Docker (Production)

```bash
docker build -t mcp-hello:latest .
docker-compose up -d
```

#### Using uv (Development)

```bash
# Run the server using uv (HTTP on port 8000)
uv run python -m mcp_hello.server

# Custom host/port using environment variables
MCP_HOST=localhost MCP_PORT=3000 uv run python -m mcp_hello.server
```

#### Accessing the HTTP Server

- **Default**: `http://0.0.0.0:8000`
- **Local access**: `http://localhost:8000`
- **Custom**: Set `MCP_HOST` and `MCP_PORT` environment variables

### Available Tools

#### 1. `say_hello`

Generate greetings in different languages.

**Parameters:**

- `name` (str, optional): Name to greet (default: "World")
- `language` (str, optional): Language code (default: "en")

**Supported languages:**

- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

**Example:**

```json
{
  "tool": "say_hello",
  "arguments": {
    "name": "Alice",
    "language": "es"
  }
}
```

**Response:**

```json
{
  "greeting": "¡Hola, Alice!",
  "language": "es",
  "name": "Alice",
  "message": "Greeting generated successfully in es"
}
```

#### 2. `get_server_info`

Get information about the server capabilities.

**Parameters:**

None

**Response:**

```json
{
  "name": "Hello World MCP Server",
  "version": "1.2.0",
  "description": "A simple hello world MCP server using FastMCP",
  "capabilities": [
    "greeting generation",
    "multi-language support",
    "server information"
  ],
  "supported_languages": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]
}
```

### Available Resources

#### 1. `file://hello-world`

A simple hello world message resource.

#### 2. `file://server-status`

Current server status and available tools/resources.

## Example Client Usage

```bash
# First, start the server in one terminal
uv run python -m mcp_hello.server

# Then in another terminal, run the HTTP client example
uv run python mcp_hello/http_client_example.py
```

### Environment Variables

The server supports the following environment variables:

- `MCP_HOST`: Server host address (default: `0.0.0.0`)
- `MCP_PORT`: Server port number (default: `8000`)

Example:

```bash
MCP_HOST=localhost MCP_PORT=3000 uv run python -m mcp_hello.server
```

## License

This project is licensed under the terms specified in the LICENSE file.

## Reference
