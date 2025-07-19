#!/bin/bash

# Bootstrap script for MCP Hello World project using uv
# This script sets up the development environment on Ubuntu

set -e

echo "🚀 Setting up MCP Hello World project with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Source the shell configuration to make uv available
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi
    if [ -f ~/.zshrc ]; then
        source ~/.zshrc
    fi

    echo "✅ uv installed successfully!"
    echo "ℹ️  You may need to restart your shell or run: source ~/.bashrc"
else
    echo "✅ uv is already installed"
fi

# Create and sync virtual environment
echo "🔧 Creating virtual environment and installing dependencies..."
uv sync --dev

echo "🧪 Running tests to verify setup..."
uv run pytest tests/ -v

echo "🎉 Setup complete!"
echo ""
echo "Available commands:"
echo "  make help        - Show all available make commands"
echo "  make run         - Run the MCP server"
echo "  make test        - Run tests"
echo "  uv run python -m mcp_hello.server  - Run server directly"
echo ""
echo "To activate the virtual environment manually:"
echo "  source .venv/bin/activate"
