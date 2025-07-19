# Makefile for MCP Hello World Server (using uv)

.PHONY: install install-dev test format lint clean run help setup-uv sync docker-build docker-run docker-stop docker-clean docker-logs

# Default target
help:
	@echo "Available targets:"
	@echo ""
	@echo "Local development:"
	@echo "  setup-uv    - Install uv if not already installed"
	@echo "  sync        - Create/sync virtual environment with uv"
	@echo "  install     - Install the package in development mode"
	@echo "  install-dev - Install package with development dependencies"
	@echo "  test        - Run tests"
	@echo "  format      - Format code with black"
	@echo "  lint        - Lint code with ruff"
	@echo "  clean       - Clean build artifacts and venv"
	@echo "  run         - Run the MCP server (HTTP)"
	@echo "  client      - Run HTTP client example"
	@echo ""
	@echo "Docker operations:"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run container with docker-compose"
	@echo "  docker-stop  - Stop running container"
	@echo "  docker-clean - Remove container and image"
	@echo "  docker-logs  - Show container logs"
	@echo ""
	@echo "  help        - Show this help message"

# Install uv if not already installed
setup-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "Please restart your shell or run: source ~/.bashrc"; \
	else \
		echo "uv is already installed"; \
	fi

# Create/sync virtual environment
sync:
	uv sync

# Install package in development mode
install:
	uv pip install -e .

# Install with development dependencies
install-dev:
	uv sync --dev

# Run tests
test:
	uv run pytest tests/ -v

# Format code
format:
	uv run black mcp_hello/ tests/

# Lint code
lint:
	uv run ruff check mcp_hello/ tests/

# Clean build artifacts and venv
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .venv/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the server (HTTP)
run:
	uv run python -m mcp_hello.server

# Run HTTP client example
client:
	uv run python mcp_hello/http_client_example.py

# Install from requirements.txt (legacy, prefer uv sync)
install-req:
	uv pip install -r requirements.txt

# Docker operations
docker-build:
	docker build -t mcp-hello:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-clean:
	docker-compose down --rmi all --volumes --remove-orphans

docker-logs:
	docker-compose logs -f mcp-hello

# Run container directly (without docker-compose)
docker-run-direct:
	docker run -d --name mcp-hello-server -p 8000:8000 mcp-hello:latest

# Stop and remove direct container
docker-stop-direct:
	docker stop mcp-hello-server || true
	docker rm mcp-hello-server || true
