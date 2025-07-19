"""Tests for the Hello World MCP server"""

import pytest
from mcp_hello.server import say_hello, get_server_info, GreetingRequest


def test_say_hello_default():
    """Test the say_hello tool with default parameters"""
    request = GreetingRequest()
    result = say_hello(request)

    assert result["greeting"] == "Hello, World!"
    assert result["language"] == "en"
    assert result["name"] == "World"
    assert "message" in result


def test_say_hello_custom_name():
    """Test the say_hello tool with a custom name"""
    request = GreetingRequest(name="Alice")
    result = say_hello(request)

    assert result["greeting"] == "Hello, Alice!"
    assert result["language"] == "en"
    assert result["name"] == "Alice"


def test_say_hello_spanish():
    """Test the say_hello tool with Spanish language"""
    request = GreetingRequest(name="María", language="es")
    result = say_hello(request)

    assert result["greeting"] == "¡Hola, María!"
    assert result["language"] == "es"
    assert result["name"] == "María"


def test_say_hello_french():
    """Test the say_hello tool with French language"""
    request = GreetingRequest(name="Jean", language="fr")
    result = say_hello(request)

    assert result["greeting"] == "Bonjour, Jean!"
    assert result["language"] == "fr"
    assert result["name"] == "Jean"


def test_say_hello_unsupported_language():
    """Test the say_hello tool with an unsupported language (should default to English)"""
    request = GreetingRequest(name="Test", language="xyz")
    result = say_hello(request)

    assert result["greeting"] == "Hello, Test!"
    assert result["language"] == "xyz"
    assert result["name"] == "Test"


def test_get_server_info():
    """Test the get_server_info tool"""
    result = get_server_info()

    assert result["name"] == "Hello World MCP Server"
    assert result["version"] == "1.0.0"
    assert "capabilities" in result
    assert "supported_languages" in result
    assert "en" in result["supported_languages"]
    assert "es" in result["supported_languages"]
