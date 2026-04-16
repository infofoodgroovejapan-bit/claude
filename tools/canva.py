"""Canva MCP tool definitions and executor.

Used primarily by the DocumentAgent (資料作成チーム) for creating
presentations, designs, and visual materials.
"""
from __future__ import annotations

TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "canva_search_designs",
        "description": (
            "Canvaのデザイン一覧を検索します / Search existing Canva designs.\n"
            "既存のデザインを検索してテンプレートとして再利用できます。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for design titles or keywords",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "canva_generate_design",
        "description": (
            "AIを使ってCanvaデザインを自動生成します / Generate a Canva design using AI.\n"
            "プレゼン、バナー、SNS画像などを自動で作成します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": (
                        "Description of the design to generate "
                        "(e.g. 'Business presentation about Q3 results, 10 slides, professional style')"
                    ),
                },
                "design_type": {
                    "type": "string",
                    "description": (
                        "Type of design to create "
                        "(e.g. 'presentation', 'social_media', 'banner', 'poster', 'document')"
                    ),
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "canva_get_design",
        "description": (
            "指定したCanvaデザインの詳細を取得します / Get details of a specific Canva design."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "design_id": {
                    "type": "string",
                    "description": "The Canva design ID",
                },
            },
            "required": ["design_id"],
        },
    },
    {
        "name": "canva_export_design",
        "description": (
            "CanvaデザインをPDFやPNG等にエクスポートします / Export a Canva design to PDF, PNG, etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "design_id": {
                    "type": "string",
                    "description": "The Canva design ID to export",
                },
                "format": {
                    "type": "string",
                    "enum": ["pdf", "png", "jpg", "pptx"],
                    "description": "Export format",
                    "default": "pdf",
                },
            },
            "required": ["design_id"],
        },
    },
]


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch to the appropriate Canva MCP function."""
    try:
        if name == "canva_search_designs":
            from mcp__8efedc3a_dab3_4964_94ed_4ac52c9dcc0b import search_designs  # type: ignore
            result = search_designs(**tool_input)
            return str(result)

        if name == "canva_generate_design":
            from mcp__8efedc3a_dab3_4964_94ed_4ac52c9dcc0b import generate_design  # type: ignore
            result = generate_design(**tool_input)
            return str(result)

        if name == "canva_get_design":
            from mcp__8efedc3a_dab3_4964_94ed_4ac52c9dcc0b import get_design  # type: ignore
            result = get_design(**tool_input)
            return str(result)

        if name == "canva_export_design":
            from mcp__8efedc3a_dab3_4964_94ed_4ac52c9dcc0b import export_design  # type: ignore
            result = export_design(**tool_input)
            return str(result)

    except ImportError:
        return f"[Canva MCP not available in this environment. Tool: {name}, Input: {tool_input}]"

    return f"[Unknown Canva tool: {name}]"
