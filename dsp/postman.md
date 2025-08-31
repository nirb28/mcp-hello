{
    "messages": [
        {
            "role": "user",
            "content": "say hi to ds"
        }
    ],
    "model": "meta/llama-3.1-70b-instruct",
    "max_tokens": 1000,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "say_hello",
                "description": "A simple greeting tool that says hello in different languages.\n\nArgs:\n request: The greeting request with name and language\n\nReturns:\n A greeting message in the specified language",
                "parameters": {
                    "$defs": {
                        "GreetingRequest": {
                            "description": "Request model for greeting tool",
                            "properties": {
                                "name": {
                                    "default": "World",
                                    "title": "Name",
                                    "type": "string"
                                },
                                "language": {
                                    "default": "en",
                                    "title": "Language",
                                    "type": "string"
                                }
                            },
                            "title": "GreetingRequest",
                            "type": "object"
                        }
                    },
                    "properties": {
                        "request": {
                            "$ref": "#/$defs/GreetingRequest",
                            "title": "Request"
                        }
                    },
                    "required": [
                        "request"
                    ],
                    "type": "object"
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_server_info",
                "description": "Get information about this MCP server.\n\nReturns:\n Server information including version and capabilities",
                "parameters": {
                    "properties": {},
                    "type": "object"
                }
            }
        }
    ]
}


{
    "messages": [
        {
            "role": "user",
            "content": "say hi to ds"
        },
        {
            "role": "assistant",
            "content": "I'll use the available tools to help you.",
            "tool_calls": [
                {
                    "id": "chatcmpl-tool-606942f79ede4fa4bf2a6fb0221fc763",
                    "type": "function",
                    "function": {
                        "name": "say_hello",
                        "arguments": "{\"request\": {\"name\": \"ds\", \"language\": \"en\"}}"
                    }
                }
            ]
        },
        {
            "role": "tool",
            "tool_call_id": "chatcmpl-tool-606942f79ede4fa4bf2a6fb0221fc763",
            "content": "[TextContent(type='text', text='{\"greeting\":\"Hello, ds!\",\"language\":\"en\",\"name\":\"ds\",\"message\":\"Greeting generated successfully in en\"}', annotations=None, meta=None)]"
        }
    ],
    "model": "meta/llama-3.1-70b-instruct",
    "max_tokens": 1000,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "say_hello",
                "description": "A simple greeting tool that says hello in different languages.\n\nArgs:\n request: The greeting request with name and language\n\nReturns:\n A greeting message in the specified language",
                "parameters": {
                    "$defs": {
                        "GreetingRequest": {
                            "description": "Request model for greeting tool",
                            "properties": {
                                "name": {
                                    "default": "World",
                                    "title": "Name",
                                    "type": "string"
                                },
                                "language": {
                                    "default": "en",
                                    "title": "Language",
                                    "type": "string"
                                }
                            },
                            "title": "GreetingRequest",
                            "type": "object"
                        }
                    },
                    "properties": {
                        "request": {
                            "$ref": "#/$defs/GreetingRequest",
                            "title": "Request"
                        }
                    },
                    "required": [
                        "request"
                    ],
                    "type": "object"
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_server_info",
                "description": "Get information about this MCP server.\n\nReturns:\n Server information including version and capabilities",
                "parameters": {
                    "properties": {},
                    "type": "object"
                }
            }
        }
    ]
}