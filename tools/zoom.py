"""Zoom MCP tool definitions and executor."""
from __future__ import annotations

TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "zoom_search_meetings",
        "description": (
            "Zoomの会議を検索します / Search Zoom meetings.\n"
            "過去・予定の会議を検索してリストを返します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string for meeting titles or topics",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "zoom_list_recordings",
        "description": (
            "Zoomの録画一覧を取得します / List Zoom recordings."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format",
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format",
                },
            },
            "required": [],
        },
    },
    {
        "name": "zoom_get_meeting_assets",
        "description": (
            "指定したZoom会議の資産（録画、文字起こし等）を取得します / "
            "Get assets for a specific Zoom meeting."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "meeting_id": {
                    "type": "string",
                    "description": "Zoom meeting ID",
                },
            },
            "required": ["meeting_id"],
        },
    },
]


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch to the appropriate Zoom MCP function."""
    try:
        if name == "zoom_search_meetings":
            from mcp__26db533d_ab5c_4307_858d_0e2a09eb542e import search_zoom  # type: ignore
            result = search_zoom(**tool_input)
            return str(result)

        if name == "zoom_list_recordings":
            from mcp__26db533d_ab5c_4307_858d_0e2a09eb542e import recordings_list  # type: ignore
            result = recordings_list(**tool_input)
            return str(result)

        if name == "zoom_get_meeting_assets":
            from mcp__26db533d_ab5c_4307_858d_0e2a09eb542e import get_meeting_assets  # type: ignore
            result = get_meeting_assets(**tool_input)
            return str(result)

    except ImportError:
        return f"[Zoom MCP not available in this environment. Tool: {name}, Input: {tool_input}]"

    return f"[Unknown Zoom tool: {name}]"
