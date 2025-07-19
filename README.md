# MCP Hello World Server

A simple Hello World MCP (Model Context Protocol) server built with the FastMCP framework in Python.

## Features

- **Multi-language greetings**: Say hello in 10 different languages
- **Server information**: Get details about the server capabilities
- **Resource serving**: Access hello world resources
- **FastMCP framework**: Built on the modern FastMCP framework
- **Type safety**: Uses Pydantic for request/response validation
- **Testing**: Includes comprehensive test suite

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install dependencies

#### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# For development dependencies
uv sync --dev
```

#### Using pip (Alternative)

```bash
# Using pip with requirements.txt
pip install -r requirements.txt

# Or using the project directly
pip install -e .

# For development
pip install -e ".[dev]"
```

## Usage

### Running the Server

#### Using uv (Recommended)

```bash
# Run the server using uv
uv run python -m mcp_hello.server

# Or using make
make run
```

#### Using pip installation

```bash
# Using the installed script
mcp-hello

# Or running directly
python -m mcp_hello.server

# Or from the source
python mcp_hello/server.py
```

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

**Parameters:** None

**Response:**
```json
{
  "name": "Hello World MCP Server",
  "version": "1.0.0",
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

#### 1. `hello-world`
A simple hello world message resource.

#### 2. `server-status`
Current server status and available tools/resources.

## Development

### Project Structure

```
mcp-hello/
├── mcp_hello/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   └── client_example.py  # Example client usage
├── tests/
│   ├── __init__.py
│   └── test_server.py     # Test suite
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
├── README.md             # This file
└── LICENSE               # License file
```

### Running Tests

#### Using uv (Recommended)

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=mcp_hello

# Run specific test file
uv run pytest tests/test_server.py

# Using make
make test
```

#### Using pip installation

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_hello

# Run specific test file
pytest tests/test_server.py
```

### Code Formatting

#### Using uv (Recommended)

```bash
# Format code with black
uv run black mcp_hello/ tests/

# Lint with ruff
uv run ruff check mcp_hello/ tests/

# Auto-fix linting issues
uv run ruff check --fix mcp_hello/ tests/

# Using make
make format  # Format code
make lint    # Lint code
```

#### Using pip installation

```bash
# Format code with black
black mcp_hello/ tests/

# Lint with ruff
ruff check mcp_hello/ tests/

# Auto-fix linting issues
ruff check --fix mcp_hello/ tests/
```

## Example Client Usage

See `mcp_hello/client_example.py` for a demonstration of how to interact with the server:

#### Using uv (Recommended)

```bash
uv run python mcp_hello/client_example.py
```

#### Using pip installation

```bash
python mcp_hello/client_example.py
```

## Configuration

The project uses `pyproject.toml` for configuration:

- **Build system**: Hatchling
- **Dependencies**: FastMCP and Pydantic
- **Development tools**: pytest, black, ruff (configured for uv)
- **Entry point**: `mcp-hello` command
- **Virtual environment**: Managed by uv

### Make Commands

The project includes a Makefile with uv-optimized commands:

```bash
make setup-uv    # Install uv if not already installed
make sync        # Create/sync virtual environment
make install-dev # Install with development dependencies
make test        # Run tests
make format      # Format code
make lint        # Lint code
make run         # Run the server
make clean       # Clean build artifacts and venv
make help        # Show all available commands
```

## Requirements

- **Python**: 3.8 or higher
- **uv**: Fast Python package installer and resolver (recommended)
- **Core dependencies**:
  - `fastmcp>=0.1.0` - FastMCP framework for building MCP servers
  - `pydantic>=2.0.0` - Data validation and settings management

## Contributing

#### Using uv (Recommended)

1. Fork the repository
2. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Create virtual environment: `uv sync --dev`
4. Create a feature branch
5. Make your changes
6. Run tests: `make test` or `uv run pytest`
7. Format code: `make format` or `uv run black .`
8. Submit a pull request

#### Using pip (Alternative)

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Format code: `black .`
6. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.
