"""Gmail MCP tool definitions and executor for the AI Secretary System.

TOOL_DEFINITIONS: Anthropic tool-use schemas passed to Claude.
execute_tool(): Dispatches to the actual MCP Gmail functions.
"""
from __future__ import annotations

TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "gmail_search_messages",
        "description": (
            "Gmailメッセージを検索します / Search Gmail messages.\n"
            "クエリ文字列で検索し、マッチするメッセージのリストを返します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Gmail search query (e.g. 'from:boss@example.com subject:report')",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 10)",
                    "default": 10,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "gmail_read_message",
        "description": (
            "指定したIDのGmailメッセージを読み取ります / Read a Gmail message by ID."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "string",
                    "description": "The Gmail message ID to read",
                },
            },
            "required": ["message_id"],
        },
    },
    {
        "name": "gmail_create_draft",
        "description": (
            "Gmailの下書きを作成します / Create a Gmail draft.\n"
            "送信前に下書きとして保存します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address",
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line",
                },
                "body": {
                    "type": "string",
                    "description": "Email body text (plain text or HTML)",
                },
                "cc": {
                    "type": "string",
                    "description": "CC recipients (comma-separated)",
                },
            },
            "required": ["to", "subject", "body"],
        },
    },
]


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch to the appropriate Gmail MCP function."""
    # These imports are resolved at call time so the MCP tools are
    # available in the environment when needed.
    try:
        if name == "gmail_search_messages":
            from mcp__159890c7_ea3a_4f40_814e_db1b9f6819dd import gmail_search_messages  # type: ignore
            result = gmail_search_messages(**tool_input)
            return str(result)

        if name == "gmail_read_message":
            from mcp__159890c7_ea3a_4f40_814e_db1b9f6819dd import gmail_read_message  # type: ignore
            result = gmail_read_message(**tool_input)
            return str(result)

        if name == "gmail_create_draft":
            from mcp__159890c7_ea3a_4f40_814e_db1b9f6819dd import gmail_create_draft  # type: ignore
            result = gmail_create_draft(**tool_input)
            return str(result)

    except ImportError:
        return f"[Gmail MCP not available in this environment. Tool: {name}, Input: {tool_input}]"

    return f"[Unknown Gmail tool: {name}]"
