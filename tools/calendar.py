"""Google Calendar MCP tool definitions and executor."""
from __future__ import annotations

TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "calendar_list_events",
        "description": (
            "Googleカレンダーのイベント一覧を取得します / List Google Calendar events.\n"
            "指定した期間のイベントを返します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID (use 'primary' for the main calendar)",
                    "default": "primary",
                },
                "time_min": {
                    "type": "string",
                    "description": "Start of time range in ISO 8601 format (e.g. '2026-04-01T00:00:00+09:00')",
                },
                "time_max": {
                    "type": "string",
                    "description": "End of time range in ISO 8601 format",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of events to return (default: 10)",
                    "default": 10,
                },
            },
            "required": [],
        },
    },
    {
        "name": "calendar_create_event",
        "description": (
            "Googleカレンダーに新しいイベントを作成します / Create a new Google Calendar event."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Event title",
                },
                "start_time": {
                    "type": "string",
                    "description": "Start time in ISO 8601 format (e.g. '2026-05-01T10:00:00+09:00')",
                },
                "end_time": {
                    "type": "string",
                    "description": "End time in ISO 8601 format",
                },
                "description": {
                    "type": "string",
                    "description": "Event description / agenda",
                },
                "location": {
                    "type": "string",
                    "description": "Event location or meeting URL",
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of attendee email addresses",
                },
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID (default: 'primary')",
                    "default": "primary",
                },
            },
            "required": ["summary", "start_time", "end_time"],
        },
    },
    {
        "name": "calendar_update_event",
        "description": (
            "Googleカレンダーのイベントを更新します / Update a Google Calendar event."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The event ID to update"},
                "calendar_id": {"type": "string", "default": "primary"},
                "summary": {"type": "string"},
                "start_time": {"type": "string"},
                "end_time": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["event_id"],
        },
    },
]


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch to the appropriate Google Calendar MCP function."""
    try:
        if name == "calendar_list_events":
            from mcp__a2de7442_7130_4acd_a6b1_60c47f18d644 import list_events  # type: ignore
            result = list_events(**tool_input)
            return str(result)

        if name == "calendar_create_event":
            from mcp__a2de7442_7130_4acd_a6b1_60c47f18d644 import create_event  # type: ignore
            result = create_event(**tool_input)
            return str(result)

        if name == "calendar_update_event":
            from mcp__a2de7442_7130_4acd_a6b1_60c47f18d644 import update_event  # type: ignore
            result = update_event(**tool_input)
            return str(result)

    except ImportError:
        return f"[Calendar MCP not available in this environment. Tool: {name}, Input: {tool_input}]"

    return f"[Unknown Calendar tool: {name}]"
