"""GitHub MCP tool definitions and executor."""
from __future__ import annotations

TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "github_create_issue",
        "description": (
            "GitHubにIssueを作成します / Create a GitHub issue.\n"
            "タスク管理やバグ報告に使用します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner (org or user)"},
                "repo": {"type": "string", "description": "Repository name"},
                "title": {"type": "string", "description": "Issue title"},
                "body": {"type": "string", "description": "Issue body / description"},
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels to apply to the issue",
                },
            },
            "required": ["owner", "repo", "title"],
        },
    },
    {
        "name": "github_list_issues",
        "description": (
            "GitHubのIssue一覧を取得します / List GitHub issues."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "state": {
                    "type": "string",
                    "enum": ["open", "closed", "all"],
                    "default": "open",
                },
                "labels": {"type": "string", "description": "Comma-separated label names"},
            },
            "required": ["owner", "repo"],
        },
    },
    {
        "name": "github_create_or_update_file",
        "description": (
            "GitHubリポジトリにファイルを作成または更新します / "
            "Create or update a file in a GitHub repository."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "path": {"type": "string", "description": "File path in the repository"},
                "message": {"type": "string", "description": "Commit message"},
                "content": {"type": "string", "description": "File content (plain text)"},
                "branch": {"type": "string", "description": "Branch name (default: main)"},
            },
            "required": ["owner", "repo", "path", "message", "content"],
        },
    },
]


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch to the appropriate GitHub MCP function."""
    try:
        if name == "github_create_issue":
            from mcp__github import issue_write  # type: ignore
            result = issue_write(**tool_input)
            return str(result)

        if name == "github_list_issues":
            from mcp__github import list_issues  # type: ignore
            result = list_issues(**tool_input)
            return str(result)

        if name == "github_create_or_update_file":
            from mcp__github import create_or_update_file  # type: ignore
            result = create_or_update_file(**tool_input)
            return str(result)

    except ImportError:
        return f"[GitHub MCP not available in this environment. Tool: {name}, Input: {tool_input}]"

    return f"[Unknown GitHub tool: {name}]"
