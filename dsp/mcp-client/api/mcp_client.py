from typing import Optional, Dict, Any, Union
from contextlib import AsyncExitStack
import traceback

# from utils.logger import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from datetime import datetime
from utils.logger import logger
import json
import os
import httpx

from openai import OpenAI

class MCPClient:
    def __init__(self, provider: str = "groq"):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.provider = provider.lower()
        self.tools = []
        self.messages = []
        self.logger = logger
        
        # MCP Server Configuration
        self.mcp_server_script_path = os.getenv("MCP_SERVER_SCRIPT_PATH", "mcp_server.py")
        self.mcp_server_protocol = os.getenv("MCP_SERVER_PROTOCOL", "stdio").lower()
        self.mcp_server_command = os.getenv("MCP_SERVER_COMMAND", "python")
        self.mcp_server_timeout = int(os.getenv("MCP_SERVER_TIMEOUT", "30"))
        
        # Additional protocol-specific configuration
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
        self.mcp_server_headers = json.loads(os.getenv("MCP_SERVER_HEADERS", "{}"))
        self.mcp_sse_read_timeout = int(os.getenv("MCP_SSE_READ_TIMEOUT", "300"))
        
        # Initialize OpenAI-compatible client
        proxy_url = os.environ.get("PROXY_URL")
        self.llm = OpenAI(
            api_key=os.getenv(f"{provider.upper()}_API_KEY"),
            base_url=os.getenv(f"{provider.upper()}_BASE_URL"),
            http_client=httpx.Client(verify=False, proxy=proxy_url)
        )
        self.model = model = os.getenv(f"{provider.upper()}_MODEL")

    # connect to the MCP server
    async def connect_to_server(self, server_script_path: str = None):
        try:
            self.logger.info(f"Connecting to MCP server using {self.mcp_server_protocol} protocol")
            
            if self.mcp_server_protocol == "stdio":
                await self._connect_stdio(server_script_path)
            elif self.mcp_server_protocol == "sse":
                await self._connect_sse()
            elif self.mcp_server_protocol == "http":
                await self._connect_http()
            else:
                raise ValueError(f"Unsupported MCP protocol: {self.mcp_server_protocol}")

            await self.session.initialize()
            self.logger.info(f"Connected to MCP server via {self.mcp_server_protocol}")

            mcp_tools = await self.get_mcp_tools()
            tool_dicts = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                }
                for tool in mcp_tools
            ]
            self.tools = self._convert_tools_for_openai(tool_dicts)
            
            tool_names = [tool['function']['name'] for tool in self.tools]
            self.logger.info(f"Available tools: {tool_names}")

            return True

        except Exception as e:
            self.logger.error(f"Error connecting to MCP server: {e}")
            traceback.print_exc()
            raise

    async def _connect_stdio(self, server_script_path: str = None):
        """Connect using stdio protocol"""
        # Use provided path or fall back to environment configuration
        script_path = server_script_path or self.mcp_server_script_path
        
        is_python = script_path.endswith(".py")
        is_js = script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        # Use environment command or auto-detect based on file extension
        command = self.mcp_server_command if self.mcp_server_command != "auto" else ("python" if is_python else "node")
        server_params = StdioServerParameters(
            command=command, args=[script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

    async def _connect_sse(self):
        """Connect using SSE protocol"""
        sse_transport = await self.exit_stack.enter_async_context(
            sse_client(
                url=self.mcp_server_url,
                headers=self.mcp_server_headers,
                timeout=self.mcp_server_timeout,
                sse_read_timeout=self.mcp_sse_read_timeout
            )
        )
        self.stdio, self.write = sse_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

    async def _connect_http(self):
        """Connect using HTTP protocol"""
        http_transport = await self.exit_stack.enter_async_context(
            streamablehttp_client(
                url=self.mcp_server_url,
                headers=self.mcp_server_headers,
                timeout=self.mcp_server_timeout,
                sse_read_timeout=self.mcp_sse_read_timeout
            )
        )
        self.stdio, self.write, self.get_session_id = http_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

    # get mcp tool list
    async def get_mcp_tools(self):
        try:
            response = await self.session.list_tools()
            return response.tools
        except Exception as e:
            self.logger.error(f"Error getting MCP tools: {e}")
            raise
    
    def _convert_tools_for_openai(self, mcp_tools):
        """Convert MCP tools to OpenAI function calling format"""
        openai_tools = []
        for tool in mcp_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"]
                }
            }
            openai_tools.append(openai_tool)
        return openai_tools
    
    def _convert_messages_for_openai(self, messages):
        """Convert messages to OpenAI format"""
        openai_messages = []
        for msg in messages:
            if isinstance(msg["content"], str):
                openai_messages.append(msg)
            elif isinstance(msg["content"], list):
                # Handle complex content - just convert to text for simplicity
                text_content = ""
                for part in msg["content"]:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text_content += part.get("text", "")
                        elif part.get("type") == "tool_use":
                            text_content += f"Tool call: {part.get('name', '')} with args {part.get('input', {})}"
                        else:
                            text_content += str(part)
                    else:
                        text_content += str(part)
                
                openai_messages.append({
                    "role": msg["role"],
                    "content": text_content
                })
        return openai_messages
    

    # process query
    async def process_query(self, query: str):
        try:
            self.logger.info(f"Processing query: {query}")
            user_message = {"role": "user", "content": query}
            self.messages = [user_message]

            while True:
                response = await self.call_llm()
                message = response.choices[0].message

                # Handle text response
                if message.content and not message.tool_calls:
                    assistant_message = {
                        "role": "assistant",
                        "content": message.content,
                    }
                    self.messages.append(assistant_message)
                    await self.log_conversation()
                    break

                # Handle tool calls
                if message.tool_calls:
                    # Ensure content is not empty for providers like NVIDIA that require min 1 character
                    content = message.content if message.content and message.content.strip() else "I'll use the available tools to help you."
                    
                    assistant_message = {
                        "role": "assistant",
                        "content": content,
                        "tool_calls": [{
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in message.tool_calls]
                    }
                    self.messages.append(assistant_message)
                    await self.log_conversation()

                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        tool_call_id = tool_call.id
                        
                        self.logger.info(f"Calling tool {tool_name} with args {tool_args}")
                        
                        try:
                            result = await self.session.call_tool(tool_name, tool_args)
                            self.logger.info(f"Tool {tool_name} result: {result}...")
                            
                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "content": str(result.content),
                            })
                            await self.log_conversation()
                        except Exception as e:
                            self.logger.error(f"Error calling tool {tool_name}: {e}")
                            raise

            return self.messages

        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            raise

    # call llm
    async def call_llm(self):
        try:
            self.logger.info(f"Calling {self.provider} LLM")
            
            # Convert messages to OpenAI format if needed
            openai_messages = self._convert_messages_for_openai(self.messages)
            
            response = self.llm.chat.completions.create(
                model=self.model,
                max_tokens=1000,
                messages=openai_messages,
                tools=self.tools if self.tools else None,
            )
            
            return response
                
        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}")
            raise

    # cleanup
    async def cleanup(self):
        try:
            await self.exit_stack.aclose()
            self.logger.info("Disconnected from MCP server")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            traceback.print_exc()
            raise

    async def log_conversation(self):
        os.makedirs("conversations", exist_ok=True)

        serializable_conversation = []

        for message in self.messages:
            try:
                serializable_message = {"role": message["role"], "content": []}

                # Handle both string and list content
                if isinstance(message["content"], str):
                    serializable_message["content"] = message["content"]
                elif isinstance(message["content"], list):
                    for content_item in message["content"]:
                        if hasattr(content_item, "to_dict"):
                            serializable_message["content"].append(
                                content_item.to_dict()
                            )
                        elif hasattr(content_item, "dict"):
                            serializable_message["content"].append(content_item.dict())
                        elif hasattr(content_item, "model_dump"):
                            serializable_message["content"].append(
                                content_item.model_dump()
                            )
                        else:
                            serializable_message["content"].append(content_item)

                serializable_conversation.append(serializable_message)
            except Exception as e:
                self.logger.error(f"Error processing message: {str(e)}")
                self.logger.debug(f"Message content: {message}")
                raise

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join("conversations", f"conversation_{timestamp}.json")

        try:
            with open(filepath, "w") as f:
                json.dump(serializable_conversation, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error writing conversation to file: {str(e)}")
            self.logger.debug(f"Serializable conversation: {serializable_conversation}")
            raise
